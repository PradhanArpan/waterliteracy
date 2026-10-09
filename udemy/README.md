# Udemy edition

Platform-neutral copies of the course for **Water Data Literacy: Rainfall, Floods and Climate Change** on Udemy.

| Folder / file | What it is |
|---|---|
| `notebooks/M1 … M6/` | The 54 Colab notebooks (no CuX or CHRIST branding; submissions go to Udemy assignments) |
| `sheets/` | The six practice workbooks, to attach as downloadable resources |
| `Udemy_curriculum.xlsx` | Every section and lecture in upload order, with durations, free-preview flags and resource links |
| `course_image_750x422.png`, `course_image_1500x844.png` | Course image (no text, as Udemy requires) |

Open any notebook in Colab with:
`https://colab.research.google.com/github/PradhanArpan/waterliteracy/blob/main/udemy/notebooks/M1/WDL_M1_S01_reading.ipynb`

## Regenerating

The CuX notebooks in `../notebooks` are the master copy. After changing them:

```
PYTHONPATH=tools python3 tools/make_udemy_edition.py
WDL_EDITION=udemy PYTHONPATH=tools python3 tools/build_m1_sheet.py
WDL_EDITION=udemy PYTHONPATH=tools python3 tools/build_sheets.py
PYTHONPATH=tools python3 tools/build_udemy_curriculum.py
```
