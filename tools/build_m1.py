"""Build all Module 1 notebooks."""
import os
from nbkit import NB, SETUP, SETUP_LIGHT

OUT = "notebooks/M1"
os.makedirs(OUT, exist_ok=True)
built = []

# =====================================================================
# SESSION 1 · Water as a data problem
# =====================================================================
nb = NB(1, "reading")
nb.md("""
## Why this session matters
Every monsoon, the news is full of water numbers: rainfall in millimetres, rivers "above the danger mark",
reservoirs "at 40%", dams releasing "cusecs". Each number is a measurement someone made, and each one
shapes real decisions. This session shows you what those numbers are, who measures them, and the four
questions to ask before you believe any of them.
""")
nb.code(SETUP_LIGHT)
nb.md("""
---
## Part 1 · Decode a water headline

Below are six example headlines, written for this course (they are not real news reports).
Choose one from the dropdown and press ▶ to see what kind of water number it contains.
""")
nb.code('''
#@title ▶ Headline decoder { run: "auto" }
headline = "City records 112 mm of rain in 24 hours" #@param ["City records 112 mm of rain in 24 hours", "River flowing 0.8 m above danger mark", "Reservoir storage at 42% of capacity", "Dam releases 50,000 cusecs downstream", "State monsoon rainfall 18% deficient", "City supplies 1,450 MLD of water"]

D = {
 "City records 112 mm of rain in 24 hours": ("Rainfall depth", "mm (millimetres)", "One day (24 hours)", "IMD or a state rain gauge network",
     "Where exactly was it measured? Is 112 mm unusual here? How does it compare with the normal for this date?"),
 "River flowing 0.8 m above danger mark": ("River level (stage)", "m (metres) above a marked level", "A single moment", "CWC or the state water resources department",
     "Is the river still rising or falling? What is the forecast for the next 24 hours?"),
 "Reservoir storage at 42% of capacity": ("Reservoir storage", "% of capacity (from MCM or TMC)", "One day's bulletin", "State water resources department or CWC",
     "Is 42% low or normal for this time of year? What was it on the same date last year?"),
 "Dam releases 50,000 cusecs downstream": ("River flow (discharge)", "cusecs (cubic feet per second)", "A rate at one moment", "Dam authority",
     "For how many hours? How much will the river rise downstream, and where?"),
 "State monsoon rainfall 18% deficient": ("Rainfall anomaly (departure from normal)", "% compared with the long-term average", "A season (June to September)", "IMD",
     "Which districts are worst affected? Is 18% within the normal range of year-to-year change?"),
 "City supplies 1,450 MLD of water": ("Water supply", "MLD (million litres per day)", "Per day", "City water supply board",
     "How much reaches each person after leaks? How does it compare with demand?"),
}
q, u, t, who, miss = D[headline]
display(Markdown(f"""
### "{headline}"
| Question | Answer |
|---|---|
| **What was measured?** | {q} |
| **In what unit?** | {u} |
| **Over what time?** | {t} |
| **Who usually measures it?** | {who} |
| **What the headline leaves out** | {miss} |
"""))
''')
nb.md("""
### 🤔 Think about it
1. Which headline do you think is the most useful to an ordinary reader? Which is the least?
2. Two headlines use **%**. Is "42%" in one the same kind of number as "18%" in the other?
""")
nb.md("""
---
## Part 2 · The water cycle as numbers

**Hydroinformatics** means using data and computers to understand water: *hydro* (water) + *informatics* (data).
The water cycle is the same one you learnt at school. The difference is that we now ask, at every step:
*what can be measured, how, and by whom?*

| Part of the water cycle | What is measured | Instrument | Unit | Who measures it in India |
|---|---|---|---|---|
| Rain | Rainfall depth | Rain gauge; radar; satellite | mm | IMD, state rain gauge networks |
| Evaporation | Water lost to the air | Evaporation pan | mm | IMD, agricultural stations |
| River | Water level (stage) | Gauge post or water-level sensor | m | CWC, state water resources departments |
| River | Flow (discharge) | Current meter; calculated from level | m³/s or cusecs | CWC, state departments |
| Reservoir | Storage | Level gauge + capacity table | MCM or TMC | Dam authorities, CWC |
| Groundwater | Depth to water in wells | Observation wells | m below ground | CGWB, state groundwater departments |
| City supply | Water supplied | Flow meters | MLD | City water boards |

You will meet every row of this table during the course.
""")
nb.md("""
---
## Part 3 · India's water in numbers

How much water does India get, and how much can it actually use? Press ▶ to see the national water budget.
These are rounded figures widely quoted from Central Water Commission assessments; treat them as approximate.
""")
nb.code('''
#@title ▶ India's water budget (approximate)
items = ["Rain and snow\\nfalling on India", "Water resources\\n(rivers + groundwater)", "Water that can\\npractically be used"]
bcm = [4000, 1999, 1122]
fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.barh(items[::-1], bcm[::-1], color=[TEAL, BLUE, GREY][::-1])
ax.bar_label(bars, labels=[f"{v:,} BCM" for v in bcm[::-1]], padding=6)
ax.set_xlim(0, 4700)
ax.set_xlabel("Billion cubic metres (BCM) per year")
ax.set_title("Less than a third of India's rain can be put to use")
ax.text(0, -0.25, "Approximate figures from Central Water Commission assessments. 1 BCM = 1,000 MCM.",
        transform=ax.transAxes, fontsize=9, color=GREY)
plt.tight_layout(); plt.show()
''')
nb.md("""
Most rain is lost to evaporation, soaks deep into the ground, or rushes to the sea during a few monsoon weeks.
That is why **when** and **how** rain falls matters as much as **how much**. The rest of this course
teaches you to read exactly that from data.
""")
nb.md("""
---
## Part 4 · Four questions to ask any water number

Use these every time you meet a water number, in this course and in the news:

1. **What was measured?** Rain, river level, flow, storage, supply?
2. **Where?** One gauge, a district average, a whole state?
3. **Over what time?** An hour, a day, a season, a year?
4. **Compared to what?** The normal, last year, a danger level, a need?

A number that cannot answer all four is not wrong, but it is incomplete. Most headlines answer only one or two.

### ⏭️ Next
Open the **Practice activity** for this session to try the four questions yourself.
""")
built.append(nb.save(OUT))

