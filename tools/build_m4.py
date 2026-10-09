"""Module 4 · Rivers, Reservoirs and Floods (Sessions 16–20)."""
import os
from nbkit import NB
from datakit import SETUP_DATA, data_cell, DATA_NOTE, num_q, choice_q

OUT = "notebooks/M4"
os.makedirs(OUT, exist_ok=True)
built = []

HYDRO = '''
#@title ▶ Load the storm-and-river model (press ▶)
PATTERN = np.array([0.10, 0.20, 0.30, 0.20, 0.12, 0.08])     # share of the storm falling in each of 6 hours
def storm_hydrograph(storm_mm=80, area_km2=250, runoff_coeff=0.4, base_flow=5.0, hours=96):
    """Hourly rain (mm) and river flow (m³/s) at the catchment outlet, using a triangular unit hydrograph.
    Illustrative teaching model, not a design tool."""
    t = np.arange(hours)
    rain_h = np.zeros(hours); rain_h[2:8] = storm_mm * PATTERN
    eff = rain_h * runoff_coeff                                  # mm that runs off
    tp = max(2.0, 1.0 + 0.35 * np.sqrt(area_km2))                # hours to peak for 1 mm of runoff
    tb = 2.67 * tp                                               # base time of the unit hydrograph
    qp = 2 * area_km2 * 1000 / (tb * 3600)                       # m³/s per mm of runoff
    uh = np.interp(t, [0, tp, tb], [0, qp, 0], right=0)
    q = np.convolve(eff, uh)[:hours] + base_flow
    return pd.DataFrame({"hour": t, "rain_mm": rain_h, "flow_m3s": q}).set_index("hour")
def summary(h, base_flow=5.0):
    rc = (h.rain_mm * h.index).sum() / h.rain_mm.sum()           # centre of the storm (hour)
    pk = h.flow_m3s.idxmax()
    vol = ((h.flow_m3s - base_flow).clip(lower=0) * 3600).sum() / 1e6
    return {"peak": h.flow_m3s.max(), "peak_hour": pk, "lag": pk - rc, "volume_mcm": vol}
display(Markdown("✅ Model ready."))
'''

RATING = '''
#@title ▶ The station's rating curve (press ▶)
A_COEF, H0, B_EXP = 40.0, 1.2, 1.6          # illustrative station: flow = 40 × (level − 1.2)^1.6
WARNING_M, DANGER_M = 5.0, 6.0
def flow_from_level(h): return A_COEF * np.clip(np.asarray(h, float) - H0, 0, None) ** B_EXP
def level_from_flow(q): return H0 + (np.asarray(q, float) / A_COEF) ** (1 / B_EXP)
display(Markdown(f"Rating curve: **Q = {A_COEF:g} × (h − {H0})^{B_EXP}** (Q in m³/s, h in m). Warning {WARNING_M} m, danger {DANGER_M} m."))
'''

RESERVOIR = '''
#@title ▶ Run the reservoir model (press ▶)
GROSS, DEAD = 1200.0, 200.0                  # MCM at full reservoir level (FRL), and dead storage
LIVE_CAP = GROSS - DEAD                      # 1,000 MCM live capacity
CATCH_KM2, RUNOFF_C = 3000, 0.31            # catchment (km²) and share of rain that reaches the reservoir
RELEASE_DRY, RELEASE_WET = 3.6, 1.0          # releases + evaporation, MCM/day: Nov–May (irrigation, supply) and Jun–Oct
def run_reservoir(r):
    r = r.fillna(0)["2013-06-01":"2024-12-31"]
    inflow = r / 1000 * CATCH_KM2 * 1e6 * RUNOFF_C / 1e6           # MCM per day
    live, out = 300.0, []
    for d, q in inflow.items():
        live = live + q - (RELEASE_WET if 6 <= d.month <= 10 else RELEASE_DRY)
        spill = max(live - LIVE_CAP, 0); live = min(max(live, 0), LIVE_CAP)
        out.append((d, q, live, spill))
    df = pd.DataFrame(out, columns=["date", "inflow_mcm", "live_mcm", "spill_mcm"]).set_index("date")
    df["pct_live"] = df.live_mcm / LIVE_CAP * 100
    return df
RES = run_reservoir(sample)
display(Markdown(f"Illustrative reservoir: gross capacity **{GROSS:,.0f} MCM**, dead storage {DEAD:,.0f} MCM, live capacity **{LIVE_CAP:,.0f} MCM**. "
                 f"Inflow from the sample district's rain over a {CATCH_KM2:,} km² catchment."))
'''

