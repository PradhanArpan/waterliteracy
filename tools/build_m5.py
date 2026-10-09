"""Module 5 · Climate Signals in Water Data (Sessions 21–25)."""
import os
from nbkit import NB
from datakit import SETUP_DATA, data_cell, DATA_NOTE, num_q, choice_q

OUT = "notebooks/M5"
os.makedirs(OUT, exist_ok=True)
built = []

HELP5 = '''
#@title ▶ Step 2 · Prepare the yearly indicators (press ▶)
from scipy import stats
A = annual(rain)                                                   # annual total (mm)
RD = (rain >= 2.5).groupby(rain.index.year).sum().loc[A.index]    # rainy days (IMD, ≥ 2.5 mm)
HD = (rain >= 64.5).groupby(rain.index.year).sum().loc[A.index]   # heavy-rain days (≥ 64.5 mm)
SDII = (A / RD).rename("SDII")                                     # average rain per rainy day (mm)
def longest_dry_spell(x):
    run = best = 0
    for v in x:
        run = run + 1 if v < 2.5 else 0
        best = max(best, run)
    return best
DRY = rain[rain.index.month.isin([6, 7, 8, 9])].groupby(rain[rain.index.month.isin([6, 7, 8, 9])].index.year).apply(longest_dry_spell).loc[A.index]
def trend(series, start=None, end=None):
    """Theil–Sen slope (units per decade) and Mann–Kendall-style p-value (Kendall's tau)."""
    s = series.loc[start:end].dropna()
    slope = stats.theilslopes(s.values, s.index)[0] * 10
    tau, p = stats.kendalltau(s.index, s.values)
    return slope, p
def verdict(p, slope):
    if p < 0.05: return "Clear increase" if slope > 0 else "Clear decrease"
    if p < 0.10: return "Possible " + ("increase" if slope > 0 else "decrease") + " (weak evidence)"
    return "No clear trend"
display(Markdown(f"Indicators ready for **{A.index.min()}–{A.index.max()}**: annual total, rainy days, heavy-rain days, rain per rainy day, longest monsoon dry spell."))
'''

def setup(nb, default="Sample district (works offline)"):
    nb.code(SETUP_DATA)
    nb.md("---\n## Step 1 · Choose your data" + DATA_NOTE)
    nb.code(data_cell(default))
    nb.code(HELP5)

