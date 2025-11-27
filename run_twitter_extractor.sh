#!/bin/bash

# Script helper pour lancer twitter_extractor.py
# Gère automatiquement la fermeture de Chrome et l'environnement virtuel

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║              LANCEMENT DE TWITTER EXTRACTOR (CHROME)                         ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"

# 1. Vérifier si Chrome est en cours d'exécution
echo ""
echo "🔍 Vérification de Chrome..."
if pgrep -x "chrome" > /dev/null || pgrep -x "google-chrome" > /dev/null; then
    echo "   ⚠️  Chrome est actuellement en cours d'exécution"
    echo ""
    read -p "   Voulez-vous fermer Chrome automatiquement ? (o/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[OoYy]$ ]]; then
        echo "   🔄 Fermeture de Chrome..."
        killall chrome google-chrome chromium-browser 2>/dev/null
        sleep 2
        echo "   ✅ Chrome fermé"
    else
        echo "   ℹ️  Chrome restera ouvert"
        echo "   ⚠️  Le script utilisera un nouveau profil (sans vos cookies)"
    fi
else
    echo "   ✅ Chrome n'est pas en cours d'exécution"
fi

# 2. Activer l'environnement virtuel
echo ""
echo "🐍 Activation de l'environnement virtuel..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "   ✅ Environnement virtuel activé"
else
    echo "   ❌ Environnement virtuel non trouvé (.venv)"
    echo "   💡 Créez-le avec : python3 -m venv .venv"
    exit 1
fi

# 3. Vérifier que Selenium est installé
echo ""
echo "🔍 Vérification de Selenium..."
python -c "import selenium" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Selenium est installé"
else
    echo "   ❌ Selenium non installé"
    echo "   💡 Installez-le avec : pip install -r requirements.txt"
    exit 1
fi

# 4. Vérifier chromedriver
echo ""
echo "🔍 Vérification de chromedriver..."
if command -v chromedriver &> /dev/null; then
    CHROMEDRIVER_VERSION=$(chromedriver --version 2>&1 | head -1)
    echo "   ✅ $CHROMEDRIVER_VERSION"
else
    echo "   ❌ chromedriver non trouvé"
    echo "   💡 Installez-le avec : sudo apt install chromium-chromedriver"
    exit 1
fi

# 5. Lancer le script
echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                      LANCEMENT DU SCRIPT                                     ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

python twitter_extractor.py

# 6. Code de sortie
EXIT_CODE=$?
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Script terminé avec succès"
else
    echo "❌ Le script a rencontré une erreur (code: $EXIT_CODE)"
fi

exit $EXIT_CODE
