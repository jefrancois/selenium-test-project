"""Lance un test Locust et archive le resultat dans l'historique des runs.

Chaque execution est sauvegardee dans un dossier horodate sous
performance/reports/history/, une ligne est ajoutee a summary.csv, et le
graphe de comparaison (comparison.html) est regenere pour superposer tous
les runs passes sur le meme graphe.

Usage:
    python run_history.py -u 800 -r 20 -t 10m
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import subprocess
import sys
from pathlib import Path

from generate_comparison import HISTORY_DIR, SUMMARY_CSV, generate_chart

PERF_DIR = Path(__file__).resolve().parent

SUMMARY_FIELDS = [
    "run_id", "timestamp", "users", "spawn_rate", "duration",
    "request_count", "failure_count", "failure_rate_pct",
    "avg_response_ms", "p95_response_ms", "p99_response_ms",
    "requests_per_s",
]


def run_locust(users: int, spawn_rate: float, run_time: str, run_dir: Path) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "locust",
        "-f", str(PERF_DIR / "locustfile.py"),
        "--headless",
        "-u", str(users),
        "-r", str(spawn_rate),
        "-t", run_time,
        "--html", str(run_dir / "report.html"),
        "--csv", str(run_dir / "stats"),
    ]
    result = subprocess.run(cmd, cwd=PERF_DIR)
    stats_csv = run_dir / "stats_stats.csv"
    if result.returncode != 0 and not stats_csv.exists():
        # Locust peut sortir en erreur (ex: crash d'un greenlet interne a la
        # fermeture des fichiers CSV sous Windows) alors que le test a tourne
        # correctement. On ne considere ca comme un echec que si le fichier de
        # stats attendu n'a pas ete produit.
        raise subprocess.CalledProcessError(result.returncode, cmd)
    if result.returncode != 0:
        print(
            f"Avertissement : locust a quitte avec le code {result.returncode}, "
            "mais stats_stats.csv a bien ete produit -> archivage quand meme."
        )


def read_aggregated(stats_csv: Path) -> dict:
    with stats_csv.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["Name"] == "Aggregated":
                return row
    raise RuntimeError(f"Ligne 'Aggregated' introuvable dans {stats_csv}")


def append_summary(run_id: str, users: int, spawn_rate: float, run_time: str, agg: dict) -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    is_new = not SUMMARY_CSV.exists()
    request_count = int(agg["Request Count"])
    failure_count = int(agg["Failure Count"])
    failure_rate = (failure_count / request_count * 100) if request_count else 0.0
    row = {
        "run_id": run_id,
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "users": users,
        "spawn_rate": spawn_rate,
        "duration": run_time,
        "request_count": request_count,
        "failure_count": failure_count,
        "failure_rate_pct": round(failure_rate, 2),
        "avg_response_ms": round(float(agg["Average Response Time"]), 1),
        "p95_response_ms": float(agg["95%"]),
        "p99_response_ms": float(agg["99%"]),
        "requests_per_s": round(float(agg["Requests/s"]), 2),
    }
    with SUMMARY_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-u", "--users", type=int, required=True)
    parser.add_argument("-r", "--spawn-rate", type=float, required=True)
    parser.add_argument("-t", "--run-time", required=True)
    args = parser.parse_args()

    run_id = dt.datetime.now().strftime("%Y%m%d_%H%M%S") + f"_u{args.users}"
    run_dir = HISTORY_DIR / run_id

    print(f"Lancement locust : -u {args.users} -r {args.spawn_rate} -t {args.run_time}")
    run_locust(args.users, args.spawn_rate, args.run_time, run_dir)

    agg = read_aggregated(run_dir / "stats_stats.csv")
    append_summary(run_id, args.users, args.spawn_rate, args.run_time, agg)
    chart_path = generate_chart()

    print(f"Resultats archives dans : {run_dir}")
    print(f"Historique mis a jour  : {SUMMARY_CSV}")
    print(f"Graphe de comparaison  : {chart_path}")


if __name__ == "__main__":
    main()
