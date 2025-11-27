from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.parse
import shutil
import os

# --- CONFIGURATION AVANCÉE ---
# Votre requête "Dorking" (telle quelle, avec les espaces)
REQUETE_BRUTE = "(from:wh1t3h4ts OR to:wh1t3h4ts OR @wh1t3h4ts) -filter:links"

# Encodage pour l'URL (transforme les espaces en %20, etc.)
REQUETE_ENCODEE = urllib.parse.quote(REQUETE_BRUTE)

# Construction de l'URL de recherche
URL_SEARCH = f"https://x.com/search?q={REQUETE_ENCODEE}&src=typed_query&f=live"
# Note : &f=live force l'ordre chronologique (plus pertinent pour l'analyse)

URL_LOGIN = "https://x.com/i/flow/login"

# Configuration du navigateur
BROWSER = "chrome"  # "chrome" ou "firefox"
HEADLESS = False  # Mettre True pour exécuter sans interface graphique
SCROLL_COUNT = 5  # Nombre de scrolls pour charger plus de tweets
USE_EXISTING_PROFILE = True  # Utiliser votre profil Chrome/Firefox existant (recommandé)


def twitter_search_extractor():
    print(f"--- 1. Lancement du Navigateur ({BROWSER.upper()}) ---")

    driver = None

    # ========== CHROME ==========
    if BROWSER.lower() == "chrome":
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.chrome.service import Service as ChromeService

        options = ChromeOptions()

        # Anti-détection pour Chrome
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")

        if HEADLESS:
            options.add_argument("--headless=new")

        # User-Agent réaliste
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # SOLUTION RECOMMANDÉE : Utiliser votre profil Chrome existant
        if USE_EXISTING_PROFILE:
            print("🔐 Utilisation du profil Chrome existant...")
            home = os.path.expanduser("~")

            # Créer une copie temporaire du profil pour éviter les conflits
            import tempfile
            import shutil as sh

            # Chemins possibles pour Chrome
            chrome_paths = [
                f"{home}/.config/google-chrome",  # Google Chrome
                f"{home}/.config/chromium",       # Chromium
                f"{home}/snap/chromium/common/chromium"  # Chromium Snap
            ]

            profile_found = False
            for chrome_path in chrome_paths:
                original_profile = os.path.join(chrome_path, "Default")
                if os.path.exists(original_profile):
                    print(f"   ✅ Profil Chrome trouvé : {chrome_path}")

                    # Créer un répertoire temporaire pour le profil Selenium
                    temp_profile = tempfile.mkdtemp(prefix="selenium_chrome_")
                    print(f"   📂 Copie du profil vers : {temp_profile}")

                    try:
                        # Copier les fichiers importants (cookies, historique, etc.)
                        important_files = ["Cookies", "Login Data", "Web Data", "History", "Preferences"]
                        for file in important_files:
                            src = os.path.join(original_profile, file)
                            if os.path.exists(src):
                                dst = os.path.join(temp_profile, file)
                                sh.copy2(src, dst)

                        options.add_argument(f"--user-data-dir={temp_profile}")
                        print("   ✅ Profil temporaire créé")
                    except Exception as e:
                        print(f"   ⚠️  Impossible de copier le profil : {e}")
                        print("   → Utilisation d'un nouveau profil")

                    profile_found = True
                    break

            if not profile_found:
                print("   ⚠️  Profil Chrome non trouvé, utilisation d'un nouveau profil")

        # Détection automatique de chromedriver
        chromedriver_path = shutil.which("chromedriver")

        if not chromedriver_path:
            print("\n❌ ERREUR : chromedriver non trouvé !")
            print("\n💡 INSTALLATION REQUISE :")
            print("   sudo apt install chromium-chromedriver")
            print("\n   Ou téléchargement manuel depuis :")
            print("   https://googlechromelabs.github.io/chrome-for-testing/")
            print("\n   Puis consultez : INSTALL_CHROMEDRIVER.md")
            print("\n⚠️  Alternative : Changez BROWSER = 'firefox' dans le script")
            return

        service = ChromeService(chromedriver_path)

        try:
            print(f"   🔧 Utilisation de chromedriver : {chromedriver_path}")
            driver = webdriver.Chrome(service=service, options=options)

            # Script pour masquer webdriver
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("   ✅ Chrome initialisé avec succès")

        except Exception as e:
            print(f"\n❌ ERREUR : Impossible d'initialiser Chrome")
            print(f"   Détails : {e}")

            # Analyser l'erreur pour donner des conseils spécifiques
            error_msg = str(e)
            if "session not created" in error_msg:
                print("\n💡 CAUSE PROBABLE : Version incompatible")
                print("   Vérifiez que chromedriver correspond à votre version de Chrome :")
                print("   google-chrome --version")
                print("   chromedriver --version")
            elif "cannot parse" in error_msg or "JSON" in error_msg:
                print("\n💡 CAUSE PROBABLE : Chrome déjà ouvert avec le même profil")
                print("   Solution 1 : Fermez toutes les instances de Chrome")
                print("   killall google-chrome")
                print("\n   Solution 2 : Désactivez USE_EXISTING_PROFILE dans le script")

            print("\n📚 Consultez : SOLUTION_GOOGLE_CHROME.md")
            return

    # ========== FIREFOX ==========
    else:
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from selenium.webdriver.firefox.service import Service as FirefoxService

        options = FirefoxOptions()

        if HEADLESS:
            options.add_argument("--headless")

        # Anti-détection pour Firefox
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        options.set_preference("general.useragent.override",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0")

        # Utiliser le profil Firefox existant
        if USE_EXISTING_PROFILE:
            print("🔐 Utilisation du profil Firefox existant...")
            home = os.path.expanduser("~")
            profile_path = f"{home}/.mozilla/firefox"

            if os.path.exists(profile_path):
                profiles = [d for d in os.listdir(profile_path) if d.endswith('.default') or d.endswith('.default-release')]
                if profiles:
                    full_profile_path = os.path.join(profile_path, profiles[0])
                    options.add_argument("-profile")
                    options.add_argument(full_profile_path)
                    print(f"   ✅ Profil trouvé : {profiles[0]}")
                else:
                    print("   ⚠️  Profil par défaut non trouvé")
            else:
                print("   ⚠️  Répertoire Firefox non trouvé")

        geckodriver_path = shutil.which("geckodriver")
        service = FirefoxService(geckodriver_path) if geckodriver_path else None

        try:
            if service:
                driver = webdriver.Firefox(service=service, options=options)
            else:
                driver = webdriver.Firefox(options=options)
        except Exception as e:
            print(f"❌ ERREUR : Impossible d'initialiser Firefox")
            print(f"   Détails : {e}")
            print("\n💡 Solutions possibles :")
            print("   1. Installer Firefox : sudo apt install firefox")
            print("   2. Installer geckodriver : sudo apt install firefox-geckodriver")
            print("   3. Ou changer BROWSER = 'chrome' dans le script")
            return

    if driver is None:
        print("❌ Échec de l'initialisation du navigateur")
        return

    try:
        # Initialisation des attentes explicites
        wait = WebDriverWait(driver, 10)

        # ÉTAPE A : Le Login (Toujours manuel pour passer les sécurités)
        print(f"🌍 Connexion requise...")
        driver.get(URL_LOGIN)

        print("\n🛑 ACTION REQUISE :")
        print("1. Connectez-vous manuellement dans Firefox.")
        print("2. Résolvez les éventuels CAPTCHA ou vérifications de sécurité.")
        input("👉 Appuyez sur [ENTRÉE] ici une fois connecté pour lancer la recherche...")

        # ÉTAPE B : Injection de la Super-Requête
        print(f"\n🚀 Lancement de la recherche : {REQUETE_BRUTE}")
        driver.get(URL_SEARCH)

        # Attente que la page de résultats soit chargée
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
            print("✅ Page de résultats chargée")
        except:
            print("⚠️  Timeout : Vérifiez que vous êtes bien connecté et que la recherche s'affiche")
            time.sleep(5)  # Fallback

        # ÉTAPE C : Scroll & Collecte
        print(f"📜 Récupération des résultats (scroll x{SCROLL_COUNT})...")
        tweets_uniques = set()  # Pour éviter les doublons
        body = driver.find_element(By.TAG_NAME, "body")

        # Scrolling progressif pour charger plus de tweets
        for i in range(SCROLL_COUNT):
            print(f"   Scroll {i+1}/{SCROLL_COUNT}...", end="\r")

            # Extraction des articles visibles
            articles = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')

            for article in articles:
                try:
                    # Nettoyage du texte
                    texte = article.text.replace("\n", " | ")
                    # On l'ajoute au set (si doublon, il sera ignoré automatiquement)
                    tweets_uniques.add(texte)
                except:
                    pass

            # Scroll vers le bas
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)  # Pause pour laisser le temps aux tweets de charger

        print(f"\n✅ TERMINÉ : {len(tweets_uniques)} tweets uniques récupérés.")
        print("-" * 80)

        # Affichage des résultats
        if tweets_uniques:
            print("\n📊 Aperçu des tweets collectés (10 premiers) :")
            for idx, tweet in enumerate(list(tweets_uniques)[:10], 1):
                print(f"\n{idx}. {tweet[:150]}...")
        else:
            print("⚠️  Aucun tweet trouvé. Vérifiez :")
            print("   - Que vous êtes bien connecté à X/Twitter")
            print("   - Que la recherche retourne des résultats")
            print("   - Que les sélecteurs CSS sont toujours valides")

    except Exception as e:
        print(f"⚠️ Erreur critique : {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("\n--- Fermeture du navigateur dans 5 secondes ---")
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    twitter_search_extractor()