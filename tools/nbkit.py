"""Shared helpers for building course notebooks (CE541E08-style header)."""
import nbformat as nbf
from course import COURSE, MODULES, sessions

GH_USER, GH_REPO, GH_BRANCH = "PradhanArpan", "waterliteracy", "main"
RAW = f"https://raw.githubusercontent.com/{GH_USER}/{GH_REPO}/{GH_BRANCH}"

# The sample-station generator. Identical code is used by the Sheet builder and
# embedded in every notebook as a fallback, so all numbers match everywhere.
SAMPLE_GEN = '''
def _make_sample_station():
    rng = np.random.default_rng(2023)
    days = pd.date_range("2023-01-01", "2023-12-31", freq="D")
    p_wet  = [0.03, 0.03, 0.08, 0.20, 0.35, 0.40, 0.45, 0.48, 0.55, 0.50, 0.30, 0.08]
    mean_r = [3, 3, 6, 9, 10, 7, 7, 8, 11, 11, 9, 4]
    rain = []
    for d in days:
        m = d.month - 1
        rain.append(rng.gamma(0.8, mean_r[m] / 0.8) if rng.random() < p_wet[m] else 0.0)
    rain = np.round(np.array(rain), 1)
    rain[days.get_loc(pd.Timestamp("2023-09-21"))] = 96.4
    rain[days.get_loc(pd.Timestamp("2023-09-22"))] = 58.2
    level, soil, channel = [], 0.0, 0.0
    for r in rain:
        soil = soil * 0.6 + max(r - 5, 0) * 0.5
        channel = channel * 0.82 + soil * 0.022
        level.append(round(1.8 + channel, 2))
    return pd.DataFrame({"date": days, "rain_mm": rain, "level_m": level})
'''.strip()

SETUP = '''
#@title ▶ Step 0 · Get ready (press ▶ once before anything else)
import numpy as np, pandas as pd
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from IPython.display import display, Markdown
plt.rcParams.update({"figure.figsize": (11, 4.5), "figure.dpi": 110, "font.size": 11,
                     "axes.titleweight": "bold", "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, RED, GREY, TEAL = "#2C6E9B", "#DD8452", "#C44E52", "#8C8C8C", "#1F7A8C"
def ok(msg="Correct!"):  display(Markdown(f"✅ **{msg}**"))
def no(msg="Not quite. Check your working and try again."): display(Markdown(f"❌ {msg}"))
def close(a, b, tol=0.02):  # within 2% (or 0.01 for very small numbers)
    try: return abs(float(a) - float(b)) <= max(abs(float(b)) * tol, 0.01)
    except (TypeError, ValueError): return False

DATA_URL = "__RAW__/data/M1/sample_station_2023.csv"
__GEN__
try:
    station = pd.read_csv(DATA_URL, parse_dates=["date"])
except Exception:
    station = _make_sample_station()   # works offline too: same numbers
station = station.set_index("date")
rainfall, river = station[["rain_mm"]], station[["level_m"]]
WARNING_LEVEL, DANGER_LEVEL = 3.6, 4.2
display(Markdown("✅ **Ready.** Sample station loaded: one year (2023) of daily rainfall and river level. "
                 "*Illustrative, synthetic data for practice; not an official IMD or CWC record.*"))
'''.strip().replace("__RAW__", RAW).replace("__GEN__", SAMPLE_GEN)

SETUP_LIGHT = '''
#@title ▶ Step 0 · Get ready (press ▶ once before anything else)
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
plt.rcParams.update({"figure.figsize": (11, 4.5), "figure.dpi": 110, "font.size": 11,
                     "axes.titleweight": "bold", "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, RED, GREY, TEAL = "#2C6E9B", "#DD8452", "#C44E52", "#8C8C8C", "#1F7A8C"
def ok(msg="Correct!"):  display(Markdown(f"✅ **{msg}**"))
def no(msg="Not quite. Check your working and try again."): display(Markdown(f"❌ {msg}"))
def close(a, b, tol=0.02):
    try: return abs(float(a) - float(b)) <= max(abs(float(b)) * tol, 0.01)
    except (TypeError, ValueError): return False
display(Markdown("✅ **Ready.** Scroll down to begin."))
'''.strip()


class NB:
    def __init__(self, num, kind):
        s = [x for x in sessions() if x["num"] == num][0]
        m = [x for x in MODULES if x["n"] == s["module"]][0]
        self.s, self.m, self.kind = s, m, kind
        self.cells = []
        label = {"reading": "Reading notebook", "practice": "Practice activity", "workshop": "Workshop"}[kind]
        self.fname = f"WDL_M{m['n']}_S{num:02d}_{kind}.ipynb"
        title = s["title"]
        self.md(f"""
# WDL — Module {m['n']} · Session {num} — {title}
### {label}

| | |
|---|---|
| **Course** | {COURSE['title']} |
| **Department** | Civil Engineering · CHRIST (Deemed to be University) |
| **Instructor** | {COURSE['instructor']} |
| **Module** | Module {m['n']} — {m['title']} |
| **Session** | Session {num} of 30 |
| **CO** | {s['co']} |
| **Topics** | {s['topics']} |
| **Water hook** | *{s['hook']}* |

---
> **How to use this notebook.** No coding needed. Read each explanation, then press ▶ on the box below it
> (or click the box and press `Shift + Enter`). Some boxes have sliders, number boxes or dropdowns: change them, then press ▶ again.
> Go to **File → Save a copy in Drive** first, so the notebook is yours.
""")

    def md(self, text):
        self.cells.append(nbf.v4.new_markdown_cell(text.strip()))

    def code(self, src, hidden=True):
        c = nbf.v4.new_code_cell(src.strip())
        if hidden:
            c.metadata["cellView"] = "form"
        self.cells.append(c)

    def save(self, folder):
        nb = nbf.v4.new_notebook()
        nb["cells"] = self.cells
        nb["metadata"] = {"colab": {"provenance": [], "toc_visible": True, "name": self.fname},
                          "kernelspec": {"name": "python3", "display_name": "Python 3"},
                          "language_info": {"name": "python"}}
        path = f"{folder}/{self.fname}"
        nbf.write(nb, path)
        return path
