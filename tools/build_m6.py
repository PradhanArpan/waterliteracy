"""Module 6 · From Data to Dashboard (Sessions 26–30)."""
import os
from nbkit import NB
from datakit import SETUP_DATA, data_cell, DATA_NOTE, num_q, choice_q

OUT = "notebooks/M6"
os.makedirs(OUT, exist_ok=True)
built = []

FACTS = '''
#@title ▶ Step 2 · Compute the facts (press ▶)
from scipy import stats
A = annual(rain); SW = monsoon(rain)
NORMAL, NORMAL_SW = A.loc[1991:2020].mean(), SW.loc[1991:2020].mean()
DEP = (SW - NORMAL_SW) / NORMAL_SW * 100
RD = (rain >= 2.5).groupby(rain.index.year).sum().loc[A.index]
SDII = A / RD
MON = rain.groupby([rain.index.year, rain.index.month]).sum().groupby(level=1).mean()
TOP = rain.sort_values(ascending=False).head(5)
def trend(series):
    s = series.dropna(); return stats.theilslopes(s.values, s.index)[0] * 10, stats.kendalltau(s.index, s.values)[1]
def verdict(p, slope):
    return ("Clear increase" if slope > 0 else "Clear decrease") if p < 0.05 else "No clear trend"
def cat(d): return "Large deficient" if d <= -60 else "Deficient" if d <= -20 else "Normal" if d < 20 else "Excess" if d < 60 else "Large excess"
CATC = {"Large deficient": "#8E2C2C", "Deficient": RED, "Normal": GREY, "Excess": BLUE, "Large excess": "#1B3F66"}
PLACE = label.split(" · ")[0]
display(Markdown(f"Facts ready for **{PLACE}**: normal {NORMAL:,.0f} mm/year; latest monsoon ({DEP.index[-1]}) {DEP.iloc[-1]:+.0f}% ({cat(DEP.iloc[-1])})."))
'''

def setup(nb, default="Sample district (works offline)"):
    nb.code(SETUP_DATA)
    nb.md("---\n## Step 1 · Choose your data" + DATA_NOTE)
    nb.code(data_cell(default))
    nb.code(FACTS)

# =====================================================================
# S26 · Honest charts
# =====================================================================
nb = NB(26, "reading")
nb.md("""
## Why this session matters
A chart is often the only part of your work people look at. In Module 5 you saw charts that mislead. This session turns that
round: five habits that make a water chart **honest and clear**, each shown as a before-and-after.
""")
setup(nb)
nb.md("""
---
## The five habits
1. **The title states the finding**, not just the topic ("Monsoon was 18% below normal in 2023", not "Rainfall 2023").
2. **Bars start at zero.**
3. **Units on every axis** (mm, mm/day, m³/s, %).
4. **Colour means something**: one colour for the main data, a highlight for the point you are making, red/blue only for below/above.
5. **Say where the data came from**, and anything unusual about it.
""")
nb.code('''
#@title ▶ Before and after { run: "auto" }
example = "Title and units" #@param ["Title and units", "Bars from zero", "Meaningful colour", "Pie vs bars"]
show_fixed = False #@param {type:"boolean"}
last = A.iloc[-10:]
fig, ax = plt.subplots(figsize=(10, 4))
if example == "Title and units":
    ax.plot(last.index, last.values, "o-", color=BLUE)
    if show_fixed:
        ax.set_title(f"{PLACE}: {last.idxmax()} was the wettest of the last ten years ({last.max():,.0f} mm)")
        ax.set_ylabel("Rainfall (mm per year)"); ax.text(0, -0.18, f"Source: {label}", transform=ax.transAxes, fontsize=9, color=GREY)
    else:
        ax.set_title("Rainfall")
elif example == "Bars from zero":
    ax.bar(last.index, last.values, color=BLUE)
    ax.set_ylim(0 if show_fixed else last.min() * 0.95, last.max() * 1.05); ax.set_ylabel("mm per year")
    ax.set_title("Bars start at zero: differences shown fairly" if show_fixed else "Exaggerated differences (axis starts high)")
elif example == "Meaningful colour":
    d = DEP.iloc[-10:]
    cols = [RED if v < 0 else BLUE for v in d.values] if show_fixed else plt.cm.rainbow(np.linspace(0, 1, len(d)))
    ax.bar(d.index, d.values, color=cols); ax.axhline(0, color="black", lw=0.8); ax.set_ylabel("Departure from normal (%)")
    ax.set_title("Red = below normal, blue = above" if show_fixed else "Rainbow colours carry no meaning")
else:
    sea = pd.Series({"Winter": MON[[1, 2]].sum(), "Pre-monsoon": MON[[3, 4, 5]].sum(), "SW monsoon": MON[[6, 7, 8, 9]].sum(), "NE monsoon": MON[[10, 11, 12]].sum()})
    if show_fixed:
        ax.barh(sea.index[::-1], sea.values[::-1], color=[GREY, BLUE, GREY, GREY][::-1]); ax.set_xlabel("mm in an average year")
        for i, v in enumerate(sea.values[::-1]): ax.text(v, i, f" {v:,.0f} mm ({v/sea.sum()*100:.0f}%)", va="center")
        ax.set_title("The southwest monsoon brings the most rain")
    else:
        ax.pie(sea.values, labels=sea.index, colors=plt.cm.Set3.colors[:4]); ax.set_title("Seasons")
plt.tight_layout(); plt.show()
''')
nb.md("""
Tick **show_fixed** on and off for each example. Pie charts are hard to read beyond two or three slices; sorted bars with
labels almost always work better.

### ⏭️ Next
Open the **Practice activity** and fix some charts yourself.
""")
built.append(nb.save(OUT))

