# Guide d'utilisation - Twitter/X Extractor

Ce document décrit le script `twitter_extractor.py` et les corrections qui ont été apportées pour le rendre robuste et fiable.

---

## Vue d'ensemble

Le script `twitter_extractor.py` permet d'extraire des tweets depuis X/Twitter (anciennement Twitter) en utilisant des requêtes de recherche avancées (Twitter Dorking).

### Caractéristiques principales
- **Authentification manuelle** : Contourne les protections anti-bot et CAPTCHA
- **Requêtes avancées** : Support complet de la syntaxe de recherche Twitter
- **Déduplication automatique** : Utilise un `set()` pour éviter les doublons
- **Scrolling progressif** : Charge plus de tweets en descendant dans la page
- **Extraction structurée** : Récupère le texte complet des tweets

---

## Fonctionnement

### 1. Configuration de la requête

Le script utilise des requêtes de recherche Twitter avancées :

```python
REQUETE_BRUTE = "(from:wh1t3h4ts OR to:wh1t3h4ts OR @wh1t3h4ts) -filter:links"
```

**Syntaxe de recherche Twitter :**
- `from:user` : Tweets envoyés par @user
- `to:user` : Tweets en réponse à @user
- `@user` : Tweets mentionnant @user
- `-filter:links` : Exclut les tweets contenant des liens
- `OR` : Opérateur logique
- `&f=live` : Trie par ordre chronologique (live)

### 2. Workflow d'exécution

```
┌─────────────────────────────────┐
│ 1. Initialisation Firefox      │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│ 2. Navigation vers login        │
│    Authentification MANUELLE    │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│ 3. Injection de la recherche    │
│    URL encodée avec requête     │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│ 4. Scroll progressif (5x)       │
│    Extraction des articles      │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│ 5. Affichage des résultats      │
│    Déduplication automatique    │
└─────────────────────────────────┘
```

---

## Corrections apportées

### Problème initial
Le script original utilisait une initialisation basique de Selenium qui échouait sur certaines configurations système.

### Solutions implémentées

#### 1. **Imports ajoutés**
```python
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
```

#### 2. **Initialisation robuste avec gestion d'erreurs**
```python
# Configuration des options Firefox
options = Options()
if HEADLESS:
    options.add_argument("--headless")

# Détection automatique du chemin geckodriver
geckodriver_path = shutil.which("geckodriver")
service = Service(geckodriver_path) if geckodriver_path else None

try:
    if service:
        driver = webdriver.Firefox(service=service, options=options)
    else:
        driver = webdriver.Firefox(options=options)
except Exception as e:
    print(f"❌ ERREUR : Impossible d'initialiser Firefox")
    # ... messages d'aide ...
    return
```

#### 3. **Attentes explicites pour la page de résultats**
**Avant :**
```python
driver.get(URL_SEARCH)
time.sleep(5)
```

**Après :**
```python
driver.get(URL_SEARCH)

wait = WebDriverWait(driver, 10)
try:
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
    print("✅ Page de résultats chargée")
except:
    print("⚠️  Timeout : Vérifiez que vous êtes bien connecté")
    time.sleep(5)  # Fallback
```

#### 4. **Affichage amélioré avec indicateur de progression**
```python
for i in range(SCROLL_COUNT):
    print(f"   Scroll {i+1}/{SCROLL_COUNT}...", end="\r")
    # ... extraction ...
```

#### 5. **Validation des résultats**
```python
if tweets_uniques:
    print("\n📊 Aperçu des tweets collectés (10 premiers) :")
    for idx, tweet in enumerate(list(tweets_uniques)[:10], 1):
        print(f"\n{idx}. {tweet[:150]}...")
else:
    print("⚠️  Aucun tweet trouvé. Vérifiez :")
    # ... diagnostics ...
```

#### 6. **Traceback complet en cas d'erreur**
```python
except Exception as e:
    print(f"⚠️ Erreur critique : {e}")
    import traceback
    traceback.print_exc()
```

---

## Configuration

### Variables personnalisables

```python
# Requête de recherche (syntaxe Twitter)
REQUETE_BRUTE = "(from:wh1t3h4ts OR to:wh1t3h4ts OR @wh1t3h4ts) -filter:links"

# Mode headless (sans interface graphique)
HEADLESS = False  # True pour serveur sans display

# Nombre de scrolls (plus = plus de tweets)
SCROLL_COUNT = 5  # Augmenter pour collecter plus de données
```

### Exemples de requêtes avancées

```python
# Tweets d'un utilisateur contenant un mot-clé
"from:username cybersecurity"

# Tweets dans une période donnée
"cybersecurity since:2024-01-01 until:2024-12-31"

# Tweets avec images uniquement
"from:username filter:images"

# Tweets populaires (min retweets)
"cybersecurity min_retweets:100"

# Combinaison complexe
"(cybersecurity OR infosec) (from:user1 OR from:user2) -filter:replies"
```

---

## Utilisation

### 1. Activation de l'environnement
```bash
source .venv/bin/activate
```

### 2. Lancement du script
```bash
python twitter_extractor.py
```

### 3. Workflow interactif

**Étape A : Authentification manuelle**
```
--- 1. Lancement du Navigateur ---
🌍 Connexion requise...

🛑 ACTION REQUISE :
1. Connectez-vous manuellement dans Firefox.
2. Résolvez les éventuels CAPTCHA ou vérifications de sécurité.
👉 Appuyez sur [ENTRÉE] ici une fois connecté pour lancer la recherche...
```

