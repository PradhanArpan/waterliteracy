"""Module 3 · Reading Rainfall (Sessions 11–15)."""
import os
from nbkit import NB
from datakit import SETUP_DATA, data_cell, DATA_NOTE, num_q, choice_q

OUT = "notebooks/M3"
os.makedirs(OUT, exist_ok=True)
built = []

HELP3 = '''
#@title ▶ Step 2 · Prepare the tables (press ▶)
A = annual(rain)                                    # annual totals
SW = monsoon(rain)                                  # June–September totals
NORMAL = A.loc[1991:2020].mean()                    # 30-year normal, WMO standard period
NORMAL_SW = SW.loc[1991:2020].mean()
def imd_category(dep):
    if dep <= -99.5: return "No rain"
    if dep <= -60: return "Large deficient"
    if dep <= -20: return "Deficient"
    if dep < 20: return "Normal"
    if dep < 60: return "Excess"
    return "Large excess"
CAT_COLOURS = {"Large deficient": "#8E2C2C", "Deficient": RED, "Normal": GREY, "Excess": BLUE, "Large excess": "#1B3F66", "No rain": "black"}
INTENSITY = [("Very light", 0.1, 2.4), ("Light", 2.5, 15.5), ("Moderate", 15.6, 64.4), ("Heavy", 64.5, 115.5),
             ("Very heavy", 115.6, 204.4), ("Extremely heavy", 204.5, 10000)]
def intensity_class(x):
    for name, lo, hi in INTENSITY:
        if lo <= x <= hi: return name
    return "No rain"
AMAX = rain.groupby(rain.index.year).max()          # annual maximum daily rainfall
display(Markdown(f"Tables ready. 1991–2020 normal: **{NORMAL:,.0f} mm** per year, **{NORMAL_SW:,.0f} mm** in the June–September monsoon."))
'''

def setup(nb, default="Sample district (works offline)"):
    nb.code(SETUP_DATA)
    nb.md("---\n## Step 1 · Choose your data" + DATA_NOTE)
    nb.code(data_cell(default))
    nb.code(HELP3)