# =====================================================================
# S21 · Trend vs variability
# =====================================================================
nb = NB(21, "reading")
nb.md("""
## Why this session matters
After every unusual monsoon someone asks: "Is this climate change?" One year cannot answer that. Rainfall swings a lot
from year to year (**variability**); a **trend** is a slow, steady shift underneath the swings. This session teaches you
to see both.
""")
setup(nb)
nb.md("---\n## Part 1 · How much does rain swing?\nPress ▶.")
nb.code('''
#@title ▶ Year-to-year swings
cv = A.std() / A.mean() * 100
fig, ax = plt.subplots(figsize=(12, 4.5))
ax.bar(A.index, A.values, color=BLUE, alpha=0.75)
ax.axhspan(A.mean() - A.std(), A.mean() + A.std(), color=GREY, alpha=0.15)
ax.axhline(A.mean(), color="black", lw=1)
ax.text(A.index[0], A.mean() + A.std() + 15, "Typical range (mean ± 1 standard deviation)", fontsize=9, color=GREY)
ax.set_ylabel("mm per year"); ax.set_title(f"Annual rainfall swings by about ±{cv:.0f}% around its mean")
plt.tight_layout(); plt.show()
outside = ((A < A.mean() - A.std()) | (A > A.mean() + A.std())).sum()
display(Markdown(f"Standard deviation **{A.std():,.0f} mm** · coefficient of variation **{cv:.0f}%** · "
                 f"**{outside} of {len(A)}** years fall outside the shaded band."))
''')
nb.md("""
About one year in three falls outside the shaded band **by chance alone**. So a very wet or very dry year, on its own,
tells us almost nothing about long-term change.
""")
nb.md("---\n## Part 2 · Smoothing: the moving average\nA **moving average** replaces each year with the average of the years around it, so the swings cancel out. Press ▶ and change the window.")
nb.code('''
#@title ▶ Moving average { run: "auto" }
window_years = 11 #@param {type:"slider", min:1, max:21, step:2}
ma = A.rolling(window_years, center=True).mean()
fig, ax = plt.subplots(figsize=(12, 4.5))
ax.bar(A.index, A.values, color=BLUE, alpha=0.35)
ax.plot(ma.index, ma.values, color=ORANGE, lw=3)
ax.set_ylabel("mm per year"); ax.set_title(f"{window_years}-year moving average (orange)")
plt.tight_layout(); plt.show()
''')
nb.md("""
With a window of 1 you see every swing. With 11 years, the line wanders far less. If it still rises or falls steadily,
that is a hint of a trend, which we will test properly next session.
""")
nb.md("---\n## Part 3 · Total rain is not the only signal\nPress ▶ to look at **rainy days** and **rain per rainy day** as well.")
nb.code('''
#@title ▶ Three indicators { run: "auto" }
indicator = "Rainy days per year" #@param ["Annual total (mm)", "Rainy days per year", "Rain per rainy day (mm)", "Heavy-rain days per year"]
S = {"Annual total (mm)": A, "Rainy days per year": RD, "Rain per rainy day (mm)": SDII, "Heavy-rain days per year": HD}[indicator]
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(S.index, S.values, "o-", color=TEAL, alpha=0.6); ax.plot(S.index, S.rolling(11, center=True).mean(), color=ORANGE, lw=3)
ax.set_title(f"{indicator}, with 11-year moving average"); plt.tight_layout(); plt.show()
''')
nb.md("""
In many places the **total** barely changes while the **number of rainy days falls** and each rainy day gets **wetter**.
Fewer, heavier rains are harder to use and more likely to flood, even when the total looks "normal".

### ⏭️ Next
Open the **Practice activity** and measure variability yourself.
""")
built.append(nb.save(OUT))

nb = NB(21, "practice")
nb.md("Use the sample district record.")
setup(nb)
nb.code('''
#@title ▶ Explorer
display(pd.DataFrame({"Total (mm)": A.round(1), "Rainy days": RD, "Heavy days": HD}).T)
''')
num_q(nb, "Q1 · Standard deviation", "What is the **standard deviation** of annual totals (mm)?", "A.std()", 0.01, "{:,.1f}", "In a spreadsheet: STDEV.S of the annual totals.")
num_q(nb, "Q2 · Coefficient of variation", "What is the **coefficient of variation** (standard deviation ÷ mean × 100, %)?", "A.std() / A.mean() * 100", 0.02, "{:.1f}%")
num_q(nb, "Q3 · Outside the band", "How many years fall **outside mean ± 1 standard deviation**?", "((A < A.mean() - A.std()) | (A > A.mean() + A.std())).sum()", 0, "{:.0f}")
num_q(nb, "Q4 · Biggest jump", "Which **year** had the biggest change in total from the year before (up or down)?", "A.diff().abs().idxmax()", 0, "{:.0f}")
num_q(nb, "Q5 · Rainy days then and now", "Average rainy days per year in **2015–2024** minus the average in **1981–1990**?", "RD.loc[2015:2024].mean() - RD.loc[1981:1990].mean()", 0.03, "{:+.1f}")
choice_q(nb, "Q6 · One wet year", "This year's rainfall was the highest in a decade. What can you conclude about climate change from this alone?",
         ["It proves rainfall is increasing", "Very little: one year is within natural variability", "It proves the climate is stable"],
         "Very little: one year is within natural variability")
built.append(nb.save(OUT))

