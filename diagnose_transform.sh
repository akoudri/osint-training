#!/bin/bash
# Script de diagnostic pour la transform Maltego

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           🔍 DIAGNOSTIC TRANSFORM MALTEGO                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERRORS=0

# 1. Vérifier le wrapper
echo "1️⃣  Vérification du wrapper"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "$PROJECT_DIR/transforms/run_transform.sh" ]; then
    if [ -x "$PROJECT_DIR/transforms/run_transform.sh" ]; then
        echo "✓ Wrapper exécutable: $PROJECT_DIR/transforms/run_transform.sh"
    else
        echo "✗ Wrapper non exécutable"
        echo "  → Correction: chmod +x $PROJECT_DIR/transforms/run_transform.sh"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "✗ Wrapper manquant"
    echo "  → Le fichier transforms/run_transform.sh n'existe pas"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 2. Vérifier le venv
echo "2️⃣  Vérification de l'environnement virtuel"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "$PROJECT_DIR/.venv" ]; then
    echo "✓ Environnement virtuel présent: $PROJECT_DIR/.venv"
else
    echo "✗ Environnement virtuel manquant"
    echo "  → Correction: python3 -m venv .venv"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 3. Vérifier maltego-trx
echo "3️⃣  Vérification de maltego-trx"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "$PROJECT_DIR/.venv" ]; then
    source "$PROJECT_DIR/.venv/bin/activate"
    if python -c "import maltego_trx" 2>/dev/null; then
        VERSION=$(python -c "import maltego_trx; print(maltego_trx.__version__)" 2>/dev/null || echo "unknown")
        echo "✓ maltego-trx installé (version: $VERSION)"
    else
        echo "✗ maltego-trx manquant dans le venv"
        echo "  → Correction: source .venv/bin/activate && pip install maltego-trx"
        ERRORS=$((ERRORS + 1))
    fi
    deactivate
else
    echo "⚠ Impossible de vérifier (venv manquant)"
fi
echo ""

# 4. Vérifier la génération de XML
echo "4️⃣  Vérification de la génération XML"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -x "$PROJECT_DIR/transforms/run_transform.sh" ]; then
    OUTPUT=$("$PROJECT_DIR/transforms/run_transform.sh" "test" 2>&1)
    if echo "$OUTPUT" | grep -q "<MaltegoMessage>"; then
        echo "✓ Transform génère du XML Maltego valide"
        # Vérifier les éléments clés
        if echo "$OUTPUT" | grep -q "<Entity Type=\"maltego.URL\">"; then
            echo "✓ Entité URL présente"
        fi
        if echo "$OUTPUT" | grep -q "twitter.alias"; then
            echo "✓ Propriété twitter.alias présente"
        fi
        if echo "$OUTPUT" | grep -q "URLs OSINT"; then
            echo "✓ Notes OSINT présentes"
        fi
    else
        echo "✗ Transform ne génère pas de XML valide"
        echo "  → Sortie reçue:"
        echo "$OUTPUT" | head -10
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "⚠ Impossible de tester (wrapper non exécutable)"
fi
echo ""

# 5. Temps d'exécution
echo "5️⃣  Test de performance"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -x "$PROJECT_DIR/transforms/run_transform.sh" ]; then
    START=$(date +%s%N)
    "$PROJECT_DIR/transforms/run_transform.sh" "test" >/dev/null 2>&1
    END=$(date +%s%N)
    ELAPSED=$((($END - $START) / 1000000))

    if [ $ELAPSED -lt 1000 ]; then
        echo "✓ Transform rapide (${ELAPSED}ms)"
    elif [ $ELAPSED -lt 2000 ]; then
        echo "⚠ Transform acceptable (${ELAPSED}ms)"
        echo "  → Recommandé: < 1000ms"
    else
        echo "✗ Transform lente (${ELAPSED}ms)"
        echo "  → Vérifier l'activation du venv dans le wrapper"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "⚠ Impossible de tester (wrapper non exécutable)"
fi
echo ""

# 6. Tests unitaires
echo "6️⃣  Vérification des tests unitaires"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "$PROJECT_DIR/test_twitter_transform.py" ]; then
    source "$PROJECT_DIR/.venv/bin/activate" 2>/dev/null
    if command -v pytest &> /dev/null; then
        TEST_OUTPUT=$(pytest "$PROJECT_DIR/test_twitter_transform.py" -v 2>&1)
        if echo "$TEST_OUTPUT" | grep -q "17 passed"; then
            echo "✓ Tous les tests passent (17/17)"
        else
            echo "⚠ Certains tests échouent"
            echo "$TEST_OUTPUT" | tail -5
        fi
    else
        echo "⚠ pytest non installé (pip install pytest)"
    fi
    deactivate 2>/dev/null
else
    echo "⚠ Fichier de test manquant"
fi
echo ""

# Résumé
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                        📊 RÉSUMÉ                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ Aucun problème détecté - Transform prête pour Maltego !"
    echo ""
    echo "📋 Chemins pour la configuration Maltego:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Command:"
    echo "$PROJECT_DIR/transforms/run_transform.sh"
    echo ""
    echo "Working directory:"
    echo "$PROJECT_DIR"
    echo ""
    echo "👉 Suivre le guide: MALTEGO_QUICKSTART.md"
else
    echo "❌ $ERRORS problème(s) détecté(s)"
    echo ""
    echo "Corrigez les erreurs ci-dessus puis relancez ce diagnostic."
    echo ""
    echo "📖 Documentation:"
    echo "  - MALTEGO_TROUBLESHOOTING.md (dépannage)"
    echo "  - MALTEGO_CONFIG_DIRECT.md (configuration)"
fi

echo ""
exit $ERRORS