# =====================================================================
# S16 · Catchments and hydrographs
# =====================================================================
nb = NB(16, "reading")
nb.md("""
## Why this session matters
Rain falls on a whole **catchment**: all the land that drains to one point on a river. How big it is, and how much of the rain
runs off, decides how high and how fast the river rises. The graph of river flow over time is a **hydrograph**, the most
important picture in flood work.
""")
nb.code(SETUP_DATA)
nb.code(HYDRO)
nb.md("""
---
## Part 1 · A storm becomes a flood wave
Press ▶, then move the sliders. *This is a simple teaching model of a catchment, not a real river.*
""")
nb.code('''
#@title ▶ Storm to hydrograph { run: "auto" }
storm_mm = 80 #@param {type:"slider", min:10, max:250, step:5}
area_km2 = 250 #@param {type:"slider", min:10, max:2000, step:10}
runoff_coeff = 0.4 #@param {type:"slider", min:0.05, max:0.95, step:0.05}
h = storm_hydrograph(storm_mm, area_km2, runoff_coeff, hours=72); s = summary(h)
fig, ax = plt.subplots(figsize=(11, 4.8)); ax2 = ax.twinx()
ax2.bar(h.index, h.rain_mm, color=BLUE, alpha=0.5, width=0.9); ax2.set_ylim(h.rain_mm.max() * 3.5, 0); ax2.set_ylabel("Rain (mm/hour)", color=BLUE)
ax.plot(h.index, h.flow_m3s, color="black", lw=2); ax.set_ylabel("River flow (m³/s)"); ax.set_xlabel("Hours from start")
ax.annotate(f"Peak {s['peak']:,.0f} m³/s", xy=(s["peak_hour"], s["peak"]), xytext=(15, -10), textcoords="offset points")
ax.set_title(f"Lag {s['lag']:.1f} h · runoff volume {s['volume_mcm']:.2f} MCM")
plt.tight_layout(); plt.show()
''')
nb.md("""
### Read the hydrograph
- **Rising limb**: flow climbs as runoff arrives. **Peak**: the highest flow. **Falling limb (recession)**: the slow drain-down.
- **Lag time**: hours from the centre of the storm to the peak. Bigger catchments have longer lags.
- **Runoff volume**: the area under the curve above base flow. It equals **runoff coefficient × rain depth × area**.
""")
nb.md("---\n## Part 2 · Check the water balance\nPress ▶ to confirm that the volume under the hydrograph matches the rain that ran off.")
nb.code('''
#@title ▶ Water balance { run: "auto" }
by_formula = runoff_coeff * storm_mm / 1000 * area_km2 * 1e6 / 1e6
display(Markdown(f"Runoff coefficient × rain × area = {runoff_coeff} × {storm_mm} mm × {area_km2} km² = **{by_formula:.2f} MCM** · "
                 f"area under the hydrograph = **{s['volume_mcm']:.2f} MCM**"))
''')
nb.md("""
---
## Part 3 · What changes the flood?

| Change | Peak | Lag |
|---|---|---|
| Bigger storm | Higher | About the same |
| Bigger catchment | Much higher | Longer |
| More paving (higher runoff coefficient) | Higher | About the same in this model; shorter in real cities (drains are fast) |
| Forest and wetlands (lower coefficient) | Lower | Longer |

### ⏭️ Next
Open the **Practice activity** and read a hydrograph yourself.
""")
built.append(nb.save(OUT))