nb = NB(26, "practice")
nb.md("For each chart description, choose the main problem. Then write a better title.")
setup(nb)
OPTS = ["Title does not state the finding", "Bars do not start at zero", "Missing units", "Colours have no meaning", "No data source"]
choice_q(nb, "Q1", 'A line chart titled "Rainfall data" shows a clear drop in 2023.', OPTS, "Title does not state the finding")
choice_q(nb, "Q2", "A bar chart's y-axis runs from 800 to 1,000 mm.", OPTS, "Bars do not start at zero")
choice_q(nb, "Q3", 'A chart\'s y-axis is labelled "Rain" with numbers 0 to 200, but does not say per day, month or year, or in what unit.', OPTS, "Missing units")
choice_q(nb, "Q4", "An anomaly chart uses a different random colour for each year.", OPTS, "Colours have no meaning")
choice_q(nb, "Q5", "A clear, well-labelled chart of a district's rainfall gives no hint of where the numbers came from.", OPTS, "No data source")
nb.md("### Q6 · Write a finding title\nUsing the sample district, write a title for a chart of the last ten annual totals that **states a finding**, with a number and unit. Press ▶ for feedback.")
nb.code('''
#@title ▶ Check my title
my_title = "" #@param {type:"string"}
import re
if AUTO: my_title = f"{A.iloc[-10:].idxmax()} was the wettest year of the decade at {A.iloc[-10:].max():,.0f} mm"
has_num = bool(re.search(r"\\d", my_title)); has_unit = bool(re.search(r"\\b(mm|%|per cent|percent|days)\\b", my_title, re.I))
long_enough = len(my_title.split()) >= 6
if not my_title.strip(): no("Type a title first.")
elif has_num and has_unit and long_enough: ok("Good: your title states a finding with a number and a unit.")
else: no("Add " + ", ".join(x for x, f in [("a number", has_num), ("a unit (mm, %, days)", has_unit), ("a complete statement (6+ words)", long_enough)] if not f) + ".")
''')
built.append(nb.save(OUT))

