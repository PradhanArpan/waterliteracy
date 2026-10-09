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

## Repository layout

```
waterliteracy/
├── README.md
├── hub/
│   ├── index.html        Course Delivery Hub (publish with GitHub Pages)
│   └── sessions.json     Session list; set "enabled": true to release a session
├── notebooks/M1/         WDL_M1_S01_reading.ipynb, WDL_M1_S01_practice.ipynb, … WDL_M1_S05_workshop.ipynb
├── sheets/               WDL_M1_practice.xlsx (master copy of the Module 1 Sheet)
├── data/M1/              sample_station_2023.csv (illustrative, synthetic)
└── tools/                Python scripts that regenerate everything above
```

## Instructor setup (once)

1. Create a public GitHub repository named `waterliteracy` and upload these files.
2. Turn on GitHub Pages (Settings → Pages → main branch). The hub is then at
   `https://PradhanArpan.github.io/waterliteracy/hub/`. Link or embed it from CuX or Google Sites.
3. Upload `sheets/WDL_M1_practice.xlsx` to Google Drive, open it with Google Sheets, save as Google Sheets,
   share as "Anyone with the link can view", and change the link ending from `/edit…` to `/copy`.
   Paste that link into the `"sheet"` field of sessions 1–5 in `hub/sessions.json`.
4. Paste YouTube or CuX video links into each session's `"videos"` list, and the CuX submission link into `"submit"` for workshops.

## Releasing sessions

Open `hub/sessions.json` on GitHub, change `"enabled": false` to `"enabled": true` for the session, and commit.
Learners refresh the hub and the links appear. Module 1 is enabled by default.

## A note on data

Module 1 uses an **illustrative, synthetic** sample station for practice. From Module 2 onwards,
notebooks use real open data from IMD, India-WRIS, CWC and NASA GPM, with sources cited in each notebook.

## Licence

Course content © CHRIST (Deemed to be University). Licence to be confirmed before release.

## Regenerating the materials

Run from the repository root: `PYTHONPATH=tools python3 tools/build_m1.py`, `PYTHONPATH=tools python3 tools/build_m1_sheet.py` and `PYTHONPATH=tools python3 tools/make_sessions_json.py`.
