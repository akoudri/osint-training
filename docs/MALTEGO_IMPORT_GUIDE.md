# Guide d'utilisation - Twitter Network Crawler pour Maltego

## 🎯 Vue d'ensemble

Ce script explore les réseaux sociaux Twitter/X de manière incrémentale et exporte les données au format CSV pour visualisation dans Maltego.

### Fonctionnalités

- ✅ Exploration en profondeur (BFS - Breadth-First Search)
- ✅ Limitation intelligente (10 relations max par nœud)
- ✅ Délais aléatoires anti-détection
- ✅ Export CSV compatible Maltego
- ✅ Logging détaillé
- ✅ Interruption gracieuse (Ctrl+C)

---

## 📊 Configuration

### Paramètres principaux (à modifier dans le script)

```python
COMPTE_INITIAL = "wh1t3h4ts"           # Compte de départ (sans @)
MAX_DEPTH = 2                           # Profondeur (0, 1, 2, ou 3)
MAX_RELATIONS_PAR_NOEUD = 10            # Limite par nœud

BROWSER = "chrome"                      # "chrome" ou "firefox"
HEADLESS = False                        # True = sans interface
USE_EXISTING_PROFILE = True             # Utiliser votre profil Chrome

# Délais anti-détection (secondes)
DELAI_MIN_ENTRE_ACTIONS = 2
DELAI_MAX_ENTRE_ACTIONS = 5
DELAI_MIN_ENTRE_PROFILS = 5
DELAI_MAX_ENTRE_PROFILS = 10
```

### Profondeurs expliquées

| Profondeur | Description | Exemple |
|------------|-------------|---------|
| 0 | Compte initial seulement | @alice |
| 1 | + Relations directes | @alice → @bob, @charlie |
| 2 | + Relations des relations | @bob → @david, @eve |
| 3 | + Un niveau supplémentaire | @david → @frank |

⚠️ **Attention :** Profondeur 3 = beaucoup de comptes explorés !

---

## 🚀 Utilisation

### Étape 1 : Configuration

Modifiez le script `twitter_network_crawler.py` :

```python
COMPTE_INITIAL = "votre_compte_cible"  # Sans le @
MAX_DEPTH = 2                           # Ajustez selon vos besoins
MAX_RELATIONS_PAR_NOEUD = 10            # 10 = équilibré
```

### Étape 2 : Fermer Chrome

```bash
killall google-chrome
```

### Étape 3 : Lancer le script

```bash
source .venv/bin/activate
python twitter_network_crawler.py
```

### Étape 4 : Authentification

1. Chrome s'ouvre automatiquement
2. Connectez-vous à Twitter/X
3. Résolvez les CAPTCHA si nécessaire
4. Revenez au terminal
5. Appuyez sur **ENTRÉE**

### Étape 5 : Exploration automatique

Le script explore automatiquement :
```
📊 Exploration de @wh1t3h4ts (profondeur 0)
   🔍 Collecte des interactions...
      → @wh1t3h4ts reply @bob
      → @wh1t3h4ts mention @alice
   ✅ 8 interactions trouvées

  📊 Exploration de @bob (profondeur 1)
     🔍 Collecte des interactions...
     ...
```

### Étape 6 : Récupération des fichiers CSV

À la fin :
```
✅ Exploration terminée !
   Nœuds explorés : 23
   Relations trouvées : 156

💾 Export des données...
   ✅ Relations exportées : twitter_network_relations.csv
   ✅ Nœuds exportés : twitter_network_noeuds.csv
```

---

## 📂 Fichiers générés

### 1. `twitter_network_relations.csv`

**Format :**
```csv
source,target,type,timestamp,depth
wh1t3h4ts,bob,reply,2025-11-27T15:30:00,0
wh1t3h4ts,alice,mention,2025-11-27T15:30:15,0
bob,charlie,reply,2025-11-27T15:35:00,1
```

**Colonnes :**
- `source` : Compte émetteur
- `target` : Compte récepteur
- `type` : Type de relation (`reply`, `mention`)
- `timestamp` : Date/heure de la collecte
- `depth` : Profondeur d'exploration

### 2. `twitter_network_noeuds.csv`

**Format :**
```csv
username,depth,timestamp
wh1t3h4ts,0,2025-11-27T15:30:00
bob,1,2025-11-27T15:35:00
alice,1,2025-11-27T15:32:00
```

**Colonnes :**
- `username` : Nom du compte
- `depth` : Profondeur de découverte
- `timestamp` : Date/heure de l'exploration

### 3. `twitter_network_log.txt`

Log détaillé de toute l'exploration.

---

## 📊 Import dans Maltego

### Méthode 1 : Import des relations (Recommandé)

**Étape A : Créer une nouvelle graph**
1. Ouvrir Maltego
2. Nouveau graph (Ctrl+N)

**Étape B : Importer le CSV**
1. Menu : **Import** → **Import Table from CSV**
2. Sélectionner `twitter_network_relations.csv`
3. Cocher "First row contains headers"
4. Cliquer **Next**

**Étape C : Mapper les colonnes**

| Colonne CSV | Type Entity Maltego | Propriété |
|-------------|---------------------|-----------|
| source | Twitter Affiliation | twitter.screen-name |
| target | Twitter Affiliation | twitter.screen-name |
| type | Link Label | - |
| timestamp | Link Label | - |

