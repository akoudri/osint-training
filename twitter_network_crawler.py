#!/usr/bin/env python3
"""
Twitter Network Crawler pour analyse Maltego
Explore les relations sociales sur Twitter/X en profondeur
Export CSV : qui parle avec qui et quand

Usage:
    python twitter_network_crawler.py <pseudo> [options]
    python twitter_network_crawler.py wh1t3h4ts --depth 2 --relations 10

Arguments:
    pseudo              Compte Twitter de départ (sans @)

Options:
    -d, --depth         Profondeur d'exploration (défaut: 2)
    -r, --relations     Nombre max de relations par nœud (défaut: 10)
    -b, --browser       Navigateur à utiliser: chrome ou firefox (défaut: chrome)
    --headless          Mode sans interface graphique
    --no-profile        Ne pas utiliser le profil existant
    -h, --help          Afficher cette aide
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import csv
import os
import urllib.parse
import sys
import argparse
from datetime import datetime
from collections import deque

# ========== CONFIGURATION PAR DÉFAUT ==========

# Ces valeurs peuvent être surchargées par les arguments CLI
COMPTE_INITIAL = "wh1t3h4ts"  # Sans le @
MAX_DEPTH = 2  # 0 = compte initial, 1 = relations directes, 2 = relations des relations
MAX_RELATIONS_PAR_NOEUD = 10

# Navigateur
BROWSER = "chrome"  # "chrome" ou "firefox"
HEADLESS = False    # Mode sans interface graphique
USE_EXISTING_PROFILE = True

# Délais aléatoires pour éviter la détection (en secondes)
DELAI_MIN_ENTRE_ACTIONS = 2
DELAI_MAX_ENTRE_ACTIONS = 5
DELAI_MIN_ENTRE_PROFILS = 5
DELAI_MAX_ENTRE_PROFILS = 10

# Fichiers de sortie
CSV_RELATIONS = "twitter_network_relations.csv"
CSV_NOEUDS = "twitter_network_noeuds.csv"
LOG_FILE = "twitter_network_log.txt"

# ========== CLASSES ==========

class TwitterNetworkCrawler:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.relations = []  # Liste des relations (source, target, type, date)
        self.noeuds = {}     # Dictionnaire des nœuds explorés
        self.queue = deque() # File d'attente pour l'exploration
        self.visited = set() # Comptes déjà visités

    def log(self, message):
        """Affiche et enregistre un message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")

    def delai_aleatoire(self, min_sec=None, max_sec=None):
        """Pause aléatoire pour éviter la détection"""
        if min_sec is None:
            min_sec = DELAI_MIN_ENTRE_ACTIONS
        if max_sec is None:
            max_sec = DELAI_MAX_ENTRE_ACTIONS

        delai = random.uniform(min_sec, max_sec)
        time.sleep(delai)

    def init_browser(self):
        """Initialise le navigateur avec anti-détection"""
        self.log("🚀 Initialisation du navigateur...")

        if BROWSER.lower() == "chrome":
            from selenium.webdriver.chrome.options import Options as ChromeOptions
            from selenium.webdriver.chrome.service import Service as ChromeService
            import shutil

            options = ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_argument("--disable-blink-features=AutomationControlled")

            if HEADLESS:
                options.add_argument("--headless=new")

            options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

            if USE_EXISTING_PROFILE:
                self.log("   🔐 Tentative d'utilisation du profil existant...")
                home = os.path.expanduser("~")
                chrome_path = f"{home}/.config/google-chrome"

                if os.path.exists(chrome_path):
                    import tempfile
                    import shutil as sh

                    original_profile = os.path.join(chrome_path, "Default")
                    if os.path.exists(original_profile):
                        temp_profile = tempfile.mkdtemp(prefix="selenium_twitter_")
                        self.log(f"   📂 Profil temporaire : {temp_profile}")

                        try:
                            important_files = ["Cookies", "Login Data", "Web Data", "Preferences"]
                            for file in important_files:
                                src = os.path.join(original_profile, file)
                                if os.path.exists(src):
                                    dst = os.path.join(temp_profile, file)
                                    sh.copy2(src, dst)

                            options.add_argument(f"--user-data-dir={temp_profile}")
                        except:
                            pass

            chromedriver_path = shutil.which("chromedriver")
            if not chromedriver_path:
                self.log("❌ chromedriver non trouvé !")
                return False

            service = ChromeService(chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        else:  # Firefox
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            from selenium.webdriver.firefox.service import Service as FirefoxService
            import shutil

            options = FirefoxOptions()
            if HEADLESS:
                options.add_argument("--headless")

            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference("useAutomationExtension", False)

            geckodriver_path = shutil.which("geckodriver")
            if not geckodriver_path:
                self.log("❌ geckodriver non trouvé !")
                return False

            service = FirefoxService(geckodriver_path)
            self.driver = webdriver.Firefox(service=service, options=options)

        self.wait = WebDriverWait(self.driver, 10)
        self.log("   ✅ Navigateur initialisé")
        return True

    def login_manuel(self):
        """Attend la connexion manuelle de l'utilisateur"""
        self.log("🌍 Navigation vers Twitter/X...")
        self.driver.get("https://x.com/i/flow/login")

        self.log("\n🛑 ACTION REQUISE :")
        self.log("   1. Connectez-vous manuellement dans le navigateur")
        self.log("   2. Résolvez les éventuels CAPTCHA")
        input("   👉 Appuyez sur [ENTRÉE] une fois connecté...\n")

        self.log("✅ Connexion confirmée")
        self.delai_aleatoire()

    def extraire_username_du_url(self, url):
        """Extrait le username depuis une URL Twitter"""
        try:
            parts = url.split('/')
            if 'x.com' in url or 'twitter.com' in url:
                for i, part in enumerate(parts):
                    if part in ['x.com', 'twitter.com'] and i + 1 < len(parts):
                        username = parts[i + 1]
                        if username and username not in ['home', 'explore', 'notifications', 'messages', 'i']:
                            return username.replace('@', '')
        except:
            pass
        return None

    def explorer_profil(self, username, depth):
        """Explore un profil et extrait ses interactions"""
        if username in self.visited:
            self.log(f"   ⏭️  @{username} déjà visité")
            return

        if depth > MAX_DEPTH:
            self.log(f"   🛑 Profondeur max atteinte pour @{username}")
            return

        self.visited.add(username)
        self.log(f"\n{'  ' * depth}📊 Exploration de @{username} (profondeur {depth})")

        # Visiter le profil
        profile_url = f"https://x.com/{username}"
        self.driver.get(profile_url)
        self.delai_aleatoire(DELAI_MIN_ENTRE_PROFILS, DELAI_MAX_ENTRE_PROFILS)

        # Vérifier que le profil existe
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
        except TimeoutException:
            self.log(f"   ⚠️  Profil @{username} inaccessible ou inexistant")
            return

        # Enregistrer le nœud
        self.noeuds[username] = {
            "username": username,
            "depth": depth,
            "timestamp": datetime.now().isoformat()
        }

        # Scroll et collecte des tweets
        self.log(f"{'  ' * depth}   🔍 Collecte des interactions...")
        interactions_count = 0
        scroll_count = 0
        max_scrolls = 3  # Limité pour éviter trop de données

        tweets_vus = set()
        body = self.driver.find_element(By.TAG_NAME, "body")

        while scroll_count < max_scrolls and interactions_count < MAX_RELATIONS_PAR_NOEUD:
            # Extraire les tweets visibles
            articles = self.driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')

            for article in articles:
                if interactions_count >= MAX_RELATIONS_PAR_NOEUD:
                    break

                try:
                    # Obtenir le texte du tweet pour dédupliquer
                    tweet_text = article.text[:100]
                    if tweet_text in tweets_vus:
                        continue
                    tweets_vus.add(tweet_text)

                    # Chercher les mentions ou réponses
                    links = article.find_elements(By.CSS_SELECTOR, 'a[href*="/"]')

                    for link in links:
                        href = link.get_attribute('href')
                        if not href:
                            continue

                        target_user = self.extraire_username_du_url(href)

                        if target_user and target_user != username and target_user not in ['home', 'explore']:
                            # Type de relation
                            relation_type = "mention"
                            if "/status/" in href:
                                relation_type = "reply"

                            # Enregistrer la relation
                            relation = {
                                "source": username,
                                "target": target_user,
                                "type": relation_type,
                                "timestamp": datetime.now().isoformat(),
                                "depth": depth
                            }

                            self.relations.append(relation)
                            self.log(f"{'  ' * depth}      → @{username} {relation_type} @{target_user}")

                            # Ajouter à la file pour exploration future
                            if depth < MAX_DEPTH and target_user not in self.visited:
                                self.queue.append((target_user, depth + 1))

                            interactions_count += 1

                            if interactions_count >= MAX_RELATIONS_PAR_NOEUD:
                                break

                except Exception as e:
                    continue

            # Scroll
            body.send_keys(Keys.PAGE_DOWN)
            self.delai_aleatoire()
            scroll_count += 1

        self.log(f"{'  ' * depth}   ✅ {interactions_count} interactions trouvées")

    def explorer_reseau(self):
        """Explore le réseau social en largeur (BFS)"""
        self.log(f"\n🌐 Démarrage de l'exploration depuis @{COMPTE_INITIAL}")
        self.log(f"   Profondeur max : {MAX_DEPTH}")
        self.log(f"   Relations max par nœud : {MAX_RELATIONS_PAR_NOEUD}\n")

        # Ajouter le compte initial
        self.queue.append((COMPTE_INITIAL, 0))

        while self.queue:
            username, depth = self.queue.popleft()
            self.explorer_profil(username, depth)

            # Pause entre chaque profil pour éviter la détection
            if self.queue:
                self.delai_aleatoire(DELAI_MIN_ENTRE_PROFILS, DELAI_MAX_ENTRE_PROFILS)

        self.log(f"\n✅ Exploration terminée !")
        self.log(f"   Nœuds explorés : {len(self.noeuds)}")
        self.log(f"   Relations trouvées : {len(self.relations)}")

    def exporter_csv(self):
        """Exporte les données en CSV pour Maltego"""
        self.log("\n💾 Export des données...")

        # CSV Relations (arêtes du graphe)
        with open(CSV_RELATIONS, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['source', 'target', 'type', 'timestamp', 'depth'])
            writer.writeheader()
            writer.writerows(self.relations)

        self.log(f"   ✅ Relations exportées : {CSV_RELATIONS}")

        # CSV Nœuds
        with open(CSV_NOEUDS, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['username', 'depth', 'timestamp'])
            writer.writeheader()
            for noeud in self.noeuds.values():
                writer.writerow(noeud)

        self.log(f"   ✅ Nœuds exportés : {CSV_NOEUDS}")

    def run(self):
        """Exécute le crawler complet"""
        try:
            if not self.init_browser():
                return

            self.login_manuel()
            self.explorer_reseau()
            self.exporter_csv()

            self.log("\n🎉 TERMINÉ ! Fichiers prêts pour Maltego :")
            self.log(f"   📊 Relations : {CSV_RELATIONS}")
            self.log(f"   📊 Nœuds : {CSV_NOEUDS}")

        except KeyboardInterrupt:
            self.log("\n⚠️  Interruption par l'utilisateur")
            if self.relations:
                self.log("   Sauvegarde des données collectées...")
                self.exporter_csv()

        except Exception as e:
            self.log(f"\n❌ Erreur critique : {e}")
            import traceback
            traceback.print_exc()

        finally:
            if self.driver:
                self.log("\n🔒 Fermeture du navigateur dans 5 secondes...")
                time.sleep(5)
                self.driver.quit()


# ========== PARSING DES ARGUMENTS ==========

def parse_arguments():
    """Parse les arguments de ligne de commande"""
    parser = argparse.ArgumentParser(
        description="Twitter Network Crawler - Analyse de réseaux sociaux pour Maltego",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python twitter_network_crawler.py wh1t3h4ts
  python twitter_network_crawler.py elonmusk --depth 3 --relations 15
  python twitter_network_crawler.py alice --depth 1 --relations 20 --browser firefox
  python twitter_network_crawler.py bob --headless --no-profile

Pour plus d'informations, consultez MALTEGO_IMPORT_GUIDE.md
        """
    )

    parser.add_argument(
        'pseudo',
        type=str,
        help='Compte Twitter de départ (sans @)'
    )

    parser.add_argument(
        '-d', '--depth',
        type=int,
        default=MAX_DEPTH,
        metavar='N',
        help=f'Profondeur d\'exploration (défaut: {MAX_DEPTH})'
    )

    parser.add_argument(
        '-r', '--relations',
        type=int,
        default=MAX_RELATIONS_PAR_NOEUD,
        metavar='N',
        help=f'Nombre max de relations par nœud (défaut: {MAX_RELATIONS_PAR_NOEUD})'
    )

    parser.add_argument(
        '-b', '--browser',
        type=str,
        choices=['chrome', 'firefox'],
        default=BROWSER,
        help=f'Navigateur à utiliser (défaut: {BROWSER})'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        help='Mode sans interface graphique'
    )

    parser.add_argument(
        '--no-profile',
        action='store_true',
        help='Ne pas utiliser le profil existant'
    )

    parser.add_argument(
        '--delai-min',
        type=int,
        default=DELAI_MIN_ENTRE_PROFILS,
        metavar='S',
        help=f'Délai minimum entre profils en secondes (défaut: {DELAI_MIN_ENTRE_PROFILS})'
    )

    parser.add_argument(
        '--delai-max',
        type=int,
        default=DELAI_MAX_ENTRE_PROFILS,
        metavar='S',
        help=f'Délai maximum entre profils en secondes (défaut: {DELAI_MAX_ENTRE_PROFILS})'
    )

    return parser.parse_args()


# ========== EXÉCUTION ==========

if __name__ == "__main__":
    # Parser les arguments
    args = parse_arguments()

    # Surcharger les variables globales avec les arguments CLI
    COMPTE_INITIAL = args.pseudo.replace('@', '')  # Enlever @ si présent
    MAX_DEPTH = args.depth
    MAX_RELATIONS_PAR_NOEUD = args.relations
    BROWSER = args.browser
    HEADLESS = args.headless
    USE_EXISTING_PROFILE = not args.no_profile
    DELAI_MIN_ENTRE_PROFILS = args.delai_min
    DELAI_MAX_ENTRE_PROFILS = args.delai_max

    # Affichage
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║           TWITTER NETWORK CRAWLER - Analyse pour Maltego                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")

    print(f"📊 Configuration :")
    print(f"   Compte initial : @{COMPTE_INITIAL}")
    print(f"   Profondeur : {MAX_DEPTH} niveau{'x' if MAX_DEPTH > 1 else ''}")
    print(f"   Relations max/nœud : {MAX_RELATIONS_PAR_NOEUD}")
    print(f"   Navigateur : {BROWSER.upper()}")
    print(f"   Mode headless : {'OUI' if HEADLESS else 'NON'}")
    print(f"   Profil existant : {'OUI' if USE_EXISTING_PROFILE else 'NON'}")
    print(f"   Délais anti-détection : {DELAI_MIN_ENTRE_ACTIONS}-{DELAI_MAX_ENTRE_ACTIONS}s")
    print(f"   Délais entre profils : {DELAI_MIN_ENTRE_PROFILS}-{DELAI_MAX_ENTRE_PROFILS}s\n")

    # Estimation du nombre de comptes
    if MAX_DEPTH == 0:
        estimation = 1
    elif MAX_DEPTH == 1:
        estimation = 1 + MAX_RELATIONS_PAR_NOEUD
    elif MAX_DEPTH == 2:
        estimation = 1 + MAX_RELATIONS_PAR_NOEUD + (MAX_RELATIONS_PAR_NOEUD * MAX_RELATIONS_PAR_NOEUD)
    else:
        estimation = "100+"

    print(f"📈 Estimation : ~{estimation} compte{'s' if estimation != 1 else ''} à explorer")
    print(f"⏱️  Temps estimé : {estimation * DELAI_MIN_ENTRE_PROFILS // 60}-{estimation * DELAI_MAX_ENTRE_PROFILS // 60} minutes\n")

    confirmation = input("Voulez-vous continuer ? (o/N) : ")
    if confirmation.lower() not in ['o', 'y', 'oui', 'yes']:
        print("❌ Annulé")
        sys.exit(0)

    crawler = TwitterNetworkCrawler()
    crawler.run()