nb = NB(16, "practice")
nb.md("Read the hydrograph of a fixed storm: **80 mm** over **250 km²**, runoff coefficient **0.4**.")
nb.code(SETUP_DATA)
nb.code(HYDRO)
nb.code('''
#@title ▶ The event
h = storm_hydrograph(80, 250, 0.4); s = summary(h)
ax = h.flow_m3s.plot(color="black", lw=2, figsize=(10, 4)); ax.set_xlabel("Hours from start"); ax.set_ylabel("Flow (m³/s)")
ax.set_xticks(range(0, 97, 6)); ax.grid(alpha=0.3); ax.set_title("Hydrograph at the outlet"); plt.tight_layout(); plt.show()
t = h.iloc[::2][["rain_mm", "flow_m3s"]].round(1).T; display(t)
''')
num_q(nb, "Q1 · Peak flow", "What is the **peak flow** (m³/s)?", "s['peak']", 0.03, "{:,.0f}")
num_q(nb, "Q2 · Peak hour", "At which **hour** does the peak occur?", "s['peak_hour']", 0.05, "{:.0f}", "Look for the largest flow in the table.")
num_q(nb, "Q3 · Runoff volume", "What is the **runoff volume** (MCM)? Use runoff coefficient × rain (m) × area (m²) ÷ 1,000,000.", "0.4 * 0.080 * 250e6 / 1e6", 0.02, "{:.2f}")
choice_q(nb, "Q4 · More paving", "If the runoff coefficient rises from 0.4 to 0.8 (more roofs and roads), the peak flow will:",
         ["Stay the same", "Roughly double", "Halve"], "Roughly double", "Twice the runoff from the same storm doubles the flood wave in this model.")
choice_q(nb, "Q5 · Bigger catchment", "Compared with a 50 km² catchment, a 1,000 km² catchment with the same storm will have:",
         ["A shorter lag time", "A longer lag time", "The same lag time"], "A longer lag time", "Water has further to travel.")
built.append(nb.save(OUT))

# =====================================================================
# S17 · From river level to river flow
# =====================================================================
nb = NB(17, "reading")
nb.md("""
## Why this session matters
Flood warnings talk about **levels** ("6.2 m, above danger"). Dam releases and flood forecasts talk about **flows**
("2 lakh cusecs"). A **rating curve** connects the two. This session shows how, and why the link is not a straight line.
""")
nb.code(SETUP_DATA)
nb.code(RATING)
nb.md("""
---
## Part 1 · How flow is measured
Flow (discharge) = **water speed × cross-section area**. Hydrologists wade or boat across the river, measure depth and speed
at many points, and add up the pieces. They repeat this at many different levels, then fit a **rating curve**.
""")
nb.code('''
#@title ▶ Flow = speed × area { run: "auto" }
river_width_m = 40 #@param {type:"slider", min:5, max:300, step:5}
average_depth_m = 3 #@param {type:"slider", min:0.2, max:12, step:0.2}
average_speed_ms = 1.5 #@param {type:"slider", min:0.1, max:4, step:0.1}
q = river_width_m * average_depth_m * average_speed_ms
display(Markdown(f"{river_width_m} m × {average_depth_m} m × {average_speed_ms} m/s = **{q:,.0f} m³/s** = **{q*35.3147:,.0f} cusecs**"))
''')
nb.md("---\n## Part 2 · The rating curve\nPress ▶. *Illustrative station.*")
nb.code('''
#@title ▶ Level to flow { run: "auto" }
level_m = 4.0 #@param {type:"slider", min:1.2, max:7.5, step:0.1}
hh = np.linspace(H0, 7.5, 200)
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(flow_from_level(hh), hh, color="black", lw=2)
ax.axhline(WARNING_M, color=ORANGE, ls="--"); ax.text(10, WARNING_M + 0.05, "Warning level", color=ORANGE)
ax.axhline(DANGER_M, color=RED, ls="--"); ax.text(10, DANGER_M + 0.05, "Danger level", color=RED)
qq = float(flow_from_level(level_m)); ax.plot(qq, level_m, "o", color=BLUE, ms=9)
ax.set_xlabel("Flow (m³/s)"); ax.set_ylabel("Level at the gauge (m)")
ax.set_title(f"At {level_m:.1f} m the river carries about {qq:,.0f} m³/s")
plt.tight_layout(); plt.show()
display(Markdown(f"At the danger level ({DANGER_M} m) the flow is about **{float(flow_from_level(DANGER_M)):,.0f} m³/s**."))
''')
nb.md("""
### Why it curves
As the river rises it gets **wider and faster**, so each extra metre carries more water than the last. Going from 2 m to 4 m
does not double the flow; it multiplies it several times. That is why a rise of "just half a metre" near the danger level
matters so much.

Rating curves **shift** when the riverbed erodes, silts up or is dredged, so agencies re-measure them regularly.
""")
nb.md("---\n## Part 3 · From flow back to level\nA dam upstream announces a release. How high will the river get here? Press ▶.")
nb.code('''
#@title ▶ Flow to level { run: "auto" }
release = 1500 #@param {type:"number"}
unit = "m³/s" #@param ["m³/s", "cusecs"]
q = release if unit == "m³/s" else release / 35.3147
lv = float(level_from_flow(q))
status = "above the DANGER level" if lv > DANGER_M else "above the warning level" if lv > WARNING_M else "below the warning level"
display(Markdown(f"{release:,} {unit} → about **{lv:.2f} m** at this gauge: **{status}**."))
''')
nb.md("### ⏭️ Next\nOpen the **Practice activity** and convert levels and flows yourself.")
built.append(nb.save(OUT))

