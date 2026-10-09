"""Generate hub/sessions.json from course.py.
Instructor workflow: set "enabled": true for a session to release it on the hub."""
import json
from course import COURSE, MODULES, sessions

REFS = {  # one external reference per teaching session (verify links before each run)
    1: ("IMD: India Meteorological Department", "https://mausam.imd.gov.in/"),
    2: ("India-WRIS: water resources information system", "https://indiawris.gov.in/"),
    3: ("IMD Pune: rainfall data services", "https://imdpune.gov.in/"),
    4: ("CWC flood forecasting portal", "https://ffs.india-water.gov.in/"),
    6: ("India-WRIS: one portal for India's water data", "https://indiawris.gov.in/"),
    7: ("NASA GPM IMERG: satellite rainfall", "https://gpm.nasa.gov/data/imerg"),
    8: ("NASA POWER: data access", "https://power.larc.nasa.gov/"),
    9: ("IMD Pune: gridded and station data", "https://imdpune.gov.in/"),
    11: ("IMD: monsoon and rainfall reports", "https://mausam.imd.gov.in/"),
    12: ("IMD: district rainfall and departures", "https://mausam.imd.gov.in/"),
    13: ("IMD: weather warnings and terms", "https://mausam.imd.gov.in/"),
    14: ("USGS: the 100-year flood explained", "https://www.usgs.gov/special-topics/water-science-school/science/100-year-flood"),
    16: ("Central Water Commission", "https://cwc.gov.in/"),
    17: ("CWC flood forecasting portal", "https://ffs.india-water.gov.in/"),
    18: ("India-WRIS: reservoirs", "https://indiawris.gov.in/"),
    19: ("NDMA: urban flooding", "https://ndma.gov.in/"),
    21: ("IPCC AR6 WGI: Summary for Policymakers", "https://www.ipcc.ch/report/ar6/wg1/chapter/summary-for-policymakers/"),
    22: ("Theil–Sen estimator (overview)", "https://en.wikipedia.org/wiki/Theil%E2%80%93Sen_estimator"),
    23: ("IPCC AR6 WGI Chapter 11: weather and climate extremes", "https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-11/"),
    24: ("IPCC AR6 WGI: Summary for Policymakers", "https://www.ipcc.ch/report/ar6/wg1/chapter/summary-for-policymakers/"),
    26: ("Datawrapper Academy", "https://academy.datawrapper.de/"),
    27: ("FT Visual Vocabulary", "https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary"),
    28: ("Looker Studio", "https://lookerstudio.google.com/"),
    29: ("NASA POWER: citing the data", "https://power.larc.nasa.gov/"),
}

data = {
    "course": {**COURSE, "total_sessions": 30, "hours": 30},
    "github": {"user": "PradhanArpan", "repo": "waterliteracy", "branch": "main"},
    "quick_links": [
        {"label": "Google Colab", "url": "https://colab.research.google.com/", "dot": "teal"},
        {"label": "GitHub repo", "url": "https://github.com/PradhanArpan/waterliteracy", "dot": "teal"},
        {"label": "CuX course page", "url": "https://mooc.christuniversity.in/my/courses.php", "dot": "teal"},
        {"label": "IMD rainfall", "url": "https://mausam.imd.gov.in/", "dot": "gold"},
        {"label": "CWC flood forecasts", "url": "https://ffs.india-water.gov.in/", "dot": "gold"},
        {"label": "India-WRIS", "url": "https://indiawris.gov.in/", "dot": "gold"},
    ],
    "modules": [{"n": m["n"], "title": m["title"], "co": m["co"], "about": m["about"]} for m in MODULES],
    "sessions": [],
}

for s in sessions():
    m, k = s["module"], s["num"]
    base = f"notebooks/M{m}/WDL_M{m}_S{k:02d}"
    row = {
        "num": k, "module": m, "title": s["title"], "hook": s["hook"],
        "workshop": s["workshop"], "enabled": True,
        "sheet": "",  # paste the Google Sheets /copy link
    }
    if s["workshop"]:
        row["videos"] = [{"label": "Briefing", "url": ""}]
        row["notebooks"] = [{"label": "Workshop", "path": f"{base}_workshop.ipynb"}]
        row["submit"] = ""  # paste the CuX submission link
    else:
        row["videos"] = [{"label": "Concept", "url": ""}, {"label": "Walkthrough", "url": ""}]
        row["notebooks"] = [{"label": "Reading", "path": f"{base}_reading.ipynb"},
                            {"label": "Practice", "path": f"{base}_practice.ipynb"}]
        lab, url = REFS.get(k, ("", ""))
        row["reference"] = {"label": lab, "url": url}
    data["sessions"].append(row)

with open("hub/sessions.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("sessions:", len(data["sessions"]), "enabled:", sum(x["enabled"] for x in data["sessions"]))
