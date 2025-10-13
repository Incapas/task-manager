import sqlite3
from sqlite3 import Connection, Cursor
from typing import Tuple, Dict, Optional, Any, List

from .logging_manager import logs


class Database:
    """Définition de la classe pour la gestion de la connexion à la base de données."""

    database: str
    con: Optional[Connection]
    cur: Optional[Cursor]
    
    def __init__(self, database: str = "database.sqlite3") -> None:
        """
        Initialise l'objet Database.

        Args:
            database (str): Le nom du fichier de la base de données SQLite. 
        """
        # Stocke le nom du fichier de la base de données
        self.database = database

        # Initialise la connexion et le curseur à None
        self.con = None
        self.cur = None
        
    def __enter__(self) -> Cursor:
        """
        Ouvre la connexion et crée un curseur, puis retourne le curseur. 
        Méthode appelée lors de l'entrée dans le bloc 'with'.
        
        Returns:
            sqlite3.Cursor: Le curseur de la connexion à la base de données.
        """
        # Établit la connexion à la base de données SQLite
        self.con = sqlite3.connect(self.database)

        # Crée un objet curseur pour exécuter les commandes SQL
        self.cur = self.con.cursor()

        # Retourne le curseur pour être utilisé dans le bloc 'with'
        return self.cur
        
    def __exit__(self, exc_type: Optional[type], exc_value: Optional[BaseException], traceback: Optional[Any]) -> None:
        """
        Gère la fermeture de la connexion, le commit ou le rollback.
        Méthode appelée lors de la sortie du bloc 'with'.
        
        Args:
            exc_type (Optional[type]): Le type de l'exception levée (None si pas d'exception).
            exc_value (Optional[BaseException]): L'instance de l'exception.
            traceback (Optional[Any]): L'objet traceback.
        """
        # Vérifie si la connexion existe et n'est pas None
        if self.con:
            # Si aucune exception n'est survenue dans le bloc 'with'
            if exc_type is None:
                # Valide les changements (commit)
                self.con.commit()
            # Si une exception est survenue
            else:
                # Annule les changements (rollback)
                self.con.rollback()
            # Ferme la connexion à la base de données
            self.con.close()

# Définit le type pour le résultat d'une ligne de base de données (Tuple d'éléments de type Any)
Row = Tuple[Any, ...]

# Définit le type pour le résultat d'une requête (Liste de lignes)
Result = List[Row]

def execute_query(query: str, data: Tuple[Any, ...]) -> Optional[Result]:
    """
    Exécute une requête SQL et retourne les résultats si c'est une requête SELECT.

    Args:
        query (str): La requête SQL à exécuter.
        data (Tuple[Any, ...]): Le tuple de données à substituer dans la requête.

    Returns:
        Optional[Result]: Les résultats de la requête (liste de tuples) si c'est un SELECT, sinon None.
    """
    # Vérifie si la requête commence par "SELECT"
    is_select: bool = query.startswith("SELECT")
    
    # Initialisation du résultat à None ou au type de retour attendu
    result: Optional[Result] = None

    # Utilisation du context manager Database pour gérer la connexion et la fermeture
    with Database() as cur:
        # Exécute la requête avec les données fournies
        cur.execute(query, data)

        # Si c'est une requête de sélection (SELECT)
        if is_select:
            # Récupère tous les résultats de la requête
            result = cur.fetchall()
            
    # Retourne le résultat (la liste des lignes ou None)
    return result

def insert_into_database(values: Tuple[Any, ...]) -> None:
    """
    Insère une nouvelle ligne dans la table 'task'.

    Args:
        values (Tuple[Any, ...]): Un tuple contenant les valeurs de la tâche à insérer.
        
    Returns:
        None: La fonction ne retourne rien.
    """
    # Crée une chaîne de caractères pour les placeholders (?), correspondant au nombre de valeurs
    placeholders: str = f"({", ".join(["?" for _ in range(len(values))])})"

    # Construction de la requête SQL d'insertion avec les placeholders
    query: str = f"INSERT INTO task (label, collection, priority, status) VALUES {placeholders}"

    # Les données à insérer sont les valeurs passées en argument
    data: Tuple[Any, ...] = values

    # Enregistrement de l'opération dans les logs
    logs(query, data)

    # Exécution de la requête d'insertion
    execute_query(query, data)

    # Retourne explicitement None
    return None

# Définit le type pour les options de filtrage (clés str, valeurs de type variable)
FilterOptions = Dict[str, Any]