# ---------------- S1 practice ----------------
nb = NB(1, "practice")
nb.md("Three short tasks. Tasks 1 and 2 check your answers automatically. Task 3 makes a card you post in the discussion forum.")
nb.code(SETUP_LIGHT)
nb.md("""
---
## Task 1 · What was measured?
For each example headline, choose what kind of water number it reports. Then press ▶.

| # | Headline (example) |
|---|---|
| A | "Heavy rain: 87 mm recorded at the city observatory" |
| B | "Lake level drops 1.2 m in three months" |
| C | "Water board to cut supply from 900 MLD to 750 MLD" |
| D | "Monsoon 9% above normal so far" |
| E | "Dam outflow raised to 30,000 cusecs" |
| F | "Groundwater at 18 m below ground in summer" |
""")
nb.code('''
#@title ▶ Check Task 1
A = "choose" #@param ["choose", "Rainfall depth", "Water level", "Water supply", "Rainfall anomaly", "River flow", "Groundwater depth"]
B = "choose" #@param ["choose", "Rainfall depth", "Water level", "Water supply", "Rainfall anomaly", "River flow", "Groundwater depth"]
C = "choose" #@param ["choose", "Rainfall depth", "Water level", "Water supply", "Rainfall anomaly", "River flow", "Groundwater depth"]
D = "choose" #@param ["choose", "Rainfall depth", "Water level", "Water supply", "Rainfall anomaly", "River flow", "Groundwater depth"]
E = "choose" #@param ["choose", "Rainfall depth", "Water level", "Water supply", "Rainfall anomaly", "River flow", "Groundwater depth"]
F = "choose" #@param ["choose", "Rainfall depth", "Water level", "Water supply", "Rainfall anomaly", "River flow", "Groundwater depth"]
key = {"A": "Rainfall depth", "B": "Water level", "C": "Water supply", "D": "Rainfall anomaly", "E": "River flow", "F": "Groundwater depth"}
given = {"A": A, "B": B, "C": C, "D": D, "E": E, "F": F}
score = sum(given[k] == v for k, v in key.items())
for k in key:
    mark = "✅" if given[k] == key[k] else ("⬜ not answered" if given[k] == "choose" else "❌")
    print(f"{k}: {given[k]:<20} {mark}")
(ok if score == 6 else no)(f"{score} / 6 correct" + ("" if score == 6 else ". Hint: look at the unit in each headline."))
''')
nb.md("""
---
## Task 2 · Which question is missing?
Headline: **"Reservoir storage at 42% of capacity."**
Which of the four questions does this headline answer *least* well?
""")
nb.code('''
#@title ▶ Check Task 2
answer = "choose" #@param ["choose", "What was measured?", "Where?", "Over what time?", "Compared to what?"]
if answer == "Compared to what?":
    ok("Right. 42% could be normal for May and alarming for September. Without last year's figure or the seasonal normal, we cannot judge it.")
elif answer == "choose":
    no("Choose an answer from the dropdown first.")
else:
    no("The headline does tell us that (storage, in one reservoir, today). Think about whether 42% is good or bad.")
''')
nb.md("""
---
## Task 3 · Your own headline (for the forum)
Find one water number in a newspaper, news site or app this week. Fill in the boxes and press ▶.
Take a screenshot of the card and post it in the discussion forum.
""")
nb.code('''
#@title ▶ Make my headline card
my_headline = "Type the headline here" #@param {type:"string"}
source = "Newspaper or website name" #@param {type:"string"}
what = "" #@param {type:"string"}
where = "" #@param {type:"string"}
when = "" #@param {type:"string"}
compared_to = "" #@param {type:"string"}
blank = lambda x: x.strip() or "_not stated_"
display(Markdown(f"""
### 📰 "{my_headline}"
*Source: {source}*

| Question | What the report says |
|---|---|
| What was measured? | {blank(what)} |
| Where? | {blank(where)} |
| Over what time? | {blank(when)} |
| Compared to what? | {blank(compared_to)} |
"""))
''')
built.append(nb.save(OUT))

