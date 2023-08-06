"""lg-rez / features / Synchronisation GSheets

Récupération et application des données des GSheets :
modifications décidées via le Tableau de bord et rôles

"""

import datetime
import time
import traceback

from discord import Embed
from discord.ext import commands
import sqlalchemy

from lgrez import config, bdd
from lgrez.blocs import tools, env, gsheets
from lgrez.bdd import (Joueur, Action, Role, Camp, BaseAction,
                       Statut, ActionTrigger)
from lgrez.features import gestion_actions


class TDBModif(gsheets.Modif):
    """Modification flag sur le Tableau de bord, à appliquer.

    Attributes:
        id (int): ID Discord du joueur concerné.
        col (str): Colonne de :class:`~bdd.Joueur` à modifier.
        val (Any): Nouvelle valeur.
        row (int): Numéro de la ligne (0 = ligne 1).
        column (int): Numéro de la colonne (0 = colonne A).

    Sous-classe de :class:`.gsheets.Modif`.
    """

    def __init__(self, id, col, val, row, column):
        """Initializes self."""
        super().__init__(row, column, val)
        self.id = id
        self.col = col

    def __repr__(self):
        """Returns repr(self)"""
        return f"<TDBModif id {self.id}: {self.col} = {self.val!r}>"

    def __eq__(self, other):
        """Returns self == other"""
        return (super().__eq__(other)
                and self.id == other.id
                and self.col == other.col)


def transtype(value, cst):
    """Utilitaire : caste une donnée brute d'un GSheet selon sa colonne.

    Args:
        value (Any): valeur à transtyper.
        cst (:class:`sqlalchemy.schema.Column` | :class:`.bdd.base.TableMeta`\
            | :class:`sqlalchemy.orm.RelationshipProperty`): colonne, table ou
            relationship (many-to-one) associée.

    Types pris en charge dans le cas d'une colonne :

        - :class:`sqlalchemy.types.String` et dérivés
          (``Text``, ``Varchar``...)
        - :class:`sqlalchemy.types.Integer` et dérivés
          (``BigInteger``...)
        - :class:`sqlalchemy.types.Boolean`
        - :class:`sqlalchemy.types.Time`
        - :class:`sqlalchemy.types.Enum`

    Dans le cas d'une table ou d'une relation many-to-one vers une table,
    ``value`` est interprété comme la clé primaire de la table / de la table
    liée. Les valeurs interprétées ``None`` ne sont pas acceptées, même dans
    le cas d'une relation avec contrainte One-to-many faite *nullable*.

    Returns:
        L'objet Python correspondant au type de la colonne / table liée
        (:class:`str`, :class:`int`, :class:`bool`, :class:`datetime.time`,
        :class:`enum.Enum`, :class:`.bdd.TableBase`) ou ``None``

    Raises:
        ValueError: la conversion n'est pas possible (ou ``value`` est
            évaluée ``None`` et la colonne n'est pas *nullable*)
        TypeError: type de colonne non pris en charge.
    """
    if isinstance(cst, sqlalchemy.orm.RelationshipProperty):
        # Relationship
        table = cst.argument()    # -> cas suivant
        if not isinstance(value, table.primary_col.type.python_type):
            raise ValueError(
                f"Valeur '{value}' incorrecte pour la colonne '{cst.key}' "
                f"(one-to-many avec '{table.__name__}', de clé primaire "
                f"'{table.primary_col.name}', type '{table.primary_col.type}')"
            ) from None

        inst = table.query.get(value)
        if inst is None:
            raise ValueError(
                f"Valeur '{value}' incorrecte pour la colonne '{cst.key}': "
                f"instance de '{table.__name__}' correspondate non trouvée."
            )

        return inst

    elif isinstance(cst, bdd.base.TableMeta):
        # Table
        if not isinstance(value, cst.primary_col.type.python_type):
            raise ValueError(
                f"Valeur '{value}' incorrecte pour la table '{cst.__name__}', "
                f"de clé primaire '{cst.primary_col.name}', type "
                f"'{cst.primary_col.type}')"
            ) from None

        inst = cst.query.get(value)
        if inst is None:
            raise ValueError(
                f"Valeur '{value}' incorrecte pour la table '{cst.__name__}': "
                f"instance correspondate non trouvée."
            )

        return inst

    # Colonne propre
    try:
        if value in (None, '', 'None', 'none', 'Null', 'null'):
            if not cst.nullable:
                if cst.default is None:
                    raise ValueError
                else:
                    return cst.default.arg
            return None
        if isinstance(cst.type, sqlalchemy.Enum):
            enum = cst.type.python_type
            try:
                return enum[value]
            except KeyError:
                raise ValueError
        if isinstance(cst.type, sqlalchemy.String):
            return str(value)
        if isinstance(cst.type, sqlalchemy.Integer):
            return int(value)
        if isinstance(cst.type, sqlalchemy.Boolean):
            if (value in {True, 1}
                or (isinstance(value, str)
                    and value.lower() in {'true', 'vrai', '1'})):
                return True
            elif (value in {False, 0}
                  or (isinstance(value, str)
                      and value.lower() in {'false', 'faux', '0'})):
                return False
            else:
                raise ValueError
        if isinstance(cst.type, sqlalchemy.Time):       # hh:mm
            try:
                h, m, _ = value.split(':')
            except ValueError:
                h, m = value.split(':')
            return datetime.time(hour=int(h), minute=int(m))

        raise TypeError(f"Unhandled type for column '{cst.key}': '{cst.type}'")

    except (ValueError, TypeError):
        raise ValueError(
            f"Valeur '{value}' incorrecte pour la colonne '{cst.key}' "
            f"(type '{cst.type}'/{'NOT NULL' if not cst.nullable else ''})"
        ) from None