nb = NB(17, "practice")
nb.md("Use the illustrative station's rating curve: **Q = 40 × (h − 1.2)^1.6**.")
nb.code(SETUP_DATA)
nb.code(RATING)
num_q(nb, "Q1 · Speed × area", "A river section is 60 m wide, 2.5 m deep on average, flowing at 1.2 m/s. What is the flow (m³/s)?", "60 * 2.5 * 1.2", 0.01, "{:,.0f}")
num_q(nb, "Q2 · Flow at 3 m", "What is the flow when the gauge reads **3.0 m** (m³/s)?", "float(flow_from_level(3.0))", 0.02, "{:,.0f}", "40 × (3.0 − 1.2)^1.6")
num_q(nb, "Q3 · Flow at danger", "What is the flow at the **danger level, 6.0 m** (m³/s)?", "float(flow_from_level(6.0))", 0.02, "{:,.0f}")
num_q(nb, "Q4 · How many times more?", "The level rises from **2 m to 4 m**. How many **times** larger is the flow?", "float(flow_from_level(4.0) / flow_from_level(2.0))", 0.03, "{:.1f}")
num_q(nb, "Q5 · Level from flow", "A flow of **1,000 m³/s** reaches the station. What level will the gauge show (m)?", "float(level_from_flow(1000))", 0.01, "{:.2f}", "Rearrange: h = 1.2 + (Q ÷ 40)^(1/1.6)")
num_q(nb, "Q6 · Cusecs", "A dam releases **50,000 cusecs**. What level will this gauge show (m)?", "float(level_from_flow(50000 / 35.3147))", 0.01, "{:.2f}", "Convert cusecs to m³/s first (÷ 35.3).")
built.append(nb.save(OUT))