# =====================================================================
# SESSION 2 · Rain is a volume; water units
# =====================================================================
nb = NB(2, "reading")
nb.md("""
## Why this session matters
"50 mm of rain" sounds small. On a city, it is millions of tankers of water arriving in a few hours.
This session turns rainfall depth into volume, and introduces every unit you will meet in water news.
""")
nb.code(SETUP_LIGHT)
nb.md("""
---
## Part 1 · The one idea to remember

**1 mm of rain = 1 litre of water on every square metre of ground.**

So: rainfall depth (mm) × area (m²) = volume of water (litres).

Imagine a 1 m × 1 m square drawn on your terrace. If 1 mm of rain falls, one litre of water lands inside it.
Move the sliders and press ▶.
""")
nb.code('''
#@title ▶ How much water fell? { run: "auto" }
rainfall_mm = 50 #@param {type:"slider", min:1, max:200, step:1}
area_value = 100 #@param {type:"number"}
area_unit = "square metres (m²) - e.g. a rooftop" #@param ["square metres (m²) - e.g. a rooftop", "hectares (ha) - e.g. a farm or campus", "square kilometres (km²) - e.g. a city or catchment"]
factor = 1 if area_unit.startswith("square m") else (1e4 if area_unit.startswith("hect") else 1e6)
litres = rainfall_mm * area_value * factor
display(Markdown(f"""
### {rainfall_mm} mm of rain on {area_value:,} {area_unit.split(" (")[0]}
| Measure | Amount |
|---|---|
| Litres | **{litres:,.0f} L** |
| Cubic metres (m³) | {litres/1e3:,.1f} |
| Million cubic metres (MCM) | {litres/1e9:,.6f} |
| 10,000-litre water tankers | {litres/1e4:,.1f} |
| Olympic swimming pools (2.5 million L each) | {litres/2.5e6:,.3g} |
| Days of water for one person (135 L/day) | {litres/135:,.0f} |
"""))
''')
nb.md("""
### Expected output
With the starting values (50 mm on 100 m²) you should see **5,000 L**, which is half a tanker.
Now try a city: set the unit to km² and the area to about 700. One storm brings tens of millions of cubic metres.
""")
nb.md("""
---
## Part 2 · Why cities flood quickly

In a forest or a field, much of the rain soaks into the soil. On roofs and roads, almost all of it runs off at once.
Press ▶ to compare the same storm on two surfaces of the same size.
""")
nb.code('''
#@title ▶ Same storm, two surfaces { run: "auto" }
storm_mm = 60 #@param {type:"slider", min:10, max:150, step:5}
area_km2 = 10 #@param {type:"number"}
# share of rain that runs off (typical textbook ranges)
runoff = {"Forest / grassland": 0.15, "Farmland": 0.35, "Dense city (roofs, roads)": 0.85}
vol = {k: storm_mm * area_km2 * 1e6 * c / 1e3 for k, c in runoff.items()}   # m³
fig, ax = plt.subplots(figsize=(10, 3.8))
bars = ax.barh(list(vol), [v / 1e3 for v in vol.values()], color=[TEAL, BLUE, RED])
ax.bar_label(bars, labels=[f"{v/1e3:,.0f} thousand m³" for v in vol.values()], padding=6)
ax.set_xlabel("Water running off the surface (thousand m³)")
ax.set_xlim(0, max(vol.values()) / 1e3 * 1.35)
ax.set_title(f"{storm_mm} mm on {area_km2} km²: the city sends far more water to its drains")
plt.tight_layout(); plt.show()
''')
nb.md("""
The fraction that runs off (0.15, 0.35, 0.85) is called a **runoff coefficient**. You will use it again in Module 4.
""")
nb.md("""
---
## Part 3 · The units water people use

| Quantity | Unit | Where you'll see it |
|---|---|---|
| Rainfall depth | **mm** | IMD reports, weather news |
| River level (stage) | **m** | CWC flood bulletins, danger levels |
| River flow (discharge) | **m³/s** ("cumecs") or **cusecs** (ft³/s) | Flood forecasts, dam releases. 1 m³/s ≈ 35.3 cusecs |
| Reservoir storage | **MCM** (million m³) or **TMC** (thousand million ft³) | Reservoir bulletins, water sharing. 1 TMC ≈ 28.3 MCM |
| City supply | **MLD** (million litres per day) | Water board reports |
| Per-person use | **LPCD** (litres per person per day) | Planning norms; 135 LPCD for cities with sewerage |
""")
nb.code('''
#@title ▶ Water volume converter { run: "auto" }
amount = 1 #@param {type:"number"}
unit = "TMC" #@param ["litres", "m³", "ML (million litres)", "MCM", "TMC"]
to_L = {"litres": 1, "m³": 1e3, "ML (million litres)": 1e6, "MCM": 1e9, "TMC": 28316.846592e6}
L = amount * to_L[unit]
display(Markdown(f"""
### {amount:,} {unit} equals
| Unit | Amount |
|---|---|
| Litres | {L:,.0f} |
| m³ | {L/1e3:,.1f} |
| ML (million litres) | {L/1e6:,.2f} |
| MCM | {L/1e9:,.4f} |
| TMC | {L/to_L['TMC']:,.5f} |
| Olympic pools | {L/2.5e6:,.0f} |
| Days of supply for a city using 1,000 MLD | {L/1e9:,.2f} |
"""))
''')
nb.md("""
### Flow to volume
A flow rate (m³/s) becomes a volume once you multiply by time. One day has 86,400 seconds.
""")
nb.code('''
#@title ▶ Flow to volume { run: "auto" }
flow = 100 #@param {type:"number"}
flow_unit = "m³/s (cumecs)" #@param ["m³/s (cumecs)", "cusecs (ft³/s)"]
hours = 24 #@param {type:"slider", min:1, max:240, step:1}
m3s = flow if flow_unit.startswith("m³") else flow / 35.3147
vol_mcm = m3s * hours * 3600 / 1e6
display(Markdown(f"**{flow:,} {flow_unit.split(' (')[0]}** for **{hours} hours** = **{vol_mcm:,.2f} MCM** "
                 f"= **{vol_mcm/28.316846592:,.3f} TMC**"))
''')
nb.md("""
### Expected output
100 m³/s for 24 hours gives **8.64 MCM**. Keep this as a mental benchmark.

### ⏭️ Next
Open the **Practice activity** and work out six real-world volumes yourself.
""")
built.append(nb.save(OUT))

