# Configuration Maltego - Transform Locale (Mode Direct)

Ce guide explique comment configurer la transform Twitter **directement dans Maltego** sans passer par un serveur Flask.

## Solution au problème d'environnement virtuel

Maltego ne peut pas utiliser directement votre `.venv`. La solution est d'utiliser un **script wrapper** qui active l'environnement avant d'exécuter la transform.

## Configuration pas-à-pas

### Étape 1 : Vérifier le wrapper

Le script `transforms/run_transform.sh` a été créé pour vous :

```bash
# Tester le wrapper
./transforms/run_transform.sh "elonmusk"
```

Si cela fonctionne sans erreur, passez à l'étape suivante.

### Étape 2 : Obtenir les chemins absolus

```bash
# Chemin absolu vers le wrapper
readlink -f transforms/run_transform.sh
# Résultat : /home/ali/Training/osint-training/transforms/run_transform.sh
```

**Notez ce chemin**, vous en aurez besoin dans Maltego.

### Étape 3 : Configuration dans Maltego

1. **Ouvrir Maltego**

2. **Aller dans le menu** :
   - **Transforms** → **New Local Transform**

3. **Transform Details** :
   - **Transform ID** : `TwitterAliasToProfileURL`
   - **Description** : `Convert Twitter/X alias to profile URL with OSINT metadata`
   - **Transform author** : `OSINT Training`
   - **Input entity type** : Cliquez sur le bouton `...` et sélectionnez `maltego.Phrase`

4. **Cliquer sur Next**

5. **Command line** :
   - **Command** : `/home/ali/Training/osint-training/transforms/run_transform.sh`
   - **Parameters** : (laisser vide - le wrapper gère tout)
   - **Working directory** : `/home/ali/Training/osint-training`

6. **Cliquer sur Next** → **Finish**

### Étape 4 : Test dans Maltego

1. **Créer un nouveau graphe** (New Graph)

2. **Ajouter une entité Phrase** :
   - Glisser-déposer "Phrase" depuis la palette d'entités
   - Double-cliquer dessus
   - Entrer : `elonmusk`

3. **Exécuter la transform** :
   - Clic droit sur l'entité
   - **All Transforms** → chercher "Twitter"
   - Cliquer sur **TwitterAliasToProfileURL**

4. **Résultat attendu** :
   - Une entité **URL** devrait apparaître
   - Valeur : `https://x.com/elonmusk`
   - Propriétés visibles dans le panneau de droite

## Vérification de la configuration

### ✅ La transform fonctionne si :
- Une entité URL est créée
- L'URL est `https://x.com/[alias]`
- Les propriétés contiennent `twitter.alias` et `twitter.handle`
- Les notes contiennent les URLs OSINT additionnelles

### ❌ Dépannage

#### Erreur : "Permission denied"

```bash
chmod +x /home/ali/Training/osint-training/transforms/run_transform.sh
```

#### Erreur : "No module named maltego_trx"

Vérifiez que l'environnement virtuel est activé dans le wrapper :

```bash
# Tester manuellement
source .venv/bin/activate
python -c "import maltego_trx; print('OK')"
```

Si erreur, installer dans le venv :
```bash
source .venv/bin/activate
pip install maltego-trx
```

#### Erreur : "Command not found"

Vérifiez que le chemin dans Maltego est **absolu** :
- ✅ `/home/ali/Training/osint-training/transforms/run_transform.sh`
- ❌ `transforms/run_transform.sh`
- ❌ `~/Training/osint-training/transforms/run_transform.sh`

#### Aucune entité créée, pas d'erreur visible

1. Ouvrir le panneau **Output** en bas de Maltego
2. Chercher les messages d'erreur
3. Si message "Partial Error" : l'alias est invalide

#### Test en ligne de commande

```bash
# Test direct du wrapper
./transforms/run_transform.sh "@snowden"

# Devrait afficher du XML Maltego
# Si erreur Python, le problème vient du script, pas de Maltego
```

## Alternative : Python système (sans venv)

Si vous préférez ne pas utiliser de venv, vous pouvez installer les packages globalement :

### ⚠️ Option 1 : Installation globale (avec sudo)

```bash
# Désactiver le venv
deactivate

# Installer globalement (nécessite sudo)
sudo pip install maltego-trx
```

Puis dans Maltego :
- **Command** : `/usr/bin/python3`
- **Parameters** : `/home/ali/Training/osint-training/transforms/twitter_transform.py`