# =====================================================================
# S18 · Reservoirs and storage bulletins
# =====================================================================
nb = NB(18, "reading")
nb.md("""
## Why this session matters
Every week, CWC and state departments publish how full the big reservoirs are. These numbers drive news about drinking water,
irrigation and inter-state sharing. This session teaches you to read a reservoir bulletin using an illustrative reservoir.
""")
nb.code(SETUP_DATA)
nb.code(RESERVOIR)
nb.md("""
---
## Part 1 · The words on a bulletin

| Term | Meaning |
|---|---|
| **FRL** (Full Reservoir Level) | The highest normal water level, in metres above sea level |
| **Gross storage** | All the water in the reservoir |
| **Dead storage** | Water below the lowest outlet: it cannot be released |
| **Live storage** | Water that can actually be used = gross − dead |
| **% of live capacity** | Live storage today ÷ live storage at FRL × 100. This is the % in most headlines |
| **Inflow / outflow** | Water coming in from the catchment / going out to canals, rivers, cities, evaporation |
""")
nb.md("---\n## Part 2 · A reservoir through the years\nPress ▶. *Illustrative reservoir driven by the sample district's rainfall.*")
nb.code('''
#@title ▶ Storage over time { run: "auto" }
show_from = 2019 #@param {type:"slider", min:2014, max:2023, step:1}
r = RES[f"{show_from}-06-01":]
fig, ax = plt.subplots(figsize=(12, 4.5))
ax.fill_between(r.index, r.pct_live, color=TEAL, alpha=0.35); ax.plot(r.index, r.pct_live, color=TEAL)
ax.axhline(100, color=GREY, ls="--"); ax.set_ylim(0, 110); ax.set_ylabel("% of live capacity")
for y in range(show_from, 2025): ax.axvline(pd.Timestamp(f"{y}-06-01"), color=GREY, lw=0.6, alpha=0.5)
ax.set_title("Fills in the monsoon, drains through the dry season")
plt.tight_layout(); plt.show()
''')
nb.md("---\n## Part 3 · Write this week's bulletin\nChoose a date and press ▶.")
nb.code('''
#@title ▶ Bulletin for a date { run: "auto" }
bulletin_date = "2024-01-15" #@param {type:"date"}
d = pd.Timestamp(bulletin_date)
if d not in RES.index or (d - pd.DateOffset(years=1)) not in RES.index:
    display(Markdown("Choose a date between June 2014 and December 2024."))
else:
    now, last = RES.loc[d], RES.loc[d - pd.DateOffset(years=1)]
    past = [RES.loc[d - pd.DateOffset(years=k), "pct_live"] for k in range(1, 11) if (d - pd.DateOffset(years=k)) in RES.index]
    display(Markdown(f"""
| Reservoir bulletin · {d:%d %B %Y} | |
|---|---|
| Live storage | **{now.live_mcm:,.0f} MCM** ({now.live_mcm/28.3168:,.1f} TMC) |
| % of live capacity | **{now.pct_live:.0f}%** |
| Same date last year | {last.pct_live:.0f}% |
| Average of past {len(past)} years, same date | {np.mean(past):.0f}% |
| Compared with that average | **{now.pct_live - np.mean(past):+.0f} percentage points** |
"""))
''')
nb.md("""
### Reading it like an expert
"42% full" is only meaningful **compared to something**: the same week last year, and the average for that week.
In January, 42% may be normal; in September, after the monsoon, it would be worrying. (Remember Module 1's four questions.)

Also watch the difference between **%** and **percentage points**: from 40% to 50% is a rise of 10 percentage points, or 25%.

### ⏭️ Next
Open the **Practice activity** and read the bulletin numbers yourself.
""")
built.append(nb.save(OUT))

nb = NB(18, "practice")
nb.md("Use the illustrative reservoir (live capacity 1,000 MCM).")
nb.code(SETUP_DATA)
nb.code(RESERVOIR)
nb.code('''
#@title ▶ Explorer { run: "auto" }
look_up_date = "2024-01-15" #@param {type:"date"}
d = pd.Timestamp(look_up_date)
display(RES.loc[d - pd.Timedelta(days=3): d + pd.Timedelta(days=3)].round(1) if d in RES.index else Markdown("Choose a date between June 2013 and December 2024."))
wy = RES["2023-06-01":"2024-05-31"]
display(Markdown(f"Water year June 2023 – May 2024: highest live storage **{wy.live_mcm.max():,.1f} MCM** on {wy.live_mcm.idxmax():%d %b %Y}; "
                 f"lowest **{wy.live_mcm.min():,.1f} MCM** on {wy.live_mcm.idxmin():%d %b %Y}; total inflow **{wy.inflow_mcm.sum():,.1f} MCM**."))
''')
num_q(nb, "Q1 · Live capacity", "Gross storage at FRL is 1,200 MCM and dead storage is 200 MCM. What is the **live capacity** (MCM)?", "1200 - 200", 0, "{:,.0f}")
num_q(nb, "Q2 · Live storage", "What is the **live storage on 15 January 2024** (MCM)?", "RES.loc['2024-01-15', 'live_mcm']", 0.01, "{:,.1f}")
num_q(nb, "Q3 · Percent full", "What **% of live capacity** is that?", "RES.loc['2024-01-15', 'pct_live']", 0.01, "{:.1f}%")
num_q(nb, "Q4 · Versus last year", "By how many **percentage points** is 15 Jan 2024 above (+) or below (−) 15 Jan 2023?",
      "RES.loc['2024-01-15', 'pct_live'] - RES.loc['2023-01-15', 'pct_live']", 0.03, "{:+.1f}", "Subtract last year's % from this year's %.")
