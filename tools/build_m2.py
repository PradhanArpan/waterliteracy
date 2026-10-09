"""Module 2 · Finding and Trusting Water Data (Sessions 6–10)."""
import os
from nbkit import NB, RAW
from datakit import SETUP_DATA, data_cell, DATA_NOTE, num_q, choice_q

OUT = "notebooks/M2"
os.makedirs(OUT, exist_ok=True)
built = []

MESSY = """
#@title ▶ Load the messy gauge record
MESSY_URL = "__RAW__/data/M2/messy_gauge_record_2018_2020.csv"
try:
    messy = pd.read_csv(MESSY_URL)
except Exception:
    messy = make_messy_record(sample)
display(Markdown(f"Loaded **{len(messy):,} rows**: one row per day (supposedly), 2018 to 2020."))
display(messy.head(8))
""".replace("__RAW__", RAW)

ILLUS = '''
def illustrative_three_sources(year=2021):
    """Illustrative only: a gauge record and how a grid cell and a satellite might see the same rain."""
    g = sample[str(year)].copy()
    rng = np.random.default_rng(7)
    grid = (0.55 * g + 0.45 * g.rolling(3, center=True, min_periods=1).mean() * 0.97).round(1)
    sat = g.rolling(2, min_periods=1).mean() * 1.03
    sat[(g > 0) & (g < 3) & (rng.random(len(g)) < 0.5)] = 0.0       # misses some light rain
    sat = (sat + np.where(rng.random(len(g)) < 0.03, rng.gamma(1, 3, len(g)), 0)).round(1)  # some false rain
    return pd.DataFrame({"Rain gauge (point)": g, "Gridded (area average)": grid, "Satellite estimate": sat})
three = illustrative_three_sources(2021)
'''