### ✅ Option 2 : Installation utilisateur (sans sudo)

```bash
# Installer pour l'utilisateur uniquement
pip install --user maltego-trx

# Vérifier
python3 -c "import maltego_trx; print('OK')"
```

Puis dans Maltego :
- **Command** : `/usr/bin/python3`
- **Parameters** : `/home/ali/Training/osint-training/transforms/twitter_transform.py`

## Configuration avancée

### Organiser les transforms dans Maltego

1. **Créer un Transform Set** :
   - Transforms → Manage Transform Sets → New
   - Nom : `OSINT Training - Twitter`

2. **Ajouter la transform au set** :
   - Clic droit sur votre transform → Add to Set
   - Sélectionner votre nouveau set

3. **Utilisation** :
   - Clic droit sur une entité → **OSINT Training - Twitter** (directement visible)

### Icône personnalisée (optionnel)

1. Créer une icône PNG 16x16 ou 32x32
2. Transform → Edit Transform
3. Icon → Browse → Sélectionner votre icône

### Raccourci clavier (optionnel)

1. Edit Transform
2. Shortcut → Assigner une touche (ex: `Ctrl+T`)

## Test de validation complète

### Cas de test à vérifier

| Input (Phrase) | Output attendu | Propriétés |
|----------------|----------------|------------|
| `elonmusk` | `https://x.com/elonmusk` | alias=`elonmusk` |
| `@snowden` | `https://x.com/snowden` | alias=`snowden` (@ retiré) |
| `  test_user  ` | `https://x.com/test_user` | alias=`test_user` |
| `invalid-user` | Partial Error | Message dans Output |
| `settings` | Partial Error | "nom réservé" |

### Validation des métadonnées

Pour chaque entité URL créée, vérifier :

1. **Propriétés** (panneau de droite) :
   - ✅ `url` : URL complète
   - ✅ `twitter.alias` : Alias sans @
   - ✅ `twitter.handle` : Avec @
   - ✅ `short-title` : Titre court

2. **Notes** (onglet Notes) :
   - ✅ "Profil Twitter/X: @alias"
   - ✅ 4 URLs OSINT additionnelles

3. **Apparence** :
   - ✅ Lien bleu entre Phrase et URL
   - ✅ Label du lien : `@alias`

## Utilisation en production

### Workflow OSINT recommandé

```
[Collecte d'alias]
    ↓ Liste des suspects
[Entités Phrase créées]
    ↓ Sélection multiple → Transform batch
[URLs Twitter générées]
    ↓ Consulter les notes OSINT
[Investigation manuelle via URLs]
    ↓ Analyse des tweets/media
[Intelligence collectée]
```

### Bonnes pratiques

1. **Batch processing** :
   - Sélectionner 10-20 entités max à la fois
   - Éviter de surcharger Twitter avec trop de requêtes

2. **Organisation** :
   - Utiliser les couleurs pour marquer les entités vérifiées
   - Ajouter des notes sur les entités importantes
   - Créer des graphes séparés par enquête

3. **Documentation** :
   - Exporter régulièrement le graphe (File → Export Graph)
   - Prendre des screenshots des résultats clés
   - Noter la date de collecte

## Fichiers de configuration Maltego

Les transforms sont sauvegardées dans :
```
~/.maltego/
├── config/
│   └── Maltego.conf
└── transforms/
    └── local/
        └── TwitterAliasToProfileURL.transform
```

**Backup recommandé** avant modification :
```bash
cp -r ~/.maltego ~/.maltego.backup
```

## Récapitulatif : 3 méthodes possibles

| Méthode | Command | Parameters | Avantages | Inconvénients |
|---------|---------|------------|-----------|---------------|
| **Wrapper (recommandé)** | `/path/to/run_transform.sh` | (vide) | Isolation venv | Script supplémentaire |
| **Python système** | `/usr/bin/python3` | `/path/to/twitter_transform.py` | Simple | Packages globaux |
| **Serveur Flask** | (via Transform Hub) | (N/A) | Découverte auto | Serveur à maintenir |

## Support et ressources

- **Test CLI** : `./transforms/run_transform.sh "test"`
- **Logs Maltego** : Panneau "Output" en bas
- **Documentation** : `MALTEGO_SETUP.md` pour le mode serveur

---

**Version** : 1.0
**Configuration testée sur** : Maltego CE, Linux
**Date** : Novembre 2025
