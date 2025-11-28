# Maltego Transforms - OSINT Training

Transforms Maltego personnalisées pour l'analyse OSINT des profils Twitter/X.

## Structure du projet

```
transforms/
├── __init__.py              # Module Python
├── twitter_transform.py     # Transform principale (script CLI)
├── transform_config.py      # Configuration des transforms (API TRX)
├── server.py               # Serveur Flask pour Maltego
└── README.md               # Cette documentation
```

## Installation

### Prérequis

```bash
# Installer les dépendances
pip install maltego-trx flask
```

### Configuration de l'environnement

```bash
# Depuis le répertoire racine du projet
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

## Utilisation

### 1. Mode Script (ligne de commande)

Le script `twitter_transform.py` peut être exécuté directement pour tester :

```bash
# Usage basique
python transforms/twitter_transform.py "elonmusk"

# Avec préfixe @
python transforms/twitter_transform.py "@snowden"

# Alias avec espaces (seront nettoyés)
python transforms/twitter_transform.py "  user_123  "
```

**Sortie** : XML Maltego sur STDOUT

### 2. Mode Serveur (intégration Maltego)

#### Démarrage du serveur

```bash
python transforms/server.py
```

Le serveur démarre sur `http://localhost:8080`

#### Configuration dans Maltego

1. **Ouvrir Maltego** → Transforms → Transform Hub
2. **New Local Transform Server**
3. Configuration :
   - **URL** : `http://localhost:8080`
   - **Cliquer** sur "Discover Transforms"
4. Les transforms disponibles apparaîtront automatiquement

#### Utilisation dans Maltego

1. Créer une entité `maltego.Phrase` avec un alias Twitter
2. Clic droit → Rechercher "Twitter Alias to Profile URL"
3. Exécuter la transform
4. **Résultat** : Entité `maltego.URL` avec métadonnées enrichies

## Transforms disponibles

### Twitter Alias to Profile URL

**Description** : Convertit un alias Twitter/X en URL de profil avec validation et métadonnées OSINT

**Input** : `maltego.Phrase` (alias Twitter, avec ou sans @)
**Output** : `maltego.URL` (profil Twitter/X)

#### Validation automatique

La transform vérifie :
- ✅ Longueur (1-15 caractères)
- ✅ Caractères autorisés (a-z, A-Z, 0-9, _)
- ✅ Noms réservés (mentions, settings, home, etc.)
- ✅ Nettoyage du préfixe @ et espaces

#### Métadonnées ajoutées

| Propriété | Type | Description |
|-----------|------|-------------|
| `url` | strict | URL complète du profil |
| `short-title` | loose | Titre court pour affichage |
| `title` | loose | Titre complet |
| `twitter.alias` | strict | Alias nettoyé |
| `twitter.handle` | strict | Handle avec @ |

#### Notes OSINT

Chaque entité inclut des URLs additionnelles :
- 🔍 Recherche de tweets : `https://x.com/search?q=from:alias`
- 💬 Tweets avec réponses : `https://x.com/search?q=from:alias+filter:replies`
- 📸 Média du profil : `https://x.com/alias/media`
- ❤️ Likes : `https://x.com/alias/likes`

## Tests

### Tests unitaires (pytest)

```bash
# Exécuter tous les tests
pytest test_twitter_transform.py -v

# Test spécifique
pytest test_twitter_transform.py::test_valid_alias -v

# Avec couverture
pytest test_twitter_transform.py --cov=transforms
```

**17 tests disponibles** couvrant :
- Validation d'alias valides
- Nettoyage (@, espaces)
- Détection d'erreurs (caractères invalides, longueur, noms réservés)
- Cas limites (None, chaîne vide, etc.)

### Démonstration interactive

```bash
# Tester plusieurs cas
python demo_transform.py

# Tester un alias spécifique
python demo_transform.py "@elonmusk"
```

## Architecture technique

### Script CLI (`twitter_transform.py`)

```python
# Point d'entrée
if __name__ == "__main__":
    main()

# Fonction principale
def main():
    # 1. Initialisation Maltego
    # 2. Récupération argument
    # 3. Validation alias
    # 4. Construction URL
    # 5. Création entité
    # 6. Ajout métadonnées
    # 7. Sortie XML
```

### API TRX (`transform_config.py`)

```python
# Enregistrement de la transform
@registry.register_transform(
    display_name="Twitter Alias to Profile URL",
    input_entity="maltego.Phrase",
    description="...",
    output_entities=["maltego.URL"]
)
def twitter_alias_to_url(request, response):
    # Logique de transformation
    return response
```

### Serveur Flask (`server.py`)

```python
# Enregistrement des transforms
registry.register_to_server(app)

# Démarrage serveur
app.run(host="0.0.0.0", port=8080)
```

## Cas d'usage OSINT

### Workflow 1 : Investigation d'un individu

```
[Phrase: "elonmusk"]
  → Twitter Alias to Profile URL
  → [URL: https://x.com/elonmusk]
      → Consulter les notes OSINT
      → Analyser tweets récents
      → Extraire followers/following
```

### Workflow 2 : Analyse de réseau

```
[Liste d'alias Twitter]
  → Batch: Twitter Alias to Profile URL
  → [Multiples URLs]
      → ToWebsite (Maltego native)
      → [Website entities]
          → DNS/WHOIS transforms
```

### Workflow 3 : Veille automatisée

```
[Phrase: "target_user"]
  → Twitter Alias to Profile URL
  → [URL avec métadonnées]
      → Utiliser URL de recherche (notes)
      → Monitorer nouveaux tweets
      → Détecter changements de comportement
```

## Dépannage

### Erreur : "No module named maltego_trx"

```bash
pip install maltego-trx
```

### Erreur : "Port 8080 already in use"

```bash
# Changer le port dans server.py
app.run(host="0.0.0.0", port=8081)  # ligne 24
```

### Maltego ne trouve pas les transforms

1. Vérifier que le serveur est démarré (`python transforms/server.py`)
2. Vérifier l'URL dans Maltego : `http://localhost:8080`
3. Cliquer sur "Discover Transforms"
4. Redémarrer Maltego si nécessaire

### XML invalide dans la sortie

Vérifier que vous utilisez `python 3.x` (pas Python 2) :
```bash
python --version  # Doit être >= 3.7
```

## Améliorations futures

### Enrichissement automatique
- [ ] Appel API Twitter pour vérifier l'existence du compte
- [ ] Récupération du nom complet, bio, followers
- [ ] Détection de liens dans la bio (email, site web)

### Nouvelles transforms
- [ ] **Twitter URL to Account Info** : Extraire métadonnées du profil
- [ ] **Twitter Alias to Followers** : Lister les followers
- [ ] **Twitter Alias to Tweets** : Extraire les tweets récents
- [ ] **Tweet URL to Content** : Analyser un tweet spécifique

### Optimisations
- [ ] Cache pour éviter appels répétés
- [ ] Rate limiting API Twitter
- [ ] Support des comptes suspendus/privés

## Ressources

- [Documentation Maltego TRX](https://docs.maltego.com/support/solutions/articles/15000017605)
- [API Twitter/X](https://developer.twitter.com/en/docs/twitter-api)
- [Règles de validation Twitter](https://help.twitter.com/en/managing-your-account/twitter-username-rules)

## Licence

Script éducatif pour formation OSINT - Usage à des fins légitimes uniquement.

---

**Auteur** : Ali
**Version** : 1.0.0
**Date** : Novembre 2025
