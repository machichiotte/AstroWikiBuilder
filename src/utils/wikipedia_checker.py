import requests
from typing import Dict, List, Optional
import time

class WikipediaChecker:
    """
    Classe pour vérifier l'existence des articles sur Wikipedia en français
    """
    BASE_URL = "https://fr.wikipedia.org/w/api.php"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AstroWikiBuilder/1.0 (https://github.com/votre-username/AstroWikiBuilder; machichiotte@gmail.com)'
        })
    
    def check_article_exists(self, title: str) -> bool:
        """
        Vérifie si un article existe sur Wikipedia en français
        
        Args:
            title: Le titre de l'article à vérifier
            
        Returns:
            bool: True si l'article existe, False sinon
        """
        params = {
            'action': 'query',
            'titles': title,
            'format': 'json',
            'prop': 'info',
            'inprop': 'url'
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Vérifier si l'article existe
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            
            # Si page_id est -1, l'article n'existe pas
            exists = page_id != '-1'
            print(f"Vérification de '{title}': {'existe' if exists else 'n\'existe pas'}")
            return exists
            
        except Exception as e:
            print(f"Erreur lors de la vérification de l'article {title}: {e}")
            return False
    
    def check_multiple_articles(self, titles: List[str], delay: float = 0.0) -> Dict[str, bool]:
        """
        Vérifie l'existence de plusieurs articles (jusqu'à 50) en une seule requête
        Args:
            titles: Liste des titres d'articles à vérifier (max 50)
            delay: Délai en secondes entre chaque requête (par défaut 0)
        Returns:
            Dict[str, bool]: Dictionnaire avec les titres comme clés et leur existence comme valeurs
        """
        assert len(titles) <= 50, "L'API MediaWiki limite à 50 titres par requête."
        results = {}
        params = {
            'action': 'query',
            'titles': '|'.join(titles),
            'format': 'json',
            'prop': 'info',
            'inprop': 'url'
        }
        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            pages = data['query']['pages']
            for page_id, page in pages.items():
                title = page['title']
                # Vérifier si la page existe et n'est pas une redirection
                exists = page_id != '-1' and 'redirect' not in page
                status = "existe" if exists else "n'existe pas"
                print(f"Vérification de '{title}': {status}")
                results[title] = exists
            if delay > 0:
                print(f"Attente de {delay} seconde(s) avant la prochaine requête...")
                time.sleep(delay)
        except Exception as e:
            print(f"Erreur lors de la vérification des articles : {e}")
            for title in titles:
                results[title] = False
        return results 