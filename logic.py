"""Regole ed elaborazione di Campus Board."""
from datetime import date

# ─────────────────────────────────────────────────────────────
# COSTANTI DI CONFIGURAZIONE
# Qui definisco le "regole del gioco": quali categorie esistono
# e quali stati sono permessi per ciascuna di esse.
# ─────────────────────────────────────────────────────────────

CATEGORIE = {
    # Per ogni categoria, elenco gli stati possibili IN ORDINE.
    # Il primo stato è quello iniziale (default),
    # l'ultimo è lo stato finale (usato da chiudi_voce).
    "Oggetto Trovato": ["trovato", "restituito"],
    "Segnalazione": ["aperta", "in_corso", "chiusa"],
}

# Insieme veloce per capire se una pratica è terminata.
STATI_CHIUSI = {"restituito", "chiusa"}

# Elenco predefinito di problemi per le segnalazioni.
# L'ultima voce ("Altro") permette di descrivere un problema non previsto.
VOCE_ALTRO = "Altro (descrivi il problema)"

PROBLEMI_SEGNALAZIONE = {
    "1": "Macchina del caffè guasta",
    "2": "Distributore di snack guasto",
    "3": "Proiettore non funzionante",
    "4": "Wi-Fi assente o lento",
    "5": "Luce rotta",
    "6": "Porta o finestra che non chiude",
    "7": "Aria condizionata o riscaldamento non funzionante",
    "8": "Bagno fuori servizio o sporco",
    "9": "Perdita d'acqua",
    "10": "Prese elettriche o prolunghe danneggiate",
    "11": "Banchi o sedie rotti",
    "12": "Computer o stampante non funzionanti",
    "13": VOCE_ALTRO,
}


# ─────────────────────────────────────────────────────────────
# UTILITÀ
# ─────────────────────────────────────────────────────────────

def oggi():
    """Restituisce la data di oggi nel formato gg/mm/aaaa."""
    return date.today().strftime("%d/%m/%Y")


# ─────────────────────────────────────────────────────────────
# NORMALIZZAZIONE E ID
# ─────────────────────────────────────────────────────────────

def normalizza(voci):
    """Prende i record grezzi caricati dal JSON e si assicura
    che abbiano tutti i campi necessari (stato e storico).
    Se una categoria non è valida, lancia un errore subito."""
    for v in voci:
        if v.get("categoria") not in CATEGORIE:
            raise ValueError(f"Categoria non valida nel record {v.get('id')}")
        # setdefault: inserisce il valore solo se la chiave manca
        v.setdefault("stato", CATEGORIE[v["categoria"]][0])
        v.setdefault("storico", [{"stato": v["stato"], "data": v["data"]}])
    return voci


def prossimo_id(voci, archivio=()):
    """Calcola il prossimo ID disponibile, ARCHIVIO COMPRESO,
    così un ID archiviato non viene mai riusato."""
    tutti = list(voci) + list(archivio)
    return max((v["id"] for v in tutti), default=0) + 1


# ─────────────────────────────────────────────────────────────
# CREAZIONE DI UNA NUOVA VOCE
# ─────────────────────────────────────────────────────────────

def registra_voce(voci, categoria, titolo, luogo, data=None, archivio=()):
    """Crea un nuovo record e lo aggiunge alla lista.
    Controlli: categoria esistente, titolo e luogo non vuoti.
    Lo stato iniziale è il primo della lista della categoria."""
    if categoria not in CATEGORIE:
        raise ValueError(f"Categoria non valida: {categoria}")
    titolo, luogo = titolo.strip(), luogo.strip()
    if not titolo or not luogo:
        raise ValueError("Titolo e luogo non possono essere vuoti")
    data = data or oggi()
    stato = CATEGORIE[categoria][0]
    voce = {
        "id": prossimo_id(voci, archivio),
        "categoria": categoria,
        "titolo": titolo,
        "luogo": luogo,
        "data": data,
        "stato": stato,
        "storico": [{"stato": stato, "data": data}],
    }
    voci.append(voce)
    return voce


