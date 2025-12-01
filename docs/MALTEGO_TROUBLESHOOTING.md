# Maltego Transform - Résolution des problèmes

## Erreur "Empty Response" ✅ RÉSOLU

### Symptôme
Maltego affiche l'erreur **"Empty Response"** lors de l'exécution de la transform.

### Cause
Le script ne produisait pas de sortie XML sur STDOUT. La méthode `response.returnOutput()` retourne le XML mais ne l'affiche pas automatiquement.

### Solution appliquée

**Avant (ne fonctionnait pas) :**
```python
response.returnOutput()  # Retourne le XML mais ne l'affiche pas
```

**Après (fonctionne) :**
```python
print(response.returnOutput())  # Affiche le XML sur STDOUT pour Maltego
```

### Vérification

Testez en ligne de commande que le XML est généré :

```bash
./transforms/run_transform.sh "elonmusk"
```

**Sortie attendue :**
```xml
<MaltegoMessage>
  <MaltegoTransformResponseMessage>
    <Entities>
      <Entity Type="maltego.URL">
        <Value>https://x.com/elonmusk</Value>
        ...
      </Entity>
    </Entities>
    <UIMessages></UIMessages>
  </MaltegoTransformResponseMessage>
</MaltegoMessage>
```

Si vous voyez ce XML, le script fonctionne correctement.

---

## Autres problèmes courants

### 1. "Permission denied"

**Symptôme :** Erreur lors de l'exécution du wrapper

**Solution :**
```bash
chmod +x /home/ali/Training/osint-training/transforms/run_transform.sh
```

### 2. "No module named maltego_trx"

**Symptôme :** Erreur Python lors de l'import

**Solution :**
```bash
source .venv/bin/activate
pip install maltego-trx
```

### 3. Aucune entité créée (pas d'erreur)

**Diagnostic :**
1. Vérifier le panneau **Output** en bas de Maltego
2. Chercher les messages d'erreur ou warnings

**Solutions possibles :**

a) **Alias invalide**
   - Message "Partial Error" visible dans Output
   - Vérifier que l'alias respecte les règles Twitter (a-z, 0-9, _, max 15 chars)

b) **Script non exécutable**
```bash
chmod +x /home/ali/Training/osint-training/transforms/run_transform.sh
```

c) **Chemin incorrect dans Maltego**
   - Utiliser le chemin **absolu complet**
   - PAS de `~` ou chemins relatifs
   - Afficher avec : `./show_maltego_paths.sh`

### 4. "Command not found"

**Symptôme :** Maltego ne trouve pas le script

**Solution :**
Vérifier que le chemin dans Maltego est correct :

```bash
# Afficher le chemin correct
./show_maltego_paths.sh
```

Configuration Maltego :
- **Command** : `/home/ali/Training/osint-training/transforms/run_transform.sh` (chemin absolu)
- **NOT** : `~/Training/osint-training/...` (chemin avec ~)
- **NOT** : `transforms/run_transform.sh` (chemin relatif)

### 5. Erreur "bad interpreter"

**Symptôme :** Erreur lors de l'exécution du wrapper bash

**Cause :** Fins de ligne Windows (CRLF) au lieu de Unix (LF)

**Solution :**
```bash
# Convertir les fins de ligne
dos2unix transforms/run_transform.sh

# Ou avec sed
sed -i 's/\r$//' transforms/run_transform.sh
```

### 6. Python utilise le mauvais environnement

**Symptôme :** "No module named maltego_trx" malgré l'installation

**Diagnostic :**
```bash
# Vérifier quel Python est utilisé
source .venv/bin/activate
which python
# Doit afficher: /home/ali/Training/osint-training/.venv/bin/python

python -c "import maltego_trx; print('OK')"
# Doit afficher: OK
```

**Solution :**
Vérifier que le wrapper `run_transform.sh` active bien le venv :
```bash
cat transforms/run_transform.sh
# Doit contenir: source "$PROJECT_DIR/.venv/bin/activate"
```

### 7. Timeout / Transform très lente

**Symptôme :** La transform prend plusieurs secondes

