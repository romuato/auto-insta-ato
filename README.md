# 🤖 Auto Insta A T O — Publication Instagram automatique

Ce projet publie **tout seul 1 à 2 posts par jour** sur l'Instagram de votre
agence **A T O** (création de sites web et logiciels) :
- **texte généré automatiquement** (GPT-4o-mini),
- **image générée automatiquement** (DALL·E 3),
- **rotation de catégories** (conseils, réalisations, preuves, offres, tendances),
- **publication automatique** via l'API officielle Meta — sans risque de bannissement.

> 💶 **Coût** : environ **2 à 3 € / mois** (génération des images OpenAI). Tout le
> reste — hébergement, planification — est **gratuit**.

---

## 🗺️ Vue d'ensemble (comment ça marche)

```
  ┌─────────────┐   chaque jour    ┌──────────────┐   ┌───────────────┐
  │ GitHub       │ ───────────────▶ │ generate.py  │──▶│ image + texte │
  │ Actions      │   (gratuit)      │ (OpenAI)     │   └───────┬───────┘
  │ (planning)   │                  └──────────────┘           │
  └─────────────┘                                              ▼
                                                       ┌───────────────┐
                                                       │ publish.py     │
                                                       │ API Instagram  │──▶ 📸 votre compte
                                                       └───────────────┘
```

---

## ✅ Ce que VOUS devez faire une seule fois (≈ 30-40 min)

Vous n'avez **pas besoin de savoir coder**. Suivez les 5 parties dans l'ordre.
Quand un mot technique apparaît, demandez-moi simplement « explique-moi l'étape X ».

### Partie 1 — Préparer le compte Instagram (5 min)

1. Ouvrez l'app Instagram → **Paramètres** → **Type de compte et outils** →
   **Passer à un compte professionnel** → choisissez **Entreprise**.
2. Gardez l'app ouverte, on relie Facebook juste après.

### Partie 2 — Compte Facebook (uniquement pour le portail développeur)

> **Aucune Page Facebook n'est nécessaire** : on utilise la nouvelle API
> « Instagram avec connexion Instagram » (2024+). Un simple compte Facebook
> (jamais visible publiquement) suffit pour ouvrir le portail développeur Meta.

### Partie 3 — Obtenir le jeton d'accès Instagram (10 min)

1. Allez sur https://developers.facebook.com/ et connectez-vous avec le compte
   Facebook → acceptez de devenir « développeur » si demandé.
2. **Mes apps** → **Créer une app** → cas d'usage : **« Gérer tout sur Instagram »**
   (ou type *Entreprise* puis produit **Instagram**).
3. Dans le tableau de bord de l'app : produit **Instagram** →
   **« Configuration de l'API avec connexion Instagram »**.
4. Section **« Générer des tokens d'accès »** → **Ajouter un compte** → connectez le
   compte Instagram professionnel → cliquez **« Générer un token »**.
5. Copiez : le **token longue durée** (60 jours) = `IG_ACCESS_TOKEN`, et
   l'**identifiant du compte Instagram** affiché à côté = `IG_USER_ID`.

> 😅 **Dites-moi quand vous y êtes** et je vous guide écran par écran.

### Partie 4 — Obtenir la clé OpenAI (5 min)

1. Créez un compte sur https://platform.openai.com/
2. **Settings → Billing** : ajoutez ~5 € de crédit (ça dure des mois).
3. **API keys → Create new secret key** : copiez la clé (commence par `sk-...`).

### Partie 5 — Mettre en route l'automatisation (10 min)

**Option recommandée : le CLOUD (gratuit, marche PC éteint)**

1. Créez un compte gratuit sur https://github.com/
2. Créez un dépôt **privé** (ex. `auto-insta-ato`) et envoyez-y le contenu de ce
   dossier. *(Je peux vous générer les commandes exactes.)*
3. Dans le dépôt → **Settings → Secrets and variables → Actions → New repository secret**,
   ajoutez ces 3 secrets :
   - `OPENAI_API_KEY`
   - `IG_USER_ID`
   - `IG_ACCESS_TOKEN`
4. Onglet **Actions** → activez les workflows. C'est fini : ça postera matin et soir.
   Vous pouvez tester tout de suite avec **Run workflow** (bouton manuel).

---

## 🧪 Tester sur votre PC d'abord (conseillé)

```powershell
# 1. Installer Python 3.11+ depuis https://www.python.org/ (cochez "Add to PATH")
# 2. Dans ce dossier :
pip install -r requirements.txt

# 3. Copier la config et la remplir
copy .env.example .env
notepad .env        # collez vos clés

# 4. Test SANS publier (vérifie texte + image) :
#    mettez DRY_RUN=1 dans .env, puis :
python main.py
```

L'image générée apparaît dans le dossier `output/`. Quand le résultat vous plaît,
retirez `DRY_RUN` et relancez pour publier pour de vrai.

---

## ⚙️ Personnaliser le contenu

Tout se règle dans **`content_plan.py`** :
- `MARQUE` : nom, activité, ton, hashtags, appel à l'action.
- `CATEGORIES` : ajoutez/retirez des thèmes, changez les « poids » (fréquence).

Pour changer les **heures** de publication : éditez les lignes `cron` dans
`.github/workflows/daily-post.yml` (heures en UTC, France = UTC+2 l'été).

---

## ❓ Questions fréquentes

- **Le jeton expire au bout de 60 jours.** Il faudra le régénérer. Je peux ajouter
  un rafraîchissement automatique plus tard si vous voulez.
- **Puis-je valider avant publication ?** Oui : laissez `DRY_RUN=1`, le post est
  préparé mais pas publié. Dites-moi si vous voulez une validation par e-mail/Telegram.
- **Et sans GitHub, juste mon PC ?** Possible avec le Planificateur de tâches Windows
  + un compte Cloudinary gratuit (pour héberger l'image). Demandez-moi le guide.

---

Besoin d'aide sur une étape ? Ouvrez Claude Code dans ce dossier et écrivez par ex.
« guide-moi pour la Partie 3 ».