# ---------------- S2 practice ----------------
nb = NB(2, "practice")
nb.md("""
Six calculations. Work each one out yourself first (on paper or with a calculator), type your answer, then press ▶.
Answers within 2% are marked correct. The Reading notebook's calculators are there if you get stuck.
""")
nb.code(SETUP_LIGHT)
QS = [
    ("Q1 · Rooftop", "A 120 m² roof receives **65 mm** of rain. How many **litres** fall on it?", "litres", "65 * 120",
     "Depth (mm) × area (m²) = litres."),
    ("Q2 · Campus", "A 30 ha campus receives **40 mm** of rain. How many **m³** fall on it?", "m3", "40 * 30 * 1e4 / 1e3",
     "Convert ha to m² first (1 ha = 10,000 m²), get litres, then divide by 1,000 for m³."),
    ("Q3 · Reservoir", "A reservoir releases **2 TMC**. How many **MCM** is that?", "mcm", "2 * 28.316846592",
     "1 TMC ≈ 28.3 MCM."),
    ("Q4 · River", "A river flows at **250 m³/s** for **one day**. How many **MCM** pass?", "mcm", "250 * 86400 / 1e6",
     "Flow × seconds in a day (86,400) gives m³. Divide by 1,000,000 for MCM."),
    ("Q5 · Dam release", "A dam releases **50,000 cusecs**. What is this in **m³/s**?", "m3s", "50000 / 35.3147",
     "1 m³/s ≈ 35.3 cusecs, so divide."),
    ("Q6 · City supply", "A city uses **1,450 MLD**. For how many **days** would **1 TMC** last?", "days", "28316.846592 / 1450",
     "1 TMC ≈ 28,317 million litres (ML). Divide by the daily use in ML."),
]
for title, text, var, formula, hint in QS:
    nb.md(f"---\n## {title}\n{text}")
    nb.code(f'''
#@title ▶ Check {title.split(" ·")[0]}
my_answer = 0 #@param {{type:"number"}}
correct = {formula}
if my_answer == 0:
    no("Type your answer in the box first.")
elif close(my_answer, correct):
    ok(f"Correct: {{correct:,.2f}}")
else:
    no("Not quite. Hint: {hint}")
''')
nb.md("""
---
## Reflect (not graded)
Which of these six numbers surprised you most? Write one sentence about it in the discussion forum.
""")
built.append(nb.save(OUT))

