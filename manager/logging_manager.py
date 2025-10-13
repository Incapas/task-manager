import logging
from typing import Tuple, Optional, Any


# Récupération d'un logger nommé pour la gestion des messages de log
logger: logging.Logger = logging.getLogger(__name__)

# Définition de la fonction de journalisation des opérations de base de données
def logs(
        query: Optional[str] = None, 
        data: Optional[Tuple[Any, ...]] = None
        ) -> None:
    """
    Configure et enregistre les logs des opérations sur la base de données.

    Args:
        query (Optional[str]): La requête SQL exécutée.
        data (Optional[Tuple[Any, ...]]): Les données associées à la requête.

    Returns:
        None: La fonction ne retourne rien.
    """
    # Configuration de base pour le système de logging (uniquement si non configuré)
    logging.basicConfig(
        # Spécifie le fichier où les logs seront écrits
        filename="task_manager.log",
        # Définit le niveau de logging minimum à INFO
        level=logging.INFO,
        # Définit le format des messages de log (horodatage - niveau - message)
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Initialisation de la variable qui contiendra le message de log final
    message: str

    # Vérifie si une requête et des données sont fournies (opérations CRUD)
    if query and data:
        # Nettoie la requête (enlève les retours à la ligne et les espaces inutiles)
        message = query.replace("\n", "").strip()
        # Ajoute les données associées à la fin du message
        message += f" = {data}"
    # Si la requête ou les données sont manquantes (souvent pour la réinitialisation)
    else: 
        # Définit un message générique pour la réinitialisation
        message = "Réinitialisation de la base de données"
 
    # Enregistrement du message de log formaté
    logger.info(msg=message)
    
    # Ne retourne rien
    return None