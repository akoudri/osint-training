# Guide Rapide : Maltego Transform (5 minutes)

## 🎯 Configuration en 4 étapes

### Étape 0 : Obtenir les chemins

```bash
./show_maltego_paths.sh
```

Copier les chemins affichés (vous en aurez besoin).

---

### Étape 1 : Ouvrir Maltego

- Lancer **Maltego** (CE ou Classic)
- Menu : **Transforms** → **New Local Transform**

---

### Étape 2 : Remplir les détails

**Transform Details (page 1)** :

| Champ | Valeur |
|-------|--------|
| Transform ID | `TwitterAliasToProfileURL` |
| Description | `Convert Twitter/X alias to profile URL` |
| Transform author | `OSINT Training` |
| Input entity type | `maltego.Phrase` (cliquer sur `...` pour sélectionner) |

Cliquer sur **Next** →

---

### Étape 3 : Configuration de la commande

**Command line (page 2)** :

```
Command:
/home/ali/Training/osint-training/transforms/run_transform.sh

Parameters:
(laisser vide)

Working directory:
/home/ali/Training/osint-training
```

Cliquer sur **Next** → **Finish**

---

### Étape 4 : Tester

1. **Créer un nouveau graphe** : File → New Graph
2. **Ajouter une entité Phrase** :
   - Palette de gauche → Glisser-déposer "Phrase"
   - Double-cliquer → Entrer : `elonmusk`
3. **Exécuter la transform** :
   - Clic droit sur l'entité
   - All Transforms → `TwitterAliasToProfileURL`
4. **Résultat attendu** :
   - Une entité **URL** apparaît : `https://x.com/elonmusk`
   - Lien bleu avec label `@elonmusk`

---

## ✅ Vérification

### Transform réussie si :
- ✅ Entité URL créée
- ✅ URL = `https://x.com/[alias]`
- ✅ Propriétés visibles (twitter.alias, twitter.handle)
- ✅ Notes contiennent 4 URLs OSINT

### En cas d'erreur :
- ❌ Vérifier le panneau **Output** en bas de Maltego
- ❌ Tester en ligne de commande : `./transforms/run_transform.sh "test"`
- ❌ Consulter : `MALTEGO_CONFIG_DIRECT.md`

---

## 🚀 Utilisation

### Cas simple : 1 alias

```
[Phrase: "elonmusk"]
   → Clic droit → TwitterAliasToProfileURL
[URL: https://x.com/elonmusk]
   → Consulter les Notes pour URLs OSINT
```

### Batch : Plusieurs alias

```
[Phrase: "user1"]  [Phrase: "user2"]  [Phrase: "user3"]
   → Sélectionner tout (Ctrl+A)
   → Clic droit → TwitterAliasToProfileURL
[URL 1]  [URL 2]  [URL 3]
```

### Métadonnées OSINT

Pour chaque URL créée, **cliquer sur l'entité** puis consulter :

1. **Propriétés** (panneau de droite) :
   - `twitter.alias` : Alias sans @
   - `twitter.handle` : @alias
   - `url` : URL complète

2. **Notes** (onglet Notes) :
   - 🔍 Recherche tweets : `https://x.com/search?q=from:alias`
   - 💬 Avec réponses : `...+filter:replies`
   - 📸 Média : `https://x.com/alias/media`
   - ❤️ Likes : `https://x.com/alias/likes`

**→ Copier-coller ces URLs dans votre navigateur pour investigation**

---

## 📝 Exemples de validation

| Input | Attendu | Notes |
|-------|---------|-------|
| `elonmusk` | `https://x.com/elonmusk` | ✅ Standard |
| `@snowden` | `https://x.com/snowden` | ✅ @ retiré auto |
| `  test_user  ` | `https://x.com/test_user` | ✅ Espaces retirés |
| `invalid-user` | **Erreur** | ⚠️ Caractère `-` interdit |
| `aaaaaaaaaaaaaaaa` | **Erreur** | ⚠️ > 15 caractères |
| `settings` | **Erreur** | ⚠️ Nom réservé |

---

## 🔧 Dépannage rapide

### "Permission denied"
```bash
chmod +x /home/ali/Training/osint-training/transforms/run_transform.sh
```

### "No module named maltego_trx"
```bash
source .venv/bin/activate
pip install maltego-trx
```

### Aucune entité créée
- Vérifier le panneau **Output** de Maltego
- Tester : `./transforms/run_transform.sh "elonmusk"`

### Chemin invalide dans Maltego
- Utiliser le **chemin absolu complet**
- PAS de `~` ou chemins relatifs
- Afficher avec : `./show_maltego_paths.sh`

---

## 📚 Documentation complète

- **Configuration détaillée** : `MALTEGO_CONFIG_DIRECT.md`
- **Installation serveur** : `MALTEGO_SETUP.md`
- **Technique** : `MALTEGO_TWITTER_TRANSFORM.md`
- **Résumé dev** : `TRANSFORM_SUMMARY.md`

---

**Version** : 1.0 | **Testé sur** : Maltego CE, Linux | **Date** : Nov 2025
