"""Shared data layer for Modules 2–6.

Every notebook gets the same Step 0 (SETUP_DATA): imports, answer checkers, the sample
district record, and live loaders for NASA POWER (daily rainfall since 1981),
Open-Meteo ERA5 (reanalysis) and Open-Meteo geocoding (place name -> lat/lon).
Live downloads always fall back to the sample district, so every notebook runs offline.
"""
from nbkit import RAW

GEN = r'''
def make_sample_district():
    """Illustrative, synthetic daily rainfall for a South Indian district, 1981-2024."""
    rng = np.random.default_rng(1981)
    days = pd.date_range("1981-01-01", "2024-12-31", freq="D")
    p_wet = np.array([0.03, 0.03, 0.06, 0.15, 0.30, 0.35, 0.42, 0.42, 0.45, 0.45, 0.28, 0.08])
    mu = np.array([4, 4, 7, 11, 13, 8, 8, 9, 13, 14, 12, 6], float)
    years = np.arange(1981, 2025)
    yf = dict(zip(years, np.exp(rng.normal(0, 0.17, len(years)))))
    m = days.month.values - 1
    t = days.year.values - 1981
    yfac = np.array([yf[y] for y in days.year.values])
    p = np.clip(p_wet[m] * (1 - 0.0025 * t) * yfac ** 0.5, 0, 0.95)
    inten = mu[m] * (1 + 0.005 * t) * yfac ** 0.5
    wet = rng.random(len(days)) < p
    amt = rng.gamma(0.7, inten / 0.7)
    rain = np.round(np.where(wet, amt, 0.0), 1)
    for d, v in [("1991-11-14", 142.0), ("2005-10-24", 186.2), ("2017-08-14", 151.4), ("2022-09-05", 168.9)]:
        rain[days.get_loc(pd.Timestamp(d))] = v
    return pd.Series(rain, index=days, name="rain_mm")

def make_messy_record(sample):
    """Three years of the sample record with typical gauge-record problems added."""
    df = sample["2018":"2020"].rename("rain_mm").reset_index()
    df.columns = ["date", "rain_mm"]
    flag_dates = ["2018-02-03", "2018-05-19", "2018-08-07", "2018-11-25", "2019-01-14",
                  "2019-04-02", "2019-09-18", "2019-12-30", "2020-06-06", "2020-10-11"]
    blank_dates = ["2018-07-21", "2019-03-09", "2020-02-17", "2020-08-28"]
    df.loc[df.date.isin(pd.to_datetime(flag_dates)), "rain_mm"] = -999.0
    df.loc[df.date.isin(pd.to_datetime(blank_dates)), "rain_mm"] = np.nan
    df.loc[df.date == "2018-09-12", "rain_mm"] = 999.9      # typing error
    df.loc[df.date == "2020-04-23", "rain_mm"] = -3.0       # impossible negative
    df = df[~df.date.between("2019-07-01", "2019-07-12")]  # 12 days never recorded
    dup = df[df.date.isin(pd.to_datetime(["2018-06-15", "2019-10-03", "2020-11-20"]))]
    df = pd.concat([df, dup]).sort_values("date", kind="stable").reset_index(drop=True)
    df["date"] = df.date.dt.strftime("%Y-%m-%d")
    return df
'''.strip()

