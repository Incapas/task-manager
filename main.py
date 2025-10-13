import typer

import commands.crud.create as create
import commands.crud.read as read
import commands.crud.update as update
import commands.crud.delete as delete
import commands.other.reset as reset


# Création de l'application Typer principale
app: typer.Typer = typer.Typer(no_args_is_help=True)

# Ajout du groupe de commandes 'create' à l'application principale
app.add_typer(
    # L'objet Typer importé du module 'create'
    create.app,
    # Nom de la sous-commande (ex: create ...)
    name="create",
    # Description courte dans l'aide
    help="Créer une tâche",
    # Regroupe la commande dans un panel d'aide Rich spécifique
    rich_help_panel="Opérations CRUD")

# Ajout du groupe de commandes 'read' à l'application principale
app.add_typer(
    # L'objet Typer importé du module 'read'
    read.app,
    # Nom de la sous-commande (ex: read ...)
    name="read",
    # Description courte dans l'aide
    help="Rechercher une ou plusieurs tâches",
    # Regroupe la commande dans le panel d'aide Rich 'Opérations CRUD'
    rich_help_panel="Opérations CRUD")

# Ajout du groupe de commandes 'update' à l'application principale
app.add_typer(
    # L'objet Typer importé du module 'update'
    update.app,
    # Nom de la sous-commande (ex: update ...)
    name="update",
    # Description courte dans l'aide
    help="Modifier une ou plusieurs tâches",
    # Regroupe la commande dans le panel d'aide Rich 'Opérations CRUD'
    rich_help_panel="Opérations CRUD")

# Ajout du groupe de commandes 'delete' à l'application principale
app.add_typer(
    # L'objet Typer importé du module 'delete'
    delete.app,
    # Nom de la sous-commande (ex: delete ...)
    name="delete",
    # Description courte dans l'aide
    help="Supprimer une ou plusieurs tâches",
    # Regroupe la commande dans le panel d'aide Rich 'Opérations CRUD'
    rich_help_panel="Opérations CRUD")

# Ajout du groupe de commandes 'reset' à l'application principale
app.add_typer(
    # L'objet Typer importé du module 'reset'
    reset.app,
    # Nom de la sous-commande (ex: reset ...)
    name="reset",
    # Description courte dans l'aide
    help="Réinitialiser la table de données",
    # Regroupe la commande dans le panel d'aide Rich 'Opérations autres'
    rich_help_panel="Opérations autres")

# Bloc principal d'exécution du script
if __name__ == "__main__":
    """
    Point d'entrée de l'application.
    Exécute l'application Typer pour analyser les arguments de la ligne de commande et dispatcher les commandes.
    
    Returns:
        None: Le bloc principal ne retourne rien.
    """
    app()