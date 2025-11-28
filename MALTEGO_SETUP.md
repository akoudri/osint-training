# Guide de Configuration Maltego

Ce guide explique comment configurer et utiliser les transforms Twitter personnalisées dans Maltego.

## Prérequis

- **Maltego CE/Classic** installé ([télécharger](https://www.maltego.com/downloads/))
- **Python 3.7+** avec `maltego-trx` installé
- Les scripts de ce projet

## Installation rapide

### 1. Installer les dépendances

```bash
# Activer l'environnement virtuel
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Installer les packages requis
pip install -r requirements.txt
```

### 2. Tester le script en ligne de commande

```bash
# Test basique
python transforms/twitter_transform.py "elonmusk"

# Exécuter les tests unitaires
pytest test_twitter_transform.py -v
```

Si aucune erreur n'apparaît, le script fonctionne correctement.

## Configuration dans Maltego

### Méthode 1 : Transform Server (recommandé)

Cette méthode utilise un serveur Flask local pour héberger les transforms.

#### Étape 1 : Démarrer le serveur

```bash
# Option A : Script automatique
./start_maltego_server.sh

# Option B : Commande manuelle
python transforms/server.py
```

Vous devriez voir :
```
============================================================
Maltego Transform Server - OSINT Training
============================================================
Serveur démarré sur http://localhost:8080
Transforms disponibles: 1
  - TwitterAliasToProfileURL
============================================================
 * Running on http://0.0.0.0:8080
```

**Important** : Laissez ce terminal ouvert tant que vous utilisez Maltego.

#### Étape 2 : Configurer Maltego

1. **Ouvrir Maltego**
2. Aller dans **Transforms** → **Transform Hub**
3. Cliquer sur **New Local Transform Server**
4. Configuration :
   - **Name** : `OSINT Training Transforms`
   - **Description** : `Transforms personnalisées pour Twitter/X`
   - **URL** : `http://localhost:8080`
5. Cliquer sur **Discover Transforms**
6. Maltego devrait trouver la transform "Twitter Alias to Profile URL"
7. Cliquer sur **Install/Update**

#### Étape 3 : Vérification

1. Créer un nouveau graphe dans Maltego
2. Ajouter une entité **Phrase** (glisser-déposer depuis la palette)
3. Double-cliquer et entrer un alias Twitter (ex: `elonmusk`)
4. Clic droit sur l'entité → **All Transforms** → **OSINT Training**
5. Vous devriez voir **Twitter Alias to Profile URL**

### Méthode 2 : Local Transform (alternative)

Si la méthode serveur ne fonctionne pas, vous pouvez configurer une transform locale.

#### Configuration manuelle

1. **Ouvrir Maltego** → **Transforms** → **New Local Transform**
2. Configuration :
   - **Transform ID** : `TwitterAliasToProfileURL`
   - **Description** : `Converts Twitter alias to profile URL`
   - **Author** : `OSINT Training`
   - **Input entity type** : `maltego.Phrase`

3. **Command line** :
   - **Command** : `/usr/bin/python3` (Linux/Mac) ou `C:\Python3\python.exe` (Windows)
   - **Parameters** : `/chemin/absolu/vers/transforms/twitter_transform.py`
   - **Working directory** : `/chemin/absolu/vers/osint-training`

4. Cliquer sur **Next** → **Finish**

**Note** : Remplacez `/chemin/absolu/vers/` par le chemin réel de votre projet.

## Utilisation

### Scénario 1 : Profil unique

1. **Créer un graphe** dans Maltego
2. **Ajouter une entité Phrase** avec un alias Twitter :
   - `elonmusk`
   - `@snowden`
   - Tout alias valide Twitter/X

3. **Clic droit** → **OSINT Training** → **Twitter Alias to Profile URL**
4. **Résultat** : Une entité URL pointant vers `https://x.com/alias`

### Scénario 2 : Analyse multiple (batch)

1. Créer plusieurs entités **Phrase** avec différents alias
2. **Sélectionner toutes les entités** (Ctrl+A ou Cmd+A)
3. **Clic droit** → **OSINT Training** → **Twitter Alias to Profile URL**
4. Maltego exécutera la transform sur chaque entité

### Scénario 3 : Enrichissement progressif

```
[Phrase: "suspect123"]
  ↓ Twitter Alias to Profile URL
[URL: https://x.com/suspect123]
  ↓ ToWebsite (transform native Maltego)
[Website Entity]
  ↓ ToServerTechnologies / ToEmails / etc.
[Entités enrichies]
```

## Exploitation des métadonnées

### Propriétés de l'entité

Après exécution, l'entité URL contient :

| Propriété | Valeur | Usage |
|-----------|--------|-------|
| `url` | `https://x.com/alias` | URL directe du profil |
| `twitter.alias` | `alias` | Alias nettoyé |
| `twitter.handle` | `@alias` | Handle complet |
| `short-title` | `Profil X de @alias` | Affichage |

**Comment voir** : Sélectionner l'entité → Panneau de droite "Property View"

### Notes OSINT

Les notes de l'entité contiennent des URLs additionnelles :

- **Recherche de tweets** : `https://x.com/search?q=from:alias`
- **Tweets avec réponses** : `https://x.com/search?q=from:alias+filter:replies`
- **Média** : `https://x.com/alias/media`
- **Likes** : `https://x.com/alias/likes`

**Comment voir** : Sélectionner l'entité → Panneau de droite "Notes"

**Usage** : Copier-coller ces URLs dans votre navigateur pour investigation approfondie.

## Validation et messages

### Alias valide
✅ Pas de message d'erreur, entité créée avec succès

### Alias nettoyé
ℹ️ Message "Inform" : `Alias nettoyé: '@user' → 'user'`

### Alias invalide (caractères interdits)
⚠️ Message "Partial Error" : `Alias invalide: L'alias contient des caractères invalides`

### Erreur fatale
❌ Message "Fatal Error" : `Erreur: Aucun argument reçu`

**Voir les messages** : Panneau "Output" en bas de Maltego

## Exemples de requêtes

### Recherche de profils liés à une organisation

```
[Phrase: "company_name"]
  → Recherche manuelle des employés sur Twitter
  → Créer entités Phrase pour chaque alias trouvé
  → Twitter Alias to Profile URL (batch)
  → Analyser les profils collectifs
```

### Investigation d'un réseau social

```
[Phrase: "target_user"]
  → Twitter Alias to Profile URL
  → [URL] Consulter followers manuellement
  → Créer Phrase pour followers pertinents
  → Twitter Alias to Profile URL (batch)
  → Mapper le réseau
```

### Veille sur des comptes spécifiques

1. Créer une liste d'alias à surveiller
2. Exécuter la transform pour générer les URLs
3. Utiliser les URLs de recherche (dans les notes) pour monitorer l'activité
4. Automatiser avec des scripts externes si nécessaire

## Dépannage

### Le serveur ne démarre pas

**Erreur** : `Address already in use`

**Solution** :
```bash
# Trouver le processus qui utilise le port 8080
lsof -i :8080  # Linux/Mac
netstat -ano | findstr :8080  # Windows

# Tuer le processus ou changer le port dans server.py
```

### Maltego ne trouve pas les transforms

**Solutions** :
1. Vérifier que le serveur est démarré (terminal ouvert)
2. Tester l'URL dans un navigateur : `http://localhost:8080`
3. Redémarrer Maltego
4. Supprimer et recréer la connexion au serveur

### Erreur "Module not found"

**Solution** :
```bash
# Vérifier l'environnement virtuel
which python  # Doit pointer vers .venv/bin/python

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Aucune entité n'est créée

**Causes possibles** :
- Alias invalide (vérifier la console Maltego pour les erreurs)
- Script mal configuré (tester en ligne de commande d'abord)
- Problème de droits (chmod +x sur le script)

**Diagnostic** :
```bash
# Tester manuellement
python transforms/twitter_transform.py "test_alias"

# Vérifier les erreurs
echo $?  # Doit retourner 0 si succès
```

### Performance lente

Pour un grand nombre d'alias (>50) :
- Exécuter par lots de 10-20 entités
- Utiliser des filtres Maltego pour cibler les plus pertinents
- Considérer l'ajout d'un cache (amélioration future)

## Personnalisation

### Modifier le port du serveur

Éditer `transforms/server.py` ligne 24 :
```python
app.run(host="0.0.0.0", port=8081)  # Changer 8080 en 8081
```

### Ajouter des propriétés personnalisées

Éditer `transforms/transform_config.py` :
```python
# Ajouter après ligne 40
entity.addProperty("custom.field", "Custom Field", "loose", "valeur")
```

### Changer la couleur du lien

Éditer `transforms/transform_config.py` ligne 44 :
```python
entity.setLinkColor("0xFF0000")  # Rouge au lieu de bleu
```

Couleurs disponibles :
- `0x0000FF` : Bleu (Twitter)
- `0xFF0000` : Rouge (alerte)
- `0x00FF00` : Vert (validé)
- `0xFFFF00` : Jaune (en attente)

## Sécurité et éthique

### Bonnes pratiques OSINT

- ✅ Toujours respecter la vie privée des individus
- ✅ Utiliser uniquement sur des données publiques
- ✅ Documenter vos sources et méthodologie
- ✅ Ne pas harceler ou contacter directement les sujets
- ✅ Respecter les CGU de Twitter/X

### Limitations légales

- 🚫 Ne pas utiliser pour du harcèlement
- 🚫 Ne pas collecter massivement sans autorisation
- 🚫 Ne pas contourner les protections anti-scraping de Twitter
- 🚫 Ne pas vendre ou partager les données collectées

## Support et contribution

### Rapporter un bug

1. Vérifier que le bug est reproductible
2. Tester avec le script en ligne de commande
3. Documenter les étapes pour reproduire
4. Fournir les logs d'erreur

### Améliorations suggérées

Pour contribuer :
- Consulter la section "Améliorations futures" dans `transforms/README.md`
- Créer une nouvelle transform en suivant le pattern existant
- Tester avec pytest avant de soumettre

## Ressources additionnelles

- [Documentation Maltego officielle](https://docs.maltego.com/)
- [Maltego TRX GitHub](https://github.com/MaltegoTech/maltego-trx)
- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [OSINT Framework](https://osintframework.com/)

---

**Version** : 1.0.0
**Dernière mise à jour** : Novembre 2025
**Auteur** : Ali
