"""Refresh photo-editor/ and pdfer/ from the two repos' Trunk builds (dist/web), keeping each
folder's manifest.webmanifest and putting back the page title and home-screen links.

    python update-site.py
"""
import pathlib
import re
import shutil

HERE = pathlib.Path(__file__).resolve().parent
APPS = {
    "photo-editor": (HERE.parent / "photocraft" / "dist" / "web", "Yangon Photo Editor"),
    "pdfer": (HERE.parent / "editor" / "dist" / "web", "Yangon Bookshop Pdfer"),
}
LINKS = ('<link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="../icon-192.png">'
         '<link rel="apple-touch-icon" href="../icon-192.png"><meta name="theme-color" content="#e0800b">')

for folder, (build, title) in APPS.items():
    dest = HERE / folder
    manifest = (dest / "manifest.webmanifest").read_bytes()
    shutil.rmtree(dest)
    shutil.copytree(build, dest)
    (dest / "manifest.webmanifest").write_bytes(manifest)
    page = dest / "index.html"
    html = page.read_text(encoding="utf-8")
    html, n = re.subn(r"<title>[^<]*</title>", f"<title>{title}</title>{LINKS}", html, count=1)
    if n != 1:
        raise SystemExit(f"{page}: no <title> to replace")
    page.write_text(html, encoding="utf-8", newline="\n")
    print(folder, sorted(p.name for p in dest.iterdir()))