SETUP_DATA = r'''
#@title ▶ Step 0 · Get ready (press ▶ once before anything else)
import os, json, warnings
import numpy as np, pandas as pd, requests
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
_orig_bar = plt.Axes.bar
def _bar_int_years(self, x, *a, **k):        # whole-number year ticks on bar charts of years
    out = _orig_bar(self, x, *a, **k)
    try:
        xs = np.asarray(x)
        if xs.dtype.kind in "iu" and xs.min() > 1800: self.xaxis.set_major_locator(MaxNLocator(integer=True))
    except Exception: pass
    return out
plt.Axes.bar = _bar_int_years
from IPython.display import display, Markdown
warnings.filterwarnings("ignore")
plt.rcParams.update({"figure.figsize": (11, 4.5), "figure.dpi": 110, "font.size": 11,
                     "axes.titleweight": "bold", "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, RED, GREY, TEAL, GOLD = "#2C6E9B", "#DD8452", "#C44E52", "#8C8C8C", "#1F7A8C", "#C9962E"
AUTO = os.environ.get("WDL_SELFTEST") == "1"

def ok(msg="Correct!"):  display(Markdown(f"✅ **{msg}**"))
def no(msg="Not quite. Check your working and try again."): display(Markdown(f"❌ {msg}"))
def _num(x):
    try: return float(str(x).replace(",", "").replace("%", "").strip())
    except (TypeError, ValueError): return None
def close(a, b, tol=0.02):
    return a is not None and abs(a - b) <= max(abs(b) * tol, 0.01)
def check_num(ans, exp, tol=0.02, fmt="{:,.1f}", hint=""):
    if AUTO: ans = exp
    v = _num(ans)
    if v is None: no("Type your answer in the box first (numbers only)."); return False
    if close(v, float(exp), tol): ok("Correct: " + fmt.format(exp)); return True
    no("Not quite. " + hint); return False
def check_choice(ans, exp, explain="", hint=""):
    if AUTO: ans = exp
    if ans in ("", "choose"): no("Choose an answer from the dropdown first."); return False
    if ans == exp: ok(("Correct. " + explain).strip()); return True
    no(("Not quite. " + hint).strip()); return False

__GEN__

SAMPLE_URL = "__RAW__/data/sample_district_daily_1981_2024.csv"
try:
    sample = pd.read_csv(SAMPLE_URL, parse_dates=["date"], index_col="date")["rain_mm"]
except Exception:
    sample = make_sample_district()   # works offline too: same numbers

def find_place(name):
    """Place name -> (lat, lon, label) using Open-Meteo geocoding. Prefers places in India."""
    parts = [p.strip() for p in str(name).split(",") if p.strip()]
    r = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                     params={"name": parts[0], "count": 10, "language": "en", "format": "json"}, timeout=20)
    res = r.json().get("results", []) or []
    res = [x for x in res if x.get("country_code") == "IN"] or res
    if len(parts) > 1:
        res = [x for x in res if parts[1].lower() in str(x.get("admin1", "")).lower()] or res
    if not res: raise ValueError(f"No place found for '{name}'")
    x = res[0]
    return x["latitude"], x["longitude"], f'{x["name"]}, {x.get("admin1", "")}'.strip(", ")

def fetch_power(lat, lon, start=1981, end=2024):
    """Daily rainfall (mm/day) from NASA POWER (PRECTOTCORR) for one point."""
    r = requests.get("https://power.larc.nasa.gov/api/temporal/daily/point", timeout=90, params={
        "parameters": "PRECTOTCORR", "community": "AG", "latitude": round(lat, 4), "longitude": round(lon, 4),
        "start": f"{start}0101", "end": f"{end}1231", "format": "JSON"})
    r.raise_for_status()
    d = r.json()["properties"]["parameter"]["PRECTOTCORR"]
    s = pd.Series(d, dtype=float)
    s.index = pd.to_datetime(s.index, format="%Y%m%d")
    s[s < -98] = np.nan
    return s.round(1).rename("rain_mm")

def fetch_era5(lat, lon, start="2021-01-01", end="2021-12-31"):
    """Daily rainfall (mm/day) from the ERA5 reanalysis via Open-Meteo."""
    r = requests.get("https://archive-api.open-meteo.com/v1/archive", timeout=60, params={
        "latitude": lat, "longitude": lon, "start_date": start, "end_date": end,
        "daily": "precipitation_sum", "timezone": "Asia/Kolkata"})
    r.raise_for_status()
    d = r.json()["daily"]
    return pd.Series(d["precipitation_sum"], index=pd.to_datetime(d["time"]), dtype=float).rename("rain_mm")

def load_rain(source, place="", lat=0.0, lon=0.0):
    """Returns (daily rainfall Series, label, lat, lon). Falls back to the sample district."""
    if source.startswith("Sample") or AUTO:
        return sample, "Sample district (synthetic)", None, None
    try:
        if not (lat and lon):
            lat, lon, place = find_place(place)
        cache = f"rain_{lat:.3f}_{lon:.3f}.csv"
        if os.path.exists(cache):
            s = pd.read_csv(cache, parse_dates=["date"], index_col="date")["rain_mm"]
        else:
            s = fetch_power(lat, lon)
            s.rename_axis("date").to_csv(cache)
        return s, f"{place} ({lat:.2f}°N, {lon:.2f}°E) · NASA POWER", lat, lon
    except Exception as e:
        display(Markdown(f"⚠️ Could not download data for **{place or 'your place'}** ({type(e).__name__}). "
                         "Using the sample district instead. Check the place name or type latitude and longitude."))
        return sample, "Sample district (synthetic)", None, None

def annual(s):  return s.groupby(s.index.year).sum(min_count=300)
def monsoon(s):
    m = s[s.index.month.isin([6, 7, 8, 9])]
    return m.groupby(m.index.year).sum(min_count=100)
display(Markdown("✅ **Ready.** Tools loaded. Now run **Step 1** to choose your data."))
'''.strip().replace("__RAW__", RAW).replace("__GEN__", GEN)

