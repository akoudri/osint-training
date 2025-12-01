# OSINT Training - Web Scraping & Social Media Extraction

## 📋 Résumé du Projet

Ce projet est une formation pratique aux techniques de collecte de données OSINT (Open Source Intelligence) avec Python. Il fournit des scripts allant du scraping HTTP basique à l'extraction avancée de données sur les réseaux sociaux (Twitter/X), ainsi que des intégrations avec Maltego.

## 🎯 Objectifs

*   **Scraping HTTP** : Apprendre à collecter des données statiques avec `requests` et `BeautifulSoup`.
*   **Automation Navigateur** : Maîtriser `Selenium` pour interagir avec des sites dynamiques.
*   **Authentification** : Gérer les connexions et les sessions utilisateur.
*   **Twitter OSINT** : Techniques avancées de recherche (dorking) et d'extraction de graphes sociaux.
*   **Intégration Maltego** : Créer des transforms personnalisées pour l'analyse visuelle.

## 🚀 Installation

### Prérequis Système
*   **OS** : Linux (Ubuntu/Debian recommandé)
*   **Python** : 3.12+
*   **Navigateur** : Firefox (et `geckodriver`) ou Chrome (et `chromedriver`)

### Installation Rapide

1.  **Cloner le dépôt**
    ```bash
    git clone https://github.com/akoudri/osint-training.git
    cd osint-training
    ```

2.  **Configurer l'environnement**
    ```bash
    # Créer et activer le venv
    python3 -m venv .venv
    source .venv/bin/activate
    
    # Installer les dépendances
    pip install -r requirements.txt
    ```

3.  **Installer les drivers (si nécessaire)**
    ```bash
    # Pour Firefox (recommandé)
    sudo apt install firefox-geckodriver
    
    # Pour Chrome
    sudo apt install chromium-chromedriver
    ```

## 💻 Exécution

### 1. Scraping Statique (Débutant)
Récupère des citations depuis un site de test.
```bash
python static_scraping.py
# Sortie : resultats_quotes.csv
```

### 2. Scraping Dynamique (Intermédiaire)
Démonstration d'authentification et de navigation automatisée.
```bash
python dynamic_scraping.py
# Credentials test : agent_osint / password123
```

### 3. Extraction Twitter (Avancé)
Recherche et extrait des tweets selon des critères précis.
```bash
python twitter_extractor.py
# Nécessite un compte Twitter actif (profil Chrome/Firefox existant recommandé)
```

### 4. Crawler de Réseau Twitter (CLI)
Cartographie les relations d'un compte Twitter.
```bash
# Usage basique
python twitter_network_crawler.py <pseudo>

# Options courantes
python twitter_network_crawler.py elonmusk --depth 1 --relations 20  # Rapide
python twitter_network_crawler.py target --depth 2 --relations 10    # Complet
python twitter_network_crawler.py target --headless                  # Sans interface
```

### 5. Maltego Transforms
Pour utiliser les transforms Maltego, référez-vous au guide rapide : [`docs/MALTEGO_QUICKSTART.md`](docs/MALTEGO_QUICKSTART.md).

---
*Pour plus de détails techniques, consultez le dossier [`docs/`](docs/).*
