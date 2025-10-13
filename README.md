# 📝 Gestionnaire de tâches CLI

## Description du Projet

Ce projet est une **Application en Ligne de Commande (CLI)** construite avec la librairie **Typer** pour les interfaces en ligne de commande et **Rich** pour un affichage enrichi et lisible. Elle permet de gérer des données de type **tâches** via des opérations **CRUD** (Create, Read, Update, Delete) stockées dans une base de données **SQLite3**.

### Fonctionnalités Clés

  * **Opérations CRUD Complètes** : Créez, lisez, modifiez et supprimez vos données (tâches).
  * **Champs de Données** : Chaque donnée gère les attributs suivants :
      * **Label** (Nom de la tâche)
      * **Collection** (Catégorie)
      * **Priorité** (Niveau d'urgence)
      * **Statut** (État de progression)
  * **Interface Utilisateur** : Utilisation de **Rich** pour une aide contextuelle claire et une sortie console formatée.
  * **Stockage Fiable** : Utilisation de **SQLite3** pour un stockage de données local et léger.

-----

## Installation

Pour commencer à utiliser l'application, suivez ces étapes :

### Prérequis

Assurez-vous d'avoir **Python** installé sur votre système.

> **⚠️ Version Minimale de Python**
>
> Pour garantir la compatibilité avec **Typer** et **Rich**, vous devez utiliser **Python 3.8 ou une version ultérieure** (projet développé avec Python 3.12.4).

### Clônage et Configuration

1.  **Clonez le dépôt :**

    ```bash
    git clone [URL_DE_VOTRE_DEPOT]
    cd [NOM_DU_DEPOT]
    ```

2.  **Installez les dépendances :**
    Toutes les dépendances nécessaires sont listées dans le fichier `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

-----

## Utilisation

L'application est exécutée via le script principal nommé **`main.py`**.

### Aide Générale

Pour afficher l'aide principale et découvrir toutes les commandes disponibles :

```bash
python main.py --help
```

Vous devriez voir les groupes de commandes clairement séparés grâce à **Rich** (e.g., "Opérations CRUD" et "Opérations autres").

### Structure des Commandes

L'application utilise des **sous-commandes** pour organiser les opérations :

| Opération | Commande | Description |
| :--- | :--- | :--- |
| **Créer** | `python main.py create ...` | Créer une nouvelle tâche. |
| **Lire** | `python main.py read ...` | Rechercher et afficher des tâches. |
| **Modifier** | `python main.py update ...` | Modifier les attributs d'une ou plusieurs tâches. |
| **Supprimer** | `python main.py delete ...` | Supprimer une ou plusieurs tâches. |
| **Réinitialiser** | `python main.py reset ...` | Réinitialiser (vider) la table de données. |

> **💡 Astuce :** Pour chaque sous-commande (ex: `create`), utilisez l'option `--help` pour voir ses arguments et options spécifiques : `python main.py create --help`.

-----

## Architecture du Code

Le fichier principal (`main.py`) regroupe l'application Typer et délègue les fonctionnalités à des modules spécifiques :

```python
# Fichier principal (main.py)

# ... Imports des modules de commande ...
import commands.crud.create as create
# ...

# Création de l'application Typer principale
app: typer.Typer = typer.Typer(no_args_is_help=True)

# Ajout des groupes de commandes
app.add_typer(create.app, name="create", help="Créer une tâche", rich_help_panel="Opérations CRUD")
app.add_typer(read.app, name="read", help="Rechercher une ou plusieurs tâches", rich_help_panel="Opérations CRUD")
# ... autres commandes CRUD ...
app.add_typer(reset.app, name="reset", help="Réinitialiser la table de données", rich_help_panel="Opérations autres")
# ...
```

Les opérations **CRUD** sont gérées dans des modules séparés (`commands/crud/create.py`, `commands/crud/read.py`, etc.), favorisant la modularité.