**Configuration des liens :**
- Link type : Custom
- Link label : Utiliser colonne `type`
- Link thickness : Weight = 1

**Étape D : Visualiser**
1. Cliquer **Finish**
2. Le graphe s'affiche automatiquement
3. Appliquer un layout : **Layout** → **Hierarchical** ou **Circular**

### Méthode 2 : Import manuel (alternatif)

1. Ouvrir `twitter_network_relations.csv` avec Excel
2. Pour chaque ligne :
   - Ajouter une entité "Twitter Affiliation" (source)
   - Ajouter une entité "Twitter Affiliation" (target)
   - Créer un lien entre les deux

---

## 🎨 Visualisation dans Maltego

### Layouts recommandés

**1. Hierarchical (Hiérarchique)**
- Montre clairement les niveaux de profondeur
- Compte initial en haut
- Relations en cascade

**2. Circular (Circulaire)**
- Visualise les clusters de comptes
- Identifie les communautés

**3. Force-Directed (Forcé)**
- Les comptes fortement connectés se rapprochent
- Détecte les hubs

### Filtres utiles

**Par profondeur :**
```
depth == 0  (Compte initial)
depth == 1  (Relations directes)
depth == 2  (Relations de niveau 2)
```

**Par type de relation :**
```
type == "reply"    (Réponses)
type == "mention"  (Mentions)
```

### Analyses avancées

**1. Identifier les hubs (comptes centraux)**
- Chercher les nœuds avec le plus de connexions
- Outils Maltego : **Find Hubs**

**2. Détecter les communautés**
- Grouper les comptes qui interagissent ensemble
- Outils Maltego : **Community Detection**

**3. Trouver les chemins**
- Chemin entre deux comptes
- Outils Maltego : **Find Path**

---

## ⚙️ Optimisations

### Réduire le temps d'exécution

```python
MAX_DEPTH = 1                    # Au lieu de 2
MAX_RELATIONS_PAR_NOEUD = 5      # Au lieu de 10
DELAI_MIN_ENTRE_PROFILS = 3      # Au lieu de 5
```

### Augmenter la collecte

```python
MAX_DEPTH = 3                    # Plus profond
MAX_RELATIONS_PAR_NOEUD = 20     # Plus de relations
```

⚠️ **Attention :** Plus = plus lent + risque de détection

### Mode discret (stealth)

```python
DELAI_MIN_ENTRE_ACTIONS = 5
DELAI_MAX_ENTRE_ACTIONS = 10
DELAI_MIN_ENTRE_PROFILS = 10
DELAI_MAX_ENTRE_PROFILS = 20
```

---

## 🐛 Résolution de problèmes

### Le script s'arrête brutalement

**Cause :** Rate limiting Twitter

**Solution :**
- Augmenter les délais
- Réduire `MAX_RELATIONS_PAR_NOEUD`
- Attendre 15 minutes puis relancer

### Peu de relations trouvées

**Causes :**
- Compte privé (tweets protégés)
- Compte peu actif
- Timeout trop court

**Solution :**
- Augmenter `max_scrolls` dans le code (ligne ~250)
- Choisir un compte plus actif

### CSV vide ou incomplet

**Cause :** Script interrompu avant l'export

**Solution :**
- Utilisez Ctrl+C pour une interruption propre
- Le script sauvegarde automatiquement les données collectées

### Maltego n'importe pas correctement

**Vérification :**
```bash
head -5 reseau_x.csv
```

Devrait afficher :
```
source,target,type,timestamp,depth
alice,bob,reply,2025-11-27T15:30:00,0
...
```

Si problème :
- Vérifier l'encodage (UTF-8 avec BOM)
- Ouvrir avec Excel et réexporter

---

## 📈 Exemples de cas d'usage

### 1. Analyser l'influence d'un compte

```python
COMPTE_INITIAL = "elonmusk"
MAX_DEPTH = 1
MAX_RELATIONS_PAR_NOEUD = 20
```

Résultat : Qui mentionne Elon et qui il mentionne

### 2. Cartographier une communauté

```python
COMPTE_INITIAL = "compte_central_communaute"
MAX_DEPTH = 2
MAX_RELATIONS_PAR_NOEUD = 15
```

Résultat : Réseau complet de la communauté

### 3. Trouver des connexions cachées

```python
COMPTE_INITIAL = "suspect1"
MAX_DEPTH = 3
MAX_RELATIONS_PAR_NOEUD = 10
```

Résultat : Connexions indirectes entre comptes

---

## ⚠️ Considérations éthiques

### ✅ Autorisé
- Analyse de comptes publics
- Recherche académique
- OSINT défensif
- Investigation légale autorisée

### ❌ Interdit
- Harcèlement
- Collecte massive automatisée
- Revente de données
- Violation de la vie privée

### Bonnes pratiques
- Respectez les délais (anti-spam)
- N'explorez que des comptes publics
- Documentez votre méthodologie
- Anonymisez les données sensibles avant partage

---

## 📚 Ressources

- [Maltego Documentation](https://docs.maltego.com/)
- [Twitter Advanced Search](https://twitter.com/search-advanced)
- [OSINT Framework](https://osintframework.com/)

---

**Date :** 2025-11-27
**Version :** 1.0
**Compatibilité :** Maltego CE/Classic/XL
