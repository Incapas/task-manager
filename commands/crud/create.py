from typing_extensions import Annotated
import typer

from manager.constant_manager import *
from manager.database_manager import insert_into_database


# Création de l'application Typer principale
app: typer.Typer = typer.Typer(no_args_is_help=True)

# Définition de la commande "task" pour l'application Typer, utilisée pour créer une tâche
@app.command(name="task", help="Commande qui permet de créer une tâche")
def create_task(
    label: Annotated[str, typer.Argument(
        help="Libellé")
        ],

    collection: Annotated[str, typer.Argument(
        help="Collection")
        ] = "divers",

    priority: Annotated[str, typer.Argument(
        help="Priorité",
        formats=PRIORITY)
        ] = PRIORITY[0],

    status: Annotated[str, typer.Argument(
        help="Statut",
        formats=STATUS)
        ] = STATUS[0],
    ) -> None:
    """
    Crée et enregistre une nouvelle tâche dans la base de données.

    Les paramètres correspondent aux colonnes de la table 'task'.

    Args:
        label (Annotated[str, typer.Argument]): Le libellé ou titre de la tâche (obligatoire).
        collection (Annotated[str, typer.Argument]): Le nom de la collection à laquelle appartient la tâche (obligatoire).
        priority (Annotated[str, typer.Argument]): Le niveau de priorité de la tâche. Par défaut à la première option de PRIORITY.
        status (Annotated[str, typer.Argument]): Le statut actuel de la tâche. Par défaut à la première option de STATUS.

    Returns:
        None: La fonction ne retourne rien explicitement, elle utilise typer.echo pour l'affichage.
    """

    # Normalisation du libellé de la tâche (minuscules et suppression des espaces blancs aux extrémités)
    label: str = label.lower().strip()

    # Normalisation du nom de la collection (minuscules et suppression des espaces blancs aux extrémités)
    collection: str = collection.lower().strip()

    # Assemblage des données de la tâche dans un tuple pour l'insertion
    data: tuple[str, str, str, str, str] = (label, collection, priority, status)

    # Appel de la fonction pour insérer le tuple de données dans la base de données
    insert_into_database(data)

    # Affichage d'un message de confirmation à l'utilisateur
    typer.echo(f"Création effectuée !")

    # Retourne explicitement None car la fonction ne doit pas retourner de valeur
    return None

# Bloc principal d'exécution du script
# Exécute l'application Typer, ce qui analyse les arguments de la ligne de commande
if __name__ == "__main__":
    app()