num_q(nb, "Q5 · Monsoon inflow", "What was the **total inflow** from 1 June to 30 September 2023 (MCM)?", "RES['2023-06-01':'2023-09-30'].inflow_mcm.sum()", 0.01, "{:,.1f}")
num_q(nb, "Q6 · In TMC", "Convert the live capacity (1,000 MCM) to **TMC**.", "1000 / 28.316846592", 0.01, "{:.1f}")
built.append(nb.save(OUT))

# =====================================================================
# S19 · Floods: river, flash and urban
# =====================================================================
nb = NB(19, "reading")
nb.md("""
## Why this session matters
Not all floods come from big rivers. A city can flood in an hour from a cloudburst that a river would barely notice.
This session compares the three kinds of flood and uses the **rational method**, the formula engineers use to size city drains.
""")
nb.code(SETUP_DATA)
nb.md("""
---
## Part 1 · Three kinds of flood

| | River flood | Flash flood | Urban flood |
|---|---|---|---|
| Cause | Days of rain over a large catchment | Very intense rain on steep, small catchments | Intense rain on paved areas with limited drains |
| Rise | Hours to days | Minutes to an hour | Minutes to hours |
| Warning | Often a day or more (CWC forecasts) | Very little | Little; depends on rainfall nowcasts |
| Key data | River levels, upstream rain | Hourly rainfall, radar | Hourly rainfall, drain capacity, land cover |
""")
nb.md("""
---
## Part 2 · The rational method
For a small area, the **peak runoff** is roughly:

**Q = C × i × A ÷ 3.6**

where Q is in m³/s, **C** is the runoff coefficient (0 to 1), **i** is rainfall intensity in **mm per hour**, and **A** is area in km².
""")
nb.code('''
#@title ▶ How much paving can the drain handle? { run: "auto" }
paved_percent = 60 #@param {type:"slider", min:0, max:100, step:5}
rain_mm_per_hour = 40 #@param {type:"slider", min:5, max:120, step:5}
area_km2 = 2.0 #@param {type:"slider", min:0.2, max:10, step:0.2}
drain_capacity_m3s = 10 #@param {type:"number"}
C = (paved_percent * 0.85 + (100 - paved_percent) * 0.20) / 100
Q = C * rain_mm_per_hour * area_km2 / 3.6
pcts = np.arange(0, 101, 5); Qs = [(p * 0.85 + (100 - p) * 0.2) / 100 * rain_mm_per_hour * area_km2 / 3.6 for p in pcts]
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(pcts, Qs, color=BLUE, lw=2); ax.axhline(drain_capacity_m3s, color=RED, ls="--"); ax.text(1, drain_capacity_m3s * 1.03, "Drain capacity", color=RED)
ax.plot(paved_percent, Q, "o", color="black", ms=9)
ax.set_xlabel("Area covered by roofs and roads (%)"); ax.set_ylabel("Peak runoff (m³/s)")
ax.set_title(f"C = {C:.2f}, peak = {Q:.1f} m³/s: " + ("FLOODS" if Q > drain_capacity_m3s else "drain copes"))
plt.tight_layout(); plt.show()
''')
nb.md("""
Typical runoff coefficients: roofs and roads **0.75–0.95**, lawns and parks **0.1–0.3**, forest **0.05–0.25**.
Here we mix paved (0.85) and green (0.20) areas by their share.
""")
nb.md("""
---
## Part 3 · Daily rain hides hourly bursts
IMD reports rain **per day**. Drains respond to rain **per hour**. 100 mm spread over 24 hours averages about 4 mm per hour,
but if most of it falls in one hour, the drain sees something like 50 mm per hour. Press ▶.
""")
nb.code('''
#@title ▶ Same day, two patterns { run: "auto" }
day_total_mm = 100 #@param {type:"slider", min:20, max:250, step:5}
share_in_worst_hour = 0.5 #@param {type:"slider", min:0.05, max:0.9, step:0.05}
even = day_total_mm / 24; burst = day_total_mm * share_in_worst_hour
for name, i in [("Spread evenly", even), ("One intense hour", burst)]:
    q = 0.6 * i * 2.0 / 3.6
    display(Markdown(f"**{name}:** {i:.1f} mm/h → peak runoff from 2 km² of mixed city (C = 0.6): **{q:.1f} m³/s**"))
''')
nb.md("### ⏭️ Next\nOpen the **Practice activity** and size a drain yourself.")
built.append(nb.save(OUT))

