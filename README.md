# OSINT Training - Web Scraping & Social Media Extraction

Formation pratique aux techniques de collecte de données OSINT (Open Source Intelligence) avec Python.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.38.0-green.svg)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-Educational-orange.svg)]()

---

## 📚 Vue d'ensemble

Ce dépôt contient des scripts d'apprentissage pour la collecte de données OSINT et l'intégration avec Maltego :

| Script | Type | Technique | Niveau |
|--------|------|-----------|--------|
| `static_scraping.py` | Scraping HTTP | BeautifulSoup + Requests | Débutant |
| `dynamic_scraping.py` | Scraping dynamique | Selenium + Authentication | Intermédiaire |
| `twitter_extractor.py` | Extraction sociale | Selenium + Twitter Dorking | Avancé |
| **`transforms/twitter_transform.py`** | **Maltego Transform** | **Twitter OSINT** | **Intermédiaire** |

---

## 🚀 Installation rapide

### 1. Cloner le dépôt
```bash
git clone https://github.com/akoudri/osint-training.git
cd osint-training
```

### 2. Installer les prérequis système
```bash
# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv firefox firefox-geckodriver -y
```

### 3. Créer l'environnement virtuel
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

### 5. Tester l'installation
```bash
python static_scraping.py
```

Pour une installation détaillée, consultez [INSTALLATION.md](docs/INSTALLATION.md).

---

## 📖 Scripts disponibles

### 1️⃣ Static Scraping (`static_scraping.py`)

**Objectif :** Apprendre le scraping HTTP basique

**Fonctionnement :**
- Requête HTTP avec `requests`
- Parsing HTML avec `BeautifulSoup`
- Export CSV avec `pandas`

**Utilisation :**
```bash
python static_scraping.py
```

**Output :** `resultats_quotes.csv`

**Site cible :** http://quotes.toscrape.com (site d'entraînement légal)

---

### 2️⃣ Dynamic Scraping (`dynamic_scraping.py`)

**Objectif :** Automatiser la navigation et l'authentification

**Fonctionnement :**
- Automation avec `Selenium`
- Remplissage de formulaires
- Extraction post-authentification

**Utilisation :**
```bash
python dynamic_scraping.py
```

**Credentials de test :** `agent_osint` / `password123`

**Améliorations v2.0 :**
- ✅ Initialisation robuste de Selenium
- ✅ Attentes explicites (`WebDriverWait`)
- ✅ Mode headless configurable
- ✅ Gestion d'erreurs améliorée

---

### 3️⃣ Twitter Extractor (`twitter_extractor.py`)

**Objectif :** Extraction de données depuis Twitter/X avec dorking avancé

**Fonctionnement :**
- Authentification manuelle (contourne anti-bot)
- Requêtes de recherche complexes (Twitter dorking)
- Scrolling progressif
- Déduplication automatique

**Utilisation :**
```bash
python twitter_extractor.py
```

**⚠️ Nécessite :** Compte Twitter/X actif

**Exemple de requête :**
```python
REQUETE_BRUTE = "(from:username OR to:username) -filter:links"
```

**Documentation complète :** [TWITTER_EXTRACTOR_GUIDE.md](docs/TWITTER_EXTRACTOR_GUIDE.md)

**Améliorations v2.0 :**
- ✅ Service geckodriver automatique
- ✅ WebDriverWait pour robustesse
- ✅ Indicateur de progression
- ✅ Validation des résultats
- ✅ Diagnostics complets

---

### 4️⃣ Maltego Twitter Transform (`transforms/twitter_transform.py`) ⭐ NOUVEAU

**Objectif :** Intégration OSINT dans Maltego pour investigation Twitter/X

**Fonctionnalités :**
- ✅ Validation stricte des alias Twitter (règles officielles)
- ✅ Nettoyage automatique (@, espaces)
- ✅ Métadonnées OSINT enrichies (4 URLs additionnelles)
- ✅ Gestion d'erreurs professionnelle
- ✅ 17 tests unitaires (100% pass)

**Configuration rapide :**
```bash
# Afficher les chemins pour Maltego
./show_maltego_paths.sh

# Puis suivre le guide : MALTEGO_QUICKSTART.md
```

