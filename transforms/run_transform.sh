#!/bin/bash
# Wrapper pour exécuter la transform Twitter avec l'environnement virtuel

# Chemin absolu vers le répertoire du projet
PROJECT_DIR="/home/ali/Training/osint-training"

# Activer l'environnement virtuel
source "$PROJECT_DIR/.venv/bin/activate"

# Exécuter la transform avec tous les arguments passés
python "$PROJECT_DIR/transforms/twitter_transform.py" "$@"
