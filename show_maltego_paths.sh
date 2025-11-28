#!/bin/bash
# Affiche les chemins nécessaires pour configurer Maltego

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     CHEMINS POUR CONFIGURATION MALTEGO                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📁 RÉPERTOIRE DU PROJET"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$PROJECT_DIR"
echo ""

echo "🔧 CONFIGURATION MALTEGO - TRANSFORM LOCALE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Transform Details:"
echo "  Transform ID:          TwitterAliasToProfileURL"
echo "  Description:           Convert Twitter/X alias to profile URL"
echo "  Author:                OSINT Training"
echo "  Input entity type:     maltego.Phrase"
echo ""
echo "Command line configuration:"
echo "  Command:               $PROJECT_DIR/transforms/run_transform.sh"
echo "  Parameters:            (laisser vide)"
echo "  Working directory:     $PROJECT_DIR"
echo ""

echo "📋 COPIER-COLLER CES VALEURS DANS MALTEGO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Command (à copier):"
echo "$PROJECT_DIR/transforms/run_transform.sh"
echo ""
echo "Working directory (à copier):"
echo "$PROJECT_DIR"
echo ""

echo "✅ VÉRIFICATION DES PRÉREQUIS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Vérifier que le wrapper existe
if [ -f "$PROJECT_DIR/transforms/run_transform.sh" ]; then
    echo "✓ Script wrapper trouvé"
else
    echo "✗ Script wrapper manquant!"
    exit 1
fi

# Vérifier que le wrapper est exécutable
if [ -x "$PROJECT_DIR/transforms/run_transform.sh" ]; then
    echo "✓ Script wrapper exécutable"
else
    echo "✗ Script wrapper non exécutable"
    echo "  Exécuter: chmod +x $PROJECT_DIR/transforms/run_transform.sh"
    exit 1
fi

# Vérifier que l'environnement virtuel existe
if [ -d "$PROJECT_DIR/.venv" ]; then
    echo "✓ Environnement virtuel trouvé"
else
    echo "✗ Environnement virtuel manquant!"
    echo "  Créer avec: python3 -m venv .venv"
    exit 1
fi

# Vérifier maltego-trx dans le venv
source "$PROJECT_DIR/.venv/bin/activate"
if python -c "import maltego_trx" 2>/dev/null; then
    echo "✓ maltego-trx installé dans le venv"
else
    echo "✗ maltego-trx manquant dans le venv"
    echo "  Installer avec: pip install maltego-trx"
    deactivate
    exit 1
fi
deactivate

echo ""
echo "🧪 TEST DE LA TRANSFORM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Tester la transform
if "$PROJECT_DIR/transforms/run_transform.sh" "elonmusk" >/dev/null 2>&1; then
    echo "✓ Transform fonctionne correctement"
else
    echo "✗ Erreur lors de l'exécution de la transform"
    echo "  Tester manuellement: ./transforms/run_transform.sh elonmusk"
    exit 1
fi

echo ""
echo "✨ TOUT EST PRÊT!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Étapes suivantes:"
echo "1. Ouvrir Maltego"
echo "2. Transforms → New Local Transform"
echo "3. Copier-coller les chemins ci-dessus"
echo "4. Tester avec une entité Phrase (ex: 'elonmusk')"
echo ""
echo "Documentation complète: MALTEGO_CONFIG_DIRECT.md"
echo ""