**Cause possible :** Le venv n'est pas activé et Python cherche des packages

**Solution :**
Vérifier le temps d'exécution :
```bash
time ./transforms/run_transform.sh "elonmusk"
# Doit être < 1 seconde
```

Si > 2 secondes, vérifier l'activation du venv dans le wrapper.

---

## Tests de validation

### Test 1 : Wrapper fonctionne

```bash
./transforms/run_transform.sh "elonmusk" | head -5
```

**Attendu :** XML Maltego affiché

### Test 2 : Alias avec @

```bash
./transforms/run_transform.sh "@snowden" | grep "UIMessage"
```

**Attendu :** Message "Alias nettoyé"

### Test 3 : Alias invalide

```bash
./transforms/run_transform.sh "invalid-user!" | grep "PartialError"
```

**Attendu :** Message d'erreur "caractères invalides"

### Test 4 : Tests unitaires

```bash
pytest test_twitter_transform.py -v
```

**Attendu :** 17 passed

---

## Diagnostic complet

Script de diagnostic automatique :

```bash
#!/bin/bash
echo "🔍 Diagnostic Transform Maltego"
echo "================================"

# 1. Vérifier le wrapper
if [ -x transforms/run_transform.sh ]; then
    echo "✓ Wrapper exécutable"
else
    echo "✗ Wrapper non exécutable"
    echo "  → chmod +x transforms/run_transform.sh"
fi

# 2. Vérifier le venv
if [ -d .venv ]; then
    echo "✓ Environnement virtuel présent"
else
    echo "✗ Environnement virtuel manquant"
    echo "  → python3 -m venv .venv"
fi

# 3. Vérifier maltego-trx
source .venv/bin/activate
if python -c "import maltego_trx" 2>/dev/null; then
    echo "✓ maltego-trx installé"
else
    echo "✗ maltego-trx manquant"
    echo "  → pip install maltego-trx"
fi

# 4. Tester la transform
if ./transforms/run_transform.sh "test" 2>&1 | grep -q "MaltegoMessage"; then
    echo "✓ Transform génère du XML"
else
    echo "✗ Transform ne génère pas de XML"
    echo "  → Vérifier les erreurs ci-dessus"
fi

# 5. Temps d'exécution
START=$(date +%s%N)
./transforms/run_transform.sh "test" >/dev/null 2>&1
END=$(date +%s%N)
ELAPSED=$((($END - $START) / 1000000))

if [ $ELAPSED -lt 1000 ]; then
    echo "✓ Transform rapide (${ELAPSED}ms)"
else
    echo "⚠ Transform lente (${ELAPSED}ms)"
    echo "  → Devrait être < 1000ms"
fi

echo ""
echo "📋 Chemins pour Maltego:"
echo "Command: $(pwd)/transforms/run_transform.sh"
echo "Working dir: $(pwd)"
```

Sauvegarder ce script dans `diagnose_transform.sh` et exécuter :
```bash
chmod +x diagnose_transform.sh
./diagnose_transform.sh
```

---

## Réinstallation complète (si tout échoue)

```bash
# 1. Sauvegarder les modifications
git status

# 2. Nettoyer le venv
rm -rf .venv

# 3. Recréer le venv
python3 -m venv .venv
source .venv/bin/activate

# 4. Réinstaller les dépendances
pip install -r requirements.txt

# 5. Vérifier
python -c "import maltego_trx; print('OK')"

# 6. Tester
./transforms/run_transform.sh "elonmusk"
```

---

## Support

Si le problème persiste :

1. **Vérifier la version** :
   ```bash
   python --version  # Doit être >= 3.7
   pip show maltego-trx  # Doit être 1.6.1
   ```

2. **Logs détaillés** :
   ```bash
   ./transforms/run_transform.sh "test" 2>&1 | tee debug.log
   ```

3. **Consulter** :
   - MALTEGO_CONFIG_DIRECT.md (configuration détaillée)
   - MALTEGO_QUICKSTART.md (guide rapide)

---

**Dernière mise à jour :** 28 Novembre 2025
**Statut :** ✅ Problème "Empty Response" résolu
