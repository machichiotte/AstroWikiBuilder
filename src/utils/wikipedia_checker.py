import requests
from typing import Dict, List, Optional, Tuple, Any
import time
from dataclasses import dataclass
import unicodedata
import re
import os
import csv
import json
from datetime import datetime

@dataclass
class WikiArticleInfo:
    """Information sur un article Wikipedia"""
    exists: bool
    title: str
    is_redirect: bool = False
    redirect_target: Optional[str] = None
    url: Optional[str] = None
    host_star: Optional[str] = None

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
    
    def normalize_title(self, title: str) -> str:
        """
        Normalise un titre pour la comparaison :
        - Convertit en minuscules
        - Remplace les espaces, underscores et tirets par des tirets
        - Retire les accents
        - Retire les caractères spéciaux
        
        Args:
            title: Le titre à normaliser
            
        Returns:
            str: Le titre normalisé
        """
        # Convertir en minuscules
        title = title.lower()
        
        # Retirer les accents
        title = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore').decode('ASCII')
        
        # Remplacer les espaces, underscores et tirets par des tirets
        title = re.sub(r'[\s_\-]+', '-', title)
        
        # Retirer les caractères spéciaux sauf les tirets
        title = re.sub(r'[^a-z0-9\-]', '', title)
        
        return title
    
    def check_article_exists(self, title: str, host_star: Optional[str] = None, aliases: Optional[List[str]] = None, allow_partial: bool = False, verbose: bool = False) -> WikiArticleInfo:
        """
        Vérifie si un article existe sur Wikipedia en français, avec gestion des alias, matching souple et logging détaillé.
        
        Args:
            title: Le titre de l'article à vérifier
            host_star: Le nom de l'étoile hôte (pour éviter les redirections vers la page de l'étoile)
            aliases: Liste d'alias possibles pour la planète
            allow_partial: Autoriser le matching partiel (par inclusion)
            verbose: Afficher les logs détaillés
            
        Returns:
            WikiArticleInfo: Informations sur l'article
        """
        logs = []
        if aliases is None:
            aliases = []
        all_titles = [title] + aliases
        normalized_titles = [self.normalize_title(t) for t in all_titles]
        
        # Normaliser le nom de l'étoile si fourni
        normalized_host_star = self.normalize_title(host_star) if host_star else None
        
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
            
            # Vérifier si la page existe vraiment
            if page_id == '-1' or 'missing' in pages[page_id]:
                logs.append(f"No page found for '{title}' (page_id -1 or missing)")
                if verbose:
                    print('\n'.join(logs))
                return WikiArticleInfo(exists=False, title=title, host_star=host_star)
            
            page = pages[page_id]
            is_redirect = 'redirects' in page
            
            # Si c'est une redirection, vérifier si la cible correspond à un alias
            if is_redirect:
                redirect_target = None
                if 'redirects' in data['query']:
                    for redirect in data['query']['redirects']:
                        if redirect['from'] == title:
                            redirect_target = redirect['to']
                            break
                
                if redirect_target:
                    normalized_target = self.normalize_title(redirect_target)
                    
                    # Vérifier si la redirection mène à la page de l'étoile
                    if normalized_host_star and normalized_target == normalized_host_star:
                        logs.append(f"Redirect target '{redirect_target}' matches host star '{host_star}' - article does not exist")
                        if verbose:
                            print('\n'.join(logs))
                        return WikiArticleInfo(exists=False, title=title, host_star=host_star)
                    
                    # Exact match avec un alias
                    if normalized_target in normalized_titles:
                        logs.append(f"Redirect target '{redirect_target}' matches one of the aliases (exact match).")
                        if verbose:
                            print('\n'.join(logs))
                        return WikiArticleInfo(
                            exists=True,
                            title=page['title'],
                            is_redirect=True,
                            redirect_target=redirect_target,
                            url=page.get('fullurl'),
                            host_star=host_star
                        )
                    # Partial match si autorisé
                    if allow_partial:
                        for norm_alias in normalized_titles:
                            if norm_alias in normalized_target or normalized_target in norm_alias:
                                # Vérifier que le match partiel n'est pas avec le nom de l'étoile
                                if not normalized_host_star or (normalized_host_star not in normalized_target and normalized_target not in normalized_host_star):
                                    logs.append(f"Redirect target '{redirect_target}' partially matches alias '{norm_alias}'.")
                                    if verbose:
                                        print('\n'.join(logs))
                                    return WikiArticleInfo(
                                        exists=True,
                                        title=page['title'],
                                        is_redirect=True,
                                        redirect_target=redirect_target,
                                        url=page.get('fullurl'),
                                        host_star=host_star
                                    )
                    logs.append(f"Redirect target '{redirect_target}' does not match any alias (exact or partial).")
                    if verbose:
                        print('\n'.join(logs))
                    return WikiArticleInfo(exists=False, title=title, host_star=host_star)
            
            # Si pas de redirection, vérifier le titre de la page retournée
            normalized_page_title = self.normalize_title(page['title'])
            
            # Vérifier si le titre ne correspond pas au nom de l'étoile
            if normalized_host_star and normalized_page_title == normalized_host_star:
                logs.append(f"Page title '{page['title']}' matches host star '{host_star}' - article does not exist")
                if verbose:
                    print('\n'.join(logs))
                return WikiArticleInfo(exists=False, title=title, host_star=host_star)
            
            if normalized_page_title in normalized_titles:
                logs.append(f"Page title '{page['title']}' matches one of the aliases (exact match).")
                if verbose:
                    print('\n'.join(logs))
                return WikiArticleInfo(
                    exists=True,
                    title=page['title'],
                    is_redirect=False,
                    redirect_target=None,
                    url=page.get('fullurl'),
                    host_star=host_star
                )
            if allow_partial:
                for norm_alias in normalized_titles:
                    if norm_alias in normalized_page_title or normalized_page_title in norm_alias:
                        # Vérifier que le match partiel n'est pas avec le nom de l'étoile
                        if not normalized_host_star or (normalized_host_star not in normalized_page_title and normalized_page_title not in normalized_host_star):
                            logs.append(f"Page title '{page['title']}' partially matches alias '{norm_alias}'.")
                            if verbose:
                                print('\n'.join(logs))
                            return WikiArticleInfo(
                                exists=True,
                                title=page['title'],
                                is_redirect=False,
                                redirect_target=None,
                                url=page.get('fullurl'),
                                host_star=host_star
                            )
            logs.append(f"Page title '{page['title']}' does not match any alias (exact or partial).")
            if verbose:
                print('\n'.join(logs))
            return WikiArticleInfo(exists=False, title=title, host_star=host_star)
        except Exception as e:
            logs.append(f"Erreur lors de la vérification de l'article {title}: {e}")
            if verbose:
                print('\n'.join(logs))
            return WikiArticleInfo(exists=False, title=title, host_star=host_star)
    
    def check_multiple_articles(self, titles: List[str], host_stars: Optional[Dict[str, str]] = None, delay: float = 0.0) -> Dict[str, WikiArticleInfo]:
        """
        Vérifie l'existence de plusieurs articles (jusqu'à 50) en une seule requête.
        
        Args:
            titles: Liste des titres d'articles à vérifier (max 50)
            host_stars: Dictionnaire associant les titres à leurs étoiles hôtes
            delay: Délai en secondes entre chaque requête (par défaut 0)
            
        Returns:
            Dict[str, WikiArticleInfo]: Dictionnaire avec les titres comme clés et les infos comme valeurs
        """
        assert len(titles) <= 50, "L'API MediaWiki limite à 50 titres par requête."
        results = {title: WikiArticleInfo(exists=False, title=title, host_star=host_stars.get(title) if host_stars else None) for title in titles}
        
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
                if page_id == '-1' or 'missing' in page:
                    continue
                    
                title = page['title']
                is_redirect = 'redirects' in page
                
                # Trouver le titre original si c'est une redirection
                original_title = None
                for orig, target in redirects.items():
                    if target == title:
                        original_title = orig
                        break
                
                # Mettre à jour le résultat pour le titre original ou le titre actuel
                result_title = original_title or title
                if result_title in results:
                    host_star = host_stars.get(result_title) if host_stars else None
                    
                    # Vérifier si la redirection pointe vers l'étoile hôte
                    if is_redirect and host_star:
                        redirect_target = redirects.get(original_title)
                        if redirect_target:
                            normalized_target = self.normalize_title(redirect_target)
                            normalized_host_star = self.normalize_title(host_star)
                            if normalized_target == normalized_host_star:
                                results[result_title] = WikiArticleInfo(
                                    exists=False,
                                    title=title,
                                    host_star=host_star
                                )
                                continue
                    
                    # Vérifier si la redirection pointe vers un alias valide
                    if is_redirect:
                        redirect_target = redirects.get(original_title)
                        if redirect_target:
                            normalized_target = self.normalize_title(redirect_target)
                            # Si la redirection ne pointe pas vers un alias valide, considérer comme manquant
                            if normalized_target not in [self.normalize_title(t) for t in [original_title] + (aliases.get(original_title, []) if aliases else [])]:
                                results[result_title] = WikiArticleInfo(
                                    exists=False,
                                    title=title,
                                    host_star=host_star
                                )
                                continue
                    
                    results[result_title] = WikiArticleInfo(
                        exists=True,
                        title=title,
                        is_redirect=is_redirect,
                        redirect_target=redirects.get(original_title) if original_title else None,
                        url=page.get('fullurl'),
                        host_star=host_star
                    )
            
            if delay > 0:
                print(f"Attente de {delay} seconde(s) avant la prochaine requête...")
                time.sleep(delay)
                
        except Exception as e:
            print(f"Erreur lors de la vérification des articles : {e}")
            
        return results

    def check_all_articles(self, articles: List[Dict[str, Any]], batch_size: int = 50, delay: float = 0.0) -> Tuple[Dict[str, WikiArticleInfo], List[str]]:
        """
        Vérifie l'existence de tous les articles en les traitant par lots.
        
        Args:
            articles: Liste des articles à vérifier, chaque article est un dictionnaire avec au moins 'name' et 'host_star'
            batch_size: Taille des lots (max 50)
            delay: Délai en secondes entre chaque lot
            
        Returns:
            Tuple[Dict[str, WikiArticleInfo], List[str]]: Résultats et erreurs
        """
        results = {}
        errors = []
        total = len(articles)
        
        # Préparer le dictionnaire des noms d'étoiles
        host_stars = {article['name']: article.get('host_star') for article in articles}
        
        for i in range(0, total, batch_size):
            batch = articles[i:i + batch_size]
            batch_titles = [article['name'] for article in batch]
            
            try:
                batch_results = self.check_multiple_articles(
                    batch_titles,
                    host_stars={title: host_stars[title] for title in batch_titles},
                    delay=delay
                )
                results.update(batch_results)
            except Exception as e:
                errors.extend(batch_titles)
                print(f"Erreur lors du traitement du lot {i//batch_size + 1}: {e}")
            
            if i + batch_size < total:
                print(f"Progression : {i + batch_size}/{total} articles traités")
                if delay > 0:
                    print(f"Attente de {delay} seconde(s) avant le prochain lot...")
                    time.sleep(delay)
        
        return results, errors 

    def save_results(self, results: Dict[str, WikiArticleInfo], output_dir: str = "output") -> None:
        """
        Sauvegarde les résultats dans des fichiers CSV et JSON.
        
        Args:
            results: Dictionnaire des résultats
            output_dir: Répertoire de sortie
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(output_dir, exist_ok=True)
        
        # Préparer les données pour les fichiers
        existing_articles = []
        missing_articles = []
        
        for title, info in results.items():
            article_data = {
                "exoplanet": title,
                "article_name": info.title,
                "type": "Redirection" if info.is_redirect else "Direct",
                "url": info.url,
                "host_star": info.host_star
            }
            if info.is_redirect:
                article_data["redirect_target"] = info.redirect_target
            
            if info.exists:
                existing_articles.append(article_data)
            else:
                missing_articles.append(article_data)
        
        # Sauvegarder les articles existants
        if existing_articles:
            existing_csv_path = os.path.join(output_dir, f"existing_wikipedia_links_{timestamp}.csv")
            existing_json_path = os.path.join(output_dir, f"existing_wikipedia_links_{timestamp}.json")
            
            with open(existing_csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["exoplanet", "article_name", "type", "url", "redirect_target", "host_star"])
                writer.writeheader()
                writer.writerows(existing_articles)
            
            with open(existing_json_path, 'w', encoding='utf-8') as f:
                json.dump(existing_articles, f, ensure_ascii=False, indent=2)
        
        # Sauvegarder les articles manquants
        if missing_articles:
            missing_csv_path = os.path.join(output_dir, f"missing_exoplanets_{timestamp}.csv")
            missing_json_path = os.path.join(output_dir, f"missing_exoplanets_{timestamp}.json")
            
            with open(missing_csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["exoplanet", "article_name", "type", "url", "redirect_target", "host_star"])
                writer.writeheader()
                writer.writerows(missing_articles)
            
            with open(missing_json_path, 'w', encoding='utf-8') as f:
                json.dump(missing_articles, f, ensure_ascii=False, indent=2) 