# =====================================================================
# S27 · Choosing the right chart
# =====================================================================
nb = NB(27, "reading")
nb.md("""
## Why this session matters
The right chart answers the question at a glance; the wrong one hides it. This session gives you a simple guide for water
data and lets you try each chart on real numbers.
""")
setup(nb)
nb.md("""
---
## A chart guide for water data

| Question | Best chart |
|---|---|
| How has something changed over the years? | **Line** (or bars for yearly totals) |
| What does a typical year look like? | **Bars by month** |
| Was this year above or below normal? | **Anomaly bars** around zero, red and blue |
| How are values spread (light vs heavy days)? | **Histogram** or bars by category |
| How do two places or two sources compare? | **Side-by-side bars** or **two lines** on the same axis |
| What share comes from each season? | **Sorted bars with % labels** (not a pie) |
""")
nb.code('''
#@title ▶ Try a question and a chart { run: "auto" }
question = "Was each monsoon above or below normal?" #@param ["How has annual rainfall changed?", "What does a typical year look like?", "Was each monsoon above or below normal?", "How are rainy days spread by intensity?"]
chart = "Anomaly bars" #@param ["Line", "Bars by month", "Anomaly bars", "Bars by category", "Pie"]
best = {"How has annual rainfall changed?": "Line", "What does a typical year look like?": "Bars by month",
        "Was each monsoon above or below normal?": "Anomaly bars", "How are rainy days spread by intensity?": "Bars by category"}[question]
fig, ax = plt.subplots(figsize=(10, 4))
if chart == "Line": ax.plot(A.index, A.values, "o-", color=BLUE); ax.set_ylabel("mm per year")
elif chart == "Bars by month": ax.bar(range(1, 13), MON.values, color=BLUE); ax.set_xticks(range(1, 13)); ax.set_xticklabels("JFMAMJJASOND"); ax.set_ylabel("mm")
elif chart == "Anomaly bars": ax.bar(DEP.index, DEP.values, color=[RED if v < 0 else BLUE for v in DEP.values]); ax.axhline(0, color="black", lw=0.8); ax.set_ylabel("% from normal")
elif chart == "Bars by category":
    bins = [0.1, 2.5, 15.6, 64.5, 115.6, 204.5, 1e4]; names = ["Very light", "Light", "Moderate", "Heavy", "Very heavy", "Extremely heavy"]
    c = pd.cut(rain[rain > 0], bins, labels=names, right=False).value_counts().reindex(names)
    ax.bar(names, c.values, color=BLUE); ax.set_ylabel("Number of days"); ax.tick_params(axis="x", rotation=25)
else:
    ax.pie(A.iloc[-6:].values, labels=A.index[-6:])
ax.set_title(question); plt.tight_layout(); plt.show()
(ok if chart == best else no)(f"For this question, the best choice is **{best}**." + ("" if chart == best else f" '{chart}' makes it harder to see the answer."))
''')
nb.md("### ⏭️ Next\nOpen the **Practice activity** and match questions to charts.")
built.append(nb.save(OUT))

nb = NB(27, "practice")
nb.md("Choose the best chart type for each question.")
setup(nb)
C = ["Line", "Bars by month", "Anomaly bars", "Histogram or bars by category", "Side-by-side bars", "Pie"]
choice_q(nb, "Q1", "How has the number of rainy days per year changed since 1981?", C, "Line")
choice_q(nb, "Q2", "Which months bring most of the rain in an average year?", C, "Bars by month")
choice_q(nb, "Q3", "Was the last monsoon deficient compared to normal, and how did it compare to recent years?", C, "Anomaly bars")
choice_q(nb, "Q4", "How many days fall into each IMD intensity class?", C, "Histogram or bars by category")
choice_q(nb, "Q5", "How does NASA POWER compare with ERA5 for each season of one year?", C, "Side-by-side bars")
choice_q(nb, "Q6", "Which of these is almost never the best choice for comparing more than three values?", C, "Pie")
built.append(nb.save(OUT))