# ─────────────────────────────────────────────────────────────
# RICERCA E FILTRI
# ─────────────────────────────────────────────────────────────

def cerca(voci, testo=None, luogo=None, stato=None, categoria=None):
    """Cerca tra le voci applicando uno o più filtri (AND).
    Un filtro None viene ignorato."""
    risultati = []
    for v in voci:
        if testo and testo.lower() not in v["titolo"].lower():
            continue
        if luogo and luogo.lower() != v["luogo"].lower():
            continue
        if stato and stato != v["stato"]:
            continue
        if categoria and categoria != v["categoria"]:
            continue
        risultati.append(v)
    return risultati


def trova_voce(voci, id_voce):
    """Cerca una voce per ID. Se non c'è lancia un KeyError."""
    for v in voci:
        if v["id"] == id_voce:
            return v
    raise KeyError(f"Nessuna voce con id {id_voce}")


# ─────────────────────────────────────────────────────────────
# AGGIORNAMENTO STATO
# ─────────────────────────────────────────────────────────────

def aggiorna_stato(voci, id_voce, nuovo_stato):
    """Cambia lo stato di una voce e lo registra nello storico.
    Il nuovo stato deve essere valido per la categoria della voce."""
    v = trova_voce(voci, id_voce)
    if nuovo_stato not in CATEGORIE[v["categoria"]]:
        raise ValueError(f"Stato '{nuovo_stato}' non valido per {v['categoria']}")
    v["stato"] = nuovo_stato
    v["storico"].append({"stato": nuovo_stato, "data": oggi()})
    return v


def chiudi_voce(voci, id_voce):
    """Porta la voce all'ULTIMO stato previsto per la sua categoria.
    Se è già chiusa lancia un errore. La voce NON viene cancellata."""
    v = trova_voce(voci, id_voce)
    if v["stato"] in STATI_CHIUSI:
        raise ValueError(f"La voce #{id_voce} è già chiusa ({v['stato']})")
    return aggiorna_stato(voci, id_voce, CATEGORIE[v["categoria"]][-1])


# ─────────────────────────────────────────────────────────────
# STATISTICHE E RIEPILOGO
# ─────────────────────────────────────────────────────────────

def conta_aperti(voci):
    """Conta quante voci NON sono in uno stato chiuso."""
    return sum(1 for v in voci if v["stato"] not in STATI_CHIUSI)


def separa_chiuse(voci):
    """Restituisce (aperte, chiuse) senza modificare la lista di partenza."""
    aperte = [v for v in voci if v["stato"] not in STATI_CHIUSI]
    chiuse = [v for v in voci if v["stato"] in STATI_CHIUSI]
    return aperte, chiuse


def da_restituire_per_luogo(voci):
    """Raggruppa per luogo gli oggetti ancora da restituire.
    Esempio: {"Aula 1": ["Zaino"], "Biblioteca": ["Chiavi"]}"""
    out = {}
    for v in voci:
        if v["categoria"] == "Oggetto Trovato" and v["stato"] == "trovato":
            out.setdefault(v["luogo"], []).append(v["titolo"])
    return out


def costruisci_riepilogo(voci, archivio=()):
    """Dato che la pagina mostra: calcolato qui, non in JavaScript.
    'chiusi' = voci chiuse nei dati + tutte quelle in archivio."""
    segnalazioni = {}
    for v in voci:
        if v["categoria"] == "Segnalazione":
            segnalazioni[v["stato"]] = segnalazioni.get(v["stato"], 0) + 1
    aperti = conta_aperti(voci)
    return {
        "aperti": aperti,
        "chiusi": len(voci) - aperti + len(archivio),
        "da_restituire_per_luogo": da_restituire_per_luogo(voci),
        "segnalazioni_per_stato": segnalazioni,
    }