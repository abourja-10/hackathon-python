"""Lettura e scrittura di JSON e CSV."""
import csv
import json
from pathlib import Path

# BASE: cartella in cui si trova questo file, così i percorsi
# funzionano da qualsiasi punto si avvii il programma.
BASE = Path(__file__).resolve().parent

# File dei dati (input/persistenza)
FILE_DATI = BASE / "dati" / "campus.json"
FILE_ARCHIVIO = BASE / "dati" / "archivio.json"

# File prodotti dall'esportazione (separati dagli input)
FILE_RIEPILOGO_JSON = BASE / "output" / "riepilogo.json"
FILE_RIEPILOGO_CSV = BASE / "output" / "riepilogo.csv"


def carica(percorso=FILE_DATI):
    """Legge una lista di voci da un file JSON.
    Se il file non esiste restituisce una lista vuota."""
    if not percorso.exists():
        return []
    try:
        # utf-8-sig ignora l'eventuale BOM aggiunto da PowerShell
        with open(percorso, encoding="utf-8-sig") as f:
            voci = json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f"Il file {percorso.name} è malformato")
    if not isinstance(voci, list):
        raise ValueError(f"Il file {percorso.name} deve contenere una lista")
    return voci


def salva(voci, percorso=FILE_DATI):
    """Scrive la lista di voci in un file JSON (UTF-8)."""
    percorso.parent.mkdir(parents=True, exist_ok=True)
    with open(percorso, "w", encoding="utf-8") as f:
        json.dump(voci, f, ensure_ascii=False, indent=2)


def esporta_json(riepilogo, percorso=FILE_RIEPILOGO_JSON):
    """Scrive il riepilogo (dizionario) in output/riepilogo.json."""
    percorso.parent.mkdir(parents=True, exist_ok=True)
    with open(percorso, "w", encoding="utf-8") as f:
        json.dump(riepilogo, f, ensure_ascii=False, indent=2)


def esporta_csv(voci, percorso=FILE_RIEPILOGO_CSV):
    """Scrive le voci in output/riepilogo.csv, con l'ID del menu."""
    percorso.parent.mkdir(parents=True, exist_ok=True)
    with open(percorso, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, fieldnames=["id", "categoria", "oggetto", "luogo", "stato"])
        w.writeheader()
        for v in voci:
            w.writerow({
                "id": v["id"],
                "categoria": v["categoria"],
                "oggetto": v["titolo"],
                "luogo": v["luogo"],
                "stato": v["stato"],
            })