# =====================================================================
# SESSION 3 · Reading a rain gauge record; time scales
# =====================================================================
nb = NB(3, "reading")
nb.md("""
## Why this session matters
Every rainfall figure in the news starts in a **rain gauge**: a funnel over a measuring container. In India the gauge
is read every morning at **8:30 am IST**, recording the rain of the previous 24 hours. In this session you will read a
full year of gauge records and see how the same data tells different stories at different time scales.
""")
nb.code(SETUP)
nb.md("""
---
## Part 1 · What a rain gauge record looks like
A rainfall record is simply a table: a date and a number. Press ▶.
""")
nb.code('''
#@title ▶ Look at the raw record
display(Markdown("**First 10 days of January** (dry season)"))
display(rainfall.head(10).T)
display(Markdown("**17 to 26 September** (monsoon)"))
display(rainfall.loc["2023-09-17":"2023-09-26"].T)
''')
nb.md("""
---
## Part 2 · One year as a chart
A table of 365 numbers hides the pattern. A chart shows it at once.
IMD counts a **rainy day** only when **2.5 mm or more** falls in 24 hours.
""")
nb.code('''
#@title ▶ Plot one year of daily rainfall
r = rainfall.rain_mm
total, rainy, wettest = r.sum(), (r >= 2.5).sum(), r.idxmax()
fig, ax = plt.subplots()
ax.bar(r.index, r, width=1.0, color=BLUE)
ax.annotate(f"Wettest day: {r.max():.0f} mm on {wettest:%d %b}", xy=(wettest, r.max()), xytext=(-190, -8),
            textcoords="offset points", arrowprops=dict(arrowstyle="->", color=GREY))
ax.set_title(f"Daily rainfall, 2023: {total:,.0f} mm in the year, {rainy} rainy days")
ax.set_ylabel("Rainfall (mm/day)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.text(0, -0.15, "Illustrative sample station · synthetic data for practice", transform=ax.transAxes, fontsize=9, color=GREY)
plt.tight_layout(); plt.show()
''')
nb.md("""
### Expected output
About **1,065 mm** in the year from **77 rainy days**, with the wettest day (**96 mm**) on **21 September**.
""")
nb.md("""
---
## Part 3 · How uneven is rain?
Press ▶ to see what share of the whole year's rain fell on the wettest few days.
""")
nb.code('''
#@title ▶ Share of the year's rain on the wettest days { run: "auto" }
top_n_days = 10 #@param {type:"slider", min:1, max:60, step:1}
r = rainfall.rain_mm.sort_values(ascending=False)
share = r.head(top_n_days).sum() / r.sum() * 100
display(Markdown(f"The **{top_n_days} wettest days** brought **{share:.0f}%** of the year's rain "
                 f"({top_n_days/365*100:.1f}% of the days in the year)."))
''')
nb.md("""
Rain that arrives in a few big bursts is harder to store and more likely to flood than the same amount spread out.
**The yearly total alone never tells the full story.**
""")
nb.md("""
---
## Part 4 · Same data, different time scales
Water data can be added up by day, week, month or season. Choose a scale and press ▶. Try all four.
""")
nb.code('''
#@title ▶ Change the time scale { run: "auto" }
time_scale = "Monthly" #@param ["Daily", "Weekly", "Monthly", "Seasonal"]
r = rainfall.rain_mm
fig, ax = plt.subplots()
if time_scale == "Seasonal":
    season = {1: "Winter\\n(Jan–Feb)", 2: "Winter\\n(Jan–Feb)", 3: "Pre-monsoon\\n(Mar–May)", 4: "Pre-monsoon\\n(Mar–May)",
              5: "Pre-monsoon\\n(Mar–May)", 6: "SW monsoon\\n(Jun–Sep)", 7: "SW monsoon\\n(Jun–Sep)", 8: "SW monsoon\\n(Jun–Sep)",
              9: "SW monsoon\\n(Jun–Sep)", 10: "NE monsoon\\n(Oct–Dec)", 11: "NE monsoon\\n(Oct–Dec)", 12: "NE monsoon\\n(Oct–Dec)"}
    order = ["Winter\\n(Jan–Feb)", "Pre-monsoon\\n(Mar–May)", "SW monsoon\\n(Jun–Sep)", "NE monsoon\\n(Oct–Dec)"]
    s = r.groupby(r.index.month.map(season)).sum().reindex(order)
    ax.bar_label(ax.bar(s.index, s.values, color=BLUE, width=0.6), fmt="%.0f mm")
    ax.set_title("Seasonal rainfall (IMD seasons)")
else:
    rule = {"Daily": "D", "Weekly": "W", "Monthly": "MS"}[time_scale]
    s = r.resample(rule).sum()
    b = ax.bar(s.index, s.values, width={"D": 1, "W": 5, "MS": 22}[rule], color=BLUE, align="edge" if rule == "MS" else "center")
    if rule == "MS": ax.bar_label(b, fmt="%.0f", fontsize=9)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_title(f"{time_scale} rainfall totals")
ax.set_ylabel("Rainfall (mm)")
plt.tight_layout(); plt.show()
display(Markdown(f"The year's total is the same in every view: **{r.sum():,.0f} mm**. Only the lens changes."))
''')
nb.md("""
### 🤔 Think about it
1. Which scale shows a flood-causing storm best? Which suits a farmer planning a crop?
2. In the monthly view, where did the 96 mm storm go?
3. This station gets a large share of its rain from October to December. Why might "monsoon" mean different months in different parts of India?

### ⏭️ Next
Open the **Practice activity** and answer five questions from this record.
""")
built.append(nb.save(OUT))

