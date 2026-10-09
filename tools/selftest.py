"""Run notebooks with WDL_SELFTEST=1 (answers auto-filled) and report ✅ / ❌ / errors."""
import os, sys, glob, nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
os.environ["WDL_SELFTEST"] = "1"
paths = sorted(p for a in sys.argv[1:] for p in glob.glob(a))
bad = 0
for p in paths:
    nb = nbformat.read(p, 4)
    try:
        ExecutePreprocessor(timeout=180, kernel_name="python3").preprocess(nb, {"metadata": {"path": "/tmp"}})
        err = ""
    except CellExecutionError as e:
        err = str(e).strip().splitlines()[-1][:200]; bad += 1
    txt = "".join(o.get("text", "") + str(o.get("data", {}).get("text/markdown", ""))
                  for c in nb.cells for o in c.get("outputs", []))
    imgs = sum("image/png" in o.get("data", {}) for c in nb.cells for o in c.get("outputs", []))
    print(f"{os.path.basename(p):34s} ✅{txt.count('✅'):3d} ❌{txt.count('❌'):3d} ⚠️{txt.count('⚠️'):2d} charts{imgs:3d}  {('ERROR: ' + err) if err else ''}")
    for line in txt.splitlines():
        if "❌" in line and "workshop" not in p: print("      ", line[:140])
print("FAILED:", bad)