**Documentation :**
- 🚀 **Guide rapide** : [MALTEGO_QUICKSTART.md](MALTEGO_QUICKSTART.md) - 5 minutes
- 📖 **Configuration détaillée** : [MALTEGO_CONFIG_DIRECT.md](MALTEGO_CONFIG_DIRECT.md)
- 🔧 **Technique** : [MALTEGO_TWITTER_TRANSFORM.md](MALTEGO_TWITTER_TRANSFORM.md)

**Utilisation dans Maltego :**
```
[Phrase: "elonmusk"]
  → TwitterAliasToProfileURL
  → [URL: https://x.com/elonmusk + métadonnées OSINT]
```

---

## 📁 Structure du projet

```
osint-training/
├── .venv/                              # Environnement virtuel Python
├── static_scraping.py                  # Script 1 : Scraping HTTP
├── dynamic_scraping.py                 # Script 2 : Selenium + Auth
├── twitter_extractor.py                # Script 3 : Twitter/X extraction
├── transforms/                         # ⭐ NOUVEAU : Maltego transforms
│   ├── __init__.py                     # Module Python
│   ├── twitter_transform.py            # Transform principale
│   ├── transform_config.py             # Config TRX/API
│   ├── server.py                       # Serveur Flask (optionnel)
│   ├── run_transform.sh                # Wrapper pour venv
│   └── README.md                       # Documentation technique
├── test_twitter_transform.py           # Tests unitaires (17 tests)
├── demo_transform.py                   # Script de démonstration
├── show_maltego_paths.sh               # Affiche chemins Maltego
├── start_maltego_server.sh             # Démarrage serveur Flask
├── requirements.txt                    # Dépendances Python
├── resultats_quotes.csv                # Données extraites (généré)
├── README.md                           # Ce fichier
├── MALTEGO_QUICKSTART.md               # Guide rapide Maltego (5 min)
├── MALTEGO_CONFIG_DIRECT.md            # Config détaillée Maltego
├── MALTEGO_TWITTER_TRANSFORM.md        # Documentation technique
├── TRANSFORM_SUMMARY.md                # Récapitulatif développeur
├── CLAUDE.md                           # Documentation pour Claude Code
├── TWITTER_EXTRACTOR_GUIDE.md          # Guide Twitter détaillé
└── CORRECTIONS_TWITTER_EXTRACTOR.md    # Détail des corrections v2.0
```

---

## 🔧 Dépendances

```
requests==2.32.5          # Client HTTP
beautifulsoup4==4.14.2    # Parser HTML
pandas==2.3.3             # Manipulation de données
selenium==4.38.0          # Automation navigateur
maltego-trx==1.6.1        # ⭐ Framework Maltego transforms
pytest==9.0.1             # Tests unitaires
```

