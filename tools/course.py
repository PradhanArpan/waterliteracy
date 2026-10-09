"""Single source of truth for the course map.
Syllabus text, course planner and hub sessions.json are all generated from this file."""

COURSE = {
    "code": "WDL",
    "title": "Hydroinformatics in a Changing Climate: Water Data Literacy for All",
    "short": "Water Data Literacy for All",
    "dept": "Department of Civil Engineering",
    "school": "School of Engineering and Technology",
    "instructor": "Dr Arpan Pradhan",
    "year": "2026-27",
}

# Minutes per planner item (videos capped at 5 min)
DUR = {
    "promo": 2, "intro": 1,
    "concept": 5, "walkthrough": 4,
    "reading": 25, "practice": 20, "reference": 5,
    "ws_video": 4, "workshop": 40, "quiz": 15,
}

MODULES = [
  {"n": 1, "title": "The Water Cycle as Data", "co": "CO1",
   "about": "What gets measured in the water cycle, by whom and how often: rain gauges, river gauges, reservoirs and satellites; rainfall depth as a volume of water; units used in water reporting (mm, m, m³/s, MCM, TMC, MLD, LPCD); time resolution of water records; reading rain and river gauge records.",
   "sessions": [
     ("Water as a data problem", "Monsoon headlines decoded",
      "Why water is now a data problem; what hydroinformatics is; the water cycle as measurable quantities; who measures water in India",
      "Spot the water numbers in a news report"),
     ("Rain is a volume; water units", "One storm on your rooftop and your city",
      "1 mm on 1 m² = 1 litre; rainfall depth × area = volume; litres, m³, MCM, TMC, MLD, LPCD",
      "Rooftop, campus and city storm volumes; unit conversions"),
     ("Reading a rain gauge record; time scales", "IMD's 8:30 am rainfall day",
      "Rain gauges and the IMD rainfall day; rainy-day definition (2.5 mm); daily, weekly, monthly and seasonal totals; IMD seasons",
      "Find the wettest day, count rainy days, compare time scales"),
     ("Reading a river gauge record", "When a river crosses the danger mark",
      "River stage; warning and danger levels; rainfall–river response; lag time; rise and recession",
      "Measure lag time and days above danger level"),
     ("Workshop: My district in numbers", "Lab 1 · quiz · capstone step 1",
      "Choose your capstone district; convert its rainfall into volumes; first water facts sheet",
      None),
   ]},
  {"n": 2, "title": "Finding and Trusting Water Data", "co": "CO1, CO2",
   "about": "India's water data ecosystem (IMD, CWC, India-WRIS, state portals, NASA GPM, ERA5); ground stations, gridded and satellite products; metadata; downloading a rainfall dataset; missing values, gaps, outliers and error flags; basic data quality checks.",
   "sessions": [
     ("India's water data ecosystem", "Who measures India's water?",
      "IMD, CWC, India-WRIS, state portals, global datasets; what each publishes and at what resolution",
      "Match datasets to the questions they can answer"),
     ("Stations, grids and satellites", "Same storm, three different numbers",
      "Point gauges vs gridded rainfall vs satellite estimates; spatial resolution; strengths and limits of each",
      "Compare a station, a grid cell and a satellite estimate"),
     ("Downloading a rainfall dataset", "Your district's rainfall, decades back",
      "Finding and downloading open rainfall data; file formats (CSV); reading metadata and units",
      "Load your district's rainfall file and describe it"),
     ("Missing values, gaps and errors", "When a gauge goes quiet: the -999 problem",
      "Missing-data flags; gaps; duplicates; impossible values; outliers vs real extremes",
      "Find and flag problems in a messy record"),
     ("Workshop: Quality-check your district's data", "Lab 2 · quiz · capstone step 2",
      "Download, check and document your capstone dataset",
      None),
   ]},
  {"n": 3, "title": "Reading Rainfall", "co": "CO2, CO3",
   "about": "Daily, monthly, seasonal and annual totals; long-period average and the monsoon normal; anomalies and IMD excess/deficit categories; rainfall intensity and IMD heavy-rainfall categories; extremes; return periods explained simply.",
   "sessions": [
     ("Totals, averages and the normal", "What does a \"normal monsoon\" mean?",
      "Annual and seasonal totals; long-period average (LPA); mean vs median",
      "Compute your district's monsoon normal"),
     ("Anomalies: excess and deficit", "Reading IMD's excess and deficit categories",
      "Departure from normal (%); IMD categories; wet and dry years",
      "Classify each year as excess, normal or deficient"),
     ("Extremes and intensity", "Heavy, very heavy, extremely heavy",
      "IMD daily rainfall intensity categories; wettest days; how much of the year falls in a few days",
      "Find your district's heaviest days and their share of the year"),
     ("Return periods made simple", "Is a \"100-year storm\" really rare?",
      "Ranking extremes; return period and probability; why rare events still happen often somewhere",
      "Estimate return periods from annual maxima"),
     ("Workshop: Your district's rainfall profile", "Lab 3 · quiz · capstone step 3",
      "Build the rainfall section of your capstone",
      None),
   ]},
  {"n": 4, "title": "Rivers, Reservoirs and Floods", "co": "CO1, CO3",
   "about": "Catchments and hydrographs; river stage and discharge; rating curves in simple terms; reservoir storage and bulletins; flood forecasts and warnings; river floods, flash floods and urban flooding.",
   "sessions": [
     ("Catchments and hydrographs", "Where does your rain go?",
      "Catchment area; runoff; the shape of a hydrograph; peak and lag",
      "Read peak, lag and volume from a hydrograph"),
     ("From river level to river flow", "Danger level vs discharge",
      "Stage vs discharge; rating curve idea; m³/s; flood bulletins",
      "Convert levels to flow with a simple rating curve"),
     ("Reservoirs and storage bulletins", "Reading a reservoir level report",
      "Live storage, gross storage, FRL; MCM and TMC; inflow and outflow",
      "Track a reservoir through a monsoon"),
     ("Floods: river, flash and urban", "Why cities flood without a big river",
      "Types of floods; impervious surfaces; drainage capacity; warning lead time",
      "Compare rural and urban runoff for the same storm"),
     ("Workshop: Reconstruct a flood event", "Lab 4 · quiz · capstone step 4",
      "Pick one extreme event in your district and tell its data story",
      None),
   ]},
  {"n": 5, "title": "Climate Signals in Water Data", "co": "CO3, CO4",
   "about": "Trend versus variability; record length and confidence; moving averages; simple trend tests; changing extremes, dry spells and droughts; reading climate statements and spotting misleading charts and headlines.",
   "sessions": [
     ("Trend vs variability", "One wet year is not climate change",
      "Year-to-year variability; moving averages; what a trend is",
      "Smooth a rainfall series and describe the pattern"),
     ("How many years are enough?", "10 vs 30 vs 100 years of rainfall",
      "Record length; start and end-point effects; simple trend tests and confidence",
      "See how a trend changes with the period chosen"),
     ("Extremes, dry spells and droughts", "Fewer rainy days, heavier bursts?",
      "Changes in heavy-rain days; dry spells; drought indicators in simple terms",
      "Count heavy-rain days and dry spells by decade"),
     ("Reading climate claims critically", "Fixing a misleading headline chart",
      "Truncated axes, cherry-picked periods, wrong baselines; how to read IPCC-style statements",
      "Critique and redraw a misleading chart"),
     ("Workshop: Test your district's trend", "Lab 5 · quiz · capstone step 5",
      "Decide, with evidence, whether your district shows a trend",
      None),
   ]},
  {"n": 6, "title": "From Data to Dashboard", "co": "CO5",
   "about": "Principles of honest data visualisation; choosing the right chart; dashboard design in Looker Studio or Colab; writing a data story for decision-makers and the public; responsible use of AI tools with water data; capstone completion and peer review.",
   "sessions": [
     ("Honest charts", "Same data, two stories",
      "Axes, baselines, colour and labels; what makes a chart honest",
      "Fix three water charts"),
     ("Choosing the right chart", "The right picture for rainfall",
      "Bars, lines, anomaly charts, maps; matching chart to question",
      "Pick and build the best chart for four questions"),
     ("Building a dashboard", "A one-page water story",
      "Dashboard layout; Looker Studio and Colab options; connecting a Sheet",
      "Build a draft dashboard from your district data"),
     ("Data stories and AI tools", "Explaining water to a panchayat or a newspaper",
      "Writing for non-experts; uncertainty; using AI tools responsibly with data",
      "Write and review a 150-word data story"),
     ("Capstone workshop and submission", "My District's Water Story · peer review",
      "Finish, submit and peer-review the capstone dashboard",
      None),
   ]},
]

