# 📝 Gestionnaire de tâches CLI

## Description du Projet

Ce projet est une **Application en Ligne de Commande (CLI)** construite avec la librairie **Typer** pour les interfaces en ligne de commande et **Rich** pour un affichage enrichi et lisible. Elle permet de gérer des données de type **tâches** via des opérations **CRUD** (Create, Read, Update, Delete) stockées dans une base de données **SQLite3** locale.

## ✨ Fonctionnalités Clés

* **Opérations CRUD Complètes** : Créez, lisez, modifiez et supprimez vos données (tâches).
* **Champs de Données** : Chaque donnée gère les attributs suivants :
    * **Label** (Nom de la tâche)
    * **Collection** (Catégorie)
    * **Priorité** (Niveau d'urgence)
    * **Statut** (État de progression)
* **Interface Utilisateur Enrichie** : Utilisation de **Rich** pour une aide contextuelle claire et une sortie console formatée.
* **Stockage Fiable** : Utilisation de **SQLite3** pour un stockage de données local et léger.

---

## 👥 Contributions au Projet

### 👩 Développeur Initial

Contribution résidant dans le **développement complet** de l'application, incluant la conception de l'architecture, la logique de base de données, et toutes les commandes utilisateur.

| Catégorie | Description de la contribution |
| :--- | :--- |
| **Logique Principale** | Développement des **Opérations CRUD** (Create, Read, Update, Delete) sur la base SQLite3. |
| **Interface de Commande** | Conception et implémentation de toutes les **Commandes Typer** (`create`, `read`, `update`, `delete`, `reset`). |
| **Architecture CLI** | Établissement de l'application Typer principale dans `main.py` et de la structure des modules de commande. |
| **Stockage des Données** | Gestion de la connexion, de l'initialisation et de la structure de la base de données **SQLite3**. |

### 🧑 Assistant IA Gemini

Contribution résidant dans l'**amélioration de la qualité logicielle** et l'**optimisation des outils de diagnostic** et de la documentation.

| Catégorie | Description de la Contribution |
| :--- | :--- |
| **Documentation Détaillée** | 📝 Rédaction complète des **docstrings** et des **commentaires** pour documenter l'usage et la logique interne de toutes les fonctions et classes. |
| **Optimisation du Logger** | Mise en place et configuration d'une structure de **logging** efficace pour le diagnostic et le suivi des opérations. |
| **Documentation Externe** | Structuration et rédaction du fichier `README.md`. |

---

## 🛠️ Installation

Pour commencer à utiliser l'application, suivez ces étapes :

### Prérequis

Assurez-vous d'avoir **Python** installé sur votre système.

> **⚠️ Version Minimale de Python**
>
> Pour garantir la compatibilité avec **Typer** et **Rich**, vous devez utiliser **Python 3.8 ou une version ultérieure** (projet développé avec Python 3.12.4).

### Clônage et Configuration

1.  **Clonez le dépôt :**

    ```bash
    git clone [URL_DEPOT]
    cd [NOM_DU_DEPOT]
    ```

2.  **Installez les dépendances :**
    Toutes les dépendances nécessaires sont listées dans le fichier `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialisez la base de données :**
    Après avoir installé les dépendances, vous devez initialiser la base de données SQLite3 en créant la structure de table nécessaire.

    ```bash
    python main.py reset table --reset
    ```
    💡 Note : Cette commande crée la table de tâches. Si elle existe déjà, l'option `--reset` force sa recréation, supprimant toute donnée existante.

---

## 🚀 Utilisation

L'application est exécutée via le script principal nommé **`main.py`**.

### Aide Générale

Pour afficher l'aide principale et découvrir toutes les commandes disponibles :

```bash
python main.py --help
````

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

## 📐 Architecture du Code

Le fichier principal (`main.py`) regroupe l'application Typer et délègue les fonctionnalités à des modules spécifiques, assurant une bonne modularité :

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

Les opérations **CRUD** sont gérées dans des modules séparés (`commands/crud/create.py`, `commands/crud/read.py`, etc.).

```
```