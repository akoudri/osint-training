# Maltego Transform: Twitter/X Alias to Profile URL

## Vue d'ensemble

Cette transform Maltego convertit un alias/username Twitter/X en URL de profil avec validation complète et métadonnées enrichies pour l'OSINT.

## Fonctionnalités

### 1. Validation robuste de l'alias
- **Nettoyage automatique** : Retire le préfixe `@` et les espaces
- **Validation des règles Twitter** :
  - Longueur : 1-15 caractères
  - Caractères autorisés : `a-z`, `A-Z`, `0-9`, `_`
  - Détection des noms réservés (`mentions`, `settings`, `home`, etc.)

### 2. Métadonnées enrichies pour Maltego

L'entité URL créée contient :

| Propriété | Type | Description |
|-----------|------|-------------|
| `url` | strict | URL complète du profil (https://x.com/alias) |
| `short-title` | loose | Titre court pour affichage |
| `title` | loose | Titre complet du profil |
| `twitter.alias` | strict | Alias nettoyé (sans @) |
| `twitter.handle` | strict | Handle complet (avec @) |

### 3. Notes OSINT automatiques

Chaque entité inclut des URLs additionnelles pour investigation :
- Recherche de tous les tweets : `https://x.com/search?q=from:alias`
- Tweets avec réponses : `https://x.com/search?q=from:alias+filter:replies`
- Média : `https://x.com/alias/media`
- Likes : `https://x.com/alias/likes`

### 4. Gestion d'erreurs complète

Types de messages Maltego :
- **FatalError** : Aucun argument fourni
- **PartialError** : Alias invalide mais récupérable
- **Inform** : Alias nettoyé avec succès

## Installation dans Maltego

### Prérequis
```bash
pip install maltego-trx
```

### Configuration manuelle

1. **Copier le script** dans votre répertoire de transforms Maltego
2. **Rendre exécutable** (Linux/Mac) :
   ```bash
   chmod +x twitter_transform.py
   ```

3. **Configuration dans Maltego** :
   - Ouvrir Maltego → Manage Transforms
   - New Local Transform
   - **Command** : `/usr/bin/python3` (ou chemin vers votre Python)
   - **Parameters** : `/path/to/twitter_transform.py`
   - **Input entity type** : `maltego.Phrase` ou `maltego.Alias`
   - **Output entity type** : `maltego.URL`

### Configuration avec maltego-trx (recommandé)

Structure de projet :
```
transforms/
├── twitter_transform.py
└── transform_config.py  # Configuration TRX
```

**transform_config.py** :

```python
from maltego_trx.decorator_registry import TransformRegistry

registry = TransformRegistry(
    owner="OSINT Training",
    author="Ali",
    host_url="http://localhost",
    seed_ids=["osint-training"]
)


@registry.register_transform(
    display_name="Twitter Alias to Profile URL",
    input_entity="maltego.Phrase",
    description="Converts Twitter/X alias to profile URL with OSINT metadata",
    output_entities=["maltego.URL"]
)
def twitter_alias_to_url(request, response):
    from transforms.twitter_transform import validate_twitter_alias

    alias = request.Value
    is_valid, cleaned_alias, error_msg = validate_twitter_alias(alias)

    if not is_valid and not cleaned_alias:
        response.addUIMessage(error_msg, messageType="PartialError")
        return response

    twitter_url = f"https://x.com/{cleaned_alias}"
    entity = response.addEntity("maltego.URL", twitter_url)

    entity.addProperty("url", "URL", "strict", twitter_url)
    entity.addProperty("twitter.alias", "Twitter Alias", "strict", cleaned_alias)
    entity.setLinkLabel(f"@{cleaned_alias}")

    return response
```

Installation :
```bash
python -m maltego_trx.transforms list
python -m maltego_trx.transforms install
```

## Utilisation

### Depuis la ligne de commande (test)

```bash
# Alias simple
python twitter_transform.py "elonmusk"

# Avec préfixe @
python twitter_transform.py "@snowden"

# Alias invalide (sera nettoyé si possible)
python twitter_transform.py "  @user_123  "

# Test d'erreur
python twitter_transform.py "invalid-user!"
```

### Dans Maltego

1. **Créer une entité** de type `Phrase` avec la valeur d'un alias Twitter
2. **Clic droit** → Rechercher votre transform "Twitter Alias to Profile URL"
3. **Exécuter** la transform
4. **Résultat** : Entité URL avec toutes les métadonnées dans le panneau de propriétés

### Cas d'usage OSINT

**Workflow typique** :
```
[Phrase: "elonmusk"]
    → Twitter Alias to Profile URL
    → [URL: https://x.com/elonmusk]
        → ToWebsite (transform Maltego native)
        → [Website Entity]
            → Extraction d'informations...
```

**Investigation approfondie** :
1. Utiliser l'URL de profil générée
2. Consulter les **Notes** de l'entité pour accéder aux URLs OSINT additionnelles
3. Combiner avec d'autres transforms (DNS, WHOIS, etc.)

## Validation et Tests

### Tests unitaires

```python
# test_twitter_transform.py
from transforms.twitter_transform import validate_twitter_alias


def test_valid_alias():
    valid, cleaned, err = validate_twitter_alias("elonmusk")
    assert valid == True
    assert cleaned == "elonmusk"
    assert err == ""


def test_alias_with_at():
    valid, cleaned, err = validate_twitter_alias("@snowden")
    assert valid == True
    assert cleaned == "snowden"


def test_invalid_chars():
    valid, cleaned, err = validate_twitter_alias("user-name!")
    assert valid == False
    assert "caractères invalides" in err


def test_too_long():
    valid, cleaned, err = validate_twitter_alias("a" * 20)
    assert valid == False
    assert "trop long" in err


def test_reserved_name():
    valid, cleaned, err = validate_twitter_alias("settings")
    assert valid == False
    assert "réservé" in err
```

Exécution :
```bash
pytest test_twitter_transform.py -v
```

### Exemples de validation

| Input | Cleaned | Valide | Remarque |
|-------|---------|--------|----------|
| `elonmusk` | `elonmusk` | ✅ | Alias standard |
| `@snowden` | `snowden` | ✅ | Préfixe @ retiré |
| `  user_123  ` | `user_123` | ✅ | Espaces nettoyés |
| `invalid-user` | `invalid-user` | ❌ | Caractère `-` interdit |
| `user@domain` | `user@domain` | ❌ | Caractère `@` au milieu |
| `aaaaaaaaaaaaaaaa` (16 chars) | `aaaaaaa...` | ❌ | > 15 caractères |
| `settings` | `settings` | ❌ | Nom réservé |

## Améliorations futures possibles

1. **Vérification d'existence** : Appel API Twitter pour vérifier si le compte existe
2. **Enrichissement automatique** : Récupération du nom complet, bio, followers
3. **Entités multiples** : Créer aussi des entités Email, Phone si détectées dans la bio
4. **Cache** : Mémoriser les alias déjà vérifiés pour éviter les appels répétés
5. **Rate limiting** : Respecter les limites API Twitter

## Ressources

- [Documentation Maltego TRX](https://docs.maltego.com/support/solutions/articles/15000017605-python-local-transforms)
- [Twitter API](https://developer.twitter.com/en/docs/twitter-api)
- [Règles de validation Twitter](https://help.twitter.com/en/managing-your-account/twitter-username-rules)

## Licence

Script éducatif pour formation OSINT - Usage à des fins légitimes uniquement.