# =====================================================================
# SESSION 6 · India's water data ecosystem
# =====================================================================
nb = NB(6, "reading")
nb.md("""
## Why this session matters
In Module 1 you read a sample station. Real work starts with a harder question: **where do water numbers come from,
and which one should I use?** India has several agencies and global datasets measuring the same rain and rivers in
different ways. This session is your map of them.
""")
nb.code(SETUP_DATA)
nb.md("""
---
## Part 1 · Who measures India's water?

| Source | What it gives | How | Typical detail | Where to find it |
|---|---|---|---|---|
| **IMD** (India Meteorological Department) | Daily rainfall at stations; district and state totals; gridded rainfall | Rain gauges, weather stations, radar | Daily; gridded 0.25° (about 27 km) back to 1901 | IMD Pune data portal; district rainfall pages |
| **State networks** (e.g. Karnataka's KSNDMC) | Rainfall at thousands of automatic gauges | Telemetric rain gauges | Every 15 minutes to daily; village/hobli level | State disaster or water department websites |
| **CWC** (Central Water Commission) | River levels, flood forecasts, reservoir storage bulletins | River gauge stations, dam reports | Hourly to daily levels; weekly reservoir bulletin | CWC flood forecasting site; India-WRIS |
| **India-WRIS** | One portal bringing many water datasets together | Compiles agency data | Varies by dataset | indiawris.gov.in |
| **CGWB** (Central Ground Water Board) | Groundwater levels in observation wells | Manual and automatic well readings | A few times a year | India-WRIS; CGWB reports |
| **NASA GPM (IMERG)** | Satellite rainfall estimates for the whole globe | Satellites measuring rain from space | Every 30 minutes; 0.1° (about 11 km); from 2000 | NASA GES DISC |
| **NASA POWER** | Daily rainfall and weather for any point | Satellite and model products, combined | Daily; about 0.5° (about 55 km); from 1981 | power.larc.nasa.gov |
| **ERA5** (European reanalysis) | A consistent "best estimate" of past weather everywhere | A weather model fed with millions of observations | Hourly; 0.25°; from 1940 | Copernicus; Open-Meteo |

The first five are **Indian agencies**: closest to the ground, often the official numbers. The last three are **global
datasets**: available everywhere, easy to download, but estimated rather than measured at a single point.
""")
nb.md("""
---
## Part 2 · Which dataset for which question?
Choose a question and press ▶ to see where you would look first, and why.
""")
nb.code('''
#@title ▶ Dataset finder { run: "auto" }
question = "Was last monsoon normal in my district?" #@param ["Was last monsoon normal in my district?", "How much did it rain in my village yesterday?", "Is a river near me about to flood?", "How full are the big reservoirs this week?", "What was rainfall like in 1920?", "I need daily rainfall for a remote place with no gauge, from 1981", "How heavy was the rain over the sea during a cyclone?", "Are wells in my district going dry?"]
A = {
 "Was last monsoon normal in my district?": ("IMD district rainfall", "IMD publishes district totals and their departure from normal every season. It is the official answer."),
 "How much did it rain in my village yesterday?": ("State telemetric network (e.g. KSNDMC)", "State networks have far more gauges than IMD, often one per hobli or panchayat."),
 "Is a river near me about to flood?": ("CWC flood forecasts", "CWC issues level forecasts at gauge stations on major rivers during the monsoon."),
 "How full are the big reservoirs this week?": ("CWC weekly reservoir bulletin / India-WRIS", "CWC reports live storage of major reservoirs every week."),
 "What was rainfall like in 1920?": ("IMD gridded rainfall (from 1901)", "Only IMD's long gauge-based record goes back that far for India."),
 "I need daily rainfall for a remote place with no gauge, from 1981": ("NASA POWER", "It gives a daily value for any point on Earth from 1981, free and without an account."),
 "How heavy was the rain over the sea during a cyclone?": ("NASA GPM (IMERG)", "Satellites see rain where there are no gauges at all, including over the ocean."),
 "Are wells in my district going dry?": ("CGWB observation wells", "CGWB measures water levels in wells several times a year."),
}
src, why = A[question]
display(Markdown(f"### Look first at: **{src}**\\n{why}"))
''')
nb.md("""
---
## Part 3 · Detail in space and in time
Every dataset makes a trade-off: fine detail, long history, or wide coverage. Rarely all three. Press ▶.
""")
nb.code('''
#@title ▶ Plot the trade-off
D = [("IMD gridded", 1901, 27, BLUE), ("ERA5", 1940, 27, GREY), ("NASA POWER", 1981, 55, ORANGE),
     ("NASA GPM IMERG", 2000, 11, TEAL), ("State telemetric gauges", 2010, 3, RED), ("IMD stations", 1875, 1, "black")]
fig, ax = plt.subplots(figsize=(10, 5))
for name, start, km, c in D:
    ax.hlines(km, start, 2024, color=c, lw=6, alpha=0.8)
    ax.text(start, km * 1.15, name, color=c, fontsize=10, fontweight="bold")
ax.set_yscale("log"); ax.set_yticks([1, 3, 10, 30, 100]); ax.set_yticklabels(["1 km\\n(a point)", "3 km", "10 km", "30 km", "100 km"])
ax.set_xlim(1860, 2030); ax.set_ylim(0.6, 150)
ax.set_xlabel("Years covered"); ax.set_ylabel("Size of one value (spacing)")
ax.set_title("Long records are coarse; fine detail is recent")
ax.text(0, -0.17, "Approximate. State network start dates vary; IMD stations: some records begin in the 1800s.", transform=ax.transAxes, fontsize=9, color=GREY)
plt.tight_layout(); plt.show()
''')
nb.md("""
A "point" record from a single gauge is the most direct measurement, but it describes only the spot around that gauge.
A 27 km grid cell describes an **average** over an area about the size of a small taluk.
""")
nb.md("""
---
## Part 4 · Read the label before you use the data
Every dataset comes with **metadata**: information about the data. Check these eight things before you trust any number:

| Check | Why it matters |
|---|---|
| **Variable** | "Precipitation" may include snow; "rainfall" may not |
| **Unit** | mm per day, mm per hour, or a total for the month? |
| **Day definition** | IMD's day ends at 8:30 am IST; many global datasets use midnight UTC (5:30 am IST) |
| **Spatial detail** | A point, a district average, or a grid cell? |
| **Period** | Which years? Are any missing? |
| **Missing-value flag** | Often −999 or blank. Never add these up! |
| **Version** | Datasets are reprocessed; numbers can change between versions |
| **Licence and citation** | Who may use it, and how to credit it |

### ⏭️ Next
Open the **Practice activity** to match questions to datasets.
""")
built.append(nb.save(OUT))

nb = NB(6, "practice")
nb.md("Choose the best first dataset for each question, then check. The Reading notebook's table will help.")
nb.code(SETUP_DATA)
DS = ["IMD district rainfall", "State telemetric network", "CWC flood forecasts", "CWC reservoir bulletin",
      "IMD gridded rainfall", "NASA POWER", "NASA GPM IMERG", "CGWB observation wells"]
