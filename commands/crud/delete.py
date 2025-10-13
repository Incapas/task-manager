from typing_extensions import Annotated
import typer

from manager.database_manager import delete_from_database
from manager.constant_manager import *


# Création de l'application Typer principale
app: typer.Typer = typer.Typer(no_args_is_help=True)

# Définition de la commande "task" pour l'application Typer, utilisée pour supprimer des tâches
@app.command(name="task", help="Supprimer une ou plusieurs tâches")
def delete_task(
    # Paramètre pour filtrer par l'identifiant unique de la tâche
    id: Annotated[int, typer.Option(
        help="Suppression par l'identifiant unique", 
        show_default="Vide")
        ] = 0,

    # Paramètre pour filtrer par le libellé de la tâche
    label: Annotated[str, typer.Option(
        help="Suppression par le libellé", 
        show_default="Vide")
        ] = "",

    # Paramètre pour filtrer par la collection de la tâche
    collection: Annotated[str, typer.Option(
        help="Suppression par la collection", 
        show_default="Vide")
        ] = "",

    # Paramètre pour filtrer par la priorité de la tâche, avec formatage basé sur les constantes
    priority: Annotated[str, typer.Option(
        help="Suppression par la priorité",
        show_default="Vide", 
        formats=PRIORITY)
        ] = "",

    # Paramètre pour filtrer par le statut de la tâche, avec formatage basé sur les constantes
    status: Annotated[str, typer.Option(
        help="Suppression par le statut",
        show_default="Vide", 
        formats=STATUS)
        ] = "",
    ) -> None:
    """
    Supprime une ou plusieurs tâches de la base de données en fonction des options de filtrage fournies.

    La suppression est basée sur l'ensemble des options non vides passées.

    Args:
        id (Annotated[int, typer.Option]): L'identifiant unique de la tâche à supprimer (par défaut: 0, ignoré si non spécifié).
        label (Annotated[str, typer.Option]): Le libellé de la tâche à supprimer (supporte la suppression de plusieurs tâches si non unique).
        collection (Annotated[str, typer.Option]): Le nom de la collection à supprimer.
        priority (Annotated[str, typer.Option]): Le niveau de priorité pour le filtre de suppression.
        status (Annotated[str, typer.Option]): Le statut pour le filtre de suppression.

    Returns:
        None: La fonction ne retourne rien explicitement.
    """
    
    # Construction du dictionnaire d'options de filtrage
    options: dict[str, int | str] = {
        "id": id,
        "label": label,
        "collection": collection,
        "priority": priority,
        "status": status,
        }

    # Appel de la fonction pour supprimer les tâches correspondantes dans la base de données
    delete_from_database(options)

    # Affichage d'un message de confirmation à l'utilisateur
    typer.echo(f"Suppression effectuée !")

    # Retourne explicitement None car la fonction ne doit pas retourner de valeur
    return None

# Bloc principal d'exécution du script
# Exécute l'application Typer, ce qui analyse les arguments de la ligne de commande
if __name__ == "__main__":
    app()