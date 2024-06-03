import os
import shutil

from pathlib import Path

from make_status import make_status

build_dir = Path("builtdocs")

make_status()
print("Created status.html")

os.makedirs(build_dir, exist_ok=True)
print("Created builtdocs folder")

shutil.move("status.html", build_dir / "index.html")
print("Moved status.html to builtdocs folder as index.html")

shutil.copy2(Path("static", "style.css"), build_dir)
print("Copied CSS to builtdocs folder")