QS6 = [
    ("Q1", "A newspaper wants to know whether your district's monsoon was deficient this year.", "IMD district rainfall"),
    ("Q2", "A panchayat wants yesterday's rainfall for its own village.", "State telemetric network"),
    ("Q3", "A school by the river wants to know if the river will cross the danger level tomorrow.", "CWC flood forecasts"),
    ("Q4", "A farmer group wants to know whether the reservoir upstream is fuller than last year, this week.", "CWC reservoir bulletin"),
    ("Q5", "A historian wants to compare rainfall in the 1918 drought with today.", "IMD gridded rainfall"),
    ("Q6", "A researcher needs daily rainfall since 1981 for a hill village with no gauge, downloaded in minutes.", "NASA POWER"),
    ("Q7", "A borewell owner wants to know if groundwater in the district has been falling.", "CGWB observation wells"),
]
for q, text, ans in QS6:
    choice_q(nb, f"{q} · Which dataset first?", text, DS, ans)
choice_q(nb, "Q8 · Day definitions",
         "IMD's daily rainfall for 5 July covers 8:30 am on 4 July to 8:30 am on 5 July (IST). A global dataset's 5 July covers "
         "midnight to midnight UTC. Which metadata item tells you to be careful when comparing them day by day?",
         ["Unit", "Day definition", "Licence", "Missing-value flag"], "Day definition",
         "The two 'days' are shifted by several hours, so one heavy shower can land on different dates.")
built.append(nb.save(OUT))

# =====================================================================
# SESSION 7 · Stations, grids and satellites
# =====================================================================
nb = NB(7, "reading")
nb.md("""
## Why this session matters
The same storm can be reported as 80 mm by a gauge, 55 mm by a grid cell and 65 mm by a satellite, and none of them is
"wrong". They measure different things. This session shows why, so you can choose and explain your source.
""")
nb.code(SETUP_DATA)
nb.code(ILLUS)
nb.md("""
---
## Part 1 · A point, an area, a view from space
- A **rain gauge** catches rain in a funnel about 20 cm wide. It is the most direct measurement, but only for that spot.
- A **gridded** dataset combines many gauges into an **average** for each square of a grid (for IMD, about 27 km × 27 km).
  Averaging smooths out the heaviest local bursts.
- A **satellite** estimate infers rain from clouds and microwaves seen from space. It covers everywhere, including oceans
  and forests, but it can miss light rain and sometimes reports rain that never reached the ground.
- A **reanalysis** (like ERA5) uses a weather model guided by observations to fill the whole globe consistently.
""")
nb.md("""
---
## Part 2 · Same year, three records (illustrative)
Below, one year of a gauge record, and how a grid cell and a satellite *might* see the same rain.
*These three series are illustrative, built from the sample district to show typical differences.*
""")
nb.code('''
#@title ▶ Compare the three records { run: "auto" }
view = "Running total through the year" #@param ["Running total through the year", "Daily values in the wettest month", "Summary table"]
if view == "Running total through the year":
    ax = three.cumsum().plot(color=[BLUE, ORANGE, TEAL], lw=2)
    ax.set_ylabel("Running total (mm)"); ax.set_title("Same rain, three records: running total through 2021")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b")); plt.tight_layout(); plt.show()
elif view == "Daily values in the wettest month":
    m = three["Rain gauge (point)"].resample("MS").sum().idxmax()
    sub = three[m:m + pd.offsets.MonthEnd(0)]
    ax = sub.plot(kind="bar", color=[BLUE, ORANGE, TEAL], width=0.85, figsize=(12, 4.5))
    ax.set_xticklabels([d.strftime("%d") for d in sub.index], rotation=0); ax.set_ylabel("mm/day")
    ax.set_title(f"Daily rainfall in {m:%B %Y}: the grid smooths peaks, the satellite smears and misses")
    plt.tight_layout(); plt.show()
else:
    t = pd.DataFrame({"Year total (mm)": three.sum().round(0), "Wettest day (mm)": three.max().round(1),
                      "Rainy days (≥2.5 mm)": (three >= 2.5).sum()})
    display(t)
''')
nb.md("""
### What to notice
- **Totals are similar; peaks are not.** Averaging and smoothing lower the wettest day.
- The satellite **misses some light rain** and **adds some false rain**, so its rainy-day count differs.
- For floods (peaks), a nearby gauge is best. For water balance (totals over a basin), grids are excellent.
""")
nb.md("""
---
## Part 3 · Two real global datasets for your place
If you chose **My place** in Step 1, press ▶ to download the same year from two real datasets:
**NASA POWER** and **ERA5**. If you are using the sample district, this cell explains how to try it.
""")
nb.code(data_cell())
nb.code('''
#@title ▶ NASA POWER vs ERA5 for one year { run: "auto" }
year = 2021 #@param {type:"slider", min:1981, max:2024, step:1}
if LAT is None:
    display(Markdown("ℹ️ You are using the sample district. In **Step 1**, choose *My place*, type a town or district, and run this cell again."))
else:
    try:
        p = rain[str(year)]
        e = fetch_era5(LAT, LON, f"{year}-01-01", f"{year}-12-31")
        both = pd.DataFrame({"NASA POWER": p, "ERA5": e}).dropna()
        ax = both.cumsum().plot(color=[ORANGE, GREY], lw=2)
        ax.set_ylabel("Running total (mm)"); ax.set_title(f"{label.split(' · ')[0]}: running total in {year}")
        plt.tight_layout(); plt.show()
        display(pd.DataFrame({"Year total (mm)": both.sum().round(0), "Wettest day (mm)": both.max().round(1),
                              "Rainy days (≥2.5 mm)": (both >= 2.5).sum()}))
    except Exception as ex:
        display(Markdown(f"⚠️ ERA5 download failed ({type(ex).__name__}). Try again in a minute."))
''')
nb.md("""
---
## Part 4 · Choosing a source

| If you need… | Prefer | Because |
|---|---|---|
| The official seasonal verdict for a district | IMD district rainfall | It is the reference others will quote |
| The peak of a local storm | The nearest gauge (state or IMD) | Grids and satellites smooth peaks |
| A long, gap-free series anywhere | IMD gridded, NASA POWER or ERA5 | No missing days, consistent method |
| Rain over sea, forest or a border area | Satellite (GPM) | Gauges are rare or absent |

Whatever you choose, **say which source you used**. Your capstone dashboard will carry a source note.

### ⏭️ Next
Open the **Practice activity** and compare the three records yourself.
""")
built.append(nb.save(OUT))