nb = NB(19, "practice")
nb.md("Use **Q = C × i × A ÷ 3.6** (Q in m³/s, i in mm/hour, A in km²).")
nb.code(SETUP_DATA)
num_q(nb, "Q1 · Rural catchment", "C = 0.3, i = 40 mm/h, A = 2 km². What is the peak runoff (m³/s)?", "0.3 * 40 * 2 / 3.6", 0.01, "{:.2f}")
num_q(nb, "Q2 · Same area, paved", "Now C = 0.85 (same storm, same area). Peak runoff (m³/s)?", "0.85 * 40 * 2 / 3.6", 0.01, "{:.2f}")
num_q(nb, "Q3 · Mixed land", "An area is 60% paved (C = 0.85) and 40% green (C = 0.20). What is its combined C?", "0.6 * 0.85 + 0.4 * 0.20", 0.01, "{:.2f}")
num_q(nb, "Q4 · Intensity", "**120 mm** of rain falls in **3 hours**. What is the average intensity (mm/h)?", "120 / 3", 0.01, "{:.0f}")
choice_q(nb, "Q5 · Will it flood?", "A drain can carry 10 m³/s. The area is 2 km², C = 0.85, and the storm gives 40 mm/h. Does the drain overflow?",
         ["Yes", "No"], "Yes", "Q = 0.85 × 40 × 2 ÷ 3.6 ≈ 18.9 m³/s, nearly twice the capacity.")
choice_q(nb, "Q6 · Which flood?", "Heavy rain for four days over a 20,000 km² basin raises a big river slowly over two days. This is a:",
         ["Flash flood", "River flood", "Urban flood"], "River flood")
built.append(nb.save(OUT))