# =====================================================================
# S11 · Totals, averages and the normal
# =====================================================================
nb = NB(11, "reading")
nb.md("""
## Why this session matters
"Normal monsoon", "below normal", "LPA": every season these words decide headlines and farm plans. This session shows
how a **normal** is calculated, why the **average** can mislead, and how much of the year's water comes in the monsoon.
""")
setup(nb)
nb.md("""
---
## Part 1 · What is a "normal"?
A **normal** is the average over a long, fixed period. The World Meteorological Organization's standard is **30 years**;
the current standard period is **1991–2020**. IMD calls its national normal the **Long Period Average (LPA)**.
Press ▶ to see each year against the normal.
""")
nb.code('''
#@title ▶ Annual totals and the normal { run: "auto" }
normal_start = 1991 #@param {type:"slider", min:1981, max:1995, step:1}
normal_end = 2020 #@param {type:"slider", min:2000, max:2024, step:1}
nm = A.loc[normal_start:normal_end].mean()
fig, ax = plt.subplots(figsize=(12, 4.5))
ax.bar(A.index, A.values, color=[BLUE if v >= nm else ORANGE for v in A.values], width=0.8)
ax.axhline(nm, color="black", lw=1.4); ax.text(A.index[0], nm * 1.03, f"Normal {normal_start}–{normal_end}: {nm:,.0f} mm", fontsize=10)
ax.axvspan(normal_start - 0.5, normal_end + 0.5, color=GREY, alpha=0.08)
ax.set_ylabel("Rainfall (mm per year)"); ax.set_title(f"{label.split(' · ')[0]}: years above (blue) and below (orange) the normal")
plt.tight_layout(); plt.show()
''')
nb.md("Move the sliders: the normal changes a little with the period chosen. That is why reports always say *which* normal they use.")
nb.md("""
---
## Part 2 · Mean or median?
The **mean** adds everything and divides. The **median** is the middle year when all years are sorted. A few very wet years
pull the mean up, so in most places the median year is a little drier than the mean. Press ▶.
""")
nb.code('''
#@title ▶ Mean vs median
fig, ax = plt.subplots(figsize=(10, 3.8))
ax.hist(A.values, bins=12, color=BLUE, alpha=0.75, edgecolor="white")
ax.axvline(A.mean(), color=ORANGE, lw=2); ax.axvline(A.median(), color=TEAL, lw=2, ls="--")
ax.text(A.mean(), ax.get_ylim()[1] * 0.92, f"  mean {A.mean():,.0f}", color=ORANGE)
ax.text(A.median(), ax.get_ylim()[1] * 0.80, f"  median {A.median():,.0f}", color=TEAL)
ax.set_xlabel("Annual rainfall (mm)"); ax.set_ylabel("Number of years"); ax.set_title("How annual totals are spread")
plt.tight_layout(); plt.show()
display(Markdown(f"Wettest year **{A.idxmax()}** ({A.max():,.0f} mm) · driest year **{A.idxmin()}** ({A.min():,.0f} mm) · "
                 f"the wettest year had **{A.max()/A.min():.1f} times** the rain of the driest."))
''')
nb.md("""
---
## Part 3 · Where the year's water comes from
Press ▶ to see the average for each month and each IMD season.
""")
nb.code('''
#@title ▶ The average year { run: "auto" }
show = "By month" #@param ["By month", "By season"]
mon = rain.groupby([rain.index.year, rain.index.month]).sum().groupby(level=1).mean()
if show == "By month":
    ax = pd.Series(mon.values, index=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]).plot(kind="bar", color=BLUE, rot=0)
    ax.bar_label(ax.containers[0], fmt="%.0f", fontsize=9); ax.set_title("Average rainfall by month (mm)")
else:
    sea = pd.Series({"Winter\\n(Jan–Feb)": mon[[1, 2]].sum(), "Pre-monsoon\\n(Mar–May)": mon[[3, 4, 5]].sum(),
                     "SW monsoon\\n(Jun–Sep)": mon[[6, 7, 8, 9]].sum(), "NE monsoon\\n(Oct–Dec)": mon[[10, 11, 12]].sum()})
    ax = sea.plot(kind="bar", color=[GREY, ORANGE, BLUE, TEAL], rot=0)
    ax.bar_label(ax.containers[0], labels=[f"{v:,.0f} mm\\n({v/sea.sum()*100:.0f}%)" for v in sea], fontsize=9)
    ax.set_title("Average rainfall by IMD season"); ax.set_ylim(0, sea.max() * 1.25)
ax.set_ylabel("mm"); plt.tight_layout(); plt.show()
''')
nb.md("""
For most of India, the **southwest monsoon (June–September)** brings 70–90% of the year's rain. In parts of Tamil Nadu,
coastal Andhra Pradesh and south interior Karnataka, the **northeast monsoon (October–December)** matters a great deal too.
Switch Step 1 to your own place and compare.

### ⏭️ Next
Open the **Practice activity** and compute the normal yourself.
""")
built.append(nb.save(OUT))

nb = NB(11, "practice")
nb.md("Answer using the sample district (the same data as the Sheet). Use the explorer to read the numbers.")
setup(nb)
nb.code('''
#@title ▶ Explorer { run: "auto" }
show = "Annual totals" #@param ["Annual totals", "June–September totals", "Sorted annual totals"]
if show == "Annual totals": display(A.round(1).to_frame("mm").T)
elif show == "June–September totals": display(SW.round(1).to_frame("mm").T)
else: display(A.sort_values().round(1).to_frame("mm").T)
''')
num_q(nb, "Q1 · The normal", "What is the **1991–2020 normal** annual rainfall (mm)? (Average of the 30 annual totals.)", "NORMAL", 0.005, "{:,.1f}")
num_q(nb, "Q2 · Median year", "What is the **median** annual total over all years (mm)?", "A.median()", 0.005, "{:,.1f}", "Sort the totals and take the middle (with 44 years, average the two middle values).")
num_q(nb, "Q3 · Driest year", "Which **year** was the driest?", "A.idxmin()", 0, "{:.0f}")
num_q(nb, "Q4 · Monsoon share", "On average, what **percentage** of the year's rain falls from June to September? (Average monsoon total ÷ average annual total × 100.)",
      "SW.mean() / A.mean() * 100", 0.02, "{:.1f}%")
choice_q(nb, "Q5 · Mean or median", "In this record, is the mean higher or lower than the median?",
         ["Higher", "Lower", "Exactly equal"], '="Higher" if A.mean() > A.median() else ("Lower" if A.mean() < A.median() else "Exactly equal")',
         "A few very wet years pull the mean up.")