# =====================================================================
# S28 · Building a dashboard
# =====================================================================
nb = NB(28, "reading")
nb.md("""
## Why this session matters
A **dashboard** is one page that answers a reader's main questions at a glance. This session builds a four-panel water
dashboard in Colab and shows how to make an interactive version in Looker Studio (free) from the same numbers.
""")
setup(nb)
nb.md("""
---
## Part 1 · Plan before you draw
Good dashboards answer **three to five questions**, in reading order: the headline first, the detail after.
For a district water dashboard:

1. **What is normal here?** (the average year, by month)
2. **How was the latest monsoon?** (anomaly bars, recent years)
3. **How heavy does it get?** (wettest days, intensity)
4. **Is anything changing?** (trend of a key indicator)
""")
nb.code('''
#@title ▶ Build the dashboard { run: "auto" }
headline = "" #@param {type:"string"}
fig = plt.figure(figsize=(14, 9))
gs = fig.add_gridspec(3, 2, height_ratios=[0.35, 1, 1])
top = fig.add_subplot(gs[0, :]); top.axis("off")
kpis = [("Normal year", f"{NORMAL:,.0f} mm"), (f"Monsoon {DEP.index[-1]}", f"{DEP.iloc[-1]:+.0f}%"),
        ("Wettest day on record", f"{rain.max():.0f} mm"), ("Rainy days / year", f"{RD.mean():.0f}")]
for i, (k, v) in enumerate(kpis):
    top.text(0.02 + i * 0.25, 0.65, v, fontsize=24, fontweight="bold", color=BLUE, transform=top.transAxes)
    top.text(0.02 + i * 0.25, 0.15, k, fontsize=11, color=GREY, transform=top.transAxes)
a1 = fig.add_subplot(gs[1, 0]); a1.bar(range(1, 13), MON.values, color=BLUE); a1.set_xticks(range(1, 13)); a1.set_xticklabels("JFMAMJJASOND")
a1.set_title("What is normal? Average rain by month (mm)", loc="left")
a2 = fig.add_subplot(gs[1, 1]); d = DEP.iloc[-12:]
a2.bar(d.index, d.values, color=[CATC[cat(v)] for v in d.values]); a2.axhline(0, color="black", lw=0.8)
a2.set_title("How were recent monsoons? % from normal", loc="left")
a3 = fig.add_subplot(gs[2, 0]); a3.barh([f"{x:%d %b %Y}" for x in TOP.index[::-1]], TOP.values[::-1], color=ORANGE)
a3.set_title("How heavy does it get? Five wettest days (mm)", loc="left")
a4 = fig.add_subplot(gs[2, 1]); sl, p = trend(RD); s_, i_ = stats.theilslopes(RD.values, RD.index)[:2]
a4.plot(RD.index, RD.values, "o", color=TEAL, alpha=0.6); a4.plot(RD.index, i_ + s_ * RD.index, color="black", lw=2)
a4.set_title(f"Is anything changing? Rainy days: {verdict(p, sl).lower()} ({sl:+.1f}/decade)", loc="left")
fig.suptitle(headline or f"{PLACE}: water at a glance", fontsize=17, fontweight="bold", x=0.01, ha="left")
fig.text(0.01, 0.005, f"Data: {label}. Normal = 1991–2020. Trend: Sen's slope, Mann–Kendall test.", fontsize=9, color=GREY)
plt.tight_layout(rect=(0, 0.02, 1, 0.96)); fig.savefig("dashboard.png", dpi=150); plt.show()
''')
nb.md("""
### Design notes
- The **numbers strip** at the top answers the headline questions in two seconds.
- Each panel's title **asks its question** and the chart answers it.
- One source note at the bottom covers the whole page.
""")
nb.md("""
---
## Part 2 · An interactive version in Looker Studio
Looker Studio (free, from Google) turns a spreadsheet into an interactive dashboard with filters. Press ▶ to save the
tables it needs, then follow the steps.
""")
nb.code('''
#@title ▶ Save tables for Looker Studio
yearly = pd.DataFrame({"year": A.index, "annual_mm": A.round(1).values, "monsoon_mm": SW.reindex(A.index).round(1).values,
                       "monsoon_departure_pct": DEP.reindex(A.index).round(1).values, "rainy_days": RD.values})
monthly = rain.resample("MS").sum().round(1).rename("rain_mm").rename_axis("month").reset_index()
yearly.to_csv("dashboard_yearly.csv", index=False); monthly.to_csv("dashboard_monthly.csv", index=False)
display(yearly.tail(3))
try:
    from google.colab import files; files.download("dashboard_yearly.csv"); files.download("dashboard_monthly.csv")
except Exception:
    display(Markdown("Saved **dashboard_yearly.csv** and **dashboard_monthly.csv** in the notebook's files."))
''')
nb.md("""
1. Upload both CSV files to Google Drive and open each with Google Sheets.
2. Go to **lookerstudio.google.com → Create → Report**, and add the Sheet as a data source.
3. Add a **scorecard** (normal year), a **bar chart** (monsoon departure by year), a **time series** (monthly rain), and a **date range control**.
4. Give every chart a finding title and add a text box with the data source.
5. **Share → Anyone with the link can view**, and put the link in your capstone.

### ⏭️ Next
Open the **Practice activity** and build your own version.
""")
built.append(nb.save(OUT))

