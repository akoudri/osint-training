#!/bin/bash

# Script helper pour lancer le Twitter Network Crawler

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║         TWITTER NETWORK CRAWLER - Analyse pour Maltego                       ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"

# Vérifier si Chrome est ouvert
echo ""
echo "🔍 Vérification de Chrome..."
if pgrep -x "chrome" > /dev/null || pgrep -x "google-chrome" > /dev/null; then
    echo "   ⚠️  Chrome est en cours d'exécution"
    read -p "   Fermer Chrome automatiquement ? (o/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[OoYy]$ ]]; then
        echo "   🔄 Fermeture de Chrome..."
        killall chrome google-chrome chromium-browser 2>/dev/null
        sleep 2
        echo "   ✅ Chrome fermé"
    fi
else
    echo "   ✅ Chrome n'est pas en cours d'exécution"
fi

# Activer l'environnement virtuel
echo ""
echo "🐍 Activation de l'environnement virtuel..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "   ✅ Environnement activé"
else
    echo "   ❌ .venv non trouvé"
    exit 1
fi

# Nettoyer les anciens fichiers CSV (optionnel)
echo ""
if [ -f "twitter_network_relations.csv" ] || [ -f "twitter_network_noeuds.csv" ]; then
    read -p "🗑️  Supprimer les anciens CSV ? (o/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[OoYy]$ ]]; then
        rm -f reseau_x.csv twitter_network_noeuds.csv twitter_network_log.txt
        echo "   ✅ Fichiers supprimés"
    fi
fi

# Lancer le script
echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                      LANCEMENT DU CRAWLER                                    ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

python twitter_network_crawler.py

EXIT_CODE=$?

# Résumé
echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                           RÉSUMÉ                                             ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    if [ -f "twitter_network_relations.csv" ]; then
        LINES=$(wc -l < reseau_x.csv)
        echo "✅ Exploration terminée avec succès"
        echo ""
        echo "📊 Fichiers générés :"
        echo "   - twitter_network_relations.csv ($((LINES - 1)) relations)"
        echo "   - twitter_network_noeuds.csv"
        echo "   - twitter_network_log.txt"
        echo ""
        echo "📖 Consultez MALTEGO_IMPORT_GUIDE.md pour importer dans Maltego"
    else
        echo "⚠️  Aucun CSV généré (possiblement aucune donnée collectée)"
    fi
else
    echo "❌ Le script a rencontré une erreur"
    if [ -f "twitter_network_log.txt" ]; then
        echo "📝 Consultez twitter_network_log.txt pour les détails"
    fi
fi

echo ""
