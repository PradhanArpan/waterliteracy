"""Generate hub/sessions.json from course.py.
Instructor workflow: set "enabled": true for a session to release it on the hub."""
import json
from course import COURSE, MODULES, sessions

REFS = {  # Module 1 references (others filled as modules are built)
    1: ("IMD: India Meteorological Department", "https://mausam.imd.gov.in/"),
    2: ("India-WRIS: reservoir and water data portal", "https://indiawris.gov.in/"),
    3: ("IMD Pune: rainfall data and normals", "https://imdpune.gov.in/"),
    4: ("CWC flood forecasting portal", "https://ffs.india-water.gov.in/"),
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
        "workshop": s["workshop"], "enabled": m == 1,
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
