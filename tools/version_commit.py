# version_commit.py
import re
import subprocess
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # <- remonte à la racine du projet
MAIN_FILE = PROJECT_ROOT / "main.py"


def extract_version() -> str:
    """Extrait la version actuelle du fichier main.py."""
    text = MAIN_FILE.read_text(encoding="utf-8")
    match = re.search(r"__version__\s*=\s*['\"](\d+)\.(\d+)\.(\d+)['\"]", text)
    if not match:
        raise ValueError("Version non trouvée dans main.py")
    return ".".join(match.groups())

def bump_version(version: str) -> str:
    """Incrémente la version (dernier chiffre)."""
    major, minor, patch = map(int, version.split("."))
    return f"{major}.{minor}.{patch + 1}"

def is_valid_version(version: str) -> bool:
    return bool(re.match(r"^\d+\.\d+\.\d+$", version))

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
        return bump_version(current_version)

def update_main_py(new_version: str):
    """Met à jour la variable __version__ dans main.py."""
    content = MAIN_FILE.read_text(encoding="utf-8")
    new_content = re.sub(
        r"__version__\s*=\s*['\"](\d+)\.(\d+)\.(\d+)['\"]",
        f"__version__ = '{new_version}'",
        content
    )
    MAIN_FILE.write_text(new_content, encoding="utf-8")

def git_commit_push(new_version: str, msg: str):
    """Ajoute tous les changements et effectue un commit."""
    subprocess.run(["git", "add", "*"], check=True)
    subprocess.run(["git", "commit", "-m", f"(v{new_version}) - {msg}"], check=True)
    subprocess.run(["git", "push"], check=True)
    # Ou alors command: (moins flexible)
    # subprocess.run(["git", "push", "origin", "main"], check=True)

def main():
    if not MAIN_FILE.exists():
        print(f"Erreur : fichier introuvable : {MAIN_FILE}")
        exit(1)
    
    if len(sys.argv) < 2:
        print("Usage : python tools/version_commit.py 'Message de commit'")
        sys.exit(1)
    commit_message = sys.argv[1]

    old_version = extract_version()
    new_version = choose_version(old_version)
    print(f"Ancienne version : {old_version} → Nouvelle version : {new_version}")

    update_main_py(new_version)
    git_commit_push(new_version, commit_message)
    print("✅ Commit effectué avec succès.")

if __name__ == "__main__":
    """
    Commande d'utilisation:
    python tools/version_commit.py "ici le commit"
    """
    main()