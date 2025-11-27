from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import shutil

# --- CONFIGURATION ---
URL_LOGIN = "http://quotes.toscrape.com/login"
USER = "agent_osint"
PASS = "password123"
HEADLESS = False  # Mettre True pour exécuter sans interface graphique


def robot_authentifie():
    print("--- 1. Initialisation du Navigateur ---")

    # Configuration des options Firefox
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")

    # Détection automatique du chemin geckodriver
    geckodriver_path = shutil.which("geckodriver")
    service = Service(geckodriver_path) if geckodriver_path else None

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
        print("   3. Ou télécharger geckodriver : https://github.com/mozilla/geckodriver/releases")
        return

    try:
        # ÉTAPE A : Accéder à la page de login
        print(f"🌍 Navigation vers {URL_LOGIN}...")
        driver.get(URL_LOGIN)

        # Attente explicite que la page soit chargée
        wait = WebDriverWait(driver, 10)

        # ÉTAPE B : Repérer les champs (Inspection HTML)
        # On cherche l'input avec l'id='username'
        print("⌨️ Remplissage du formulaire...")
        champ_user = wait.until(EC.presence_of_element_located((By.ID, "username")))

        # On cherche l'input avec l'id='password'
        champ_pass = driver.find_element(By.ID, "password")

        # ÉTAPE C : L'Action (Taper au clavier)
        champ_user.clear()  # Bon réflexe : vider le champ avant d'écrire
        champ_user.send_keys(USER)
        time.sleep(1)  # Juste pour l'effet visuel pédagogique

        champ_pass.clear()
        champ_pass.send_keys(PASS)

        # ÉTAPE D : La Validation
        # On peut soit cliquer sur le bouton, soit appuyer sur "Entrée" (RETURN)
        print("🖱️ Validation...")
        # Méthode 1 : Clic sur le bouton
        # bouton = driver.find_element(By.CSS_SELECTOR, ".btn-primary")
        # bouton.click()

        # Méthode 2 : Appuyer sur Entrée directement dans le champ mot de passe
        champ_pass.send_keys(Keys.RETURN)

        # ÉTAPE E : Vérification du succès
        # Attente explicite du lien "Logout" (preuve de connexion réussie)
        try:
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
            print("✅ SUCCÈS : Authentification réussie !")

            # ÉTAPE F : Le Scraping (Maintenant qu'on est connecté)
            print("--- Extraction des données (Vue Connectée) ---")
            # Exemple : On prend juste la première citation pour prouver que ça marche
            premier_texte = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "text"))
            ).text
            print(f"Citation du jour : {premier_texte}")

        except:
            print("❌ ÉCHEC : Le login a échoué ou timeout.")

    except Exception as e:
        print(f"Erreur critique : {e}")

    finally:
        print("--- Fermeture du robot dans 5 secondes ---")
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    robot_authentifie()