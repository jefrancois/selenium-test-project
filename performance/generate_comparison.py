"""Regenere le graphe de comparaison HTML a partir de l'historique des runs Locust.

Lit performance/reports/history/summary.csv (une ligne par execution) et produit
performance/reports/history/comparison.html : 3 graphes en courbes (temps de
reponse, debit, taux d'erreur) qui superposent toutes les executions passees,
pour comparer facilement un run a 800 utilisateurs avec les runs precedents.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

PERF_DIR = Path(__file__).resolve().parent
HISTORY_DIR = PERF_DIR / "reports" / "history"
SUMMARY_CSV = HISTORY_DIR / "summary.csv"
OUTPUT_HTML = HISTORY_DIR / "comparison.html"


def load_runs() -> list[dict]:
    if not SUMMARY_CSV.exists():
        return []
    with SUMMARY_CSV.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_html(runs: list[dict]) -> str:
    points = []
    for row in runs:
        points.append(
            {
                "run_id": row["run_id"],
                "label": f"{row['timestamp'][5:16].replace('T', ' ')} (u={row['users']})",
                "timestamp": row["timestamp"],
                "users": row["users"],
                "spawn_rate": row["spawn_rate"],
                "duration": row["duration"],
                "avg_response_ms": float(row["avg_response_ms"]),
                "p95_response_ms": float(row["p95_response_ms"]),
                "requests_per_s": float(row["requests_per_s"]),
                "failure_rate_pct": float(row["failure_rate_pct"]),
                "request_count": row["request_count"],
                "failure_count": row["failure_count"],
            }
        )
    data_json = json.dumps(points, ensure_ascii=False)

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Historique des tests de performance</title>
<style>
  :root {{ color-scheme: light; }}
  .viz-root {{
    --surface-1:      #fcfcfb;
    --page-plane:     #f9f9f7;
    --text-primary:   #0b0b0b;
    --text-secondary: #52514e;
    --text-muted:     #898781;
    --grid:           #e1e0d9;
    --baseline:       #c3c2b7;
    --series-1:       #2a78d6; /* avg response time */
    --series-2:       #eb6834; /* p95 response time */
    --series-3:       #1baf7a; /* requests/s */
    --series-8:       #e34948; /* failure rate */
    --border:         rgba(11,11,11,0.10);
  }}
  @media (prefers-color-scheme: dark) {{
    :root:where(:not([data-theme="light"])) .viz-root {{
      color-scheme: dark;
      --surface-1:      #1a1a19;
      --page-plane:     #0d0d0d;
      --text-primary:   #f0efec;
      --text-secondary: #c3c2b7;
      --text-muted:     #898781;
      --grid:           #2c2c2a;
      --baseline:       #383835;
      --series-1:       #3987e5;
      --series-2:       #d95926;
      --series-3:       #199e70;
      --series-8:       #e66767;
      --border:         rgba(255,255,255,0.10);
    }}
  }}
  :root[data-theme="dark"] .viz-root {{
    color-scheme: dark;
    --surface-1:      #1a1a19;
    --page-plane:     #0d0d0d;
    --text-primary:   #f0efec;
    --text-secondary: #c3c2b7;
    --text-muted:     #898781;
    --grid:           #2c2c2a;
    --baseline:       #383835;
    --series-1:       #3987e5;
    --series-2:       #d95926;
    --series-3:       #199e70;
    --series-8:       #e66767;
    --border:         rgba(255,255,255,0.10);
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--page-plane, #f9f9f7);
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    color: var(--text-primary, #0b0b0b);
  }}
  .viz-root {{ max-width: 960px; margin: 0 auto; padding: 24px 16px 48px; }}
  h1 {{ font-size: 20px; margin: 8px 0 4px; }}
  .subtitle {{ color: var(--text-secondary); font-size: 13px; margin: 0 0 28px; }}
  .card {{
    background: var(--surface-1);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 16px 8px;
    margin-bottom: 20px;
  }}
  .card h2 {{ font-size: 14px; margin: 0 0 2px; }}
  .card .unit {{ color: var(--text-muted); font-size: 12px; margin: 0 0 8px; }}
  .legend {{ display: flex; gap: 16px; font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; }}
  .legend span {{ display: inline-flex; align-items: center; gap: 6px; }}
  .swatch {{ width: 10px; height: 10px; border-radius: 3px; display: inline-block; }}
  svg {{ width: 100%; height: auto; display: block; overflow: visible; }}
  .gridline {{ stroke: var(--grid); stroke-width: 1; }}
  .axis-label {{ fill: var(--text-muted); font-size: 10px; }}
  .tooltip {{
    position: absolute;
    pointer-events: none;
    background: var(--surface-1);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 12px;
    color: var(--text-primary);
    box-shadow: 0 2px 10px rgba(0,0,0,0.12);
    opacity: 0;
    transition: opacity 0.08s;
    white-space: nowrap;
    z-index: 10;
  }}
  .chart-wrap {{ position: relative; }}
  details {{ margin-top: 4px; }}
  summary {{ cursor: pointer; font-size: 12px; color: var(--text-secondary); }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 10px; }}
  th, td {{ text-align: right; padding: 4px 8px; border-bottom: 1px solid var(--grid); }}
  th:first-child, td:first-child {{ text-align: left; }}
  th {{ color: var(--text-muted); font-weight: 600; }}
  .empty {{ color: var(--text-secondary); font-size: 13px; }}
</style>
</head>
<body>
<div class="viz-root">
  <h1>Historique des tests de performance (Locust)</h1>
  <p class="subtitle">On Bricole &mdash; pages publiques &mdash; chaque point est une execution complete, superposee pour comparer les paliers.</p>

  <div id="charts">
    <div id="chart-latency"></div>
    <div id="chart-throughput"></div>
    <div id="chart-errors"></div>
  </div>

  <div class="card">
    <details>
      <summary>Voir le detail en tableau</summary>
      <div id="table-wrap"></div>
    </details>
  </div>
</div>

<script>
const RUNS = {data_json};

function fmt(n, d=0) {{
  return Number(n).toLocaleString('fr-FR', {{ minimumFractionDigits: d, maximumFractionDigits: d }});
}}

function renderLineChart(containerId, title, unit, seriesList) {{
  const container = document.getElementById(containerId);
  if (!RUNS.length) {{
    container.innerHTML = '<p class="empty">Pas encore de donnees.</p>';
    return;
  }}
  const W = 900, H = 260, padL = 44, padR = 16, padT = 16, padB = 36;
  const innerW = W - padL - padR, innerH = H - padT - padB;
  const n = RUNS.length;
  const xStep = n > 1 ? innerW / (n - 1) : 0;
  const x = i => padL + i * xStep;

  let allVals = [];
  seriesList.forEach(s => RUNS.forEach(r => allVals.push(r[s.key])));
  let maxV = Math.max(...allVals, 0.0001);
  maxV = maxV * 1.15;
  const y = v => padT + innerH - (v / maxV) * innerH;

  const card = document.createElement('div');
  card.className = 'card';

  const legendHtml = seriesList.length > 1
    ? `<div class="legend">${{seriesList.map(s => `<span><span class="swatch" style="background:${{s.color}}"></span>${{s.name}}</span>`).join('')}}</div>`
    : '';

  const gridLines = [0, 0.25, 0.5, 0.75, 1].map(f => {{
    const yy = padT + innerH * (1 - f);
    const val = maxV * f;
    return `<line class="gridline" x1="${{padL}}" x2="${{W - padR}}" y1="${{yy}}" y2="${{yy}}" />
            <text class="axis-label" x="${{padL - 6}}" y="${{yy + 3}}" text-anchor="end">${{fmt(val, val < 10 ? 1 : 0)}}</text>`;
  }}).join('');

  const xLabels = RUNS.map((r, i) => {{
    if (n > 8 && i % Math.ceil(n / 8) !== 0 && i !== n - 1) return '';
    return `<text class="axis-label" x="${{x(i)}}" y="${{H - 8}}" text-anchor="middle">${{r.label.split(' ')[0]}}</text>`;
  }}).join('');

  const seriesSvg = seriesList.map(s => {{
    const pts = RUNS.map((r, i) => `${{x(i)}},${{y(r[s.key])}}`).join(' ');
    const dots = RUNS.map((r, i) => `<circle class="pt" data-i="${{i}}" cx="${{x(i)}}" cy="${{y(r[s.key])}}" r="4" fill="${{s.color}}" stroke="var(--surface-1)" stroke-width="2" />`).join('');
    return `<polyline points="${{pts}}" fill="none" stroke="${{s.color}}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />${{dots}}`;
  }}).join('');

  const hitAreas = RUNS.map((r, i) => `<rect class="hit" data-i="${{i}}" x="${{x(i) - xStep / 2}}" y="${{padT}}" width="${{xStep || 20}}" height="${{innerH}}" fill="transparent" />`).join('');

  card.innerHTML = `
    <h2>${{title}}</h2>
    <p class="unit">${{unit}}</p>
    ${{legendHtml}}
    <div class="chart-wrap">
      <svg viewBox="0 0 ${{W}} ${{H}}">
        ${{gridLines}}
        <line class="gridline" x1="${{padL}}" x2="${{W - padR}}" y1="${{padT + innerH}}" y2="${{padT + innerH}}" stroke="var(--baseline)" />
        ${{seriesSvg}}
        ${{xLabels}}
        ${{hitAreas}}
      </svg>
      <div class="tooltip"></div>
    </div>`;
  container.appendChild(card);

  const tooltip = card.querySelector('.tooltip');
  card.querySelectorAll('.hit').forEach(hit => {{
    hit.addEventListener('mouseenter', () => {{
      const i = +hit.dataset.i;
      const r = RUNS[i];
      const rows = seriesList.map(s => `${{s.name}}: <b>${{fmt(r[s.key], 1)}}</b>`).join('<br>');
      tooltip.innerHTML = `<b>${{r.label}}</b><br>${{rows}}<br>reqs: ${{r.request_count}} / erreurs: ${{r.failure_count}}`;
      const svg = card.querySelector('svg');
      const rect = svg.getBoundingClientRect();
      const scale = rect.width / W;
      tooltip.style.left = (x(i) * scale) + 'px';
      tooltip.style.top = (y(r[seriesList[0].key]) * scale - 10) + 'px';
      tooltip.style.opacity = '1';
    }});
    hit.addEventListener('mouseleave', () => {{ tooltip.style.opacity = '0'; }});
  }});
}}

renderLineChart('chart-latency', 'Temps de reponse', 'millisecondes', [
  {{ key: 'avg_response_ms', name: 'Moyenne', color: 'var(--series-1)' }},
  {{ key: 'p95_response_ms', name: 'p95', color: 'var(--series-2)' }},
]);
renderLineChart('chart-throughput', 'Debit', 'requetes / seconde', [
  {{ key: 'requests_per_s', name: 'Requetes/s', color: 'var(--series-3)' }},
]);
renderLineChart('chart-errors', 'Taux d\\'erreur', 'pourcentage des requetes en echec', [
  {{ key: 'failure_rate_pct', name: 'Erreurs', color: 'var(--series-8)' }},
]);

const tableWrap = document.getElementById('table-wrap');
if (RUNS.length) {{
  tableWrap.innerHTML = `<table>
    <thead><tr><th>Run</th><th>Utilisateurs</th><th>Duree</th><th>Requetes</th><th>Echecs</th><th>% erreur</th><th>Moy (ms)</th><th>p95 (ms)</th><th>req/s</th></tr></thead>
    <tbody>${{RUNS.map(r => `<tr>
      <td>${{r.label}}</td><td>${{r.users}}</td><td>${{r.duration}}</td><td>${{r.request_count}}</td>
      <td>${{r.failure_count}}</td><td>${{fmt(r.failure_rate_pct,2)}}%</td>
      <td>${{fmt(r.avg_response_ms,0)}}</td><td>${{fmt(r.p95_response_ms,0)}}</td><td>${{fmt(r.requests_per_s,2)}}</td>
    </tr>`).join('')}}</tbody>
  </table>`;
}} else {{
  tableWrap.innerHTML = '<p class="empty">Pas encore de donnees.</p>';
}}
</script>
</body>
</html>
"""


def generate_chart() -> Path:
    runs = load_runs()
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(build_html(runs), encoding="utf-8")
    return OUTPUT_HTML


if __name__ == "__main__":
    out = generate_chart()
    print(f"Graphe regenere : {out}")