**Actions à effectuer :**
1. Entrez vos identifiants X/Twitter dans le navigateur qui s'ouvre
2. Résolvez les CAPTCHA si demandés
3. Attendez d'être connecté
4. Revenez au terminal et appuyez sur ENTRÉE

**Étape B : Extraction automatique**
```
🚀 Lancement de la recherche : (from:wh1t3h4ts OR to:wh1t3h4ts OR @wh1t3h4ts) -filter:links
✅ Page de résultats chargée
📜 Récupération des résultats (scroll x5)...
   Scroll 5/5...
✅ TERMINÉ : 42 tweets uniques récupérés.
```

**Étape C : Résultats**
```
📊 Aperçu des tweets collectés (10 premiers) :

1. @wh1t3h4ts | Tweet text here...
2. @user | Reply to @wh1t3h4ts...
...
```

---

## Export des données

### Option 1 : Copier-coller depuis le terminal
Les tweets s'affichent directement dans la console.

### Option 2 : Redirection vers fichier
```bash
python twitter_extractor.py > tweets_output.txt
```

### Option 3 : Modification du script pour export CSV

Ajoutez à la fin de la fonction (avant le `finally`) :

```python
import pandas as pd

if tweets_uniques:
    df = pd.DataFrame({"tweet": list(tweets_uniques)})
    df.to_csv("tweets_extracted.csv", index=False, encoding="utf-8-sig")
    print(f"\n💾 {len(tweets_uniques)} tweets sauvegardés dans 'tweets_extracted.csv'")
```

---

## Résolution des problèmes

### Problème 1 : "Aucun tweet trouvé"

**Causes possibles :**
- Vous n'êtes pas connecté
- La recherche ne retourne aucun résultat
- Les sélecteurs CSS ont changé (Twitter modifie régulièrement son HTML)

**Solutions :**
```bash
# Vérifiez que vous êtes bien connecté
# Testez votre requête directement sur x.com/search
# Augmentez le timeout
```

### Problème 2 : Rate limiting / Blocage

**Symptômes :**
- Message "Vous êtes temporairement limité"
- Page blanche
- Erreur 429

**Solutions :**
```python
# Augmentez les délais entre scrolls
time.sleep(5)  # au lieu de 2

# Réduisez le nombre de scrolls
SCROLL_COUNT = 3
```

### Problème 3 : Sélecteurs CSS invalides

Twitter change régulièrement sa structure HTML. Si le script ne trouve plus les tweets :

**Diagnostic :**
```python
# Testez manuellement dans le navigateur (Console F12)
document.querySelectorAll('article[data-testid="tweet"]')
```

**Solution :**
Modifiez le sélecteur dans le code si nécessaire :
```python
# Si le data-testid a changé
articles = driver.find_elements(By.CSS_SELECTOR, 'article[role="article"]')
```

### Problème 4 : Mode headless ne fonctionne pas

**Solution :**
```bash
# Utilisez Xvfb pour simuler un display
sudo apt install xvfb
xvfb-run python twitter_extractor.py
```

---

## Limitations et considérations éthiques

### Limitations techniques
- Authentification manuelle requise (pas de support API)
- Nombre de tweets limité par le scrolling
- Peut être détecté comme comportement automatisé
- Dépendant de la structure HTML de Twitter

### Considérations légales et éthiques
- ⚠️ **Respectez les conditions d'utilisation de X/Twitter**
- ⚠️ **N'utilisez pas pour du spam ou du harcèlement**
- ⚠️ **Limitez la fréquence des requêtes**
- ⚠️ **Ne collectez pas de données personnelles sensibles**
- ⚠️ **Utilisez uniquement dans un cadre légal (OSINT défensif, recherche, etc.)**

### Bonnes pratiques OSINT
1. Documentez vos sources et méthodologie
2. Ne partagez pas de données personnelles collectées
3. Respectez les délais entre les requêtes
4. Utilisez un compte dédié à l'OSINT
5. Vérifiez toujours l'information collectée

---

## Améliorations possibles

### Export automatique en JSON
```python
import json

tweets_list = [{"id": idx, "content": tweet} for idx, tweet in enumerate(tweets_uniques)]
with open("tweets.json", "w", encoding="utf-8") as f:
    json.dump(tweets_list, f, ensure_ascii=False, indent=2)
```

### Extraction de métadonnées enrichies
```python
# Extraire aussi les dates, likes, retweets
for article in articles:
    texte = article.find_element(By.CSS_SELECTOR, 'div[lang]').text
    date = article.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
    # ...
```

### Scrolling infini jusqu'à épuisement
```python
previous_count = 0
while True:
    # ... extraction ...
    if len(tweets_uniques) == previous_count:
        break  # Plus de nouveaux tweets
    previous_count = len(tweets_uniques)
```

---

## Comparaison avec l'API officielle

| Critère | Script Selenium | API X/Twitter |
|---------|----------------|---------------|
| Coût | Gratuit | Payant (API v2) |
| Limite de tweets | Limité par scrolling | Limites par endpoint |
| Authentification | Manuelle | Token OAuth |
| Fiabilité | Dépend du HTML | Stable |
| Facilité | Installation simple | Configuration OAuth complexe |
| Légalité | Zone grise | Conforme TOS |

**Recommandation :** Pour un usage professionnel à grande échelle, préférez l'API officielle. Pour de l'OSINT ponctuel et de la formation, ce script est adapté.

---

**Date de création :** 2025-11-27
**Version du script :** 2.0 (Corrigé)
**Auteur des corrections :** Claude Code
**Testé sur :** Linux Ubuntu avec Python 3.12, Selenium 4.38.0