built.append(nb.save(OUT))

# =====================================================================
# S12 · Anomalies: excess and deficit
# =====================================================================
nb = NB(12, "reading")
nb.md("""
## Why this session matters
"Monsoon 18% deficient" is a **departure from normal**. IMD sorts every district's rainfall into categories using these
percentages. This session shows how they are calculated and how often each category actually happens.
""")
setup(nb)
nb.md("""
---
## Part 1 · Departure from normal
**Departure (%) = (actual − normal) ÷ normal × 100**

IMD's categories for a district or state:

| Departure | Category |
|---|---|
| +60% or more | Large excess |
| +20% to +59% | Excess |
| −19% to +19% | Normal |
| −20% to −59% | Deficient |
| −60% to −99% | Large deficient |
| −100% | No rain |

Notice how wide "Normal" is: anything within about one-fifth of the average counts as normal.
""")
nb.code('''
#@title ▶ Departure calculator { run: "auto" }
actual_mm = 640 #@param {type:"number"}
normal_mm = 780 #@param {type:"number"}
dep = (actual_mm - normal_mm) / normal_mm * 100
display(Markdown(f"Departure = ({actual_mm:,} − {normal_mm:,}) ÷ {normal_mm:,} × 100 = **{dep:+.0f}%** → **{imd_category(dep)}**"))
''')
nb.md("---\n## Part 2 · Every year, coloured by category\nPress ▶. Choose the whole year or the June–September monsoon.")
nb.code('''
#@title ▶ Anomaly chart { run: "auto" }
period = "June–September monsoon" #@param ["June–September monsoon", "Whole year"]
S, N = (SW, NORMAL_SW) if period.startswith("June") else (A, NORMAL)
dep = (S - N) / N * 100
cats = dep.apply(imd_category)
fig, ax = plt.subplots(figsize=(12, 4.5))
ax.bar(dep.index, dep.values, color=[CAT_COLOURS[c] for c in cats], width=0.8)
for y in (-20, 20): ax.axhline(y, color=GREY, ls="--", lw=1)
ax.axhline(0, color="black", lw=0.8)
ax.set_ylabel("Departure from 1991–2020 normal (%)")
ax.set_title(f"{period}: departure from normal, coloured by IMD category")
plt.tight_layout(); plt.show()
counts = cats.value_counts().reindex(["Large excess", "Excess", "Normal", "Deficient", "Large deficient"]).fillna(0).astype(int)
display(counts.to_frame("Number of years").T)
''')
nb.md("""
### What to notice
- Most years are **Normal**. Deficient and excess years come in **runs** sometimes, but not always.
- A "deficient" season (−20%) can still bring hundreds of millimetres of rain.
- The **same year** can be deficient in the monsoon and normal for the whole year, if October–December makes up.
""")
nb.md("""
---
## Part 3 · Reading a headline
*"Monsoon 18% deficient in the district"* means the season's rain was 18% below its normal. By IMD's categories, that is
still **Normal** (just). A newspaper calling it a "drought" is going beyond what the number says.

### ⏭️ Next
Open the **Practice activity** and classify the years yourself.
""")
built.append(nb.save(OUT))

nb = NB(12, "practice")
nb.md("Use the June–September monsoon totals for the sample district.")
setup(nb)
nb.code('''
#@title ▶ Monsoon totals and departures
D = ((SW - NORMAL_SW) / NORMAL_SW * 100)
display(pd.DataFrame({"Jun–Sep total (mm)": SW.round(1), "Departure (%)": D.round(1)}).T)
''')
num_q(nb, "Q1 · Monsoon normal", "What is the **1991–2020 normal** for June–September (mm)?", "NORMAL_SW", 0.005, "{:,.1f}")
num_q(nb, "Q2 · Departure in 2002", "What was the **departure (%)** of the 2002 monsoon from its normal?", "(SW[2002] - NORMAL_SW) / NORMAL_SW * 100", 0.03, "{:+.1f}%", "(actual − normal) ÷ normal × 100.")
choice_q(nb, "Q3 · Category for 2002", "What is IMD's category for the 2002 monsoon?",
         ["Large excess", "Excess", "Normal", "Deficient", "Large deficient"], "=imd_category((SW[2002] - NORMAL_SW) / NORMAL_SW * 100)")