def data_cell(default="Sample district (works offline)", place="Mysuru, Karnataka"):
    return f'''
#@title ▶ Step 1 · Choose your data {{ run: "auto" }}
data_source = "{default}" #@param ["Sample district (works offline)", "My place (live download from NASA POWER)"]
place = "{place}" #@param {{type:"string"}}
latitude = 0 #@param {{type:"number"}}
longitude = 0 #@param {{type:"number"}}
rain, label, LAT, LON = load_rain(data_source, place, latitude, longitude)
display(Markdown(f"**Data:** {{label}} · {{rain.index.min():%d %b %Y}} to {{rain.index.max():%d %b %Y}} · "
                 f"{{len(rain):,}} days"))
'''

DATA_NOTE = """
> **About the data.** *Sample district* is an illustrative, synthetic 44-year record (1981–2024) made for practice;
> it is not an official record, and answers in the practice tasks and the Sheet use it.
> *My place* downloads real daily rainfall for any location from **NASA POWER** (satellite and model based, from 1981).
> Type a town or district name, or enter latitude and longitude.
"""


# ---------------- question helpers (used by every module builder) ----------------
def num_q(nb, title, prompt, expr, tol=0.02, fmt="{:,.1f}", hint=""):
    """A numeric question: learner types an answer; `expr` is Python computed in the notebook."""
    nb.md(f"### {title}\n{prompt}")
    nb.code("#@title ▶ Check " + title.split(" ·")[0] + "\n"
            'my_answer = "" #@param {type:"string"}\n'
            f"check_num(my_answer, {expr}, tol={tol}, fmt={fmt!r}, hint={hint!r})")

def choice_q(nb, title, prompt, options, answer, explain="", hint=""):
    """A dropdown question. `answer` is one of `options` (or a Python expression if it starts with '=')."""
    import json
    opts = json.dumps(["choose"] + list(options), ensure_ascii=False)[1:-1]
    exp = answer[1:] if answer.startswith("=") else repr(answer)
    nb.md(f"### {title}\n{prompt}")
    nb.code("#@title ▶ Check " + title.split(" ·")[0] + "\n"
            f'my_answer = "choose" #@param [{opts}]\n'
            f"check_choice(my_answer, {exp}, explain={explain!r}, hint={hint!r})")
