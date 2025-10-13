from typing_extensions import Annotated
from typing import Dict, Tuple, Any

import typer

from manager.database_manager import update_from_database
from manager.constant_manager import *


# Création de l'application Typer principale
app: typer.Typer = typer.Typer(no_args_is_help=True)

# Définition de la commande "task" pour l'application Typer, utilisée pour modifier des tâches
@app.command(name="task", help="Modifier une ou plusieurs tâches")
def update_task(
    # --- Critères de sélection (Clause WHERE) ---

    # Critère de sélection par ID
    expr_id: Annotated[int, typer.Option(
        "--where-id",
        help="Condition sur l'id",
        show_default="Vide")
        ] = 0,

    # Critère de sélection par libellé
    expr_label: Annotated[str, typer.Option(
        "--where-label",
        help="Condition sur le libellé",
        show_default="Vide")
        ] = "",

    # Critère de sélection par collection
    expr_collection: Annotated[str, typer.Option(
        "--where-collection",
        help="Condition sur la collection",
        show_default="Vide",)
        ] = "",

    # Critère de sélection par priorité, avec formatage basé sur les constantes
    expr_priority: Annotated[str, typer.Option(
        "--where-priority",
        help="Condition sur la priorité",
        show_default="Vide",
        formats=PRIORITY)
        ] = "",

    # Critère de sélection par statut, avec formatage basé sur les constantes
    expr_status: Annotated[str, typer.Option(
        "--where-status",
        help="Condition sur le statut",
        show_default="Vide",
        formats=STATUS)
        ] = "",

    # --- Colonnes à mettre à jour (Clause SET) ---

    # Nouvelle valeur pour le libellé
    column_label: Annotated[str, typer.Option(
        "--col-label",
        help="Modifier le libellé",
        show_default="Vide")
        ] = "",

    # Nouvelle valeur pour la collection
    column_collection: Annotated[str, typer.Option(
        "--col-collection",
        help="Modifier la collection",
        show_default="Vide")
        ] = "",

    # Nouvelle valeur pour la priorité, avec formatage basé sur les constantes
    column_priority: Annotated[str, typer.Option(
        "--col-priority",
        help="Modifier la priorité",
        show_default="Vide",
        formats=PRIORITY)
        ] = "",

    # Nouvelle valeur pour le statut, avec formatage basé sur les constantes
    column_status: Annotated[str, typer.Option(
        "--col-status",
        help="Modifier le statut",
        show_default="Vide",
        formats=STATUS)
        ] = "",
    ) -> None:
    """
    Met à jour une ou plusieurs tâches dans la base de données.

    Nécessite à la fois des critères de sélection (WHERE) et des valeurs à modifier (SET).

    Args:
        expr_id (Annotated[int, typer.Option]): Critère WHERE sur l'ID de la tâche.
        expr_label (Annotated[str, typer.Option]): Critère WHERE sur le libellé.
        expr_collection (Annotated[str, typer.Option]): Critère WHERE sur la collection.
        expr_priority (Annotated[str, typer.Option]): Critère WHERE sur la priorité.
        expr_status (Annotated[str, typer.Option]): Critère WHERE sur le statut.
        column_label (Annotated[str, typer.Option]): Nouvelle valeur SET pour le libellé.
        column_collection (Annotated[str, typer.Option]): Nouvelle valeur SET pour la collection.
        column_priority (Annotated[str, typer.Option]): Nouvelle valeur SET pour la priorité.
        column_status (Annotated[str, typer.Option]): Nouvelle valeur SET pour le statut.

    Returns:
        None: La fonction ne retourne rien explicitement, elle utilise typer.echo pour la validation.
    """

    # Création du dictionnaire des colonnes à mettre à jour (Clause SET)
    columns: Dict[str, str] = {
        "label": column_label,
        "collection": column_collection,
        "priority": column_priority,
        "status": column_status,
    }

    # Création du dictionnaire des critères de sélection (Clause WHERE)
    options: Dict[str, int | str] = {
        "id": expr_id,
        "label": expr_label,
        "collection": expr_collection,
        "priority": expr_priority,
        "status": expr_status,
    }

    # Vérifie si au moins une colonne à mettre à jour a été renseignée
    verif_columns: bool = any(tuple(columns.values()))

    # Vérifie si au moins un critère de sélection a été renseigné
    verif_options: bool = any(tuple(options.values()))

    # Logique de validation des entrées utilisateur :
    
    # Cas 1 : Aucune option (SET ou WHERE) n'a été utilisée
    if not verif_columns and not verif_options:
        # Affiche un message d'erreur général
        typer.echo("Aucune option n'a été utilisée")

    # Cas 2 : Des critères de sélection (WHERE) sont là, mais pas de colonnes à mettre à jour (SET)
    elif not verif_columns:
        # Affiche un message d'erreur spécifique pour les colonnes à modifier
        typer.echo("Aucun critère n'a été renseigné pour la condition WHERE")

    # Cas 3 : Des colonnes à mettre à jour (SET) sont là, mais pas de critères de sélection (WHERE)
    elif not verif_options:
        # Affiche un message d'erreur spécifique pour les critères de sélection
        typer.echo("Aucune nouvelle valeur a été renseignée")

    # Cas 4 : Tout est correct (colonnes SET et critères WHERE sont présents)
    else:
        # Exécute la mise à jour des tâches dans la base de données
        update_from_database(columns, options)

        # Affichage d'un message de confirmation à l'utilisateur
        typer.echo(f"Modification effectuée !")
        
    # Retourne explicitement None car la fonction ne doit pas retourner de valeur
    return None
    
# Bloc principal d'exécution du script
# Exécute l'application Typer, ce qui analyse les arguments de la ligne de commande
if __name__ == "__main__":
    app()