nb = NB(7, "practice")
nb.md("Use the illustrative three-record table to answer. Press ▶ on the table first.")
nb.code(SETUP_DATA)
nb.code(ILLUS)
nb.code('''
#@title ▶ The three records, 2021 (illustrative)
t = pd.DataFrame({"Year total (mm)": three.sum().round(1), "Wettest day (mm)": three.max().round(1),
                  "Rainy days (≥2.5 mm)": (three >= 2.5).sum()})
display(t)
''')
num_q(nb, "Q1 · Gauge total", "What is the 2021 year total for the **rain gauge** (mm)?", 'three["Rain gauge (point)"].sum()', 0.01, hint="Read the first row of the table.")
num_q(nb, "Q2 · Satellite vs gauge", "By what percentage does the **satellite** year total differ from the **gauge** total? "
      "Use (satellite − gauge) ÷ gauge × 100. Give a negative number if the satellite is lower.",
      '(three["Satellite estimate"].sum() - three["Rain gauge (point)"].sum()) / three["Rain gauge (point)"].sum() * 100',
      0.05, "{:+.1f}%", "Subtract, divide by the gauge total, multiply by 100.")
choice_q(nb, "Q3 · Highest peak", "Which record has the **highest wettest day**?",
         ["Rain gauge (point)", "Gridded (area average)", "Satellite estimate"], '=three.max().idxmax()',
         "A point gauge catches local bursts that averaging smooths out.")
num_q(nb, "Q4 · Peak lost by averaging", "How many mm lower is the **gridded** wettest day than the **gauge** wettest day?",
      'three["Rain gauge (point)"].max() - three["Gridded (area average)"].max()', 0.02, hint="Subtract the two values in the 'Wettest day' column.")
choice_q(nb, "Q5 · Why do grids lower peaks?", "Why does a gridded dataset usually show a smaller wettest day than a single gauge?",
         ["Grids use older instruments", "A grid value is an average over a large area", "Grids only record every other day", "Gauges overestimate rain"],
         "A grid value is an average over a large area", "Heavy rain rarely covers a whole 27 km square evenly, so the average is lower than the peak at one spot.")
choice_q(nb, "Q6 · Pick a source", "You want the rain over the Bay of Bengal during a cyclone. Which source?",
         ["Rain gauge", "IMD gridded rainfall", "Satellite estimate"], "Satellite estimate", "There are no gauges at sea.")
built.append(nb.save(OUT))