**Dépendances système :**
- Firefox (navigateur)
- geckodriver (pilote Selenium)
- Maltego CE/Classic (pour l'intégration OSINT - optionnel)

---

## 📚 Documentation

| Fichier | Description |
|---------|-------------|
| **Maltego Transforms** | |
| [MALTEGO_QUICKSTART.md](MALTEGO_QUICKSTART.md) | ⭐ Guide rapide (5 min) - configuration Maltego |
| [MALTEGO_CONFIG_DIRECT.md](MALTEGO_CONFIG_DIRECT.md) | Configuration détaillée + dépannage |
| [MALTEGO_TWITTER_TRANSFORM.md](MALTEGO_TWITTER_TRANSFORM.md) | Documentation technique complète |
| [TRANSFORM_SUMMARY.md](TRANSFORM_SUMMARY.md) | Récapitulatif développeur |
| **Scripts OSINT** | |
| [INSTALLATION.md](docs/INSTALLATION.md) | Installation complète sur nouvelle machine |
| [TWITTER_EXTRACTOR_GUIDE.md](docs/TWITTER_EXTRACTOR_GUIDE.md) | Guide complet Twitter/X avec syntaxe dorking |
| [CORRECTIONS_TWITTER_EXTRACTOR.md](docs/CORRECTIONS_TWITTER_EXTRACTOR.md) | Détail des corrections v2.0 |
| [CLAUDE.md](CLAUDE.md) | Documentation architecture pour Claude Code |

---

## ⚙️ Configuration

### Mode headless (sans interface graphique)

Pour `dynamic_scraping.py` et `twitter_extractor.py` :

```python
HEADLESS = True  # Activer le mode headless
```

Utile pour :
- Serveurs sans display
- Execution automatisée
- Tests en CI/CD

### Nombre de scrolls (Twitter)

```python
SCROLL_COUNT = 10  # Défaut: 5
```

Plus de scrolls = plus de tweets collectés (mais plus lent)

---

## 🛡️ Considérations éthiques et légales

### ✅ Autorisé
- Formation et apprentissage
- Recherche académique
- OSINT défensif
- Analyse de sécurité autorisée
- Sites d'entraînement publics

### ❌ Interdit
- Collecte massive non autorisée
- Violation des conditions d'utilisation
- Spam ou harcèlement
- Revente de données personnelles
- Atteinte à la vie privée

### 🔐 Bonnes pratiques OSINT
1. **Respectez les `robots.txt`**
2. **Limitez la fréquence des requêtes**
3. **Anonymisez les données personnelles**
4. **Documentez vos sources**
5. **Utilisez un compte dédié pour l'OSINT**
6. **Ne partagez jamais de données sensibles collectées**

---

## 🐛 Résolution de problèmes

### Problème : "geckodriver not found"
```bash
sudo apt install firefox-geckodriver
# ou télécharger depuis https://github.com/mozilla/geckodriver/releases
```

### Problème : "Firefox binary not found"
```bash
sudo apt install firefox
```

### Problème : "Module not found"
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Problème : Twitter - "Aucun tweet trouvé"
- Vérifiez que vous êtes connecté
- Testez la requête directement sur x.com/search
- Vérifiez les sélecteurs CSS (Twitter change régulièrement)

Pour plus de diagnostics : [TWITTER_EXTRACTOR_GUIDE.md](docs/TWITTER_EXTRACTOR_GUIDE.md#résolution-des-problèmes)

---

## 📈 Évolution et améliorations

### Version 2.0 (2025-11-27)
- ✅ Corrections complètes de `dynamic_scraping.py`
- ✅ Corrections complètes de `twitter_extractor.py`
- ✅ Initialisation robuste de Selenium
- ✅ Attentes explicites (`WebDriverWait`)
- ✅ Mode headless configurable
- ✅ Documentation complète créée

### Version 1.0 (Initial)
- Scripts de base fonctionnels
- Scraping statique
- Scraping dynamique
- Extraction Twitter

### Roadmap (futures améliorations)
- [ ] Export JSON automatique
- [ ] Support Chrome en plus de Firefox
- [ ] Interface CLI avec arguments
- [ ] Tests unitaires
- [ ] Support Docker
- [ ] Extraction de métadonnées enrichies (dates, likes, RT)

---

## 🎓 Objectifs pédagogiques

À la fin de cette formation, vous saurez :

1. ✅ Faire du scraping HTTP avec BeautifulSoup
2. ✅ Automatiser un navigateur avec Selenium
3. ✅ Gérer l'authentification web
4. ✅ Utiliser les attentes explicites (WebDriverWait)
5. ✅ Faire du Twitter dorking
6. ✅ Exporter des données en CSV
7. ✅ Gérer les erreurs robustement
8. ✅ Respecter les bonnes pratiques OSINT

---

## 🤝 Contribution

Ce projet est à but éducatif. Les suggestions d'amélioration sont les bienvenues via :
- Issues GitHub
- Pull requests
- Discussions

---

## 📝 Licence

**Usage éducatif uniquement**

Ce projet est destiné à l'apprentissage des techniques OSINT. L'utilisation à des fins malveillantes, de spam, ou violant les conditions d'utilisation de services tiers est strictement interdite.

---

## 🔗 Ressources complémentaires

### Documentation officielle
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Twitter Search Operators
- [Twitter Advanced Search](https://twitter.com/search-advanced)
- [Twitter Search Operators Guide](https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators)

### OSINT Resources
- [OSINT Framework](https://osintframework.com/)
- [Awesome OSINT](https://github.com/jivoi/awesome-osint)

---

## 👨‍💻 Auteur

**Projet de formation OSINT**

Corrections et documentation v2.0 : Claude Code (2025-11-27)

---

## ⚡ Quick Start

```bash
# Installation complète en 4 commandes
git clone https://github.com/akoudri/osint-training.git
cd osint-training
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && python static_scraping.py
```

**Prêt à apprendre l'OSINT ! 🎯**

---

**Note :** Ce projet a été corrigé et amélioré avec l'assistance de Claude Code pour garantir la robustesse et la reproductibilité sur toutes les machines Linux.