nb = NB(28, "practice")
nb.md("Answer questions about the dashboard, then build your own with a finding headline.")
setup(nb)
choice_q(nb, "Q1 · Reading order", "In a district water dashboard, what should come first?",
         ["The detailed daily table", "A strip of headline numbers", "The data source note", "A map of all of India"], "A strip of headline numbers")
choice_q(nb, "Q2 · Panel for a question", "Which panel best answers 'Was the last monsoon unusual?'",
         ["Average rain by month", "Monsoon departure bars for recent years", "Five wettest days", "Rainy-day trend"], "Monsoon departure bars for recent years")
choice_q(nb, "Q3 · How many questions?", "How many main questions should a one-page dashboard try to answer?",
         ["One", "Three to five", "Ten or more"], "Three to five")
num_q(nb, "Q4 · Headline number", "From the sample district facts: what is the **latest monsoon's departure** from normal (%)?", "DEP.iloc[-1]", 0.03, "{:+.1f}%")
nb.md("### Q5 · Build mine\nWrite a headline that states a finding and press ▶ to draw your dashboard. Save the image for the forum.")
nb.code('''
#@title ▶ My dashboard
my_headline = "" #@param {type:"string"}
fig, ax = plt.subplots(1, 2, figsize=(13, 4))
ax[0].bar(range(1, 13), MON.values, color=BLUE); ax[0].set_xticks(range(1, 13)); ax[0].set_xticklabels("JFMAMJJASOND"); ax[0].set_title("Average rain by month (mm)", loc="left")
d = DEP.iloc[-12:]; ax[1].bar(d.index, d.values, color=[CATC[cat(v)] for v in d.values]); ax[1].axhline(0, color="black", lw=0.8); ax[1].set_title("Monsoon, % from normal", loc="left")
fig.suptitle(my_headline or "Type a finding headline above", fontweight="bold", x=0.01, ha="left")
plt.tight_layout(); fig.savefig("my_dashboard.png", dpi=150); plt.show()
(ok if AUTO or len(my_headline.split()) >= 6 else no)("Saved my_dashboard.png." if (AUTO or len(my_headline.split()) >= 6) else "Write a full-sentence headline (6+ words).")
''')
built.append(nb.save(OUT))