# =====================================================================
# S22 · How many years are enough?
# =====================================================================
nb = NB(22, "reading")
nb.md("""
## Why this session matters
Pick the right ten years and you can "show" rainfall rising. Pick another ten and it is falling. This session shows how
the **period** you choose changes the answer, and how to test whether a trend is real or could easily be chance.
""")
setup(nb)
nb.md("""
---
## Part 1 · Two tools
- **Sen's slope** (Theil–Sen): the median of the slopes between every pair of years. Unlike a straight-line fit, one extreme
  year cannot drag it around. We report it in **mm per decade**.
- **Mann–Kendall test**: counts how often later years are higher than earlier ones. Its **p-value** answers:
  *"If there were no trend at all, how often would chance alone produce a pattern this strong?"*
  A p-value below **0.05** (5%) is the usual bar for "clear evidence".
""")
nb.code('''
#@title ▶ Trend over a period you choose { run: "auto" }
start_year = 1981 #@param {type:"slider", min:1981, max:2014, step:1}
end_year = 2024 #@param {type:"slider", min:1991, max:2024, step:1}
if end_year - start_year < 9:
    display(Markdown("Choose at least 10 years."))
else:
    s = A.loc[start_year:end_year]; slope, p = trend(A, start_year, end_year)
    med_slope, inter = stats.theilslopes(s.values, s.index)[:2]
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.bar(A.index, A.values, color=GREY, alpha=0.3); ax.bar(s.index, s.values, color=BLUE, alpha=0.8)
    ax.plot(s.index, inter + med_slope * s.index, color=ORANGE, lw=3)
    ax.set_title(f"{start_year}–{end_year}: {slope:+.0f} mm per decade · p = {p:.2f} → {verdict(p, slope)}")
    ax.set_ylabel("mm per year"); plt.tight_layout(); plt.show()
''')
nb.md("""
Try 2010–2019, then 2014–2024, then the full record. Short windows give large, confident-looking slopes that flip sign.
The **p-value** usually stays high for short windows: the test is telling you *not to trust them*.
""")
nb.md("---\n## Part 2 · Every 10-year window\nPress ▶. Each arrow is the Sen's slope of one 10-year window.")
nb.code('''
#@title ▶ All 10-year windows
rows = []
for y0 in range(A.index.min(), A.index.max() - 8):
    sl, p = trend(A, y0, y0 + 9); rows.append((y0, sl, p))
W = pd.DataFrame(rows, columns=["start", "slope", "p"]).set_index("start")
fig, ax = plt.subplots(figsize=(12, 4))
ax.bar(W.index, W.slope, color=[BLUE if v > 0 else ORANGE for v in W.slope])
ax.axhline(trend(A)[0], color="black", lw=2); ax.text(W.index[0], trend(A)[0] + 15, "whole-record slope", fontsize=9)
ax.set_xlabel("First year of the 10-year window"); ax.set_ylabel("mm per decade")
ax.set_title(f"{(W.slope > 0).sum()} windows say 'rising', {(W.slope < 0).sum()} say 'falling'")
plt.tight_layout(); plt.show()
''')
nb.md("""
### The rule of thumb
Climate scientists use **at least 30 years** for trends, and they report the **uncertainty** (the p-value or a confidence
range) along with the slope. Be suspicious of any claim built on a short period, especially one that starts or ends on an
unusual year.

### ⏭️ Next
Open the **Practice activity** and test trends yourself.
""")
built.append(nb.save(OUT))

nb = NB(22, "practice")
nb.md("Use the sample district. Slopes are Sen's slopes in mm per decade; p-values come from the Mann–Kendall (Kendall's tau) test.")
setup(nb)
nb.code('''
#@title ▶ Trend calculator { run: "auto" }
start_year = 1981 #@param {type:"slider", min:1981, max:2014, step:1}
end_year = 2024 #@param {type:"slider", min:1991, max:2024, step:1}
indicator = "Annual total (mm)" #@param ["Annual total (mm)", "Rainy days", "Heavy-rain days", "Rain per rainy day (mm)"]
S = {"Annual total (mm)": A, "Rainy days": RD, "Heavy-rain days": HD, "Rain per rainy day (mm)": SDII}[indicator]
sl, p = trend(S, start_year, end_year)
display(Markdown(f"**{indicator}, {start_year}–{end_year}:** Sen's slope **{sl:+.2f} per decade**, p = **{p:.3f}** → {verdict(p, sl)}"))
''')
num_q(nb, "Q1 · Full-record slope", "Sen's slope of the **annual total**, 1981–2024 (mm per decade)?", "trend(A)[0]", 0.03, "{:+.1f}")
choice_q(nb, "Q2 · Is it clear?", "Is the 1981–2024 annual-total trend clear at the 0.05 level?",
         ["Yes, p < 0.05", "No, p ≥ 0.05"], '="Yes, p < 0.05" if trend(A)[1] < 0.05 else "No, p ≥ 0.05"')
