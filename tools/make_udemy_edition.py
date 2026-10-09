"""Build the Udemy edition: platform-neutral copies of every notebook under udemy/notebooks/.

The CuX edition in notebooks/ stays the master. This script rewrites only the lines that name CuX or CHRIST,
so the two editions never drift apart. Run after the module builders:
    PYTHONPATH=tools python3 tools/make_udemy_edition.py
"""
import glob, os, re, nbformat

UDEMY_TITLE = "Water Data Literacy: Rainfall, Floods and Climate Change"
SUBS = [
    ("| **Course** | Hydroinformatics in a Changing Climate: Water Data Literacy for All |", f"| **Course** | {UDEMY_TITLE} |"),
    ("| **Department** | Civil Engineering · CHRIST (Deemed to be University) |", "| **Edition** | Udemy |"),
    ("Hydroinformatics in a Changing Climate: Water Data Literacy for All", "Water Data Literacy"),
    ("Water Data Literacy for All · CHRIST CuX", "Water Data Literacy · Dr Arpan Pradhan"),
    ("Then submit it on CuX and review two classmates' work.", "Then submit it in the **Capstone assignment** and give feedback on two other learners' work."),
    ("**Submit on CuX:** the PNG or PDF, plus the Looker Studio link if you made one. Then review two classmates using this rubric.",
     "**Submit in the Capstone assignment:** upload the PNG (and paste your Looker Studio link if you made one). Then give feedback on two other learners' submissions using this rubric."),
    ("Take a screenshot of the card (or File → Print → Save as PDF) and upload it on CuX.", "Take a screenshot of the card and upload it in this module's Udemy assignment."),
    ("and upload it on CuX.", "and upload it in this module's Udemy assignment."),
]
REGEX = [
    (re.compile(r"Take the \*\*Module (\d) quiz\*\* on CuX\."), r"Take the **Module \1 quiz** at the end of this section."),
    (re.compile(r"(Upload|upload) (.*?) on CuX \((Lab \d)\)\."), r"Submit \2 in the **\3** assignment (Udemy accepts JPG or PNG images)."),
    (re.compile(r"^\| \*\*CO\*\* \|.*\|\n", re.M), ""),
]

def convert(src):
    for a, b in SUBS: src = src.replace(a, b)
    for rx, b in REGEX: src = rx.sub(b, src)
    return src

if __name__ == "__main__":
    n = 0
    for p in sorted(glob.glob("notebooks/M*/*.ipynb")):
        nb = nbformat.read(p, 4)
        for c in nb.cells: c.source = convert(c.source)
        out = os.path.join("udemy", p)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        nbformat.write(nb, out); n += 1
    left = [p for p in glob.glob("udemy/notebooks/M*/*.ipynb") if re.search(r"CuX|CHRIST", open(p).read())]
    print(f"Udemy edition: {n} notebooks written; files still naming CuX/CHRIST: {left or 'none'}")