# ---------------- S3 practice ----------------
nb = NB(3, "practice")
nb.md("Answer five questions about the sample station's 2023 record. Use the explorer below to find each answer, then check it.")
nb.code(SETUP)
nb.md("""
---
## Explorer
Choose what to show, press ▶, and read off the numbers you need.
""")
nb.code('''
#@title ▶ Rainfall explorer { run: "auto" }
show = "Monthly totals" #@param ["Monthly totals", "Seasonal totals", "Ten wettest days", "Days at or above a threshold"]
threshold_mm = 2.5 #@param {type:"number"}
r = rainfall.rain_mm
if show == "Monthly totals":
    t = r.resample("MS").sum().round(1); t.index = t.index.strftime("%b"); display(t.to_frame("Rain (mm)").T)
elif show == "Seasonal totals":
    sea = r.index.month.map(lambda m: "Winter (Jan–Feb)" if m <= 2 else "Pre-monsoon (Mar–May)" if m <= 5 else "SW monsoon (Jun–Sep)" if m <= 9 else "NE monsoon (Oct–Dec)")
    display(r.groupby(sea).sum().round(1).to_frame("Rain (mm)"))
elif show == "Ten wettest days":
    t = r.sort_values(ascending=False).head(10).to_frame("Rain (mm)"); t.index = t.index.strftime("%Y-%m-%d"); display(t)
else:
    display(Markdown(f"Days with **{threshold_mm} mm or more**: **{(r >= threshold_mm).sum()}**"))
''')
nb.code('''
#@title ▶ Check Q1 · Total rainfall in 2023 (mm)
total_mm = 0 #@param {type:"number"}
ans = rainfall.rain_mm.sum()
ok(f"Correct: {ans:,.1f} mm") if close(total_mm, ans) else no("Hint: add up the monthly totals in the explorer.")
''')
nb.code('''
#@title ▶ Check Q2 · Number of rainy days (IMD definition, 2.5 mm or more)
rainy_days = 0 #@param {type:"number"}
ans = (rainfall.rain_mm >= 2.5).sum()
ok(f"Correct: {ans} rainy days") if rainy_days == ans else no("Hint: use 'Days at or above a threshold' with 2.5.")
''')
nb.code('''
#@title ▶ Check Q3 · Wettest month
wettest_month = "choose" #@param ["choose", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ans = rainfall.rain_mm.resample("MS").sum().idxmax().strftime("%b")
ok(f"Correct: {ans}") if wettest_month == ans else no("Hint: look for the largest monthly total.")
''')
nb.code('''
#@title ▶ Check Q4 · Percentage of the year's rain that fell on the 10 wettest days
percent = 0 #@param {type:"number"}
r = rainfall.rain_mm
ans = r.sort_values(ascending=False).head(10).sum() / r.sum() * 100
ok(f"Correct: {ans:.1f}%") if close(percent, ans, tol=0.05) else no("Hint: add the ten wettest days, divide by the year's total, multiply by 100.")
''')
nb.code('''
#@title ▶ Check Q5 · Which season brought the most rain?
season = "choose" #@param ["choose", "Winter (Jan–Feb)", "Pre-monsoon (Mar–May)", "SW monsoon (Jun–Sep)", "NE monsoon (Oct–Dec)"]
ok("Correct: the southwest monsoon (June to September).") if season == "SW monsoon (Jun–Sep)" else no("Hint: use 'Seasonal totals' in the explorer.")
''')
built.append(nb.save(OUT))

# =====================================================================
# SESSION 4 · Reading a river gauge record
# =====================================================================
nb = NB(4, "reading")
nb.md("""
## Why this session matters
Rain gauges tell us what falls from the sky. Floods happen in rivers. At a river **gauge station**, a tall marked scale
(or an automatic sensor) records the **water level**, called the **stage**, in metres. Each station has two key lines:
the **warning level** (get ready) and the **danger level** (water may spill over the banks).
In India, CWC and state water resources departments run these stations.
""")
nb.code(SETUP)
nb.md("""
---
## Part 1 · Rain and river, side by side
Press ▶ to plot the river level under the same year's rainfall.
""")
nb.code('''
#@title ▶ Plot rainfall and river level together
fig, (a1, a2) = plt.subplots(2, 1, sharex=True, figsize=(11, 6.5), gridspec_kw={"height_ratios": [1, 1.6]})
a1.bar(rainfall.index, rainfall.rain_mm, width=1.0, color=BLUE); a1.set_ylabel("Rain (mm/day)")
a1.set_title("Rain falls first; the river responds after")
lv = river.level_m
a2.plot(lv.index, lv, color="black", lw=1.4, label="River level")
a2.axhline(WARNING_LEVEL, color=ORANGE, ls="--", lw=1.3, label=f"Warning level ({WARNING_LEVEL} m)")
a2.axhline(DANGER_LEVEL, color=RED, ls="--", lw=1.3, label=f"Danger level ({DANGER_LEVEL} m)")
a2.fill_between(lv.index, DANGER_LEVEL, lv, where=lv > DANGER_LEVEL, color=RED, alpha=0.25)
a2.text(lv.index[5], WARNING_LEVEL + 0.04, f"Warning level {WARNING_LEVEL} m", color=ORANGE, fontsize=10)
a2.text(lv.index[5], DANGER_LEVEL + 0.04, f"Danger level {DANGER_LEVEL} m", color=RED, fontsize=10)
a2.set_ylabel("Water level (m)")
a2.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
plt.tight_layout(); plt.show()
''')
nb.md("""
### What to notice
- **January to March:** no rain, and the river sits flat. This is **base flow**: groundwater slowly seeping into the river.
- **Small rains barely move the river.** Dry soil soaks up light rain first.
- **The big September storm** pushes the river above the danger level.
""")
nb.md("""
---
## Part 2 · Lag time
Zoom in on the September storm. Press ▶.
""")
nb.code('''
#@title ▶ Zoom in on the flood { run: "auto" }
days_either_side = 12 #@param {type:"slider", min:5, max:30, step:1}
peak_rain_day = rainfall.rain_mm.idxmax()
win = slice(peak_rain_day - pd.Timedelta(days=days_either_side), peak_rain_day + pd.Timedelta(days=days_either_side))
r, lv = rainfall.rain_mm[win], river.level_m[win]
peak_level_day = lv.idxmax()
fig, ax = plt.subplots(figsize=(11, 4.5)); ax2 = ax.twinx()
ax.bar(r.index, r, color=BLUE, alpha=0.6, width=0.8); ax.set_ylabel("Rain (mm/day)", color=BLUE)
ax2.plot(lv.index, lv, "k-o", ms=3); ax2.set_ylabel("River level (m)")
ax2.axhline(DANGER_LEVEL, color=RED, ls="--", lw=1.2)
ax2.text(lv.index[0], DANGER_LEVEL + 0.04, "Danger level", color=RED, fontsize=10)
ax2.annotate("Peak level", xy=(peak_level_day, lv.max()), xytext=(15, -5), textcoords="offset points")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
lag = (peak_level_day - peak_rain_day).days
ax.set_title(f"Heaviest rain {peak_rain_day:%d %b}, river peak {peak_level_day:%d %b}: lag time {lag} days")
plt.tight_layout(); plt.show()
''')
nb.md("""
**Lag time** is the delay between the heaviest rain and the highest river level. Water has to run off the land, gather in
streams and travel down to the gauge. Lag time is precious: it is the window in which flood warnings can be issued.

Notice too that the river **rises fast and falls slowly**. The falling part is called the **recession**.
""")
nb.md("""
---
## Part 3 · How long was the river in danger?
Move the danger level and see how the count of dangerous days changes. Press ▶.
""")
nb.code('''
#@title ▶ Days above a level { run: "auto" }
level_to_test = 4.2 #@param {type:"slider", min:2.0, max:4.6, step:0.1}
lv = river.level_m
above = lv > level_to_test
display(Markdown(f"Days above **{level_to_test:.1f} m**: **{above.sum()}**. "
                 f"Highest level of the year: **{lv.max():.2f} m** on **{lv.idxmax():%d %B}**."))
''')
nb.md("""
### Expected output
At the official danger level (**4.2 m**) you should see **4 days**; at the warning level (**3.6 m**), **6 days**.

### 🤔 Think about it
1. Why is a danger level set by the local bank height rather than a single number for every river?
2. If the city upstream paved over its fields, would the lag time get shorter or longer? Why?

### ⏭️ Next
Open the **Practice activity** and measure the flood yourself.
""")
built.append(nb.save(OUT))