num_q(nb, "Q3 · A short window", "Sen's slope of the annual total for **2011–2020** (mm per decade)?", "trend(A, 2011, 2020)[0]", 0.03, "{:+.1f}")
num_q(nb, "Q4 · Rainy days", "Sen's slope of **rainy days**, 1981–2024 (days per decade)?", "trend(RD)[0]", 0.03, "{:+.2f}")
choice_q(nb, "Q5 · Rainy-day verdict", "What is the verdict for rainy days, 1981–2024?",
         ["Clear increase", "Clear decrease", "Possible increase (weak evidence)", "Possible decrease (weak evidence)", "No clear trend"],
         "=verdict(trend(RD)[1], trend(RD)[0])")
choice_q(nb, "Q6 · Why 30 years?", "Why do climate scientists prefer at least 30 years of data for a trend?",
         ["Older data is more accurate", "Short periods are dominated by natural year-to-year swings", "Computers need 30 values"],
         "Short periods are dominated by natural year-to-year swings")
built.append(nb.save(OUT))

# =====================================================================
# S23 · Extremes, dry spells and droughts
# =====================================================================
nb = NB(23, "reading")
nb.md("""
## Why this session matters
For people on the ground, climate change shows up less in yearly totals and more in **how** rain arrives: longer gaps
between rains, and heavier bursts when it does rain. This session measures both, decade by decade.
""")
setup(nb)
nb.md("---\n## Part 1 · Decade by decade\nPress ▶.")
nb.code('''
#@title ▶ Indicators by decade
dec = (A.index // 10) * 10
T = pd.DataFrame({"Total (mm/yr)": A.groupby(dec).mean(), "Rainy days/yr": RD.groupby(dec).mean(),
                  "Rain per rainy day (mm)": SDII.groupby(dec).mean(), "Heavy days/yr": HD.groupby(dec).mean(),
                  "Longest monsoon dry spell (days)": DRY.groupby(dec).mean()}).round(1)
T.index = [f"{d}s" for d in T.index]; display(T)
display(Markdown("*The 2020s include only the years available so far.*"))
''')
nb.md("---\n## Part 2 · The longest dry spell in each monsoon\nA **dry spell** here means consecutive days with less than 2.5 mm, during June–September. Long breaks in the monsoon stress crops. Press ▶.")
nb.code('''
#@title ▶ Monsoon dry spells
fig, ax = plt.subplots(figsize=(12, 4))
ax.bar(DRY.index, DRY.values, color=ORANGE); ax.plot(DRY.index, DRY.rolling(11, center=True).mean(), color="black", lw=2)
sl, p = trend(DRY)
ax.set_ylabel("Days"); ax.set_title(f"Longest June–September dry spell each year · {sl:+.1f} days per decade, p = {p:.2f}")
plt.tight_layout(); plt.show()
''')
nb.md("---\n## Part 3 · Trend table for all indicators\nPress ▶. This is the table you will build for your own district in the workshop.")
nb.code('''
#@title ▶ Trend table
rows = []
for name, S in [("Annual total (mm)", A), ("Rainy days", RD), ("Rain per rainy day (mm)", SDII), ("Heavy-rain days", HD), ("Longest monsoon dry spell (days)", DRY)]:
    sl, p = trend(S); rows.append((name, round(sl, 2), round(p, 3), verdict(p, sl)))
display(pd.DataFrame(rows, columns=["Indicator", "Sen's slope per decade", "p-value", "Verdict"]).set_index("Indicator"))
''')
nb.md("""
### Drought is more than low rain
Meteorologists call a season with much less rain than normal a **meteorological drought** (IMD uses a deficit of 20% or more).
**Agricultural drought** is when soils are too dry for crops, which depends on timing and dry spells as well as totals.
**Hydrological drought** is when rivers, tanks, reservoirs and groundwater run low, often months later.

### ⏭️ Next
Open the **Practice activity** and compare decades yourself.
""")
built.append(nb.save(OUT))