num_q(nb, "Q4 · Deficient years", "How many monsoons were **Deficient or Large deficient** (−20% or lower)?",
      "(((SW - NORMAL_SW) / NORMAL_SW * 100) <= -20).sum()", 0, "{:.0f}")
num_q(nb, "Q5 · Wettest monsoon", "Which **year** had the largest positive departure?", "((SW - NORMAL_SW) / NORMAL_SW).idxmax()", 0, "{:.0f}")
choice_q(nb, "Q6 · Headline check", 'A headline says: "Monsoon 15% below normal: drought fears". By IMD\'s categories, the season was:',
         ["Large deficient", "Deficient", "Normal", "Excess"], "Normal", "−15% falls inside −19% to +19%, the Normal band.")
built.append(nb.save(OUT))

# =====================================================================
# S13 · Extremes and intensity
# =====================================================================
nb = NB(13, "reading")
nb.md("""
## Why this session matters
"Heavy rain warning", "very heavy", "extremely heavy": IMD uses exact thresholds for these words. This session shows how
often each kind of rainy day happens, and how much of the year's water comes from a few heavy days.
""")
setup(nb)
nb.md("""
---
## Part 1 · IMD's words for daily rainfall

| Daily rainfall (24 hours) | IMD term |
|---|---|
| 0.1 – 2.4 mm | Very light rain |
| 2.5 – 15.5 mm | Light rain |
| 15.6 – 64.4 mm | Moderate rain |
| 64.5 – 115.5 mm | Heavy rain |
| 115.6 – 204.4 mm | Very heavy rain |
| 204.5 mm or more | Extremely heavy rain |
""")
nb.code('''
#@title ▶ How many days of each kind?
cls = rain[rain > 0].apply(intensity_class)
order = [n for n, _, _ in INTENSITY]
cnt = cls.value_counts().reindex(order).fillna(0).astype(int)
share = rain[rain > 0].groupby(cls).sum().reindex(order).fillna(0) / rain.sum() * 100
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4))
a1.bar(order, cnt.values, color=BLUE); a1.set_title("Number of days"); a1.tick_params(axis="x", rotation=35)
for i, v in enumerate(cnt.values): a1.text(i, v, f"{v:,}", ha="center", va="bottom", fontsize=9)
a2.bar(order, share.values, color=ORANGE); a2.set_title("Share of all rain (%)"); a2.tick_params(axis="x", rotation=35)
for i, v in enumerate(share.values): a2.text(i, v, f"{v:.0f}%", ha="center", va="bottom", fontsize=9)
plt.suptitle(f"{label.split(' · ')[0]}, {rain.index.min().year}–{rain.index.max().year}", fontweight="bold"); plt.tight_layout(); plt.show()
''')
nb.md("""
### What to notice
Heavy, very heavy and extremely heavy days are a tiny fraction of all rainy days, yet they bring a large slice of the water.
Those are the days that fill tanks and cause floods.
""")
nb.md("---\n## Part 2 · The wettest days on record\nPress ▶.")
nb.code('''
#@title ▶ Top days { run: "auto" }
how_many = 10 #@param {type:"slider", min:5, max:25, step:1}
top = rain.sort_values(ascending=False).head(how_many)
t = pd.DataFrame({"Rain (mm)": top.round(1), "IMD term": top.apply(intensity_class), "Month": top.index.strftime("%B")})
t.index = t.index.strftime("%d %b %Y"); display(t)
''')
nb.md("---\n## Part 3 · The wettest day of every year\nThis **annual maximum** series is what engineers use to design drains and culverts. Press ▶.")
nb.code('''
#@title ▶ Annual maximum daily rainfall
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(AMAX.index, AMAX.values, "o-", color=BLUE)
ax.axhline(64.5, color=ORANGE, ls="--"); ax.text(AMAX.index[0], 66, "Heavy (64.5 mm)", color=ORANGE, fontsize=9)
ax.axhline(115.6, color=RED, ls="--"); ax.text(AMAX.index[0], 117, "Very heavy (115.6 mm)", color=RED, fontsize=9)
ax.set_ylabel("Wettest day of the year (mm)"); ax.set_title("Annual maximum daily rainfall")
plt.tight_layout(); plt.show()
''')
nb.md("### ⏭️ Next\nOpen the **Practice activity** and count the extremes yourself. Next session, we turn this series into return periods.")
built.append(nb.save(OUT))

