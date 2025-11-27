# Guide d'utilisation - Arguments en ligne de commande

## 🎯 Vue d'ensemble

Le script `twitter_network_crawler.py` accepte maintenant des arguments en ligne de commande pour une utilisation flexible sans modification du code.

---

## 📝 Syntaxe de base

```bash
python twitter_network_crawler.py <pseudo> [options]
```

### Argument obligatoire

- **`pseudo`** : Compte Twitter de départ (avec ou sans @)

### Options disponibles

| Option | Alias | Description | Défaut |
|--------|-------|-------------|--------|
| `-d N` | `--depth N` | Profondeur d'exploration (0-3) | 2 |
| `-r N` | `--relations N` | Nombre max de relations par nœud | 10 |
| `-b BROWSER` | `--browser BROWSER` | Navigateur (chrome/firefox) | chrome |
| | `--headless` | Mode sans interface graphique | false |
| | `--no-profile` | Ne pas utiliser le profil existant | false |
| | `--delai-min S` | Délai min entre profils (secondes) | 5 |
| | `--delai-max S` | Délai max entre profils (secondes) | 10 |
| `-h` | `--help` | Afficher l'aide | - |

---

## 📚 Exemples d'utilisation

### 1. Utilisation basique (valeurs par défaut)

```bash
python twitter_network_crawler.py wh1t3h4ts
```

**Équivalent à :**
- Pseudo : `wh1t3h4ts`
- Profondeur : 2
- Relations : 10 par nœud
- Navigateur : Chrome
- Profil existant : Oui

---

### 2. Explorer un niveau uniquement (rapide)

```bash
python twitter_network_crawler.py elonmusk --depth 1
```

**Résultat :**
- Compte initial + 10 relations directes max
- ~11 comptes explorés
- Temps : ~1-2 minutes

---

### 3. Exploration approfondie (3 niveaux)

```bash
python twitter_network_crawler.py alice --depth 3 --relations 15
```

**Résultat :**
- Exploration sur 3 niveaux
- 15 relations max par nœud
- ~100+ comptes explorés
- Temps : ~30-60 minutes

⚠️ **Attention :** Risque de détection plus élevé

---

### 4. Collecte rapide (peu de relations)

```bash
python twitter_network_crawler.py bob --depth 2 --relations 5
```

**Résultat :**
- 2 niveaux
- Seulement 5 relations par nœud
- ~26 comptes max
- Temps : ~5-10 minutes

---

### 5. Mode discret (délais augmentés)

```bash
python twitter_network_crawler.py charlie --delai-min 10 --delai-max 20
```

**Résultat :**
- Délais de 10-20s entre chaque profil
- Réduit le risque de détection
- Temps d'exécution doublé

---

### 6. Utiliser Firefox au lieu de Chrome

```bash
python twitter_network_crawler.py david --browser firefox
```

**Résultat :**
- Firefox au lieu de Chrome
- Utile si Chrome est déjà ouvert
- Moins efficace contre la détection Google

---

### 7. Mode headless (serveur sans display)

```bash
python twitter_network_crawler.py eve --headless
```

**Résultat :**
- Navigateur invisible
- Idéal pour serveurs
- Attention : plus facilement détectable

---

### 8. Sans profil existant (nouveau profil)

```bash
python twitter_network_crawler.py frank --no-profile
```

**Résultat :**
- Nouveau profil vierge
- Pas de cookies/sessions
- Authentification manuelle requise

---

### 9. Combinaison d'options

```bash
python twitter_network_crawler.py alice --depth 3 --relations 8 --delai-min 8 --delai-max 15
```

**Résultat :**
- 3 niveaux de profondeur
- 8 relations max par nœud
- Délais augmentés (8-15s)
- Mode discret mais approfondi

---

## 🔍 Afficher l'aide

```bash
python twitter_network_crawler.py --help
```

**Affiche :**
```
usage: twitter_network_crawler.py [-h] [-d N] [-r N] [-b {chrome,firefox}]
                                   [--headless] [--no-profile]
                                   [--delai-min S] [--delai-max S]
                                   pseudo

Twitter Network Crawler - Analyse de réseaux sociaux pour Maltego

positional arguments:
  pseudo                Compte Twitter de départ (sans @)

optional arguments:
  -h, --help            show this help message and exit
  -d N, --depth N       Profondeur d'exploration (défaut: 2)
  -r N, --relations N   Nombre max de relations par nœud (défaut: 10)
  -b {chrome,firefox}, --browser {chrome,firefox}
                        Navigateur à utiliser (défaut: chrome)
  --headless            Mode sans interface graphique
  --no-profile          Ne pas utiliser le profil existant
  --delai-min S         Délai minimum entre profils en secondes (défaut: 5)
  --delai-max S         Délai maximum entre profils en secondes (défaut: 10)
```

---

## 📊 Estimations par configuration