nb = NB(23, "practice")
nb.md("Use the sample district.")
setup(nb)
nb.code('''
#@title ▶ Explorer
display(pd.DataFrame({"Rainy days": RD, "Rain per rainy day (mm)": SDII.round(1), "Heavy days": HD, "Longest monsoon dry spell": DRY}).T)
''')
num_q(nb, "Q1 · Rain per rainy day", "Average **rain per rainy day** in 2015–2024 (mm)?", "SDII.loc[2015:2024].mean()", 0.02, "{:.1f}")
num_q(nb, "Q2 · Change", "By how many mm has rain per rainy day changed from 1981–1990 to 2015–2024?", "SDII.loc[2015:2024].mean() - SDII.loc[1981:1990].mean()", 0.05, "{:+.1f}")
num_q(nb, "Q3 · Longest dry spell", "Which **year** had the longest June–September dry spell?", "DRY.idxmax()", 0, "{:.0f}", "If two years tie, enter the first.")
num_q(nb, "Q4 · Heavy days recently", "How many heavy-rain days (≥ 64.5 mm) in **2015–2024** in total?", "HD.loc[2015:2024].sum()", 0, "{:.0f}")
choice_q(nb, "Q5 · Rainy days verdict", "Over 1981–2024, rainy days show:",
         ["Clear increase", "Clear decrease", "Possible increase (weak evidence)", "Possible decrease (weak evidence)", "No clear trend"], "=verdict(trend(RD)[1], trend(RD)[0])")
choice_q(nb, "Q6 · Which drought?", "A district had normal rainfall, but its reservoir and wells are very low because of three earlier dry years. This is:",
         ["Meteorological drought", "Agricultural drought", "Hydrological drought"], "Hydrological drought")
built.append(nb.save(OUT))