# =====================================================================
# S20 · Workshop: reconstruct a flood event
# =====================================================================
nb = NB(20, "workshop")
nb.md("""
## Workshop brief
Choose one **extreme rain event** in your district's record and tell its story with data. This is **step 4 of your capstone**.
""")
nb.code(SETUP_DATA)
nb.code(data_cell("My place (live download from NASA POWER)", "Type your district, State"))
nb.md("---\n## Step 2 · Choose the event")
nb.code('''
#@title ▶ Pick one of the ten wettest days { run: "auto" }
which = 1 #@param {type:"slider", min:1, max:10, step:1}
top = rain.sort_values(ascending=False).head(10)
day = top.index[which - 1]
def term(x):
    return ("Extremely heavy" if x >= 204.5 else "Very heavy" if x >= 115.6 else "Heavy" if x >= 64.5 else "Moderate" if x >= 15.6 else "Light")
t = top.round(1).to_frame("mm"); t["IMD term"] = top.apply(term); t.index = t.index.strftime("%d %b %Y"); display(t)
display(Markdown(f"Chosen event: **{day:%d %B %Y}**, {rain[day]:.1f} mm ({term(rain[day])} rain)."))
''')
nb.md("---\n## Step 3 · The event in context")
nb.code('''
#@title ▶ Event chart and numbers { run: "auto" }
district_area_km2 = 4000 #@param {type:"number"}
w = rain[day - pd.Timedelta(days=10): day + pd.Timedelta(days=10)]
three = rain[day - pd.Timedelta(days=1): day + pd.Timedelta(days=1)].sum()
five = rain[day - pd.Timedelta(days=2): day + pd.Timedelta(days=2)].sum()
month_normal = rain[rain.index.month == day.month].groupby(rain[rain.index.month == day.month].index.year).sum().mean()
vol_mcm = rain[day] / 1000 * district_area_km2
fig, ax = plt.subplots(figsize=(11, 4))
ax.bar(w.index, w.values, color=[RED if d == day else BLUE for d in w.index])
ax.set_ylabel("mm/day"); ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.set_title(f"{label.split(' · ')[0]}: rain around {day:%d %b %Y}")
plt.tight_layout(); fig.savefig("capstone_step4_event.png", dpi=150); plt.show()
display(Markdown(f"""
| Event fact | Value |
|---|---|
| Rain on the day | **{rain[day]:.1f} mm** ({term(rain[day])}) |
| 3-day and 5-day totals | {three:.0f} mm and {five:.0f} mm |
| Compared with a normal {day:%B} | {rain[day] / month_normal * 100:.0f}% of the whole month's normal ({month_normal:.0f} mm) in one day |
| Water falling on the district that day | about **{vol_mcm:,.0f} MCM** ({vol_mcm/28.3168:,.1f} TMC) |
| Rank in the record | {which} of {len(rain):,} days |
"""))
''')
nb.md("---\n## Step 4 · What might a town have felt?\nAssume a share of the day's rain fell in the worst hour (state your assumption).")
nb.code('''
#@title ▶ Urban runoff estimate { run: "auto" }
share_in_worst_hour = 0.35 #@param {type:"slider", min:0.1, max:0.8, step:0.05}
town_area_km2 = 5 #@param {type:"number"}
town_C = 0.7 #@param {type:"slider", min:0.2, max:0.95, step:0.05}
i = rain[day] * share_in_worst_hour
Q = town_C * i * town_area_km2 / 3.6
display(Markdown(f"If {share_in_worst_hour*100:.0f}% fell in one hour: **{i:.0f} mm/h** → peak runoff from a {town_area_km2} km² town (C = {town_C}) of about **{Q:,.0f} m³/s**. "
                 "*This is an assumption-based estimate, not a measurement: grid data cannot show hourly peaks.*"))
''')
nb.md("---\n## Step 5 · Event story card")
nb.code('''
#@title ▶ Event card (capstone step 4)
what_happened = "" #@param {type:"string"}
news_source = "" #@param {type:"string"}
display(Markdown(f"""
## 🌊 Extreme event: {day:%d %B %Y}, {label.split(' · ')[0]}
*Capstone step 4 · Water Data Literacy for All*

- **{rain[day]:.0f} mm** in one day ({term(rain[day])} rain), {rain[day] / month_normal * 100:.0f}% of a normal {day:%B}
- **{five:.0f} mm** over five days
- About **{vol_mcm:,.0f} MCM** of water fell on the district that day
- Estimated town peak runoff: about **{Q:,.0f} m³/s** (assuming {share_in_worst_hour*100:.0f}% of the day's rain in one hour)

**What happened (from news or local knowledge):** {what_happened or "_not written_"}

*Sources: {label}; {news_source or "news source not given"}.*
"""))
if LAT is None: no("This card uses the sample district. Go back to Step 1 and use your own district.")
''')
nb.md("""
---
## Before you leave
1. Upload the event chart and a screenshot of the card on CuX (Lab 4).
2. Take the **Module 4 quiz** on CuX.
""")
built.append(nb.save(OUT))
print("\n".join(built))
