#!/bin/bash
# Script de démarrage rapide du serveur Maltego

echo "=========================================="
echo "Maltego Transform Server - OSINT Training"
echo "=========================================="
echo ""

# Vérifier l'environnement virtuel
if [ ! -d ".venv" ]; then
    echo "❌ Environnement virtuel non trouvé"
    echo "Créez-le avec: python3 -m venv .venv"
    exit 1
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Vérifier les dépendances
echo "🔍 Vérification des dépendances..."
if ! python -c "import maltego_trx" 2>/dev/null; then
    echo "📦 Installation de maltego-trx..."
    pip install -q maltego-trx
fi

if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Installation de flask..."
    pip install -q flask
fi

echo "✅ Dépendances OK"
echo ""

# Démarrer le serveur
echo "🚀 Démarrage du serveur..."
echo ""
python transforms/server.py
