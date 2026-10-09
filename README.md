# Hydroinformatics in a Changing Climate: Water Data Literacy for All

Course materials for the CuX micro-credential offered by the Department of Civil Engineering,
School of Engineering and Technology, CHRIST (Deemed to be University), Bengaluru.

**30 sessions · 6 modules · about 30 hours · no coding needed**

Learners use the **Course Delivery Hub** (`hub/index.html`), which lists every session with its videos,
Colab notebooks, Google Sheet and reference.

## Each session

| Part | What it is | Time |
|---|---|---|
| Videos | One concept video and one notebook walkthrough, each 5 minutes or less | ~9 min |
| Reading notebook (Colab) | Explanations, interactive charts and calculators | ~25 min |
| Practice (Colab or Sheet) | Short tasks with instant ✅ / ❌ feedback; the Sheet has the same questions | ~20 min |
| Reference | One external source (IMD, CWC, India-WRIS) | ~5 min |

Session 5 of every module is a **workshop**: one step of the capstone, *My District's Water Story*, plus the module quiz on CuX.

## Modules

| Module | Sessions | Theme |
|---|---|---|
| 1 | 1–5 | The Water Cycle as Data |
| 2 | 6–10 | Finding and Trusting Water Data |
| 3 | 11–15 | Reading Rainfall |
| 4 | 16–20 | Rivers, Reservoirs and Floods |
| 5 | 21–25 | Climate Signals in Water Data |
| 6 | 26–30 | From Data to Dashboard (capstone) |

## Repository layout

```
waterliteracy/
├── index.html            redirects to the hub
├── hub/
│   ├── index.html        Course Delivery Hub (GitHub Pages)
│   └── sessions.json     Session list; "enabled": true/false releases or locks a session
├── notebooks/M1 … M6/    WDL_M{module}_S{session}_{reading|practice|workshop}.ipynb  (54 notebooks)
├── sheets/               WDL_M1_practice.xlsx … WDL_M6_practice.xlsx (master copies of the Sheets)
├── data/                 sample_district_daily_1981_2024.csv, M1/ and M2/ practice files (illustrative, synthetic)
└── tools/                Python scripts that regenerate everything above, plus automated tests
```

## Data used in the course

- **Module 1:** an illustrative sample station (one year).
- **Modules 2–6:** an illustrative **sample district** (daily, 1981–2024) for practice tasks and the Sheets, and **real data for the
  learner's own place**, downloaded live in Colab from **NASA POWER** (daily rainfall since 1981) and **ERA5 via Open-Meteo**,
  with place lookup by **Open-Meteo geocoding**. No accounts or keys are needed. If a download fails, notebooks fall back to the sample district.
- Rivers and reservoirs (Module 4) use illustrative teaching models, clearly labelled.

## Instructor setup (once)

1. Create a public GitHub repository named `waterliteracy` and upload these files.
2. Turn on GitHub Pages (Settings → Pages → main branch). The hub is then at
   `https://PradhanArpan.github.io/waterliteracy/hub/`. Link or embed it from CuX or Google Sites.
3. Upload each `sheets/WDL_M*_practice.xlsx` to Google Drive, open it with Google Sheets, save as Google Sheets,
   share as "Anyone with the link can view", and change the link ending from `/edit…` to `/copy`.
   Paste each link into the `"sheet"` field of that module's sessions in `hub/sessions.json`.
4. Paste YouTube or CuX video links into each session's `"videos"` list, and the CuX submission link into `"submit"` for workshops.

## Releasing sessions

Open `hub/sessions.json` on GitHub, change `"enabled": false` to `"enabled": true` for the session, and commit.
Learners refresh the hub and the links appear. All sessions are enabled at present; set later modules to false to release them week by week.

## Licence

Course content © CHRIST (Deemed to be University). Licence to be confirmed before release.

## Regenerating the materials

From the repository root:

```
for m in 1 2 3 4 5 6; do PYTHONPATH=tools python3 tools/build_m$m.py; done
PYTHONPATH=tools python3 tools/build_m1_sheet.py && PYTHONPATH=tools python3 tools/build_sheets.py
PYTHONPATH=tools python3 tools/make_sessions_json.py
python3 tools/selftest.py "notebooks/M[2-6]/*.ipynb"   # runs every notebook with answers auto-filled
python3 tools/test_sheets.py                             # fills every Sheet answer and checks ✓
```