# =====================================================================
# SESSION 8 · Downloading a rainfall dataset
# =====================================================================
nb = NB(8, "reading")
nb.md("""
## Why this session matters
From now on you can work with **your own place**. This session downloads decades of daily rainfall for any town or
district in India, shows you how to describe it properly, and saves it as a file you can open in a spreadsheet.
""")
nb.code(SETUP_DATA)
nb.md("---\n## Part 1 · Download your place\nChoose **My place**, type your town or district (for example *Tumakuru, Karnataka*), and press ▶." + DATA_NOTE)
nb.code(data_cell("My place (live download from NASA POWER)", "Mysuru, Karnataka"))
nb.md("""
The download takes a few seconds. Behind the scenes the notebook (1) finds your place's latitude and longitude,
(2) asks NASA POWER for daily rainfall from 1981 to 2024, and (3) keeps a copy so the next run is instant.
""")
nb.md("---\n## Part 2 · Look before you use\nPress ▶ to see the first rows and a summary.")
nb.code('''
#@title ▶ First look
display(rain.head(7).to_frame().T)
d = rain.describe()
display(Markdown(f"""
| Summary | Value |
|---|---|
| Days in the record | {int(d['count']):,} |
| Missing days | {int(rain.isna().sum()):,} |
| Average daily rainfall | {d['mean']:.2f} mm |
| Wettest day | {d['max']:.1f} mm on {rain.idxmax():%d %b %Y} |
| Days with no rain (0 mm) | {(rain == 0).sum():,} ({(rain == 0).mean()*100:.0f}% of days) |
"""))
''')
nb.md("""
---
## Part 3 · Write the data card
Good practice: describe any dataset in a short **data card** before analysing it. Press ▶.
""")
nb.code('''
#@title ▶ My data card
is_live = LAT is not None
display(Markdown(f"""
| Item | Value |
|---|---|
| Place | {label.split(' · ')[0]} |
| Source | {"NASA POWER, daily, parameter PRECTOTCORR (bias-corrected precipitation)" if is_live else "Sample district (synthetic, for practice)"} |
| Unit | mm per day |
| Spatial detail | {"Grid value of about 0.5° (about 55 km) around the point" if is_live else "Illustrative single record"} |
| Day definition | {"UTC day (midnight to midnight UTC = 5:30 am to 5:30 am IST)" if is_live else "Not applicable"} |
| Period | {rain.index.min():%d %b %Y} to {rain.index.max():%d %b %Y} |
| Missing values | {int(rain.isna().sum())} days |
| Citation | {"NASA Langley Research Center POWER Project, accessed " + pd.Timestamp.today().strftime('%d %b %Y') if is_live else "WDL course sample data"} |
"""))
''')
nb.md("---\n## Part 4 · Year by year\nPress ▶ to plot annual totals.")
nb.code('''
#@title ▶ Annual totals
a = annual(rain)
ax = a.plot(kind="bar", color=BLUE, width=0.8, figsize=(12, 4.5))
ax.axhline(a.mean(), color=ORANGE, ls="--", lw=1.5)
ax.text(0, a.mean() * 1.03, f"Average {a.mean():,.0f} mm", color=ORANGE)
ax.set_ylabel("Rainfall (mm per year)"); ax.set_xlabel("")
ax.set_xticks(range(0, len(a), 5)); ax.set_xticklabels(a.index[::5], rotation=0)
ax.set_title(f"{label.split(' · ')[0]}: annual rainfall {a.index.min()}–{a.index.max()}")
plt.tight_layout(); plt.show()
''')
nb.md("""
---
## Part 5 · Check against the official normal
IMD publishes a **normal annual rainfall** for every district (the long-term average from its gauges).
Type it here to see how close the downloaded data is.
""")
nb.code('''
#@title ▶ Compare with IMD's normal { run: "auto" }
imd_normal_mm = 0 #@param {type:"number"}
mine = annual(rain).loc[1991:2020].mean()
if imd_normal_mm <= 0:
    display(Markdown(f"Your data's 1991–2020 average is **{mine:,.0f} mm**. Type IMD's normal for your district above to compare."))
else:
    diff = (mine - imd_normal_mm) / imd_normal_mm * 100
    display(Markdown(f"Downloaded average **{mine:,.0f} mm** vs IMD normal **{imd_normal_mm:,.0f} mm**: **{diff:+.0f}%**. "
                     + ("Close agreement." if abs(diff) < 15 else "A large gap: remember the dataset is a coarse grid value, not your district's gauges.")))
''')
nb.md("---\n## Part 6 · Save your data\nPress ▶ to save a CSV file you can open in Google Sheets or Excel.")
nb.code('''
#@title ▶ Save as CSV
fname = "my_rainfall_daily.csv"
rain.rename_axis("date").to_csv(fname)
try:
    from google.colab import files; files.download(fname)
except Exception:
    display(Markdown(f"Saved **{fname}** in the notebook's files (folder icon on the left)."))
''')
nb.md("### ⏭️ Next\nOpen the **Practice activity** and describe a dataset yourself.")
built.append(nb.save(OUT))

