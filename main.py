"""Campus Board: menu da terminale. Avvio: python main.py"""
import logic
import storage

OPZIONI_INSERIMENTO = {"1": "Oggetto Trovato", "2": "Segnalazione"}


# ---------- Funzioni di input (0 = indietro) ----------
def chiedi_numero(opzioni, titolo):
    """Restituisce la scelta, oppure None se l'utente preme 0 (indietro)."""
    while True:
        print(titolo)
        for num, nome in opzioni.items():
            print(f"  {num}) {nome}")
        print("  0) Indietro")
        scelta = input("> ").strip()
        if scelta == "0":
            return None
        if scelta in opzioni:
            return opzioni[scelta]
        print("Scelta non valida, riprova.")


def chiedi_testo(domanda):
    """Restituisce il testo, oppure None se l'utente scrive 0 (indietro)."""
    testo = input(f"{domanda} (0 = indietro) ").strip()
    if testo == "0":
        return None
    return testo


def chiedi_id():
    """Restituisce l'ID, oppure None se l'utente scrive 0 (indietro)."""
    testo = input("ID della voce (0 = indietro): ").strip()
    if testo == "0":
        return None
    try:
        valore = int(testo)
    except ValueError:
        raise ValueError("L'ID deve essere un numero intero")
    if valore <= 0:
        raise ValueError("L'ID deve essere maggiore di zero")
    return valore


def annullato():
    print("Operazione annullata.")


# ---------- Stampa ----------
def stampa(voci):
    if not voci:
        print("  (nessun risultato)")
    for v in voci:
        print(f"  #{v['id']} [{v['categoria']}] {v['titolo']} - "
              f"{v['luogo']} - {v['data']} - {v['stato']}")


def mostra_elenco(voci, solo_aperte=False):
    """Stampa le voci con il loro ID, prima di chiederne uno."""
    if solo_aperte:
        voci, _ = logic.separa_chiuse(voci)
    print("Voci disponibili:")
    stampa(voci)


# ---------- Operazioni del menu ----------
def inserisci(voci, archivio):
    categoria = chiedi_numero(OPZIONI_INSERIMENTO, "Cosa vuoi registrare?")
    if categoria is None:
        return annullato()

    if categoria == "Segnalazione":
        titolo = chiedi_numero(logic.PROBLEMI_SEGNALAZIONE,
                               "Quale problema stai riscontrando?")
        if titolo == logic.VOCE_ALTRO:
            titolo = chiedi_testo("Descrivi il problema")
    else:
        titolo = chiedi_testo("Che oggetto hai trovato?")
    if titolo is None:
        return annullato()

    luogo = chiedi_testo("Dove?")
    if luogo is None:
        return annullato()

    v = logic.registra_voce(voci, categoria, titolo, luogo, archivio=archivio)
    storage.salva(voci)
    print(f"Registrata la voce #{v['id']}: {v['titolo']} ({v['luogo']})")


def cambia_stato(voci):
    mostra_elenco(voci)
    id_voce = chiedi_id()
    if id_voce is None:
        return annullato()
    v = logic.trova_voce(voci, id_voce)

    stati = logic.CATEGORIE[v["categoria"]]
    opzioni = {str(i): s for i, s in enumerate(stati, 1)}
    nuovo = chiedi_numero(opzioni, f"Stato attuale: {v['stato']}. Nuovo stato:")
    if nuovo is None:
        return annullato()

    logic.aggiorna_stato(voci, id_voce, nuovo)
    storage.salva(voci)
    print("Stato aggiornato.")


def chiudi_caso(voci):
    mostra_elenco(voci, solo_aperte=True)
    id_voce = chiedi_id()
    if id_voce is None:
        return annullato()
    v = logic.trova_voce(voci, id_voce)

    conferma = input(f"Chiudere #{v['id']} '{v['titolo']}'? (s/n) ").strip().lower()
    if conferma != "s":
        return annullato()

    logic.chiudi_voce(voci, id_voce)
    storage.salva(voci)
    print(f"Caso #{v['id']} chiuso: {v['titolo']} -> {v['stato']}")


def mostra_dettaglio(voci, archivio):
    """Elenca solo le voci aperte; una voce chiusa si vede scrivendo il suo ID
    (gli ID delle chiuse si trovano con l'opzione 8)."""
    mostra_elenco(voci, solo_aperte=True)
    print("(Per una voce chiusa scrivi comunque il suo ID: le trovi con l'opzione 8)")
    id_voce = chiedi_id()
    if id_voce is None:
        return annullato()
    v = logic.trova_voce(voci + archivio, id_voce)
    print(f"\n#{v['id']} [{v['categoria']}] {v['titolo']} - {v['luogo']}")
    print(f"Stato attuale: {v['stato']}")
    print("Storico:")
    for passo in v["storico"]:
        print(f"  {passo['data']} -> {passo['stato']}")


def esporta(voci, archivio):
    """Archivia le voci chiuse, poi esporta solo quelle ancora aperte."""
    aperte, chiuse = logic.separa_chiuse(voci)
    if chiuse:
        archivio.extend(chiuse)
        voci[:] = aperte
        # Prima l'archivio, poi i dati: se qualcosa si interrompe
        # una voce può comparire due volte, ma non va mai persa.
        storage.salva(archivio, storage.FILE_ARCHIVIO)
        storage.salva(voci)
    storage.esporta_json(logic.costruisci_riepilogo(voci, archivio))
    storage.esporta_csv(voci)
    print(f"Esportate {len(voci)} voci aperte. "
          f"Archiviate ora: {len(chiuse)} (totale in archivio: {len(archivio)})")


# ---------- Programma principale ----------
def main():
    try:
        voci = logic.normalizza(storage.carica())
        archivio = logic.normalizza(storage.carica(storage.FILE_ARCHIVIO))
    except ValueError as e:
        print("Errore nel caricamento:", e)
        return

    while True:
        print("\n=== CAMPUS BOARD ===")
        print("1) Registra  2) Cerca  3) Aggiorna stato  4) Casi aperti  "
              "5) Esporta e archivia")
        print("6) Chiudi caso  7) Dettaglio  8) Chiuse e archivio  0) Esci")
        scelta = input("> ").strip()
        try:
            if scelta == "1":
                inserisci(voci, archivio)
            elif scelta == "2":
                stampa(logic.cerca(
                    voci,
                    testo=input("Testo (invio=salta): ").strip() or None,
                    luogo=input("Luogo (invio=salta): ").strip() or None,
                    stato=input("Stato (invio=salta): ").strip() or None))
            elif scelta == "3":
                cambia_stato(voci)
            elif scelta == "4":
                print("Casi aperti:", logic.conta_aperti(voci))
                for luogo, titoli in logic.da_restituire_per_luogo(voci).items():
                    print(f"  {luogo}: {', '.join(titoli)}")
            elif scelta == "5":
                esporta(voci, archivio)
            elif scelta == "6":
                chiudi_caso(voci)
            elif scelta == "7":
                mostra_dettaglio(voci, archivio)
            elif scelta == "8":
                _, chiuse = logic.separa_chiuse(voci)
                print(f"Chiuse da archiviare: {len(chiuse)} - "
                      f"Già in archivio: {len(archivio)}")
                stampa(chiuse + archivio)
            elif scelta == "0":
                print("Arrivederci.")
                break
            else:
                print("Scelta non valida.")
        except (ValueError, KeyError) as e:
            print("Errore:", e)


if __name__ == "__main__":
    main()