# =====================================================================
# S29 · Data stories and AI tools
# =====================================================================
nb = NB(29, "reading")
nb.md("""
## Why this session matters
Numbers persuade only when someone reads them. A short **data story** puts the key number first, compares it with something
familiar, explains what it means, and is honest about uncertainty. This session also covers using AI tools with water data:
helpful for drafting, risky for facts.
""")
setup(nb)
nb.md("""
---
## Part 1 · The five-part data story
1. **Headline with a number:** "Our district's monsoon was 24% below normal this year."
2. **Comparison:** "That makes it the third deficient monsoon in five years."
3. **Meaning for people:** "Tanks filled late and borewells ran dry by March."
4. **Uncertainty:** "Rainfall varies a lot; one year does not show a trend, but rainy days have fallen since 1981."
5. **Source:** "Data: IMD district rainfall; NASA POWER."
""")
nb.code('''
#@title ▶ Story starter from your data
y = DEP.index[-1]; d = DEP.iloc[-1]
recent = DEP.iloc[-5:].apply(cat)
sl, p = trend(RD)
draft = (f"{PLACE}'s {y} monsoon brought {SW.iloc[-1]:,.0f} mm, {abs(d):.0f}% {'below' if d < 0 else 'above'} the 1991–2020 normal "
         f"of {NORMAL_SW:,.0f} mm ({cat(d).lower()} by IMD's categories). "
         f"In the last five monsoons, {(recent.isin(['Deficient', 'Large deficient'])).sum()} were deficient and {(recent.isin(['Excess', 'Large excess'])).sum()} in excess. "
         f"The wettest single day on record was {rain.max():.0f} mm on {rain.idxmax():%d %B %Y}. "
         f"Since {A.index.min()}, the number of rainy days shows {verdict(p, sl).lower()} ({sl:+.1f} days per decade), "
         f"so a year's total alone may hide how rain is changing. Data: {label}.")
display(Markdown(f"> {draft}\\n\\n*{len(draft.split())} words. This is a starting point: add what it meant for people, in your own words.*"))
''')
nb.md("""
---
## Part 2 · Using AI tools responsibly
AI writing tools can help you draft and simplify, and explain a method. But they can also **invent numbers** that look
plausible. Five rules:

1. **Every number comes from your data, not from the AI.** Paste your numbers in; check every number it writes back.
2. **Ask it to explain, not to decide.** "Explain Sen's slope simply" is fine; "Is my district getting drier?" needs your data.
3. **Do not paste private data** (names, phone numbers, unpublished records).
4. **Say when you used AI**, and for what.
5. **Read the output aloud.** If it sounds too confident about something your data cannot show, cut it.
""")
nb.code('''
#@title ▶ Spot the invented facts
truth = {"normal": NORMAL, "wettest": rain.max(), "year": rain.idxmax().year}
ai_text = (f"{PLACE} receives about {truth['normal']*1.35:,.0f} mm of rain a year. Its wettest day ever was {truth['wettest']:.0f} mm in "
           f"{truth['year']}. Scientists agree rainfall here has increased by 30% because of climate change.")
display(Markdown(f"**An AI tool wrote:**\\n\\n> {ai_text}\\n\\n"
                 f"**Check against the data:** normal is {truth['normal']:,.0f} mm (the AI's figure is 35% too high) · "
                 f"wettest day {truth['wettest']:.0f} mm in {truth['year']} (correct) · "
                 f"'increased by 30%': not supported; the annual trend is {verdict(*trend(A)[::-1]).lower()}."))
''')
nb.md("### ⏭️ Next\nOpen the **Practice activity** and write your own 150-word story.")
built.append(nb.save(OUT))

nb = NB(29, "practice")
nb.md("Write a data story and check it against the five parts. Then spot errors in an AI-written paragraph.")
setup(nb)
nb.md("### Q1 · My 150-word story\nWrite 120–180 words about the sample district (or your own). Press ▶ for automatic checks.")
nb.code('''
#@title ▶ Check my story
my_story = "" #@param {type:"string"}
import re
if AUTO:
    my_story = ("The district's monsoon was 12% below the 1991-2020 normal this year, compared with an average of 700 mm. " * 8) + "Data: NASA POWER."
words = len(my_story.split())
checks = [("120–180 words", 120 <= words <= 180),
          ("Has a number with a unit (mm, %, days)", bool(re.search(r"\\d[\\d,.]*\\s*(mm|%|per cent|days)", my_story, re.I))),
          ("Makes a comparison (normal, average, compared, than, since)", bool(re.search(r"\\b(normal|average|compared|than|since)\\b", my_story, re.I))),
          ("Names a source (IMD, NASA, POWER, ERA5, CWC, data)", bool(re.search(r"\\b(IMD|NASA|POWER|ERA5|CWC|data)\\b", my_story, re.I)))]
display(Markdown(f"**{words} words**\\n\\n" + "\\n".join(f"- {'✅' if c else '❌'} {n}" for n, c in checks)))
(ok if all(c for _, c in checks) else no)("All checks passed. Post your story in the forum." if all(c for _, c in checks) else "Fix the items marked ❌.")
''')
nb.code('''
#@title ▶ The AI paragraph
ai = (f"The district gets {NORMAL*1.35:,.0f} mm of rain in a normal year. Its wettest day was {rain.max():.0f} mm in {rain.idxmax().year}. "
      f"The monsoon of {DEP.index[-1]} was {abs(DEP.iloc[-1]) + 15:.0f}% {'below' if DEP.iloc[-1] < 0 else 'above'} normal.")
display(Markdown(f"> {ai}"))
''')
choice_q(nb, "Q2 · First sentence", "Is the AI's **normal annual rainfall** correct?", ["Correct", "Wrong"], "Wrong", "Compare with NORMAL (1991–2020 average).")
choice_q(nb, "Q3 · Second sentence", "Is the AI's **wettest day** correct?", ["Correct", "Wrong"], "Correct")
choice_q(nb, "Q4 · Third sentence", "Is the AI's **monsoon departure** correct?", ["Correct", "Wrong"], "Wrong", "Compare with DEP for the latest year.")
choice_q(nb, "Q5 · Good practice", "Which use of an AI tool is most responsible?",
         ["Ask it for your district's rainfall figures", "Paste your verified numbers and ask it to simplify your wording", "Let it decide whether there is a trend"],
         "Paste your verified numbers and ask it to simplify your wording")