nb = NB(8, "practice")
nb.md("Describe the **sample district** record (the same data as the Sheet). If you switch to your own place, the checks still work: they use whatever data is loaded.")
nb.code(SETUP_DATA)
nb.code(data_cell())
nb.code('''
#@title ▶ Explorer { run: "auto" }
show = "First and last rows" #@param ["First and last rows", "Summary statistics", "Annual totals table"]
if show == "First and last rows":
    display(rain.head(3).to_frame().T); display(rain.tail(3).to_frame().T)
elif show == "Summary statistics":
    display(rain.describe().round(2).to_frame().T)
else:
    display(annual(rain).round(1).to_frame("Total (mm)").T)
''')
num_q(nb, "Q1 · Length of record", "How many **days** are in the record?", "len(rain)", 0, "{:,.0f}", "Use 'count' in the summary statistics (plus any missing days).")
num_q(nb, "Q2 · First year", "In which **year** does the record start?", "rain.index.min().year", 0, "{:.0f}")
num_q(nb, "Q3 · Average year", "What is the **average annual total** over all complete years (mm)?", "annual(rain).mean()", 0.01, "{:,.0f}", "Average the 'Annual totals table'.")
num_q(nb, "Q4 · Wettest year", "In which **year** was the annual total highest?", "annual(rain).idxmax()", 0, "{:.0f}")
num_q(nb, "Q5 · Dry days", "What **percentage of days** had no rain at all (exactly 0 mm)?", "(rain == 0).mean() * 100", 0.02, "{:.1f}%")
choice_q(nb, "Q6 · Data card", "Which item is **most important** to write on a data card before sharing a chart made from NASA POWER data?",
         ["The file size", "The source and its spatial detail", "The colour of the chart", "The number of rows printed"],
         "The source and its spatial detail", "Readers need to know it is a 0.5° grid value from NASA POWER, not a local gauge.")
built.append(nb.save(OUT))

# =====================================================================
# SESSION 9 · Missing values, gaps and errors
# =====================================================================
nb = NB(9, "reading")
nb.md("""
## Why this session matters
Real records are messy. A gauge breaks, an observer is on leave, a number is typed wrongly, a spreadsheet row is copied twice.
If you add up a column containing **−999** (a common code for "missing"), you get nonsense. This session teaches you to
find and fix the six most common problems.
""")
nb.code(SETUP_DATA)
nb.code(MESSY)
nb.md("""
---
## Part 1 · Six problems to look for

| Problem | What it looks like | Why it happens |
|---|---|---|
| **Missing-value flag** | −999 (or −99, 9999) | The agency's code for "no reading" |
| **Blank cell** | Empty | Not recorded, or lost when copying |
| **Impossible value** | Negative rain; 999.9 mm in a day | Typing error, sensor fault |
| **Duplicate row** | Same date twice | Files joined twice |
| **Gap** | Dates missing entirely | Station not working |
| **Real extreme** | 186 mm in a day | A genuine storm! Do not delete it |
""")
nb.md("---\n## Part 2 · Detective work\nPress ▶ to run all six checks on the messy record.")
nb.code('''
#@title ▶ Run the checks
m = messy.copy(); m["date"] = pd.to_datetime(m["date"])
flags = (m.rain_mm == -999).sum()
blanks = m.rain_mm.isna().sum()
impossible = m[(m.rain_mm != -999) & ((m.rain_mm < 0) | (m.rain_mm > 500))]
dups = m.date.duplicated().sum()
full = pd.date_range(m.date.min(), m.date.max(), freq="D")
missing_dates = full.difference(m.date)
display(Markdown(f"""
| Check | Found |
|---|---|
| −999 flags | **{flags}** |
| Blank cells | **{blanks}** |
| Impossible values | **{len(impossible)}** ({", ".join(f"{v:g} mm on {d:%d %b %Y}" for d, v in zip(impossible.date, impossible.rain_mm))}) |
| Duplicate dates | **{dups}** |
| Dates missing entirely | **{len(missing_dates)}** ({missing_dates.min():%d %b %Y} to {missing_dates.max():%d %b %Y}) |
"""))
''')
nb.md("---\n## Part 3 · Why it matters: the −999 trap\nPress ▶ to compare the 2019 total before and after cleaning.")
nb.code('''
#@title ▶ Clean the record step by step { run: "auto" }
fix_flags = True #@param {type:"boolean"}
fix_impossible = True #@param {type:"boolean"}
remove_duplicates = True #@param {type:"boolean"}
c = messy.copy(); c["date"] = pd.to_datetime(c["date"])
if fix_flags: c.loc[c.rain_mm == -999, "rain_mm"] = np.nan
if fix_impossible: c.loc[(c.rain_mm < 0) | (c.rain_mm > 500), "rain_mm"] = np.nan
if remove_duplicates: c = c.drop_duplicates("date")
tot = c[c.date.dt.year == 2019].rain_mm.sum()
true = sample["2019"].sum()
display(Markdown(f"2019 total with these fixes: **{tot:,.1f} mm**. (The gauge record before the problems were added: {true:,.1f} mm.)"))
''')
nb.md("""
Try turning the fixes off one by one. The −999 flags alone pull the total down by thousands of millimetres.
Even after cleaning, the total is a little low, because **missing days are not zero rain**: we simply do not know.

### Good practice
1. **Never** treat a missing day as 0 mm. Mark it missing (NaN).
2. Report **completeness**: what share of days have valid data. A common rule: use a year only if at least 95% of days are present.
3. Check suspicious values against **neighbouring days and other sources** before deleting. 999.9 mm is impossible here;
   186 mm in a day is rare but real.
4. **Keep a log** of every change you made.
""")
nb.code('''
#@title ▶ Completeness by year
c = messy.copy(); c["date"] = pd.to_datetime(c["date"])
c.loc[(c.rain_mm == -999) | (c.rain_mm < 0) | (c.rain_mm > 500), "rain_mm"] = np.nan
c = c.drop_duplicates("date").set_index("date").reindex(pd.date_range("2018-01-01", "2020-12-31"))
comp = c.rain_mm.notna().groupby(c.index.year).mean() * 100
display(comp.round(1).to_frame("Days with valid data (%)").T)
display(Markdown("A year with less than 95% valid days should be flagged before you compare its total with other years."))
''')
nb.md("### ⏭️ Next\nOpen the **Practice activity** and clean the record yourself.")
built.append(nb.save(OUT))