def get_sync():
    """Récupère les modifications en attente sur le TDB.

    Charge les données du Tableau de bord (variable d'environment
    ``LGREZ_TDB_SHEET_ID``), compare les informations qui y figurent
    avec celles de la base de données (:class:`.bdd.Joueur`).

    Supprime les joueurs en base absents du Tableau de bord, lève une
    erreur dans le cas inverse, n'applique aucune autre modification.

    Returns:
        list[.TDBModif]: La liste des modifications à apporter
    """
    # RÉCUPÉRATION INFOS GSHEET ET VÉRIFICATIONS

    SHEET_ID = env.load("LGREZ_TDB_SHEET_ID")
    workbook = gsheets.connect(SHEET_ID)
    sheet = workbook.worksheet(config.tdb_main_sheet)
    values = sheet.get_all_values()         # Liste de listes

    head = values[config.tdb_header_row - 1]
    # Ligne d'en-têtes (noms des colonnes), - 1 car indexé à 0

    id_index = gsheets.a_to_index(config.tdb_id_column)
    pk = head[id_index]
    if pk != Joueur.primary_col.key:
        raise ValueError(
            "Tableau de bord : la cellule "
            "`config.tdb_id_column` / `config.tdb_header_row` = "
            f"`{config.tdb_id_column}{config.tdb_header_row}` "
            f"vaut `{pk}` au lieu de la clé primaire de la table "
            f"`Joueur`, `{Joueur.primary_col.key}` !"
        )

    mstart, mstop = config.tdb_main_columns
    main_indexes = range(gsheets.a_to_index(mstart),
                         gsheets.a_to_index(mstop) + 1)
    # Indices des colonnes à remplir
    cols = {}
    for index in main_indexes:
        col = head[index]
        if col in Joueur.attrs:
            cols[col] = Joueur.attrs[col]
        else:
            raise ValueError(
                f"Tableau de bord : l'index de la zone principale "
                f"`{col}` n'est pas une colonne de la table `Joueur` !"
                " (voir `lgrez.config.main_indexes` / "
                "`lgrez.config.tdb_header_row`)"
            )

    tstart, tstop = config.tdb_tampon_columns
    tampon_indexes = range(gsheets.a_to_index(tstart),
                           gsheets.a_to_index(tstop) + 1)

    TDB_tampon_index = {}
    for index in tampon_indexes:
        col = head[index].partition("_")[2]
        if col in cols:
            TDB_tampon_index[col] = index
        else:
            raise ValueError(
                f"Tableau de bord : l'index de zone tampon `{head[index]}` "
                f"réfère à la colonne `{col}` (partie suivant le premier "
                f"underscore), qui n'est pas une colonne de la zone "
                "principale ! (voir `lgrez.config.tampon_indexes` / "
                "`lgrez.config.main_indexes`)"
            )

    # CONVERSION INFOS GSHEET EN PSEUDO-UTILISATEURS

    joueurs_TDB = []    # Joueurs tels qu'actuellement dans le TDB
    ids_TDB = []        # discord_ids des différents joueurs du TDB
    rows_TDB = {}       # Lignes ou sont les différents joueurs du TDB

    for i_row, row in enumerate(values):
        # On parcourt les lignes du TDB
        if i_row < config.tdb_header_row:
            # Ligne avant le header / le header (car décalage de 1)
            continue

        id_cell = row[id_index]
        if not id_cell.isdigit():
            # La cellule ne contient pas un ID ==> skip
            continue

        id = int(id_cell)
        # Construction dictionnaire correspondant à l'utilisateur
        joueur_TDB = {head[index]: transtype(row[index], cols[head[index]])
                      for index in main_indexes}
        joueur_TDB[pk] = id
        joueurs_TDB.append(joueur_TDB)
        ids_TDB.append(id)
        rows_TDB[id] = i_row

    # RÉCUPÉRATION UTILISATEURS BDD

    joueurs_BDD = {joueur.discord_id: joueur for joueur in Joueur.query.all()}

    # COMPARAISON

    for id, joueur in list(joueurs_BDD.items()):
        if id not in ids_TDB:
            # Joueur en base supprimé du TDB
            del joueurs_BDD[id]
            joueur.delete()

    modifs = []         # modifs à porter au TDB (liste de TDBModifs)
    for joueur_TDB in joueurs_TDB:              # Différences
        id = joueur_TDB[pk]

        try:
            joueur = joueurs_BDD[id]
        except KeyError:        # Joueur en base pas dans le TDB
            raise ValueError(f"Joueur `{joueur_TDB['nom']}` hors base : "
                             "vérifier processus d'inscription") from None

        for col in cols:
            if getattr(joueur, col) != joueur_TDB[col]:
                # Si <col> diffère entre TDB et cache,
                # on ajoute la modif (avec update du tampon)
                modifs.append(TDBModif(
                    id=id, col=col, val=joueur_TDB[col],
                    row=rows_TDB[id], column=TDB_tampon_index[col]
                ))

    return modifs