def select_from_database(options: FilterOptions) -> Optional[Result]:
    """
    Sélectionne des tâches dans la table 'task' en fonction des options de filtre.

    Args:
        options (FilterOptions): Un dictionnaire de critères de filtrage.

    Returns:
        Optional[Result]: Une liste des tâches (lignes de la DB) ou None.
    """
    # Filtre les options pour ne garder que celles qui ont une valeur (non nulles/vides)
    criteria: FilterOptions = {k: v for k, v in options.items() if v}

    # Crée la chaîne de caractères pour la clause WHERE (ex: "key1 = ? AND key2 = ?")
    expression: str = " AND ".join([f"{k} = ?" for k, v in criteria.items()])

    # Extrait les valeurs des critères pour les utiliser comme données dans la requête
    data: Tuple[Any, ...] = tuple(criteria.values())

    # Si aucune donnée de filtre n'est présente (sélectionner tout)
    if not data:
        # Requête pour sélectionner toutes les colonnes de toutes les tâches
        # Le tri sera automatiquement appliqué sur le libellé de la collection de façon ascendante A -> Z
        query: str = "SELECT * FROM task ORDER BY collection ASC"
        # Enregistrement de l'opération (READ) sans les données (elles sont vides)
        logs(query) 
        # Exécution et retour des résultats
        return execute_query(query, data)
    
    # Si des critères sont présents, construction de la requête avec la clause WHERE
    # Le tri sera automatiquement appliqué sur le libellé de la collection de façon ascendante A -> Z
    query: str = f"SELECT * FROM task WHERE {expression} ORDER BY collection ASC"

    # Enregistrement de l'opération (READ) avec la requête et les données de filtrage
    logs(query, data)

    # Exécution et retour des résultats
    return execute_query(query, data)
    
def update_from_database(columns: FilterOptions, options: FilterOptions) -> None:
    """
    Met à jour les colonnes de tâches sélectionnées par les options de critère.

    Args:
        columns (FilterOptions): Un dictionnaire de colonnes à mettre à jour et leurs nouvelles valeurs.
        options (FilterOptions): Un dictionnaire de critères pour sélectionner les tâches à mettre à jour.
        
    Returns:
        None: La fonction ne retourne rien.
    """
    # Filtre les colonnes à mettre à jour pour ne garder que celles qui ont une valeur
    columns: FilterOptions = {k: v for k, v in columns.items() if v}
    # Filtre les critères de sélection pour ne garder que ceux qui ont une valeur
    criteria: FilterOptions = {k: v for k, v in options.items() if v}

    # Crée la chaîne de caractères pour la clause SET (colonnes à mettre à jour)
    expression_column: str = ", ".join([f"{k} = ?" for k, v in columns.items()])
    # Crée la chaîne de caractères pour la clause WHERE (critères de sélection)
    expression_criteria: str = " AND ".join([f"{k} = ?" for k, v in criteria.items()])

    # Construction de la requête SQL de mise à jour
    query: str = f"UPDATE task SET {expression_column} WHERE {expression_criteria}"

    # Crée le tuple de données en combinant les valeurs des colonnes à mettre à jour et des critères
    data: Tuple[Any, ...] = (*columns.values(), *criteria.values())
        
    # Enregistrement de l'opération (UPDATE) dans les logs (Note: l'appel à logs a été simplifié dans votre code)
    logs(query, data)

    # Exécution de la requête de mise à jour
    execute_query(query, data)
    # Retourne explicitement None (conforme à l'annotation de type -> None)
    return None
   
def delete_from_database(options: FilterOptions) -> None:
    """
    Supprime des tâches dans la table 'task' en fonction des options de critère.

    Args:
        options (FilterOptions): Un dictionnaire de critères pour sélectionner les tâches à supprimer.
        
    Returns:
        None: La fonction ne retourne rien.
    """
    # Filtre les critères de sélection pour ne garder que ceux qui ont une valeur
    criteria: FilterOptions = {k: v for k, v in options.items() if v}

    # Crée la chaîne de caractères pour la clause WHERE (critères de sélection)
    expression: str = " AND ".join([f"{k} = ?" for k, v in criteria.items()])
    
    # Construction de la requête SQL de suppression
    query: str = f"DELETE FROM task WHERE {expression}"

    # Extrait les valeurs des critères pour les utiliser comme données dans la requête
    data: Tuple[Any, ...] = tuple(criteria.values())

    # Enregistrement de l'opération (DELETE) dans les logs
    logs(query, data)

    # Exécution de la requête de suppression
    execute_query(query, data)

    # Retourne explicitement None
    return None

def drop_create_table() -> None:
    """
    Supprime la table 'task' si elle existe, puis la recrée avec la structure définie.

    Returns:
        None: La fonction ne retourne rien.
    """
    # Définition de la requête SQL multiple (DROP et CREATE TABLE)
    query: str = """
    DROP TABLE IF EXISTS task;
    
    CREATE TABLE IF NOT EXISTS task(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        label TEXT NOT NULL,
        collection TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL
    );
    """
    # Utilisation du context manager Database
    with Database() as cur:
        # Exécute un script SQL (plusieurs commandes séparées par ;)
        cur.executescript(query)
    
    # Enregistrement de l'opération (RESET) dans les logs
    logs()
    
    # Retourne explicitement None
    return None