nb = NB(13, "practice")
nb.md("Use the sample district record. Thresholds: heavy ≥ 64.5 mm, very heavy ≥ 115.6 mm.")
setup(nb)
nb.code('''
#@title ▶ Explorer { run: "auto" }
threshold_mm = 64.5 #@param {type:"number"}
d = rain[rain >= threshold_mm]
display(Markdown(f"Days with **{threshold_mm} mm or more**: **{len(d)}**, bringing **{d.sum():,.1f} mm** in total "
                 f"({d.sum()/rain.sum()*100:.1f}% of all rain)."))
t = d.sort_values(ascending=False).round(1).to_frame("mm"); t.index = t.index.strftime("%d %b %Y"); display(t.head(15))
''')
num_q(nb, "Q1 · Heavy days", "How many days had **64.5 mm or more** in the whole record?", "(rain >= 64.5).sum()", 0, "{:.0f}")
num_q(nb, "Q2 · Very heavy days", "How many days had **115.6 mm or more**?", "(rain >= 115.6).sum()", 0, "{:.0f}")
num_q(nb, "Q3 · Share from heavy days", "What **percentage** of all rain fell on days of 64.5 mm or more?", "rain[rain >= 64.5].sum() / rain.sum() * 100", 0.02, "{:.1f}%")
num_q(nb, "Q4 · Record day", "What is the **wettest day** in the record (mm)?", "rain.max()", 0.001, "{:.1f}")
choice_q(nb, "Q5 · IMD term", "A gauge records **72 mm** in 24 hours. What does IMD call it?",
         ["Moderate rain", "Heavy rain", "Very heavy rain", "Extremely heavy rain"], "Heavy rain", "64.5 to 115.5 mm is 'heavy'.")
num_q(nb, "Q6 · Light days", "What **percentage of rainy days** (any rain above 0) were *very light* (0.1–2.4 mm)?",
      "((rain > 0) & (rain < 2.5)).sum() / (rain > 0).sum() * 100", 0.02, "{:.1f}%")
built.append(nb.save(OUT))

# =====================================================================
# S14 · Return periods made simple
# =====================================================================
nb = NB(14, "reading")
nb.md("""
## Why this session matters
"A 1-in-100-year storm" does **not** mean it happens once a century like a clock. This session builds return periods
from the annual maximum series, in plain arithmetic, and shows why "rare" events still happen surprisingly often.
""")
setup(nb)
nb.md("""
---
## Part 1 · Ranking the wettest day of every year
1. Take the wettest day of each year (the **annual maximum**).
2. Sort them from largest (rank 1) to smallest.
3. **Return period T = (number of years + 1) ÷ rank.** This is the *Weibull plotting position*.
4. **Chance in any one year = 1 ÷ T.**
""")
nb.code('''
#@title ▶ Ranked annual maxima
n = len(AMAX)
R = AMAX.sort_values(ascending=False).to_frame("Wettest day (mm)")
R["Year"] = R.index; R["Rank"] = range(1, n + 1)
R["Return period T (years)"] = ((n + 1) / R["Rank"]).round(1)
R["Chance in any year"] = (1 / R["Return period T (years)"] * 100).round(1).astype(str) + "%"
display(R.reset_index(drop=True).head(12))
''')
nb.md("---\n## Part 2 · The return-period curve\nPress ▶. Each dot is one year's wettest day, placed by its return period.")
nb.code('''
#@title ▶ Plot rain against return period
T = (n + 1) / np.arange(1, n + 1); vals = AMAX.sort_values(ascending=False).values
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.semilogx(T, vals, "o", color=BLUE)
for t in (2, 5, 10, 25):
    v = np.interp(np.log(t), np.log(T[::-1]), vals[::-1])
    ax.axvline(t, color=GREY, ls=":", lw=1); ax.text(t, vals.max() * 0.98, f"{t}-yr\\n≈{v:.0f} mm", fontsize=9, ha="center", va="top")
ax.set_xticks([1, 2, 5, 10, 25, 50]); ax.set_xticklabels(["1", "2", "5", "10", "25", "50"])
ax.set_xlabel("Return period (years, log scale)"); ax.set_ylabel("Wettest day of the year (mm)")
ax.set_title("Bigger storms are rarer")
plt.tight_layout(); plt.show()
''')
nb.md("""
With 44 years of data, we can estimate return periods up to about 45 years. Engineers estimate 100-year values by fitting
a curve (such as the Gumbel distribution) beyond the data. That is beyond this course, but the idea is the same.
""")
nb.md("---\n## Part 3 · Why rare events happen often\nPress ▶. Change the return period and the number of years you are planning for.")
nb.code('''
#@title ▶ Chance of at least one event { run: "auto" }
return_period_years = 100 #@param {type:"slider", min:2, max:200, step:1}
planning_years = 30 #@param {type:"slider", min:1, max:100, step:1}
p = 1 - (1 - 1 / return_period_years) ** planning_years
display(Markdown(f"Chance of at least one **{return_period_years}-year** event in **{planning_years} years**: **{p*100:.0f}%**"))
yrs = np.arange(1, 101)
fig, ax = plt.subplots(figsize=(10, 3.6))
for t, c in [(10, BLUE), (50, ORANGE), (100, RED)]:
    ax.plot(yrs, (1 - (1 - 1 / t) ** yrs) * 100, color=c, label=f"{t}-year event")
ax.axvline(planning_years, color=GREY, ls=":"); ax.set_xlabel("Years"); ax.set_ylabel("Chance of at least one (%)")
ax.legend(frameon=False); ax.set_title("Probability grows with time"); plt.tight_layout(); plt.show()
''')
nb.md("""
A house loan lasts 20–30 years. Over 30 years, a "100-year" flood has about a **26%** chance of happening at least once.
And across India's hundreds of districts, *somewhere* has a 100-year storm almost every year.

### ⏭️ Next
Open the **Practice activity** and calculate return periods yourself.
""")
built.append(nb.save(OUT))