def validate_sync(modifs):
    """Valide des modificatons sur le Tableau de bord (case plus en rouge).

    Args:
        modifs (list[.TDBModif]): liste des modifications à apporter.

    Modifie sur le Tableau de bord (variable d'environment
    ``LGREZ_TDB_SHEET_ID``) et applique les modifications contenues
    dans ``modifs``.
    """
    SHEET_ID = env.load("LGREZ_TDB_SHEET_ID")
    workbook = gsheets.connect(SHEET_ID)    # Tableau de bord
    sheet = workbook.worksheet(config.tdb_main_sheet)

    gsheets.update(sheet, *modifs)


async def modif_joueur(joueur_id, modifs, silent=False):
    """Attribue les modifications demandées au joueur

    Args:
        joueur_id (int): id Discord du joueur concerné.
        modifs (list[.TDBModif]): liste des modifications à apporter.
        silent (bool): si ``True``, ne notifie pas le joueur des
            modifications.

    Returns:
        (list[.TDBModif], str): La liste des modifications appliquées
            et le changelog textuel associé (pour log global).

    Raises:
        ValueError: pas de joueur d'ID ``joueur_id`` en base

    Pour chaque modification dans ``modifs``, applique les conséquences
    adéquates (rôles, nouvelles actions, tâches planifiées...) et
    informe le joueur si ``silent`` vaut ``False``.
    """
    joueur = Joueur.query.get(joueur_id)
    if not joueur:
        raise ValueError(f"!sync : joueur d'ID {joueur_id} introuvable")

    member = joueur.member
    chan = joueur.private_chan

    changelog = (f"\n- {member.display_name} "
                 f"(@{member.name}#{member.discriminator}) :\n")
    notif = ""
    af = ":arrow_forward:"      # Flèche introduisant chaque modif

    if not modifs:
        changelog +=  f"    [NO MODIFS]\n"
        return [], changelog

    done = []
    for modif in modifs:
        changelog += f"    - {modif.col} : {modif.val}\n"

        if modif.col == "nom":                          # Renommage joueur
            await member.edit(nick=modif.val)
            await chan.edit(name=f"{config.private_chan_prefix}{modif.val}")
            if not silent:
                notif += (f"{af} Tu t'appelles maintenant "
                          f"{tools.bold(modif.val)}.\n")

        elif modif.col == "chambre" and not silent:     # Modification chambre
            notif += (f"{af} Tu habites maintenant "
                      f"en chambre {tools.bold(modif.val)}.\n")

        elif modif.col == "statut":
            if modif.val == Statut.vivant:              # Statut = vivant
                await member.add_roles(config.Role.joueur_en_vie)
                await member.remove_roles(config.Role.joueur_mort)
                if not silent:
                    notif += f"{af} Tu es maintenant en vie. EN VIE !!!\n"

            elif modif.val == Statut.mort:              # Statut = mort
                await member.add_roles(config.Role.joueur_mort)
                await member.remove_roles(config.Role.joueur_en_vie)
                if not silent:
                    notif += (f"{af} Tu es malheureusement décédé(e) :cry:\n"
                              "Ça arrive même aux meilleurs, en espérant "
                              "que ta mort ait été belle !\n")
                # Actions à la mort
                for action in joueur.actions:
                    if action.base.trigger_debut == ActionTrigger.mort:
                        await gestion_actions.open_action(action)

            elif modif.val == Statut.MV:                # Statut = MV
                await member.add_roles(config.Role.joueur_en_vie)
                await member.remove_roles(config.Role.joueur_mort)
                if not silent:
                    notif += (
                        f"{af} Oh ! Tu viens d'être réduit(e) au statut de "
                        "mort-vivant... Un MJ viendra te voir très vite, "
                        "si ce n'est déjà fait, mais retient que la partie "
                        "n'est pas finie pour toi !\n"
                    )

            elif not silent:                            # Statut = autre
                notif += f"{af} Nouveau statut : {tools.bold(modif.val)} !\n"

        elif modif.col == "role":                       # Modification rôle
            new_role = modif.val
            for action in joueur.actions:
                if action.base in joueur.role.base_actions:
                    # Suppression anciennes actions de rôle
                    gestion_actions.delete_action(action)

            for base in new_role.base_actions:
                # Ajout et création des tâches si trigger temporel
                action = Action(joueur=joueur, base=base, cooldown=0,
                                charges=base.base_charges)
                gestion_actions.add_action(action)

            if not silent:
                notif += (
                    f"{af} Ton nouveau rôle, si tu l'acceptes : "
                    f"{tools.bold(new_role.nom_complet)} !\nQue ce soit pour "
                    "un jour ou pour le reste de la partie, renseigne-toi en "
                    f"tapant {tools.code(f'!roles {new_role.slug}')}.\n"
                )

        elif modif.col == "camp" and not silent:    # Modification camp
            notif += (f"{af} Tu fais maintenant partie "
                      f"du camp « {tools.bold(modif.val.nom)} ».\n")

        elif modif.col == "votant_village" and not silent:
            if modif.val:                           # votant_village = True
                notif += (f"{af} Tu peux maintenant participer "
                          "aux votes du village !\n")
            else:                                   # votant_village = False
                notif += (f"{af} Tu ne peux maintenant plus participer "
                          "aux votes du village.\n")

        elif modif.col == "votant_loups" and not silent:
            if modif.val:                           # votant_loups = True
                notif += (f"{af} Tu peux maintenant participer "
                          "aux votes des loups ! Amuse-toi bien :wolf:\n")
            else:                                   # votant_loups = False
                notif += (f"{af} Tu ne peux maintenant plus participer "
                          "aux votes des loups.\n")

        elif modif.col == "role_actif" and not silent:
            if modif.val:                           # role_actif = True
                notif += (f"{af} Tu peux maintenant utiliser tes pouvoirs !\n")
            else:                                   # role_actif = False
                notif += (f"{af} Tu ne peux maintenant plus utiliser "
                          "aucun pouvoir.\n")

        setattr(joueur, modif.col, modif.val)
        # Dans tous les cas, on modifie en base
        # (après, pour pouvoir accéder aux vieux attribus plus haut)
        done.append(modif)

    if not silent:
        await chan.send(
            f":zap: {member.mention} Une action divine vient "
            f"de modifier ton existence ! :zap:\n\n{notif}\n"
            + tools.ital(":warning: Si tu penses qu'il y a erreur, "
                         "appelle un MJ au plus vite !")
        )

    return done, changelog