# ---------------- S4 practice ----------------
nb = NB(4, "practice")
nb.md("Measure the September flood at the sample station. Use the table to find each answer, then check it.")
nb.code(SETUP)
nb.code('''
#@title ▶ Flood table: 15 Sep to 10 Oct
t = station.loc["2023-09-15":"2023-10-10"].copy()
t["above warning?"] = np.where(t.level_m > WARNING_LEVEL, "yes", "")
t["above danger?"] = np.where(t.level_m > DANGER_LEVEL, "yes", "")
t.index = t.index.strftime("%d %b")
display(t)
''')
nb.code('''
#@title ▶ Check Q1 · Highest river level of the year (m)
peak_m = 0 #@param {type:"number"}
ans = river.level_m.max()
ok(f"Correct: {ans:.2f} m") if close(peak_m, ans, tol=0.005) else no("Hint: find the largest number in the level_m column.")
''')
nb.code('''
#@title ▶ Check Q2 · Lag time (days between the heaviest rain and the river peak)
lag_days = 0 #@param {type:"integer"}
ans = (river.level_m.idxmax() - rainfall.rain_mm.idxmax()).days
ok(f"Correct: {ans} days") if lag_days == ans else no("Hint: find the date of the most rain and the date of the highest level, then count the days between.")
''')
nb.code('''
#@title ▶ Check Q3 · Days above the danger level (4.2 m)
danger_days = 0 #@param {type:"integer"}
ans = int((river.level_m > DANGER_LEVEL).sum())
ok(f"Correct: {ans} days") if danger_days == ans else no("Hint: count the 'yes' entries in the 'above danger?' column.")
''')
nb.code('''
#@title ▶ Check Q4 · Days from the peak until the river fell back below the warning level
days_to_safety = 0 #@param {type:"integer"}
lv = river.level_m; pk = lv.idxmax()
after = lv[pk:]; below = after[after <= WARNING_LEVEL].index[0]
ans = (below - pk).days
ok(f"Correct: {ans} days (back below warning on {below:%d %b})") if days_to_safety == ans else no("Hint: start at the peak date and count forward to the first day with no 'yes' under 'above warning?'.")
''')
nb.code('''
#@title ▶ Check Q5 · Did the river rise faster than it fell?
answer = "choose" #@param ["choose", "Yes, it rose faster", "No, it fell faster", "Both took the same time"]
lv = river.level_m; pk = lv.idxmax()
start = lv[:pk][lv[:pk] <= WARNING_LEVEL].index[-1]
after = lv[pk:]; end = after[after <= WARNING_LEVEL].index[0]
rise, fall = (pk - start).days, (end - pk).days
msg = f"From the warning level it took {rise} days to rise to the peak and {fall} days to fall back."
ok("Correct. " + msg) if answer == "Yes, it rose faster" else no("Look again at the table. " if answer == "choose" else "Not quite. " + msg)
''')
built.append(nb.save(OUT))

