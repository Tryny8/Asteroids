import re
from pathlib import Path

def extract_version(pyfile: Path) -> str:
    """Extrait __version__ = 'x.y.z' depuis un fichier Python."""
    content = pyfile.read_text(encoding='utf-8')
    match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", content)
    return match.group(1) if match else "0.0.0"

def inject_version(index_file: Path, version: str):
    """Ajoute un commentaire de version dans index.html"""
    html = index_file.read_text(encoding='utf-8')
    if f"<!-- version:" not in html:
        html = html.replace("</title>", f"</title>\n<!-- version: {version} -->")
    index_file.write_text(html, encoding='utf-8')

def write_version_txt(folder: Path, version: str):
    """Écrit la version dans version.txt"""
    (folder / "version.txt").write_text(version, encoding='utf-8')

if __name__ == "__main__":
    base_dir = Path("build/web")
    version = extract_version(Path("main.py"))
    inject_version(base_dir / "index.html", version)
    write_version_txt(base_dir, version)
    print(f"[postprocess] Injected version: {version}")