nb = NB(9, "practice")
nb.md("Investigate the messy gauge record (also in the Sheet). Use the explorer, then check each answer.")
nb.code(SETUP_DATA)
nb.code(MESSY)
nb.code('''
#@title ▶ Explorer { run: "auto" }
show = "Rows with -999" #@param ["Rows with -999", "Blank cells", "Values below 0 or above 500", "Duplicate dates", "Rows around 1 July 2019"]
m = messy.copy()
if show == "Rows with -999": display(m[m.rain_mm == -999])
elif show == "Blank cells": display(m[m.rain_mm.isna()])
elif show == "Values below 0 or above 500": display(m[(m.rain_mm != -999) & ((m.rain_mm < 0) | (m.rain_mm > 500))])
elif show == "Duplicate dates": display(m[m.date.duplicated(keep=False)])
else: display(m[(m.date >= "2019-06-27") & (m.date <= "2019-07-16")])
''')
ANS9 = '''
_m = messy.copy(); _m["date"] = pd.to_datetime(_m["date"])
_c = _m.copy(); _c.loc[(_c.rain_mm == -999) | (_c.rain_mm < 0) | (_c.rain_mm > 500), "rain_mm"] = np.nan
_c = _c.drop_duplicates("date")
'''
nb.code("#@title ▶ Prepare the answer checks (press ▶ once)\n" + ANS9.strip())
num_q(nb, "Q1 · Flags", "How many rows contain the missing-value flag **−999**?", "(_m.rain_mm == -999).sum()", 0, "{:.0f}")
num_q(nb, "Q2 · Blanks", "How many **blank** cells are there?", "_m.rain_mm.isna().sum()", 0, "{:.0f}")
num_q(nb, "Q3 · Impossible values", "How many **impossible** values (below 0 or above 500 mm, not counting −999)?",
      "((_m.rain_mm != -999) & ((_m.rain_mm < 0) | (_m.rain_mm > 500))).sum()", 0, "{:.0f}")
num_q(nb, "Q4 · Duplicates", "How many **extra duplicate rows** are there (dates that appear a second time)?", "_m.date.duplicated().sum()", 0, "{:.0f}")
num_q(nb, "Q5 · Gap", "How many **days are missing entirely** from the record (no row at all)?",
      "len(pd.date_range(_m.date.min(), _m.date.max()).difference(_m.date))", 0, "{:.0f}", "Look at the rows around 1 July 2019.")
num_q(nb, "Q6 · Clean total", "After cleaning (flags and impossible values set to missing, duplicates removed), what is the **2019 total** (mm)?",
      "_c[_c.date.dt.year == 2019].rain_mm.sum()", 0.005, "{:,.1f}")
choice_q(nb, "Q7 · Real or error?", "The record shows **186.2 mm** on one day in another year, with heavy rain the days before. What should you do?",
         ["Delete it as an outlier", "Keep it, after checking neighbouring days and another source", "Replace it with the monthly average", "Set it to 0"],
         "Keep it, after checking neighbouring days and another source", "Extremes are exactly what flood studies need. Delete only what is impossible.")