| Profondeur | Relations | Comptes | Temps estimé | Cas d'usage |
|------------|-----------|---------|--------------|-------------|
| 1 | 5 | ~6 | 1 min | Test rapide |
| 1 | 10 | ~11 | 2 min | Influence directe |
| 2 | 5 | ~26 | 5 min | Communauté compacte |
| 2 | 10 | ~111 | 20 min | **Recommandé** |
| 2 | 15 | ~226 | 40 min | Analyse détaillée |
| 3 | 5 | ~126 | 30 min | Connexions cachées |
| 3 | 10 | ~1111 | 3h+ | ⚠️ Très long |

---

## 🎯 Cas d'usage recommandés

### Analyse rapide d'influence

```bash
python twitter_network_crawler.py target --depth 1 --relations 20
```

**Objectif :** Voir qui mentionne/répond au compte cible

---

### Cartographie de communauté (optimal)

```bash
python twitter_network_crawler.py target --depth 2 --relations 10
```

**Objectif :** Réseau complet avec bon équilibre temps/données

---

### Recherche de connexions cachées

```bash
python twitter_network_crawler.py target --depth 3 --relations 8 --delai-min 10
```

**Objectif :** Connexions indirectes, mode discret

---

### Test rapide avant analyse complète

```bash
python twitter_network_crawler.py target --depth 1 --relations 5
```

**Objectif :** Vérifier que le compte est accessible et actif

---

## ⚙️ Optimisation des performances

### Pour aller plus vite

```bash
--depth 1                    # Moins de niveaux
--relations 5                # Moins de relations
--delai-min 3 --delai-max 5  # Délais réduits (risqué)
```

### Pour être plus discret

```bash
--delai-min 10 --delai-max 20  # Délais augmentés
--relations 5                   # Moins de requêtes
```

### Pour collecter plus de données

```bash
--depth 3                    # Plus de niveaux
--relations 15               # Plus de relations
```

⚠️ **Attention :** Plus = plus de temps + risque de détection

---

## 🐛 Gestion des erreurs

### Argument manquant

```bash
python twitter_network_crawler.py
```

**Erreur :**
```
error: the following arguments are required: pseudo
```

**Solution :** Ajouter le pseudo
```bash
python twitter_network_crawler.py wh1t3h4ts
```

---

### Valeur invalide

```bash
python twitter_network_crawler.py alice --depth abc
```

**Erreur :**
```
error: argument -d/--depth: invalid int value: 'abc'
```

**Solution :** Utiliser un nombre
```bash
python twitter_network_crawler.py alice --depth 2
```

---

### Navigateur invalide

```bash
python twitter_network_crawler.py alice --browser safari
```

**Erreur :**
```
error: argument -b/--browser: invalid choice: 'safari' (choose from 'chrome', 'firefox')
```

**Solution :** Utiliser chrome ou firefox
```bash
python twitter_network_crawler.py alice --browser chrome
```

---

## 📝 Script wrapper (optionnel)

Pour faciliter l'utilisation, vous pouvez créer des alias ou scripts :

### Alias bash

```bash
# Dans ~/.bashrc ou ~/.zshrc
alias twitter-quick='python twitter_network_crawler.py $1 --depth 1 --relations 10'
alias twitter-full='python twitter_network_crawler.py $1 --depth 2 --relations 15'
alias twitter-deep='python twitter_network_crawler.py $1 --depth 3 --relations 10 --delai-min 10'
```

**Usage :**
```bash
twitter-quick elonmusk
twitter-full alice
twitter-deep bob
```

---

## 🔄 Comparaison : Avant / Après

### Avant (modification du code requise)

```python
# Éditer le fichier twitter_network_crawler.py
COMPTE_INITIAL = "alice"
MAX_DEPTH = 3
MAX_RELATIONS_PAR_NOEUD = 15

# Puis exécuter
python twitter_network_crawler.py
```

### Après (arguments CLI)

```bash
# Directement en ligne de commande
python twitter_network_crawler.py alice --depth 3 --relations 15
```

**Avantages :**
- ✅ Plus rapide
- ✅ Pas de modification du code
- ✅ Réutilisable dans des scripts
- ✅ Documentation intégrée (--help)

---

## 📚 Intégration avec d'autres outils

### Boucle bash (analyser plusieurs comptes)

```bash
#!/bin/bash
comptes=("alice" "bob" "charlie")

for compte in "${comptes[@]}"; do
    echo "Analyse de @$compte..."
    python twitter_network_crawler.py "$compte" --depth 2 --relations 10
    sleep 60  # Pause de 1 minute entre chaque
done
```

### Script Python d'automatisation

```python
import subprocess

comptes = ["alice", "bob", "charlie"]

for compte in comptes:
    print(f"Analyse de @{compte}...")
    subprocess.run([
        "python", "twitter_network_crawler.py",
        compte,
        "--depth", "2",
        "--relations", "10"
    ])
```

---

**Date :** 2025-11-27
**Version :** 2.0 (avec support CLI)
