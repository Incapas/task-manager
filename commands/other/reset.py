from typing_extensions import Annotated
import typer

from manager.database_manager import drop_create_table


# Création de l'application Typer principale
app: typer.Typer = typer.Typer(no_args_is_help=True)

# Définition de la commande "table" pour l'application Typer
@app.command(name="table", help="Réinitialiser la table de données")
def reset_table(reset: Annotated[bool, typer.Option(show_default="Réinitialisation abandonnée")] = False) -> None:
    """
    Réinitialise la table 'task' dans la base de données.

    Args:
        reset (Annotated[bool, typer.Option]): Confirmation de la réinitialisation de la table.
                                               Par défaut à False.
    
    Returns:
        None: La fonction ne retourne rien explicitement, elle utilise typer.echo pour l'affichage.
    """
    # Vérifie si l'utilisateur a confirmé la réinitialisation (passé --reset)
    if reset:
        # Appelle la fonction pour supprimer et recréer la table de la base de données
        drop_create_table()
        # Affiche un message de succès
        return typer.echo("Réinitialisation accomplie !")
    # Si la réinitialisation n'est pas confirmée
    return typer.echo("Réinitilisation abandonnée !")
  
# Bloc principal d'exécution du script
# Exécute l'application Typer, ce qui analyse les arguments de la ligne de commande
if __name__ == "__main__":
    app()