class Sync(commands.Cog):
    """Commandes de synchronisation des GSheets vers la BDD et les joueurs"""

    @commands.command()
    @tools.mjs_only
    async def sync(self, ctx, silent=False):
        """Récupère et applique les modifs du Tableau de bord (COMMANDE MJ)

        Args:
            silent: si spécifié (quelque soit sa valeur), les joueurs
                ne sont pas notifiés des modifications.

        Cette commande va récupérer les modifications en attente sur le
        Tableau de bord (lignes en rouge), modifer la BDD, et appliquer
        les modificatons dans Discord le cas échéant : renommage des
        utilisateurs, modification des rôles...
        """
        await ctx.send("Récupération des modifications...")
        async with ctx.typing():
            # Récupération de la liste des modifs
            modifs = get_sync()
            silent = bool(silent)
            changelog = f"Synchronisation TDB (silencieux = {silent}) :"

        if not modifs:
            await ctx.send("Pas de nouvelles modificatons.")
            return

        dic = {}        # Dicionnaire {ID joueur: modifs}
        for modif in modifs:
            if modif.id not in dic:
                dic[modif.id] = []
            dic[modif.id].append(modif)

        message = await ctx.send(
            f"{len(modifs)} modification(s) trouvée(s) "
            f"pour {len(dic)} joueur(s), go ?"
        )
        if not await tools.yes_no(message):
            await ctx.send("Mission aborted.")
            return

        # Go sync
        done = []
        async with ctx.typing():
            for joueur_id, modifs in dic.items():
                # Joueur dont au moins un attribut a été modifié
                try:
                    dn, cgl = await modif_joueur(int(joueur_id),
                                                 modifs, silent)
                except Exception:
                    # Erreur lors d'une des modifs
                    changelog += traceback.format_exc()
                    await ctx.send(
                        f"Erreur joueur {joueur_id}, passage au suivant "
                        "(voir logs pour les détails)"
                    )
                else:
                    # Pas d'erreur pour ce joueur, on enregistre
                    done.extend(dn)
                    changelog += cgl

            if done:
                # Au moins une modification a été appliquée
                config.session.commit()
                validate_sync(done)

            await tools.log(changelog, code=True)

        await ctx.send(
            f"Fait (voir {config.Channel.logs.mention} pour le détail)"
        )


    @commands.command()
    @tools.mjs_only
    async def fillroles(self, ctx):
        """Remplit les tables et #roles depuis le GSheet ad hoc (COMMANDE MJ)

        - Remplit les tables :class:`.bdd.Camp`, :class:`.bdd.Role` et
          :class:`.bdd.BaseAction` avec les informations du Google Sheets
          "Rôles et actions" (variable d'environnement
          ``LGREZ_ROLES_SHEET_ID``) ;
        - Vide le chan ``#roles`` puis le remplit avec les descriptifs
          de chaque rôle.

        Utile à chaque début de saison / changement dans les rôles/actions.
        Écrase toutes les entrées déjà en base, mais ne supprime pas
        celles obsolètes.
        """
        SHEET_ID = env.load("LGREZ_ROLES_SHEET_ID")
        workbook = gsheets.connect(SHEET_ID)    # Rôles et actions

        for table in [Camp, Role, BaseAction]:
            await ctx.send(
                f"Remplissage de la table {tools.code(table.__name__)}..."
            )
            async with ctx.typing():
                try:
                    sheet = workbook.worksheet(table.__tablename__)
                except gsheets.WorksheetNotFound:
                    raise ValueError(
                        f"!fillroles : feuille '{table.__tablename__}' non "
                        "trouvée dans le GSheet *Rôles et actions* "
                        "(`LGREZ_ROLES_SHEET_ID`)"
                    ) from None

                values = sheet.get_all_values()
                # Liste de liste des valeurs des cellules

                cols = table.columns   # "dictionnaire" nom -> colonne
                cols = {col: cols[col]
                        for col in cols.keys()
                        if not col.startswith("_")}
                if table == Role:
                    cols["camp"] = Role.attrs["camp"]
                primary_key = table.primary_col.key

                # Indices des colonnes GSheet pour chaque colonne de la table
                cols_index = {}
                try:
                    for key in cols.keys():
                        cols_index[key] = values[0].index(key)
                    if table == BaseAction:
                        roles_idx = values[0].index("roles")
                except ValueError:
                    raise ValueError(
                        f"!fillroles : colonne '{key}' non trouvée dans "
                        f"la feuille '{table.__tablename__}' du GSheet "
                        "*Rôles et actions* (`LGREZ_ROLES_SHEET_ID`)"
                    ) from None

                existants = {getattr(item, primary_key): item
                             for item in table.query.all()}

                for row in values[1:]:
                    args = {key: transtype(row[cols_index[key]], col)
                            for key, col in cols.items()}
                    if table == BaseAction:
                        # Many-to-many BaseAction <-> Rôle
                        args["roles"] = [transtype(slug.strip(), Role)
                                         for slug in row[roles_idx].split(",")
                                         if slug]

                    id = args[primary_key]
                    if id in existants:
                        for col in cols.keys():
                            if getattr(existants[id], col) != args[col]:
                                setattr(existants[id], col, args[col])
                        if table == BaseAction:
                            # Many-to-many BaseAction <-> Rôle
                            if existants[id].roles != args["roles"]:
                                existants[id].roles = args["roles"]
                    else:
                        config.session.add(table(**args))

                config.session.commit()

            await ctx.send(f"Table {tools.code(table.__name__)} remplie !")
            await tools.log(f"Table {tools.code(table.__name__)} remplie !")

        chan_roles = config.Channel.roles

        await ctx.send(f"Vidage de {chan_roles.mention}...")
        async with ctx.typing():
            await chan_roles.purge(limit=1000)

        camps = Camp.query.filter_by(public=True).all()
        est = sum(len(camp.roles) + 2 for camp in camps) + 2
        await ctx.send(f"Remplissage... (temps estimé : {est} secondes)")

        t0 = time.time()
        await chan_roles.send(
            "Voici la liste des rôles : (accessible en faisant "
            f"{tools.code('!roles')}, mais on l'a mis là parce que "
            "pourquoi pas)\n\n——————————————————————————"
        )
        async with ctx.typing():
            for camp in camps:
                if not camp.roles:
                    continue

                emoji = camp.discord_emoji_or_none
                await chan_roles.send(
                    embed=Embed(title=f"Camp : {camp.nom}").set_image(
                        url=emoji.url if emoji else None
                    )
                )
                await chan_roles.send("——————————————————————————")
                for role in camp.roles:
                    await chan_roles.send(
                        f"{emoji or ''} {tools.bold(role.nom_complet)} "
                        f"– {role.description_courte} (camp : {camp.nom})\n\n"
                        f"{role.description_longue}\n\n"
                        "——————————————————————————"
                    )

        rt = time.time() - t0
        await ctx.send(f"{chan_roles.mention} rempli ! (en {rt:.4} secondes)")