# =====================================================================
# SESSION 5 · Workshop: My district in numbers
# =====================================================================
nb = NB(5, "workshop")
nb.md("""
## Workshop brief
Today you choose the district you will follow for the whole course, and make its first **water facts card**.
This card is **step 1 of your capstone**, *My District's Water Story*.

**You will need** (look these up before you start):
- your district's **area** in km² (district website or Census of India)
- its **population** (Census of India or district website)
- its **normal annual rainfall** in mm (IMD district rainfall pages; links in the session reference)
- the **main river or lake** in or near the district

The boxes start with **example values for an imaginary district**. Replace every one with your own.
""")
nb.code(SETUP_LIGHT)
nb.md("---\n## Step 1 · Enter your district's facts")
nb.code('''
#@title ▶ My district { run: "auto" }
district = "Example district" #@param {type:"string"}
state = "Example state" #@param {type:"string"}
area_km2 = 2000 #@param {type:"number"}
population = 2000000 #@param {type:"number"}
normal_annual_rain_mm = 900 #@param {type:"number"}
main_water_body = "Example river" #@param {type:"string"}
example = district == "Example district"
if example:
    display(Markdown("⚠️ These are **example values**. Replace them with your own district's facts."))
else:
    ok(f"Saved facts for {district}, {state}.")
''')
nb.md("""
---
## Step 2 · Turn rainfall into water
Using what you learnt in Session 2: rainfall depth × area = volume. Press ▶.
""")
nb.code('''
#@title ▶ My district's rain as a volume
vol_m3 = normal_annual_rain_mm / 1000 * area_km2 * 1e6
vol_mcm, vol_tmc = vol_m3 / 1e6, vol_m3 / 28.316846592e6
lpcd_if_all = vol_m3 * 1000 / population / 365
need_mcm = population * 135 * 365 / 1e9
display(Markdown(f"""
| In a normal year, {district} receives | |
|---|---|
| Rain on the whole district | **{vol_mcm:,.0f} MCM** ({vol_tmc:,.1f} TMC) |
| If every drop were shared out | **{lpcd_if_all:,.0f} litres per person per day** |
| What the population needs at 135 LPCD | **{need_mcm:,.0f} MCM per year** |
| Rain received ÷ water needed | **{vol_mcm/need_mcm:,.1f} times** |
"""))
fig, ax = plt.subplots(figsize=(10, 3.2))
b = ax.barh(["Need at 135 LPCD", "Rain on the district"], [need_mcm, vol_mcm], color=[ORANGE, TEAL])
ax.bar_label(b, labels=[f"{need_mcm:,.0f} MCM", f"{vol_mcm:,.0f} MCM"], padding=6)
ax.set_xlim(0, max(vol_mcm, need_mcm) * 1.3); ax.set_xlabel("Million cubic metres per year")
ax.set_title(f"{district}: rain received vs domestic water needed in a normal year")
plt.tight_layout(); plt.show()
''')
nb.md("""
Remember Session 1: only a fraction of rain can actually be used. A district that receives many times
its need can still face shortages if the rain comes in a few weeks and runs away.
""")
nb.md("---\n## Step 3 · Lab 1 answers\nAnswer in your own words, then press ▶. Your answers go on the card.")
nb.code('''
#@title ▶ My Lab 1 answers
why_cities_flood = "" #@param {type:"string"}
best_time_scale_for_farmer = "Monthly" #@param ["Daily", "Weekly", "Monthly", "Seasonal"]
why_that_scale = "" #@param {type:"string"}
lag_time_reason = "" #@param {type:"string"}
filled = all(x.strip() for x in [why_cities_flood, why_that_scale, lag_time_reason])
ok("All answers filled in.") if filled else no("Fill in all three text boxes before making your card.")
''')
nb.md("---\n## Step 4 · Make your water facts card\nPress ▶. Take a screenshot of the card (or File → Print → Save as PDF) and upload it on CuX.")
nb.code('''
#@title ▶ My district water facts card
display(Markdown(f"""
## 💧 {district}, {state}: water facts card
*Capstone step 1 · Hydroinformatics in a Changing Climate: Water Data Literacy for All*

| Fact | Value |
|---|---|
| Area | {area_km2:,} km² |
| Population | {population:,} |
| Normal annual rainfall | {normal_annual_rain_mm:,} mm |
| Main river or lake | {main_water_body} |
| Rain on the district in a normal year | {vol_mcm:,.0f} MCM ({vol_tmc:,.1f} TMC) |
| Domestic need at 135 LPCD | {need_mcm:,.0f} MCM per year |

**Why cities flood quickly:** {why_cities_flood or "_not answered_"}

**Most useful time scale for a farmer:** {best_time_scale_for_farmer}. {why_that_scale or "_not answered_"}

**Why the river peaks after the rain:** {lag_time_reason or "_not answered_"}
"""))
if example:
    no("This card still uses the example district. Go back to Step 1 and enter your own.")
''')
nb.md("""
---
## Before you leave
1. Upload your card on CuX (Lab 1).
2. Take the **Module 1 quiz** on CuX.
3. Keep your district facts handy: in Module 2 you will download its real rainfall record.
""")
built.append(nb.save(OUT))

print("\n".join(built))
