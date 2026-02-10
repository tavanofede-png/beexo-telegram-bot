import os
import sqlite3
import argparse
from html.parser import HTMLParser

# Intentar importar BeautifulSoup; si no está disponible, usar fallback sencillo
try:
    from bs4 import BeautifulSoup  # type: ignore
    _HAVE_BS4 = True
except Exception:
    BeautifulSoup = None  # type: ignore
    _HAVE_BS4 = False

DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), "beexy_history.db")

EXTENSIONS = [".md", ".txt", ".html", ".htm"]


def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
        if ext in (".html", ".htm"):
            if _HAVE_BS4 and BeautifulSoup is not None:
                soup = BeautifulSoup(raw, "html.parser")
                return soup.get_text(separator=" \n ")
            else:
                # Fallback simple stripper
                class _MLStripper(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self._fed = []

                    def handle_data(self, d):
                        self._fed.append(d)

                    def get_data(self):
                        return " ".join(self._fed)

                s = _MLStripper()
                s.feed(raw)
                return s.get_data()
        return raw
    except Exception as e:
        return ""


def ingest_folder(folder: str, source_label: str = "local"):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS kb_docs USING fts5(title, content, source);")
    conn.commit()

    for root, dirs, files in os.walk(folder):
        for fn in files:
            if os.path.splitext(fn)[1].lower() in EXTENSIONS:
                path = os.path.join(root, fn)
                print("Indexing:", path)
                text = extract_text_from_file(path)
                title = fn
                try:
                    cur.execute("INSERT INTO kb_docs (title, content, source) VALUES (?, ?, ?)", (title, text, source_label))
                except Exception as e:
                    print("Failed to insert", path, e)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("folder", nargs="?", default=os.path.join(os.path.dirname(os.path.dirname(__file__)), "beexo-telegram-bot"), help="Carpeta a indexar")
    args = p.parse_args()
    ingest_folder(args.folder)