nb = NB(14, "practice")
nb.md("Use the ranked annual maxima of the sample district. T = (n + 1) ÷ rank; chance in one year = 1 ÷ T; chance of at least one in N years = 1 − (1 − 1/T)ᴺ.")
setup(nb)
nb.code('''
#@title ▶ Ranked annual maxima
n = len(AMAX)
R = AMAX.sort_values(ascending=False).to_frame("Wettest day (mm)")
R["Year"] = R.index; R["Rank"] = range(1, n + 1)
display(R.reset_index(drop=True).head(10))
display(Markdown(f"Number of years n = **{n}**"))
''')
num_q(nb, "Q1 · Largest event", "What is the return period **T** of the largest annual maximum (rank 1), in years?", "len(AMAX) + 1", 0.01, "{:.1f}")
num_q(nb, "Q2 · Rank 5", "What is the return period of the **rank 5** event (years)?", "(len(AMAX) + 1) / 5", 0.01, "{:.1f}")
num_q(nb, "Q3 · Rank 5 value", "How much rain fell on the **rank 5** wettest day (mm)?", "AMAX.sort_values(ascending=False).iloc[4]", 0.001, "{:.1f}")
num_q(nb, "Q4 · Chance in a year", "What is the chance (%) of a **50-year** event in any single year?", "100 / 50", 0.01, "{:.1f}%")
num_q(nb, "Q5 · Over ten years", "What is the chance (%) of **at least one 10-year event in the next 10 years**?", "(1 - (1 - 1/10) ** 10) * 100", 0.01, "{:.1f}%", "1 − 0.9¹⁰")
choice_q(nb, "Q6 · A common mistake", 'A 100-year storm hit a town last year. A resident says, "We are safe for the next 99 years." Is that right?',
         ["Yes, it cannot happen again soon", "No, the chance is still 1% every year", "Yes, unless the climate changes"],
         "No, the chance is still 1% every year", "Return periods describe average frequency, not a schedule.")
built.append(nb.save(OUT))

