# Guide d'installation et de déploiement - OSINT Training

Ce document décrit comment installer et configurer l'environnement de scraping OSINT sur une nouvelle machine.

## Table des matières
1. [Prérequis système](#prérequis-système)
2. [Installation des dépendances](#installation-des-dépendances)
3. [Configuration de l'environnement Python](#configuration-de-lenvironnement-python)

---

## Prérequis système

### Système d'exploitation
- Linux (testé sur Ubuntu/Debian)
- Python 3.12 ou supérieur

### Logiciels requis
- Git
- Python 3 et pip
- Firefox (navigateur)
- geckodriver (pilote Selenium pour Firefox)

---

## Installation des dépendances

### 1. Mise à jour du système
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Installation de Python et pip
```bash
sudo apt install python3 python3-pip python3-venv -y
```

### 3. Installation de Firefox
```bash
sudo apt install firefox -y

# Vérification
firefox --version
```

### 4. Installation de geckodriver

**Option A : Via le gestionnaire de paquets (recommandé)**
```bash
sudo apt install firefox-geckodriver -y

# Vérification
geckodriver --version
which geckodriver
```

**Option B : Installation manuelle**
```bash
# Télécharger la dernière version
wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz

# Extraire
tar -xvzf geckodriver-v0.34.0-linux64.tar.gz

# Déplacer vers /usr/local/bin
sudo mv geckodriver /usr/local/bin/

# Rendre exécutable
sudo chmod +x /usr/local/bin/geckodriver

# Vérification
geckodriver --version
```

---

## Configuration de l'environnement Python

### 1. Cloner le dépôt (ou créer le répertoire)
```bash
git clone https://github.com/akoudri/osint-training.git osint-training
cd osint-training
```

### 2. Créer l'environnement virtuel
```bash
python3 -m venv .venv
```

### 3. Activer l'environnement virtuel
```bash
source .venv/bin/activate
```

Vous devriez voir `(.venv)` apparaître au début de votre prompt.

### 4. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

Le fichier `requirements.txt` contient :
```
requests==2.32.5
beautifulsoup4==4.14.2
pandas==2.3.3
selenium==4.38.0
```