built.append(nb.save(OUT))

# =====================================================================
# S30 · Capstone workshop
# =====================================================================
nb = NB(30, "workshop")
nb.md("""
## Capstone: My District's Water Story
This notebook puts your five capstone steps together into **one shareable page**. Run each step, fill in your words, and
download the finished dashboard. Then submit it on CuX and review two classmates' work.

**You will need:** your district name, its area (km²), IMD's normal rainfall (Module 1), and your notes from the
workshops in Modules 2–5.
""")
setup(nb, "My place (live download from NASA POWER)")
nb.md("---\n## Step 3 · Your words")
nb.code('''
#@title ▶ My text { run: "auto" }
district_name = "" #@param {type:"string"}
headline = "" #@param {type:"string"}
data_story_150_words = "" #@param {type:"string"}
what_people_experienced = "" #@param {type:"string"}
data_notes_and_limits = "" #@param {type:"string"}
NAME = district_name or PLACE
if AUTO:
    headline = "The sample district's monsoon swings widely, and rainy days are getting fewer"
    data_story_150_words = "Practice text."
words = len(data_story_150_words.split())
display(Markdown(f"Story length: **{words} words** " + ("✅" if 120 <= words <= 180 else "(aim for 120–180)")))
''')
nb.md("---\n## Step 4 · Build the page")
nb.code('''
#@title ▶ Build My District's Water Story
import textwrap
sl_a, p_a = trend(A); sl_r, p_r = trend(RD)
ev = rain.idxmax()
fig = plt.figure(figsize=(16.5, 11.7))      # A3 landscape
gs = fig.add_gridspec(4, 3, height_ratios=[0.32, 1, 1, 0.75], hspace=0.55, wspace=0.28)
t = fig.add_subplot(gs[0, :]); t.axis("off")
for i, (k, v) in enumerate([("Normal year (1991–2020)", f"{NORMAL:,.0f} mm"), (f"Monsoon {DEP.index[-1]} vs normal", f"{DEP.iloc[-1]:+.0f}%"),
                            ("Wettest day on record", f"{rain.max():.0f} mm"), ("Rainy days per year", f"{RD.mean():.0f}"),
                            ("Annual total trend", verdict(p_a, sl_a))]):
    t.text(0.01 + i * 0.2, 0.62, v, fontsize=21, fontweight="bold", color=BLUE, transform=t.transAxes)
    t.text(0.01 + i * 0.2, 0.12, k, fontsize=11, color=GREY, transform=t.transAxes)
a = fig.add_subplot(gs[1, 0]); a.bar(range(1, 13), MON.values, color=BLUE); a.set_xticks(range(1, 13)); a.set_xticklabels("JFMAMJJASOND")
a.set_title("1 · What is normal here? (mm by month)", loc="left", fontsize=12)
a = fig.add_subplot(gs[1, 1]); d = DEP.iloc[-15:]; a.bar(d.index, d.values, color=[CATC[cat(v)] for v in d.values]); a.axhline(0, color="black", lw=0.8)
[a.axhline(y, color=GREY, ls="--", lw=0.8) for y in (-20, 20)]; a.set_title("2 · Recent monsoons (% from normal)", loc="left", fontsize=12)
a = fig.add_subplot(gs[1, 2]); w = rain[ev - pd.Timedelta(days=10): ev + pd.Timedelta(days=10)]
a.bar(w.index, w.values, color=[RED if x == ev else BLUE for x in w.index]); a.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
a.tick_params(axis="x", rotation=30); a.set_title(f"3 · Biggest event: {rain[ev]:.0f} mm on {ev:%d %b %Y}", loc="left", fontsize=12)
for k, (S, nm, c) in enumerate([(A, "Annual total (mm)", BLUE), (RD, "Rainy days", TEAL), (SDII, "Rain per rainy day (mm)", ORANGE)]):
    a = fig.add_subplot(gs[2, k]); s_, i_ = stats.theilslopes(S.values, S.index)[:2]; sl, p = trend(S)
    a.plot(S.index, S.values, "o", color=c, alpha=0.55, ms=4); a.plot(S.index, i_ + s_ * S.index, color="black", lw=2)
    a.set_title(f"4 · {nm}: {verdict(p, sl).lower()}", loc="left", fontsize=12)
tx = fig.add_subplot(gs[3, :]); tx.axis("off")
story = textwrap.fill(data_story_150_words or "(Write your 150-word data story in Step 3.)", 190)
people = textwrap.fill("What people experienced: " + (what_people_experienced or "(add from news or local knowledge)"), 190)
tx.text(0, 1, story, va="top", fontsize=11, transform=tx.transAxes)
tx.text(0, 0.38, people, va="top", fontsize=11, style="italic", transform=tx.transAxes)
tx.text(0, 0.02, f"Data: {label}. Normal = 1991–2020 average; categories: IMD; trends: Sen's slope, Mann–Kendall (p < 0.05 = clear). "
        f"{data_notes_and_limits}", fontsize=9, color=GREY, transform=tx.transAxes)
fig.suptitle(headline or f"{NAME}: water story", fontsize=22, fontweight="bold", x=0.01, ha="left", y=0.995)
fig.text(0.99, 0.995, "My District's Water Story · Water Data Literacy for All · CHRIST CuX", ha="right", va="top", fontsize=9, color=GREY)
fig.savefig("My_District_Water_Story.png", dpi=150, bbox_inches="tight"); fig.savefig("My_District_Water_Story.pdf", bbox_inches="tight")
plt.show()
''')
nb.md("---\n## Step 5 · Download and submit")
nb.code('''
#@title ▶ Download my capstone
try:
    from google.colab import files; files.download("My_District_Water_Story.png"); files.download("My_District_Water_Story.pdf")
except Exception:
    display(Markdown("Saved **My_District_Water_Story.png** and **.pdf** in the notebook's files."))
problems = [m for m, bad in [("Using the sample district: download your own district in Step 1", LAT is None and not AUTO),
                             ("Write a headline that states a finding", len(headline.split()) < 6),
                             ("Story should be 120–180 words", not (120 <= len(data_story_150_words.split()) <= 180) and not AUTO)] if bad]
(ok if not problems else no)("Ready to submit." if not problems else "Before submitting: " + "; ".join(problems) + ".")
''')
nb.md("""
---
## Peer review rubric (use it on two classmates' dashboards)

| Criterion | Weight | Look for |
|---|---|---|
| Correct use and citation of data | 25% | Source named; units right; own district used |
| Accuracy of analysis | 25% | Numbers match the data; categories and return periods used correctly |
| Honest interpretation of trends and limits | 20% | Says "no clear trend" when p ≥ 0.05; mentions data limits |
| Clarity of visual design | 15% | Finding headline; bars from zero; labelled axes |
| Quality of the data story | 15% | Number first, comparison, meaning for people, source |

**Submit on CuX:** the PNG or PDF, plus the Looker Studio link if you made one. Then review two classmates using this rubric.
Congratulations on finishing the course!
""")
built.append(nb.save(OUT))
print("\n".join(built))
