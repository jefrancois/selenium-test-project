# Tests de performance (Locust)

Charge HTTP sur les pages **publiques** de On Bricole (https://lpb-web-psi.vercel.app).
Independant de la suite Selenium : aucune dependance partagee, aucune page objet reutilisee
(Locust parle HTTP directement, pas au navigateur).

## Pourquoi il n'y a pas de "gros" test ici
Le site cible est heberge sur Vercel (facturation a l'usage, protection anti-abus) et semble
etre un projet en developpement, pas une infrastructure dimensionnee pour la charge. Un volume
eleve envoye d'un coup (ex. des dizaines de milliers d'utilisateurs instantanes) se comporte
comme un deni de service, que l'intention soit malveillante ou non :
- il peut faire tomber le site pour de vrais visiteurs,
- generer une facture Vercel significative,
- declencher un blocage anti-abus ou une suspension du compte d'hebergement,
- et ce, sans jamais mesurer une "vraie" limite utile (un pic instantane ne dit rien
  sur la tenue en charge reelle, seulement qu'on a sature le serveur d'un coup).

`locustfile.py` refuse donc de demarrer si `LOCUST_USERS` depasse `MAX_SAFE_USERS` (200 par
defaut). C'est volontaire : augmenter cette limite est un choix a faire explicitement dans le
code, pas une option de ligne de commande qu'on peut pousser par erreur.

## Installation
```powershell
python -m venv .venv-perf
.venv-perf\Scripts\Activate.ps1
pip install -r performance/requirements.txt
```

## Lancer un premier test (recommande)
Un test raisonnable : montee progressive (*ramp-up*), pas un pic instantane.

```powershell
cd performance
locust -f locustfile.py --headless -u 10 -r 1 -t 2m --html reports/report.html --csv reports/stats
```
- `-u 10` : 10 utilisateurs simules au maximum
- `-r 1` : 1 nouvel utilisateur ajoute par seconde (montee progressive sur 10 s)
- `-t 2m` : duree totale du test
- `--html` / `--csv` : rapports generes dans `performance/reports/` (ignore par git)

## Interface web (pilotage manuel, pratique pour explorer)
```powershell
locust -f locustfile.py
```
Puis ouvrir http://localhost:8089, choisir le nombre d'utilisateurs et le taux de montee a
la main, et observer les graphes de latence/erreurs en direct avant d'augmenter.

## Augmenter progressivement
Procede par paliers, en observant `reports/stats_stats.csv` (p95, taux d'erreur) a chaque
etape avant de passer au palier suivant, par exemple 10 -> 50 -> 100 -> 200 utilisateurs,
toujours avec un `-r` qui etale la montee sur au moins quelques dizaines de secondes.

## Dans GitHub Actions
Un job separe du job Selenium (schedule nocturne ou `workflow_dispatch`), avec les memes
bornes de securite. A mettre en place avec le workflow CI quand tu seras pret.
