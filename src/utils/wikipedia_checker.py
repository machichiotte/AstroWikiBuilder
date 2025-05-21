import requests
from typing import Dict, List, Optional, Tuple
import time
from dataclasses import dataclass

@dataclass
class WikiArticleInfo:
    """Information sur un article Wikipedia"""
    exists: bool
    title: str
    is_redirect: bool = False
    redirect_target: Optional[str] = None
    url: Optional[str] = None

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
    
    def check_article_exists(self, title: str) -> WikiArticleInfo:
        """
        Vérifie si un article existe sur Wikipedia en français
        
        Args:
            title: Le titre de l'article à vérifier
            
        Returns:
            WikiArticleInfo: Informations sur l'article
        """
        params = {
            'action': 'query',
            'titles': title,
            'format': 'json',
            'prop': 'info|redirects',
            'inprop': 'url',
            'redirects': 'true'
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            
            if page_id == '-1':
                return WikiArticleInfo(exists=False, title=title)
            
            page = pages[page_id]
            is_redirect = 'redirects' in page
            
            # Si c'est une redirection, obtenir la cible
            redirect_target = None
            if is_redirect and 'redirects' in data['query']:
                for redirect in data['query']['redirects']:
                    if redirect['from'] == title:
                        redirect_target = redirect['to']
                        break
            
            return WikiArticleInfo(
                exists=True,
                title=page['title'],
                is_redirect=is_redirect,
                redirect_target=redirect_target,
                url=page.get('fullurl')
            )
            
        except Exception as e:
            print(f"Erreur lors de la vérification de l'article {title}: {e}")
            return WikiArticleInfo(exists=False, title=title)
    
    def check_multiple_articles(self, titles: List[str], delay: float = 0.0) -> Dict[str, WikiArticleInfo]:
        """
        Vérifie l'existence de plusieurs articles (jusqu'à 50) en une seule requête
        
        Args:
            titles: Liste des titres d'articles à vérifier (max 50)
            delay: Délai en secondes entre chaque requête (par défaut 0)
            
        Returns:
            Dict[str, WikiArticleInfo]: Dictionnaire avec les titres comme clés et les infos comme valeurs
        """
        assert len(titles) <= 50, "L'API MediaWiki limite à 50 titres par requête."
        results = {}
        
        params = {
            'action': 'query',
            'titles': '|'.join(titles),
            'format': 'json',
            'prop': 'info|redirects',
            'inprop': 'url',
            'redirects': 'true'
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Traiter les redirections
            redirects = {}
            if 'redirects' in data['query']:
                for redirect in data['query']['redirects']:
                    redirects[redirect['from']] = redirect['to']
            
            # Traiter les pages
            pages = data['query']['pages']
            for page_id, page in pages.items():
                title = page['title']
                is_redirect = 'redirects' in page
                
                # Trouver le titre original si c'est une redirection
                original_title = None
                for orig, target in redirects.items():
                    if target == title:
                        original_title = orig
                        break
                
                results[original_title or title] = WikiArticleInfo(
                    exists=page_id != '-1',
                    title=title,
                    is_redirect=is_redirect,
                    redirect_target=redirects.get(original_title) if original_title else None,
                    url=page.get('fullurl')
                )
            
            if delay > 0:
                print(f"Attente de {delay} seconde(s) avant la prochaine requête...")
                time.sleep(delay)
                
        except Exception as e:
            print(f"Erreur lors de la vérification des articles : {e}")
            for title in titles:
                results[title] = WikiArticleInfo(exists=False, title=title)
                
        return results 