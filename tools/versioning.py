import re
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # <- remonte à la racine du projet
MAIN_FILE = PROJECT_ROOT / "main.py"
INDEX_HTML = Path("build/web/index.html")

if not MAIN_FILE.exists():
    print(f"Erreur : fichier introuvable : {MAIN_FILE}")
    exit(1)


def get_current_version() -> str:
    for line in MAIN_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("__version__"):
            match = re.search(r'"([\d.]+)"', line)
            if match:
                return match.group(1)
    raise ValueError("Aucune version trouvée dans main.py")


def is_valid_version(version: str) -> bool:
    return bool(re.match(r"^\d+\.\d+\.\d+$", version))


def increment_version(version: str) -> str:
    major, minor, patch = map(int, version.split("."))
    return f"{major}.{minor}.{patch + 1}"


def choose_version(current_version: str) -> str:
    print(f"Version actuelle : {current_version}")
    choice = input("Souhaites-tu entrer une version manuellement ? (y/N): ").strip().lower()
    if choice == "y":
        while True:
            new_version = input("Entrez la nouvelle version (ex: 1.2.0): ").strip()
            if is_valid_version(new_version):
                return new_version
            print("⚠️ Format invalide. Utilise le format majeur.mineur.correctif (ex: 1.2.0)")
    else:
        return increment_version(current_version)


def update_version_in_file(old: str, new: str):
    text = MAIN_FILE.read_text(encoding="utf-8")
    updated = re.sub(r'__version__\s*=\s*["\']' + re.escape(old) + r'["\']', f'__version__ = "{new}"', text)
    MAIN_FILE.write_text(updated, encoding="utf-8")
    print(f"✅ main.py mis à jour : version {new}")


def inject_version_in_html(version: str):
    if not INDEX_HTML.exists():
        print("⚠️ Aucun index.html trouvé pour injecter la version.")
        return
    content = INDEX_HTML.read_text(encoding="utf-8")
    if "<!-- version:" in content:
        content = re.sub(r"<!-- version: .*? -->", f"<!-- version: {version} -->", content)
    else:
        content = content.replace("</title>", f"</title>\n<!-- version: {version} -->")
    INDEX_HTML.write_text(content, encoding="utf-8")
    (INDEX_HTML.parent / "version.txt").write_text(version + "\n", encoding="utf-8")
    print(f"✅ index.html mis à jour avec la version {version}")


def git_commit(version: str, msg: str):
    subprocess.run(["git", "add", str(MAIN_FILE)], check=True)
    subprocess.run(["git", "add", "build/web/index.html", "build/web/version.txt"], check=True)
    subprocess.run(["git", "commit", "-m", f"{msg} (v{version})"], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"🚀 Commit et push réalisés pour la version {version}")


def main():
    current_version = get_current_version()
    new_version = choose_version(current_version)
    update_version_in_file(current_version, new_version)
    inject_version_in_html(new_version)
    msg = input("Message de commit : ").strip()
    git_commit(new_version, msg)


if __name__ == "__main__":
    main()