# =====================================================================
# S24 · Reading climate claims critically
# =====================================================================
nb = NB(24, "reading")
nb.md("""
## Why this session matters
Charts can mislead without a single false number. This session shows the three most common tricks in climate and water
charts, using the sample district, and how to fix each one. It also decodes the careful language of IPCC reports.
""")
setup(nb)
nb.md("---\n## Trick 1 · The truncated axis\nPress ▶ and switch between the misleading and the honest version.")
nb.code('''
#@title ▶ Trick 1 { run: "auto" }
show_honest_version = False #@param {type:"boolean"}
s = A.loc[2015:2024]
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(s.index, s.values, color=RED if not show_honest_version else BLUE)
if not show_honest_version:
    ax.set_ylim(s.min() * 0.97, s.max() * 1.01); ax.set_title("RAINFALL COLLAPSES!")
else:
    ax.set_ylim(0, s.max() * 1.1); ax.set_title(f"Annual rainfall 2015–2024: ups and downs around {A.mean():,.0f} mm")
ax.set_ylabel("mm"); plt.tight_layout(); plt.show()
''')
nb.md("**Fix:** bar charts must start at zero, because the bar's length *is* the value. (Line charts may zoom in, if the axis is clearly labelled.)")
nb.md("---\n## Trick 2 · The cherry-picked period\nPress ▶.")
nb.code('''
#@title ▶ Trick 2 { run: "auto" }
show_honest_version = False #@param {type:"boolean"}
rows = [(y0, trend(A, y0, y0 + 9)[0]) for y0 in range(A.index.min(), A.index.max() - 8)]
worst = min(rows, key=lambda r: r[1])[0]
fig, ax = plt.subplots(figsize=(10, 4))
if not show_honest_version:
    s = A.loc[worst:worst + 9]; sl, inter = stats.theilslopes(s.values, s.index)[:2]
    ax.plot(s.index, s.values, "o-", color=RED); ax.plot(s.index, inter + sl * s.index, color="black", lw=2)
    ax.set_title(f"Rainfall falling fast: {sl*10:+.0f} mm per decade! ({worst}–{worst+9})")
else:
    sl, inter = stats.theilslopes(A.values, A.index)[:2]; full, p = trend(A)
    ax.plot(A.index, A.values, "o-", color=BLUE, alpha=0.6); ax.plot(A.index, inter + sl * A.index, color="black", lw=2)
    ax.axvspan(worst, worst + 9, color=RED, alpha=0.1)
    ax.set_title(f"Full record: {full:+.0f} mm per decade, p = {p:.2f} ({verdict(p, full)}). Shaded: the cherry-picked decade")
ax.set_ylabel("mm per year"); plt.tight_layout(); plt.show()
''')
nb.md("**Fix:** show the full record, and say how you chose the period before you look at the result.")
nb.md("---\n## Trick 3 · Two axes, one false story\nPress ▶.")
nb.code('''
#@title ▶ Trick 3 { run: "auto" }
show_honest_version = False #@param {type:"boolean"}
yrs = A.index.values
other = pd.Series(np.linspace(100, 260, len(yrs)) + np.random.default_rng(3).normal(0, 8, len(yrs)), index=yrs)   # e.g. vehicles (illustrative)
if not show_honest_version:
    fig, ax = plt.subplots(figsize=(10, 4)); ax2 = ax.twinx()
    ax.plot(A.index, A.rolling(5, center=True).mean(), color=BLUE, lw=3); ax2.plot(other.index, other.values, color=RED, lw=3)
    ax.set_ylim(A.rolling(5, center=True).mean().min() * 0.98, A.rolling(5, center=True).mean().max() * 1.02); ax2.set_ylim(other.min() * 0.9, other.max() * 1.05)
    ax.set_title("Vehicles rise, rainfall follows!"); ax.set_yticks([]); ax2.set_yticks([])
else:
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax.plot(A.index, A.values, "o-", color=BLUE, alpha=0.6); ax.set_ylim(0, A.max() * 1.1); ax.set_title("Annual rainfall (mm)")
    ax2.plot(other.index, other.values, color=RED); ax2.set_ylim(0, other.max() * 1.1); ax2.set_title("Registered vehicles (thousands, illustrative)")
plt.tight_layout(); plt.show()
''')
nb.md("""
**Fix:** two different quantities get two panels, each with a labelled axis starting at a sensible value. Two lines moving
together does not show that one causes the other.
""")
nb.md("""
---
## Reading IPCC language
IPCC reports use exact words for likelihood:

| Term | Probability |
|---|---|
| Virtually certain | 99–100% |
| Very likely | 90–100% |
| Likely | 66–100% |
| About as likely as not | 33–66% |
| Unlikely | 0–33% |
| Very unlikely | 0–10% |

They also state **confidence** (low, medium, high) in a finding, based on the evidence and how much experts agree.
"Heavy precipitation has *likely* increased over most land areas" is a careful, global statement; it does not say that
every district has more heavy rain.

### ⏭️ Next
Open the **Practice activity** and spot the tricks yourself.
""")
built.append(nb.save(OUT))

nb = NB(24, "practice")
nb.md("Identify what is wrong with each description, then check two numbers.")
setup(nb)
choice_q(nb, "Q1 · Chart A", "A bar chart of five years of rainfall has a y-axis running from 950 to 1,050 mm, making one year look half as wet as another. The problem is:",
         ["Cherry-picked period", "Truncated axis", "Two axes", "Wrong unit"], "Truncated axis")
choice_q(nb, "Q2 · Chart B", 'A post shows rainfall from 2012 to 2018 only, with the caption "rainfall has been falling for years". The problem is:',
         ["Cherry-picked period", "Truncated axis", "Two axes", "Wrong unit"], "Cherry-picked period")
choice_q(nb, "Q3 · Chart C", "A chart overlays rainfall and mobile phone users on two different y-axes, scaled so the lines match. The problem is:",
         ["Cherry-picked period", "Truncated axis", "Two axes implying a link", "Wrong unit"], "Two axes implying a link")
