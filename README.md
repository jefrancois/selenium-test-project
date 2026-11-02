# Selenium Test Project

Tests UI automatises avec **Python + Selenium + pytest** sur https://lpb-web-psi.vercel.app (On Bricole).

## Bonnes pratiques appliquees
- **Page Object Model par blocs** : `components/` (sections, scopees a leur racine DOM), `pages/` (ecrans, sans assertion), `flows/` (enchainements metier reutilisables, sans locator), `core/` (actions Selenium, decoupees en petites interfaces : `Locating` / `Interacting` / `UrlAware`)
- **Tests par mots-cles** (`tests/keyword_suites/*.json`) au-dessus du POM, pour les scenarios qu'une interface QA non technique pourra composer plus tard — voir [Tests par mots-cles](#tests-par-mots-cles)
- **Donnees attendues separees** : `tests/expectations.py`
- **Tests atomiques** (un comportement par test) + **scenarios** dans `tests/test_flows.py`
- **Attentes explicites** uniquement (pas de `sleep`, pas d'attente implicite)
- **Configuration externalisee** (`.env`, variables d'environnement, options CLI)
- **Isolation a 3 niveaux** : navigateur partage en lecture seule (`public_site`, `worker_site`) ou neuf par test (`fresh_site`) des qu'un test modifie la session
- **Parametrage** des cas similaires, **markers** pour filtrer (`smoke`, `navigation`, `worker`, `flow`, `keyword`)
- **Capture d'ecran** automatique en cas d'echec (`reports/`)
- **Lint** avec ruff, typage, structure `src/` + `tests/`

## Installation
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

## Execution
```powershell
pytest                       # tous les tests (headless)
pytest -m smoke              # smoke uniquement
pytest -m keyword             # uniquement les scenarios par mots-cles
pytest --browser firefox     # autre navigateur
pytest --headed              # avec interface
ruff check .                 # lint
```

## Rapport HTML
Chaque execution genere `reports/report.html` (autonome, captures d'ecran integrees aux echecs).

## Tests par mots-cles

Une couche au-dessus du Page Object Model, pensee pour qu'une future interface QA
puisse composer des scenarios sans ecrire de Python ni connaitre les locators.
Chaque scenario est une liste de `{"keyword": ..., ...parametres}` dans un fichier
JSON sous `tests/keyword_suites/` ; chaque cas devient un test pytest normal (meme
rapport HTML, meme capture d'ecran automatique que les tests Python).

```json
[
  {
    "id": "home_header_link_to_search",
    "description": "Depuis l'accueil, le lien 'Recherche' du header mene a /recherche.",
    "steps": [
      {"keyword": "open_page", "page": "HomePage"},
      {"keyword": "click_header_link", "href": "/recherche"},
      {"keyword": "assert_current_path", "path": "/recherche"}
    ]
  }
]
```

- `${VARIABLE}` dans une valeur est resolu depuis les variables d'environnement
  (donc depuis `.env`) au chargement du fichier : jamais de secret en clair dans
  un scenario versionne (voir `tests/keyword_suites/authentication.json`).
- Mots-cles disponibles : `src/framework/keywords/catalog.py`. Pages ouvrables
  par `open_page` : `src/framework/keywords/pages_registry.py`.
- **Ajouter un mot-cle** : ecrire une fonction `def mon_mot_cle(ctx, **params)` dans
  `catalog.py`, la decorer avec `@keyword("mon_mot_cle")`, et l'implementer en
  appelant uniquement des methodes de page/flow deja existantes (jamais de
  locator ici). Aucune autre modification n'est necessaire.
- Cette couche complete les tests Python, elle ne les remplace pas : les tests
  `tests/test_*.py` restent la reference pour la couverture technique fine.
