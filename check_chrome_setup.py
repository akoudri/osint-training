#!/usr/bin/env python3
"""
Script de vérification de la configuration Chrome pour Selenium
"""

import os
import shutil
import subprocess

def check_chrome():
    """Vérifie si Chrome est installé"""
    print("🔍 Vérification de Chrome...")
    chrome_paths = ["google-chrome", "chromium-browser", "chromium"]

    for chrome in chrome_paths:
        path = shutil.which(chrome)
        if path:
            try:
                result = subprocess.run([chrome, "--version"],
                                      capture_output=True, text=True, timeout=5)
                version = result.stdout.strip()
                print(f"   ✅ {chrome} trouvé : {version}")
                return True, version
            except:
                pass

    print("   ❌ Chrome non trouvé")
    print("   💡 Installation : sudo apt install google-chrome-stable")
    return False, None

def check_chromedriver():
    """Vérifie si chromedriver est installé"""
    print("\n🔍 Vérification de chromedriver...")
    path = shutil.which("chromedriver")

    if path:
        try:
            result = subprocess.run(["chromedriver", "--version"],
                                  capture_output=True, text=True, timeout=5)
            version = result.stdout.strip()
            print(f"   ✅ chromedriver trouvé : {version}")
            print(f"   📍 Chemin : {path}")
            return True, version
        except:
            pass

    print("   ❌ chromedriver non trouvé")
    print("   💡 Installation : sudo apt install chromium-chromedriver")
    return False, None

def check_profile():
    """Vérifie si le profil Chrome existe"""
    print("\n🔍 Vérification du profil Chrome...")
    home = os.path.expanduser("~")

    chrome_paths = [
        (f"{home}/.config/google-chrome", "Google Chrome"),
        (f"{home}/.config/chromium", "Chromium"),
        (f"{home}/snap/chromium/common/chromium", "Chromium Snap")
    ]

    profile_found = False
    for path, name in chrome_paths:
        if os.path.exists(path):
            default_profile = os.path.join(path, "Default")
            if os.path.exists(default_profile):
                print(f"   ✅ Profil {name} trouvé : {path}")

                # Vérifier les fichiers importants
                important_files = ["Cookies", "History", "Preferences"]
                existing = [f for f in important_files if os.path.exists(os.path.join(default_profile, f))]
                print(f"   📂 Fichiers trouvés : {', '.join(existing)}")
                profile_found = True
            else:
                print(f"   ⚠️  Répertoire {name} existe mais pas de profil Default")

    if not profile_found:
        print("   ❌ Aucun profil Chrome trouvé")
        print("   💡 Ouvrez Chrome au moins une fois pour créer un profil")

    return profile_found

def check_selenium():
    """Vérifie si Selenium est installé"""
    print("\n🔍 Vérification de Selenium...")
    try:
        import selenium
        from selenium import webdriver
        print(f"   ✅ Selenium installé : version {selenium.__version__}")
        return True
    except ImportError:
        print("   ❌ Selenium non installé")
        print("   💡 Installation : pip install selenium")
        return False

def check_versions_compatibility(chrome_version, chromedriver_version):
    """Vérifie la compatibilité des versions"""
    if not chrome_version or not chromedriver_version:
        return False

    print("\n🔍 Vérification de compatibilité...")

    # Extraire les numéros de version majeure
    try:
        chrome_major = chrome_version.split()[2].split('.')[0]
        chromedriver_major = chromedriver_version.split()[1].split('.')[0]

        print(f"   Chrome version majeure : {chrome_major}")
        print(f"   ChromeDriver version majeure : {chromedriver_major}")

        if chrome_major == chromedriver_major:
            print("   ✅ Versions compatibles")
            return True
        else:
            print("   ⚠️  Versions différentes (peut causer des problèmes)")
            print("   💡 Mettez à jour chromedriver pour correspondre à Chrome")
            return False
    except:
        print("   ⚠️  Impossible de vérifier la compatibilité")
        return None

def main():
    print("=" * 70)
    print("  VÉRIFICATION DE LA CONFIGURATION CHROME POUR SELENIUM")
    print("=" * 70)

    chrome_ok, chrome_version = check_chrome()
    chromedriver_ok, chromedriver_version = check_chromedriver()
    profile_ok = check_profile()
    selenium_ok = check_selenium()

    if chrome_ok and chromedriver_ok:
        check_versions_compatibility(chrome_version, chromedriver_version)

    # Résumé
    print("\n" + "=" * 70)
    print("  RÉSUMÉ")
    print("=" * 70)

    checks = [
        ("Chrome installé", chrome_ok),
        ("chromedriver installé", chromedriver_ok),
        ("Profil Chrome existant", profile_ok),
        ("Selenium installé", selenium_ok)
    ]

    for check_name, status in checks:
        symbol = "✅" if status else "❌"
        print(f"{symbol} {check_name}")

    all_ok = all(status for _, status in checks)

    print("\n" + "=" * 70)
    if all_ok:
        print("🎉 TOUT EST PRÊT ! Vous pouvez lancer twitter_extractor.py")
        print("\nCommande :")
        print("  source .venv/bin/activate")
        print("  python twitter_extractor.py")
    else:
        print("⚠️  Configuration incomplète. Suivez les instructions ci-dessus.")
        print("\nConsultez le fichier SOLUTION_GOOGLE_CHROME.md pour plus de détails.")
    print("=" * 70)

if __name__ == "__main__":
    main()