COS = [
  ("CO1", "Explain how rainfall, river flow, reservoir storage and floods are measured, by which agencies in India, and in what units."),
  ("CO2", "Locate, download and check the quality of open water datasets such as IMD, India-WRIS, CWC and NASA GPM."),
  ("CO3", "Compute and interpret basic water statistics, including totals, anomalies, extremes and return periods."),
  ("CO4", "Distinguish long-term climate trends from year-to-year variability, and critically evaluate claims made in news and reports."),
  ("CO5", "Build and present a simple, honest dashboard and data story using water data."),
]


def sessions():
    """Flat list of 30 sessions with numbering."""
    out, k = [], 0
    for m in MODULES:
        for j, (title, hook, topics, practice) in enumerate(m["sessions"], 1):
            k += 1
            out.append({"num": k, "module": m["n"], "idx": j, "title": title, "hook": hook,
                        "topics": topics, "practice": practice,
                        "workshop": practice is None, "co": m["co"]})
    return out


def planner_rows():
    """(module label, item type, title, minutes) rows in the SSR planner layout."""
    rows = [("", "Promo Video", f"Promo Video - {COURSE['short']}", DUR["promo"])]
    S = sessions()
    for m in MODULES:
        lab = f"Module {m['n']}: {m['title']}"
        rows.append((lab, "Intro Video", f"Introduction to {m['title']}", DUR["intro"]))
        for s in [x for x in S if x["module"] == m["n"]]:
            tag = f"Session {s['num']}"
            if not s["workshop"]:
                rows += [
                    (lab, tag, f"{s['title']} — {s['hook']}", None),
                    (lab, "Video", f"{s['title']}: concept", DUR["concept"]),
                    (lab, "Video", f"{s['title']}: notebook walkthrough", DUR["walkthrough"]),
                    (lab, "Reading Material", f"Reading notebook (Colab): {s['title']}", DUR["reading"]),
                    (lab, "Activity", f"Practice (Colab / Sheet): {s['practice']}", DUR["practice"]),
                    (lab, "Reference Material", f"Reference: {s['title']}", DUR["reference"]),
                ]
            else:
                rows += [
                    (lab, tag, f"{s['title']} — {s['hook']}", None),
                    (lab, "Video", "Workshop briefing", DUR["ws_video"]),
                    (lab, "Assessment", f"Workshop notebook (Colab / Sheet): {s['topics']}", DUR["workshop"] + (20 if m["n"] == 6 else 0)),
                    (lab, "Quiz", f"Module {m['n']} quiz: {m['title']}", DUR["quiz"]),
                ]
    return rows


if __name__ == "__main__":
    rows = planner_rows()
    tot = sum(r[3] for r in rows if r[3])
    vid = sum(r[3] for r in rows if r[3] and r[1] in ("Video", "Intro Video", "Promo Video"))
    nv = sum(1 for r in rows if r[1] in ("Video", "Intro Video", "Promo Video"))
    print(f"sessions={len(sessions())} total={tot} min = {tot/60:.2f} h; video={vid} min = {vid/60:.2f} h in {nv} videos")