# =====================================================================
# S15 · Workshop: your district's rainfall profile
# =====================================================================
nb = NB(15, "workshop")
nb.md("""
## Workshop brief
Build the **rainfall section** of your capstone: your district's normal, its wet and dry years, its heavy-rain days, and
its 10-year storm. This is **step 3 of your capstone**. Use the same district as in Module 2.
""")
setup(nb, "My place (live download from NASA POWER)")
nb.md("---\n## Step 3 · My rainfall profile")
nb.code('''
#@title ▶ Build the profile figure
dep = (SW - NORMAL_SW) / NORMAL_SW * 100
mon = rain.groupby([rain.index.year, rain.index.month]).sum().groupby(level=1).mean()
n = len(AMAX); T = (n + 1) / np.arange(1, n + 1); vals = AMAX.sort_values(ascending=False).values
r10 = np.interp(np.log(10), np.log(T[::-1]), vals[::-1]); r25 = np.interp(np.log(25), np.log(T[::-1]), vals[::-1])
fig, ax = plt.subplots(2, 2, figsize=(13, 8))
ax[0, 0].bar(range(1, 13), mon.values, color=BLUE); ax[0, 0].set_xticks(range(1, 13)); ax[0, 0].set_xticklabels("JFMAMJJASOND")
ax[0, 0].set_title(f"Average month (normal year {NORMAL:,.0f} mm)"); ax[0, 0].set_ylabel("mm")
last = dep.loc[dep.index[-15]:]
ax[0, 1].bar(last.index, last.values, color=[CAT_COLOURS[imd_category(v)] for v in last.values])
ax[0, 1].axhline(0, color="black", lw=0.8); [ax[0, 1].axhline(y, color=GREY, ls="--", lw=1) for y in (-20, 20)]
ax[0, 1].set_title("Monsoon departure from normal, last 15 years (%)")
order = [n_ for n_, _, _ in INTENSITY]
cls = rain[rain > 0].apply(intensity_class)
share = rain[rain > 0].groupby(cls).sum().reindex(order).fillna(0) / rain.sum() * 100
ax[1, 0].barh(order[::-1], share.values[::-1], color=ORANGE); ax[1, 0].set_title("Share of all rain by day type (%)")
ax[1, 1].semilogx(T, vals, "o", color=BLUE); ax[1, 1].set_title(f"Wettest day vs return period (10-yr ≈ {r10:.0f} mm)")
ax[1, 1].set_xticks([1, 2, 5, 10, 25, 50]); ax[1, 1].set_xticklabels(["1", "2", "5", "10", "25", "50"]); ax[1, 1].set_xlabel("Return period (years)")
fig.suptitle(f"Rainfall profile: {label.split(' · ')[0]}", fontsize=15, fontweight="bold")
fig.text(0.01, 0.005, f"Data: {label}. Normal = 1991–2020 average. Categories: IMD.", fontsize=9, color=GREY)
plt.tight_layout(rect=(0, 0.02, 1, 0.97)); fig.savefig("capstone_step3_rainfall_profile.png", dpi=150); plt.show()
''')
nb.md("---\n## Step 4 · My rainfall card")
nb.code('''
#@title ▶ Rainfall card (capstone step 3)
my_district = "" #@param {type:"string"}
one_sentence_summary = "" #@param {type:"string"}
cats = dep.apply(imd_category).value_counts()
top = rain.sort_values(ascending=False).head(3)
display(Markdown(f"""
## 🌧️ Rainfall profile: {my_district or label.split(' · ')[0]}
*Capstone step 3 · Water Data Literacy for All*

| Fact | Value |
|---|---|
| Normal annual rainfall (1991–2020) | {NORMAL:,.0f} mm |
| June–September normal | {NORMAL_SW:,.0f} mm ({NORMAL_SW/NORMAL*100:.0f}% of the year) |
| Wettest / driest year | {A.idxmax()} ({A.max():,.0f} mm) / {A.idxmin()} ({A.min():,.0f} mm) |
| Monsoons: excess or more / normal / deficient or less | {cats.get('Excess',0)+cats.get('Large excess',0)} / {cats.get('Normal',0)} / {cats.get('Deficient',0)+cats.get('Large deficient',0)} |
| Heavy-rain days (≥ 64.5 mm) per decade | {(rain >= 64.5).sum() / (len(A) / 10):.1f} |
| Three wettest days | {"; ".join(f"{v:.0f} mm ({d:%d %b %Y})" for d, v in top.items())} |
| 10-year / 25-year wettest day | about {r10:.0f} mm / {r25:.0f} mm |

**In one sentence:** {one_sentence_summary or "_not written_"}

*Data: {label}*
"""))
if LAT is None: no("This card uses the sample district. Go back to Step 1 and use your own district.")
try:
    from google.colab import files; files.download("capstone_step3_rainfall_profile.png")
except Exception: pass
''')
nb.md("""
---
## Before you leave
1. Upload the profile figure and a screenshot of the card on CuX (Lab 3).
2. Take the **Module 3 quiz** on CuX.
""")
built.append(nb.save(OUT))
print("\n".join(built))