built.append(nb.save(OUT))

# =====================================================================
# SESSION 10 · Workshop
# =====================================================================
nb = NB(10, "workshop")
nb.md("""
## Workshop brief
Today you download **your capstone district's** rainfall, check its quality, and write its **data card**.
This is **step 2 of your capstone**.

1. In Step 1, choose *My place* and type your district (as in Module 1). If the place is not found, type latitude and longitude
   (search the district headquarters on a map).
2. Run each step. Then take a screenshot of the final card and upload it on CuX.
""")
nb.code(SETUP_DATA)
nb.code(data_cell("My place (live download from NASA POWER)", "Type your district, State"))
nb.md("---\n## Step 2 · Completeness check")
nb.code('''
#@title ▶ How complete is the record?
valid = rain.notna().groupby(rain.index.year).mean() * 100
bad_years = list(valid[valid < 95].index)
fig, ax = plt.subplots(figsize=(12, 3.2))
ax.bar(valid.index, valid.values, color=[RED if v < 95 else TEAL for v in valid.values])
ax.axhline(95, color=GREY, ls="--"); ax.set_ylim(0, 105); ax.set_ylabel("Valid days (%)")
ax.set_title("Completeness by year (95% line dashed)"); plt.tight_layout(); plt.show()
display(Markdown(f"Years below 95% complete: **{', '.join(map(str, bad_years)) or 'none'}**."))
''')
nb.md("---\n## Step 3 · Suspicious values")
nb.code('''
#@title ▶ Look for impossible or extreme values
neg = (rain < 0).sum(); huge = (rain > 500).sum()
top = rain.sort_values(ascending=False).head(5)
display(Markdown(f"Negative values: **{neg}** · Values above 500 mm: **{huge}**"))
display(top.round(1).to_frame("Five wettest days (mm)").rename_axis("Date"))
display(Markdown("Check: do these dates match storms you know of (news reports, IMD warnings)? Grid datasets rarely show impossible values, "
                 "but they do smooth peaks, so a nearby gauge may have recorded more."))
''')
nb.md("---\n## Step 4 · Compare with the official normal")
nb.code('''
#@title ▶ My district vs IMD normal { run: "auto" }
imd_normal_mm = 0 #@param {type:"number"}
avg = annual(rain).loc[1991:2020].mean()
gap = (avg - imd_normal_mm) / imd_normal_mm * 100 if imd_normal_mm > 0 else None
display(Markdown(f"Downloaded 1991–2020 average: **{avg:,.0f} mm**" + (f" · IMD normal: **{imd_normal_mm:,.0f} mm** · difference **{gap:+.0f}%**" if gap is not None else " · *Type the IMD normal above.*")))
''')
nb.md("---\n## Step 5 · Notes and data card")
nb.code('''
#@title ▶ My data card (capstone step 2)
my_district = "" #@param {type:"string"}
problems_found = "" #@param {type:"string"}
decision = "" #@param {type:"string"}
is_live = LAT is not None
display(Markdown(f"""
## 🗂️ Data card: {my_district or label.split(' · ')[0]}
*Capstone step 2 · Water Data Literacy for All*

| Item | Value |
|---|---|
| Source | {"NASA POWER daily precipitation (PRECTOTCORR)" if is_live else "Sample district (synthetic) — replace with your own district"} |
| Location used | {label.split(' · ')[0]}{f" ({LAT:.2f}°N, {LON:.2f}°E)" if is_live else ""} |
| Period | {rain.index.min():%d %b %Y} to {rain.index.max():%d %b %Y} |
| Spatial detail | {"About 0.5° grid (about 55 km)" if is_live else "n/a"} |
| Missing days | {int(rain.isna().sum())} · years below 95% complete: {', '.join(map(str, bad_years)) or 'none'} |
| 1991–2020 average | {avg:,.0f} mm{f" (IMD normal {imd_normal_mm:,.0f} mm, {gap:+.0f}%)" if gap is not None else ""} |
| Wettest day | {rain.max():.1f} mm on {rain.idxmax():%d %b %Y} |

**Problems found:** {problems_found or "_not written_"}

**My decision about using this data:** {decision or "_not written_"}
"""))
if not is_live:
    no("This card uses the sample district. Go back to Step 1 and download your own district.")
''')
nb.md("""
---
## Before you leave
1. Upload a screenshot of your data card on CuX (Lab 2).
2. Take the **Module 2 quiz** on CuX.
3. In Module 3 you will turn this record into your district's rainfall profile.
""")
built.append(nb.save(OUT))
print("\n".join(built))
