from typing_extensions import Annotated
from typing import Dict, List, Tuple, Any

import typer
from rich.console import Console
from rich.table import Table

from manager.database_manager import select_from_database
from manager.constant_manager import *


# Création de l'application Typer principale
app: typer.Typer = typer.Typer(no_args_is_help=True)

# Définition de la commande "task" pour l'application Typer, utilisée pour rechercher des tâches
@app.command(name="task", help="Rechercher une ou plusieurs tâches")
def read_task(
    # Paramètre pour filtrer par l'identifiant unique de la tâche
    id: Annotated[int, typer.Option(
        help="Recherche par l'identifiant unique",
        show_default="Vide")
        ] = 0,

    # Paramètre pour filtrer par le libellé de la tâche
    label: Annotated[str, typer.Option(
        help="Recherche par le libellé",
        show_default="Vide")
        ] = "",

    # Paramètre pour filtrer par la collection de la tâche
    collection: Annotated[str, typer.Option(
        help="Recherche par la collection",
        show_default="Vide")
        ] = "",

    # Paramètre pour filtrer par la priorité, avec formatage basé sur les constantes
    priority: Annotated[str, typer.Option(
        help="Recherche par la priorité",
        show_default="Vide",
        formats=PRIORITY)
        ] = "",

    # Paramètre pour filtrer par le statut, avec formatage basé sur les constantes
    status: Annotated[str, typer.Option(
        help="Recherche par le statut",
        show_default="Vide",
        formats=STATUS)
        ] = "",

    ) -> None:
    """
    Recherche et affiche des tâches de la base de données en fonction des options de filtrage fournies.

    Affiche les résultats dans un tableau formaté par Rich.

    Args:
        id (Annotated[int, typer.Option]): L'identifiant unique de la tâche (0 par défaut, ignoré si non spécifié).
        label (Annotated[str, typer.Option]): Le libellé de la tâche.
        collection (Annotated[str, typer.Option]): La collection de la tâche.
        priority (Annotated[str, typer.Option]): Le niveau de priorité de la tâche.
        status (Annotated[str, typer.Option]): Le statut actuel de la tâche.

    Returns:
        None: La fonction ne retourne rien explicitement, elle affiche les résultats via Rich.
    """
    
    # Construction du dictionnaire des critères de recherche
    options: Dict[str, int | str] = {
        "id": id,
        "label": label,
        "collection": collection,
        "priority": priority,
        "status": status,
        }

    # Appel de la fonction pour récupérer la liste des tâches (Row = Tuple[Any, ...])
    tasks: List[Tuple[Any, ...]] = select_from_database(options)

    # Création de l'objet Table de Rich pour la présentation des données
    table: Table = Table(
        # Titre du tableau
        title="Liste des tâches", 
        # Affichage des lignes de séparation
        show_lines=True, 
        # Espacement intérieur
        padding=1,
        # Style du titre (en gras)
        title_style="bold"
        )
    
    # Ajout des en-têtes de colonnes au tableau Rich
    table.add_column("ID")
    table.add_column("Libellé")
    table.add_column("Collection")
    table.add_column("Priorité")
    table.add_column("Statut")

    # Style de la colonne "priorité"
    priority_style: Dict[str, str] = {
        "optionnelle": ":white_circle: optionnelle",
        "basse": ":blue_circle: basse",
        "moyenne": ":yellow_circle: moyenne",
        "haute": ":orange_circle: haute",
        "urgente": ":red_circle: urgente"
    }

    # Style de la colonne "statut"
    status_style: Dict[str, str] = {
        "à faire": ":exclamation: à faire",
        "en cours": ":hourglass_flowing_sand: en cours",
        "terminée": ":white_check_mark: terminée",
        "annulée": ":x: annulée"
    }

    # Itération sur chaque tâche récupérée depuis la base de données
    for task in tasks:
        # Ajout d'une ligne au tableau, convertissant les types non-string si nécessaire (ID)
        table.add_row(
        str(task[0]),               # ID (converti en str)
        task[1],                    # Libellé
        task[2],                    # Collection
        priority_style[task[3]],    # Priorité
        status_style[task[4]]       # Statut
        )

    # Création de l'objet Console Rich
    console: Console = Console()

    # Efface le contenu de la console avant l'affichage du tableau
    console.clear()

    # Affiche le tableau Rich formaté dans la console
    console.print(table)
    
    # Retourne explicitement None car la fonction ne doit pas retourner de valeur
    return None

# Bloc principal d'exécution du script
# Exécute l'application Typer, ce qui analyse les arguments de la ligne de commande
if __name__ == "__main__":
    app()