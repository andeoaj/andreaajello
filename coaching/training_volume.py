"""
Training volume tracker.

Computes total volume (sets x reps x load) per muscle group per session
from the athlete's training log, and renders PNG charts.

Assumptions:
- Bodyweight = 75 kg (used only for assisted pull-ups / dips).
- Where reps are given as a range only (e.g. 4x6/9), the midpoint is used.
- Where loads are given as a range (e.g. @10/12), the midpoint is used.
- Unilateral DB work is logged as written (no doubling).
- Strip-set / forzate "extras" are ignored.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

BW = 75.0  # kg, assumed bodyweight for assisted lifts

# --- helpers ----------------------------------------------------------------

def vol(sets_loads_reps):
    """Sum sets x reps x load over a list of (load, reps) tuples."""
    return sum(l * r for l, r in sets_loads_reps)


def assisted(reps_per_set, assistance):
    """Effective load for assisted pull-up / dip given the assistance kg (positive)."""
    return max(0.0, BW - assistance), reps_per_set


# --- data -------------------------------------------------------------------
# Each entry: (date, exercise, muscle_group, volume_kg)
# Volume = sum over working sets of (effective_load * reps).

sessions = []

def add(d: date, exercise: str, muscle: str, sets_):
    sessions.append((d, exercise, muscle, vol(sets_)))


# === MESOCICLO 1 ============================================================

# --- 24/12/25 -- A (Cosce, bicipiti) #1 ---
d = date(2025, 12, 24)
add(d, "Deadlift", "legs", [(60, 6)] * 3)                       # 3 sets of (3 partial + 3 full)
add(d, "DB Lunges", "legs", [(12, 16)] * 3)                     # 2x6kg DBs, 8/side
add(d, "Artis Leg Curl", "legs", [(27.5, 11)] * 3)
add(d, "DB Curl 75°", "biceps", [(10, 8)] * 4)
add(d, "Cable bar curl", "biceps", [(16.25, 12)] * 3)

# --- 7/1/26 -- C #2 ---
d = date(2026, 1, 7)
add(d, "Bench press tecnica", "chest", [(60, 5)] * 2)
add(d, "Bench press", "chest", [(65, 5), (70, 5)])
add(d, "DB incline 30°", "chest", [(15, 9)] * 3)
add(d, "Artis Pectoral machine", "chest", [(32.5, 11), (37.5, 11), (40, 11)])
add(d, "French press DB", "triceps", [(6, 8), (7, 7), (8, 8), (8, 6)])
add(d, "Pushdown sbarra", "triceps", [(15, 12)] * 3)

# --- 13/1/26 -- B #3 ---
d = date(2026, 1, 13)
add(d, "Trazioni alla sbarra", "back",
    [assisted(6, 35), assisted(6, 35), assisted(5, 35), assisted(3, 35)])
add(d, "Pulley triangolo", "back", [(35, 9), (40, 10), (40, 8)])
add(d, "Artis Low Row", "back", [(50, 11), (50, 11), (55, 11)])
add(d, "Shoulder press DB 75°", "shoulders", [(12, 6), (16, 6), (16, 6), (16, 6)])
add(d, "Alzate laterali", "shoulders", [(4, 9)] * 3)
add(d, "Artis Rear Delt Row", "shoulders", [(30, 11), (35, 11), (35, 11)])

# --- 21/1/26 -- C #4 ---
d = date(2026, 1, 21)
add(d, "Bench press tecnica", "chest", [(65, 4), (67.5, 4)])
add(d, "Bench press", "chest", [(70, 4), (72.5, 4), (72.5, 4)])
add(d, "DB incline 30°", "chest", [(18, 9), (18, 9), (20, 6)])
add(d, "Artis Pectoral machine", "chest", [(40, 11), (42.5, 11), (42.5, 11)])
add(d, "French press DB", "triceps", [(9, 8), (10, 8), (10, 7), (10, 5)])
add(d, "Pushdown sbarra", "triceps", [(17.5, 11)] * 3)

# --- 28/1/26 -- A #5 ---
d = date(2026, 1, 28)
add(d, "Deadlift", "legs", [(90, 4)] * 3 + [(90, 5)])           # 3x(2+2) + 1x MAX(5)
add(d, "DB Lunges", "legs", [(22, 16)] * 3)                     # 2x11kg DBs, 8/side
add(d, "Artis Leg Curl", "legs", [(45, 11)] * 3)
add(d, "DB Curl 75°", "biceps", [(13, 7)] * 4)
add(d, "Cable bar curl", "biceps", [(17.5, 11)] * 3)

# --- 29/1/26 -- B #6 ---
d = date(2026, 1, 29)
add(d, "Trazioni alla sbarra", "back",
    [assisted(4, 39), assisted(4, 39),
     assisted(4, 35), assisted(4, 32), assisted(4, 32)])
add(d, "Pulley triangolo", "back", [(40, 9), (45, 9), (50, 8)])
add(d, "Artis Low Row", "back", [(55, 11), (62.5, 11), (65, 11)])
add(d, "Shoulder press DB 75°", "shoulders", [(18, 4), (20, 4), (22, 4), (20, 4)])
add(d, "Alzate laterali", "shoulders", [(5, 9)] * 3)
add(d, "Artis Rear Delt Row", "shoulders", [(37.5, 11), (42.5, 11), (42.5, 11)])

# --- 23/2/26 -- C #7 ---
d = date(2026, 2, 23)
add(d, "Bench press tecnica", "chest", [(65, 3), (70, 3)])
add(d, "Bench press", "chest", [(75, 3), (77.5, 3), (80, 3)])
add(d, "DB incline 30°", "chest", [(20, 9)] * 3)
add(d, "Artis Pectoral machine", "chest", [(42.5, 11), (45, 11), (47.5, 11)])
add(d, "French press DB", "triceps", [(10, 8), (10, 8), (12, 5), (12, 3)])
add(d, "Pushdown sbarra", "triceps", [(20, 11)] * 3)

# --- 20/3/26 -- B (MESO1 MICRO3) ---
d = date(2026, 3, 20)
# Trazioni: tecnica 2x3 @ avg -32.5, then 3x3 @ -25, -20, -20
add(d, "Trazioni alla sbarra", "back",
    [assisted(3, 32.5)] * 2 + [assisted(3, 25), assisted(3, 20), assisted(3, 20)])
add(d, "Vertical Row #2 (presa media)", "back", [(40, 9), (45, 9), (55, 9)])
add(d, "Panatta Rowing Machine", "back", [(20, 11)] * 3)
add(d, "Shoulder press DB 75°", "shoulders",
    [(20, 4), (20, 4), (22, 4), (22, 4)])
add(d, "Alzate laterali", "shoulders", [(5, 9)] * 3)
add(d, "Vertical Row #1 (presa larga)", "back", [(42.5, 11)] * 3)


# === MESOCICLO 2 ============================================================

# --- 27/3/26 -- A (DABLIU) #8 ---
d = date(2026, 3, 27)
add(d, "Deadlift", "legs", [(95, 3)] * 4)                       # 4x2/3 @ 90-100
add(d, "Squat (high bar)", "legs", [(57.5, 5)] * 4)             # 4x4/6 @ 55-60
add(d, "Sterling Hip Thrust", "legs", [(10, 7), (15, 7), (15, 16)])
add(d, "Leg Extension", "legs", [(35, 7.5)] * 3)
add(d, "DB Curl 60°", "biceps", [(14, 5)] * 4)
add(d, "Cable bar curl", "biceps", [(35, 7.5)] * 3)

# --- 2/4/26 -- C (DABLIU #2) ---
d = date(2026, 4, 2)
add(d, "Bench press tecnica", "chest",
    [(60, 4), (60, 4), (70, 4), (76, 4)])
add(d, "Bench inclinata BB", "chest", [(50, 5), (50, 5), (55, 6), (55, 6)])
add(d, "Dips ascensore", "chest",
    [(max(0, BW - 50), 7.5)] * 3)
add(d, "Croci cavi alti", "chest", [(22.5, 7.5)] * 3)
add(d, "French press cavo singolo", "triceps", [(17.5, 6)] * 4)
add(d, "Pushdown corda", "triceps", [(22.5, 7.5)] * 3)

# --- 10/4/26 -- B (lighter / Virgin) ---
d = date(2026, 4, 10)
add(d, "Trazioni alla sbarra", "back",
    [assisted(4, 27.5)] * 5)                                    # 5x3/5 @ avg -27.5
add(d, "Rematore DB", "back",
    [(22, 5), (26, 5), (30, 5), (34, 5)])
add(d, "Pulldown cavo singolo", "back", [(15, 7.5)] * 4)
add(d, "Shoulder press DB 75°", "shoulders",
    [(18, 4), (18, 4), (20, 4), (20, 4), (20, 4)])
add(d, "Alzate frontali p60°", "shoulders", [(6, 7.5)] * 4)
# alzate laterali prono load not reported -> skipped

# --- 10/4/26 (b) -- B (heavier / BLOCCO II MICRO 2) ---
# Same date but clearly a separate, heavier session ("limite" annotations).
# Logged as a second point on the same day.
d = date(2026, 4, 10)
add(d, "Trazioni (heavy)", "back",
    [assisted(4, 30), assisted(4, 25), assisted(3, 15),
     assisted(3, 15), assisted(2, 5)])
add(d, "Rematore DB (heavy)", "back",
    [(30, 5), (34, 5), (34, 5), (34, 5)])
add(d, "Pulldown cavo alto, fermo giu (heavy)", "back",
    [(30, 7), (40, 7), (50, 7), (60, 5)])
add(d, "Spinte manubri 75° SR (heavy)", "shoulders",
    [(18, 4), (20, 6), (20, 5), (20, 5), (20, 5)])
add(d, "Alzate frontali p60°", "shoulders", [(6, 7.5)] * 4)
add(d, "Alzate laterali prono p60°", "shoulders", [(6, 7.5)] * 4)

# --- 28/4/26 -- C (MICRO 2 di BLOCCO I) ---
d = date(2026, 4, 28)
add(d, "Bench press tecnica", "chest",
    [(70, 4), (76, 4), (80, 3), (80, 2)])
add(d, "Bench inclinata BB", "chest", [(60, 5), (60, 6), (60, 4)])
add(d, "Dips ascensore", "chest",
    [(max(0, BW - 50), 7), (max(0, BW - 45), 7), (max(0, BW - 40), 9)])
add(d, "Croci cavi alti", "chest", [(25, 7.5), (27, 7.5)])
add(d, "French press cavo singolo", "triceps", [(16, 6)] * 4)
add(d, "Pushdown corda", "triceps", [(25, 7.5), (25, 7.5), (24.5, 7.5)])

# --- 28/4/26 (b) -- C (MICRO 1 di BLOCCO II #7) ---
d = date(2026, 4, 28)
add(d, "Bench press tecnica (heavy)", "chest",
    [(75, 5), (75, 5), (75, 4), (75, 4)])
add(d, "Bench inclinata BB (heavy)", "chest",
    [(50, 5), (55, 6), (55, 5), (55, 4)])
add(d, "Panca piana DB", "chest", [(20, 6), (20, 8), (20, 10)])
add(d, "Croci cavi alti", "chest", [(25, 8), (28, 8), (28, 8)])
add(d, "Tate press p30°", "triceps", [(10, 7.5)] * 4)           # @8-12 mid 10
add(d, "Pushdown corda", "triceps", [(30, 8.5)] * 3)

# --- 5/5/26 -- A (DABLIU) ---
d = date(2026, 5, 5)
add(d, "Deadlift", "legs",
    [(100, 2.5), (110, 2.5), (110, 2.5), (115, 2.5)])
add(d, "Squat (high bar)", "legs",
    [(70, 5), (70, 5), (70, 5), (75, 5)])
add(d, "Sterling Hip Thrust", "legs",
    [(20, 7.5), (20, 7.5), (25, 17)])
add(d, "Leg Extension", "legs", [(35, 7.5), (40, 7.5), (45, 7.5)])
add(d, "DB Curl 60°", "biceps", [(16, 5)] * 4)
add(d, "Cable bar curl", "biceps", [(35, 7.5), (40, 7.5), (45, 7.5)])


# --- aggregate --------------------------------------------------------------

MUSCLES = ["chest", "back", "shoulders", "legs", "biceps", "triceps"]
LABELS = {
    "chest": "Pettorali",
    "back": "Dorsali",
    "shoulders": "Deltoidi",
    "legs": "Cosce (quad/ham/glutei)",
    "biceps": "Bicipiti",
    "triceps": "Tricipiti",
}
COLORS = {
    "chest": "#d9534f",
    "back": "#5bc0de",
    "shoulders": "#f0ad4e",
    "legs": "#5cb85c",
    "biceps": "#9b59b6",
    "triceps": "#e67e22",
}

# date -> muscle -> volume
from collections import defaultdict
by_session: dict[date, dict[str, float]] = defaultdict(lambda: defaultdict(float))
for d, ex, m, v in sessions:
    by_session[d][m] += v

dates_sorted = sorted(by_session)


# --- charts -----------------------------------------------------------------

OUT = Path(__file__).parent / "charts"
OUT.mkdir(exist_ok=True)


def fmt_date_axis(ax):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    for label in ax.get_xticklabels():
        label.set_rotation(35)
        label.set_ha("right")


# 1) one chart per muscle group ---------------------------------------------
for m in MUSCLES:
    pts = [(d, by_session[d].get(m, 0.0)) for d in dates_sorted if by_session[d].get(m, 0.0) > 0]
    if not pts:
        continue
    xs, ys = zip(*pts)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(xs, ys, marker="o", color=COLORS[m], linewidth=2)
    for x, y in zip(xs, ys):
        ax.annotate(f"{int(y)}", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8, color="#333")
    ax.set_title(f"Volume totale per sessione — {LABELS[m]}", fontsize=13)
    ax.set_ylabel("Volume (kg) = Σ serie × reps × carico")
    ax.set_xlabel("Data sessione")
    ax.grid(True, alpha=0.3)
    fmt_date_axis(ax)
    fig.tight_layout()
    fig.savefig(OUT / f"volume_{m}.png", dpi=130)
    plt.close(fig)


# 2) overview: all muscles on one chart -------------------------------------
fig, ax = plt.subplots(figsize=(11, 6))
for m in MUSCLES:
    pts = [(d, by_session[d].get(m, 0.0)) for d in dates_sorted if by_session[d].get(m, 0.0) > 0]
    if not pts:
        continue
    xs, ys = zip(*pts)
    ax.plot(xs, ys, marker="o", label=LABELS[m], color=COLORS[m], linewidth=1.8)
ax.set_title("Volume totale per sessione — tutti i gruppi muscolari", fontsize=14)
ax.set_ylabel("Volume (kg)")
ax.set_xlabel("Data")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper left", frameon=True)
fmt_date_axis(ax)
fig.tight_layout()
fig.savefig(OUT / "volume_overview.png", dpi=130)
plt.close(fig)


# 3) stacked-bar per session: composition of each workout -------------------
fig, ax = plt.subplots(figsize=(12, 6))
import numpy as np
xs = np.arange(len(dates_sorted))
bottom = np.zeros(len(dates_sorted))
for m in MUSCLES:
    ys = np.array([by_session[d].get(m, 0.0) for d in dates_sorted])
    if ys.sum() == 0:
        continue
    ax.bar(xs, ys, bottom=bottom, label=LABELS[m], color=COLORS[m])
    bottom += ys
ax.set_xticks(xs)
ax.set_xticklabels([d.strftime("%d %b %y") for d in dates_sorted], rotation=40, ha="right")
ax.set_ylabel("Volume (kg)")
ax.set_title("Composizione del volume per sessione", fontsize=14)
ax.legend(loc="upper left")
ax.grid(True, axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "volume_stacked.png", dpi=130)
plt.close(fig)


# 4) bar chart: total volume per muscle group across all sessions ----------
totals = {m: sum(by_session[d].get(m, 0.0) for d in dates_sorted) for m in MUSCLES}
fig, ax = plt.subplots(figsize=(9, 5))
muscles_sorted = sorted(MUSCLES, key=lambda m: -totals[m])
ax.bar([LABELS[m] for m in muscles_sorted],
       [totals[m] for m in muscles_sorted],
       color=[COLORS[m] for m in muscles_sorted])
for i, m in enumerate(muscles_sorted):
    ax.annotate(f"{int(totals[m]):,}", (i, totals[m]),
                textcoords="offset points", xytext=(0, 4),
                ha="center", fontsize=10)
ax.set_ylabel("Volume cumulato (kg)")
ax.set_title("Volume cumulato per gruppo muscolare (intero periodo)",
             fontsize=13)
ax.grid(True, axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "volume_totals.png", dpi=130)
plt.close(fig)


# --- text summary ----------------------------------------------------------
print("=" * 72)
print(f"Sessioni totali analizzate: {len(dates_sorted)}")
print(f"Periodo: {dates_sorted[0]}  →  {dates_sorted[-1]}")
print("=" * 72)
print(f"\n{'Data':12s} | {'Petto':>7s} | {'Dorso':>7s} | {'Spalle':>7s} | "
      f"{'Cosce':>7s} | {'Bici':>7s} | {'Trici':>7s}")
print("-" * 72)
for d in dates_sorted:
    row = by_session[d]
    print(f"{d.strftime('%d/%m/%Y'):12s} | "
          f"{int(row.get('chest',0)):>7d} | "
          f"{int(row.get('back',0)):>7d} | "
          f"{int(row.get('shoulders',0)):>7d} | "
          f"{int(row.get('legs',0)):>7d} | "
          f"{int(row.get('biceps',0)):>7d} | "
          f"{int(row.get('triceps',0)):>7d}")

print("-" * 72)
print("TOTALI")
print(f"{'':12s} | "
      f"{int(totals['chest']):>7d} | "
      f"{int(totals['back']):>7d} | "
      f"{int(totals['shoulders']):>7d} | "
      f"{int(totals['legs']):>7d} | "
      f"{int(totals['biceps']):>7d} | "
      f"{int(totals['triceps']):>7d}")
print()
print(f"Output: {OUT}")