nb.code('''
#@title ▶ Find the steepest falling 10-year window
rows = [(y0, trend(A, y0, y0 + 9)[0]) for y0 in range(A.index.min(), A.index.max() - 8)]
W = pd.DataFrame(rows, columns=["First year", "Sen's slope (mm per decade)"]).set_index("First year").round(1)
display(W.T)
''')
num_q(nb, "Q4 · Steepest fall", "What is the **most negative** 10-year slope (mm per decade)?", "min(trend(A, y0, y0 + 9)[0] for y0 in range(A.index.min(), A.index.max() - 8))", 0.03, "{:+.0f}")
num_q(nb, "Q5 · Full record", "What is the slope over the **full record** (mm per decade)?", "trend(A)[0]", 0.03, "{:+.1f}")
choice_q(nb, "Q6 · IPCC words", 'An IPCC statement says an outcome is "likely". What probability does that mean?',
         ["33–66%", "66–100%", "90–100%", "99–100%"], "66–100%")
built.append(nb.save(OUT))

# =====================================================================
# S25 · Workshop: test your district's trend
# =====================================================================
nb = NB(25, "workshop")
nb.md("""
## Workshop brief
Decide, **with evidence**, whether your district's rainfall shows a trend. This is **step 5 of your capstone**.
Remember: "no clear trend" is a perfectly good, honest answer.
""")
setup(nb, "My place (live download from NASA POWER)")
nb.md("---\n## Step 3 · My trend table and chart")
nb.code('''
#@title ▶ Trend verdicts
rows = []
for name, S in [("Annual total (mm)", A), ("Rainy days", RD), ("Rain per rainy day (mm)", SDII), ("Heavy-rain days", HD), ("Longest monsoon dry spell (days)", DRY)]:
    sl, p = trend(S); rows.append((name, round(sl, 2), round(p, 3), verdict(p, sl)))
V = pd.DataFrame(rows, columns=["Indicator", "Sen's slope per decade", "p-value", "Verdict"]).set_index("Indicator"); display(V)
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
for a, (name, S, c) in zip(ax, [("Annual total (mm)", A, BLUE), ("Rainy days", RD, TEAL), ("Rain per rainy day (mm)", SDII, ORANGE)]):
    sl, inter = stats.theilslopes(S.values, S.index)[:2]
    a.plot(S.index, S.values, "o", color=c, alpha=0.6); a.plot(S.index, inter + sl * S.index, color="black", lw=2)
    a.set_title(f"{name}\\n{V.loc[name, 'Verdict']} (p = {V.loc[name, 'p-value']:.2f})", fontsize=11)
fig.suptitle(f"Climate signals: {label.split(' · ')[0]}, {A.index.min()}–{A.index.max()}", fontweight="bold")
plt.tight_layout(); fig.savefig("capstone_step5_trends.png", dpi=150); plt.show()
''')
nb.md("---\n## Step 4 · My verdict card")
nb.code('''
#@title ▶ Trend card (capstone step 5)
my_verdict_in_words = "" #@param {type:"string"}
caveats = "" #@param {type:"string"}
display(Markdown(f"""
## 📈 Climate signals: {label.split(' · ')[0]}
*Capstone step 5 · Water Data Literacy for All*

| Indicator | Sen's slope per decade | p-value | Verdict |
|---|---|---|---|
{chr(10).join(f'| {r[0]} | {r[1]:+.2f} | {r[2]:.3f} | {r[3]} |' for r in V.itertuples())}

**My verdict:** {my_verdict_in_words or "_not written_"}

**Caveats (data source, record length, what the test cannot tell us):** {caveats or "_not written_"}

*Method: Sen's slope; Mann–Kendall (Kendall's tau) test; 'clear' means p < 0.05. Data: {label}.*
"""))
if LAT is None: no("This card uses the sample district. Go back to Step 1 and use your own district.")
''')
nb.md("""
---
## Before you leave
1. Upload the trend figure and a screenshot of the card on CuX (Lab 5).
2. Take the **Module 5 quiz** on CuX.
""")
built.append(nb.save(OUT))
print("\n".join(built))
