# 📌 CampusBoard

**CampusBoard** è un'applicazione sviluppata per il Python Innovation Hackathon, con l'obiettivo di migliorare la comunicazione e la collaborazione all'interno della comunità universitaria.

Il progetto propone una bacheca digitale attraverso cui gestire oggetti smarriti o ritrovati, segnalazioni e informazioni utili per la vita del campus.

## 🎯 Obiettivo del progetto

CampusBoard nasce per rendere più semplice e organizzata la condivisione di informazioni tra gli studenti e la comunità universitaria.

L'applicazione permette di:
- Registrare nuovi oggetti ritrovati e segnalazioni.
- Cercare informazioni già presenti nella bacheca.
- Aggiornare lo stato delle segnalazioni.
- Consultare i casi aperti e quelli chiusi.
- Archiviare le segnalazioni concluse.
- Esportare i dati per facilitarne la gestione.
- Visualizzare le informazioni attraverso un'interfaccia web.

## 🏗️ Architettura del progetto

Il progetto combina un backend sviluppato in Python con un'interfaccia web realizzata utilizzando Node.js, HTML, CSS e JavaScript.

### Backend — Python

Il backend è costituito da un'applicazione a riga di comando.

Il file `main.py` permette di accedere alle principali funzionalità attraverso un menu interattivo.

La logica di gestione dei dati è organizzata nei moduli Python del progetto.

### Database — File JSON

I dati vengono salvati localmente attraverso file JSON.

I principali file utilizzati sono:

- `dati/campus.json`: contiene i dati della bacheca.
- `dati/archivio.json`: contiene le segnalazioni archiviate.

Questo approccio permette di gestire le informazioni senza utilizzare un database esterno.

### Frontend — Node.js ed Express

Il frontend è realizzato attraverso un server Node.js con Express.

L'interfaccia web utilizza:
- **HTML** per la struttura della pagina.
- **CSS** per lo stile e il layout.
- **JavaScript** per le funzionalità interattive.

La bacheca presenta le informazioni attraverso card e strumenti di filtraggio.

## ✨ Funzionalità principali

### Gestione tramite Python CLI

L'applicazione Python mette a disposizione un menu interattivo con le seguenti operazioni:

1. Registrazione di una nuova segnalazione.
2. Ricerca delle informazioni.
3. Aggiornamento dello stato.
4. Visualizzazione dei casi aperti.
5. Esportazione e archiviazione.
6. Chiusura di un caso.
7. Visualizzazione dei dettagli.
8. Consultazione delle segnalazioni chiuse e archiviate.
0. Uscita dall'applicazione.

### Visualizzazione tramite frontend

L'interfaccia web consente di consultare le informazioni della bacheca in modo semplice e intuitivo.

Le segnalazioni vengono visualizzate attraverso card e possono essere filtrate in base alla categoria.

## 🛠️ Tecnologie utilizzate

| Tecnologia | Utilizzo |
|---|---|
| Python | Logica applicativa e gestione dei dati |
| JSON | Memorizzazione locale delle informazioni |
| Node.js | Ambiente di esecuzione del frontend |
| Express | Server web |
| HTML | Struttura dell'interfaccia |
| CSS | Stile e layout |
| JavaScript | Interattività e filtri |
| Git e GitHub | Versionamento e collaborazione |

## 📂 Struttura del repository

```text
hackathon-python/
│
├── dati/
│   ├── campus.json
│   └── archivio.json
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── app.js
│   ├── package.json
│   ├── package-lock.json
│   └── server.js
│
├── output/
│
├── main.py
├── logic.py
├── storage.py
└── README.md
```

## 🚀 Installazione e avvio

### Requisiti

Prima di avviare il progetto, assicurarsi di avere installato:

- Python 3
- Node.js
- npm
- Git (facoltativo, per clonare il repository)

### 1. Clonare il repository

```bash
git clone https://github.com/abourja-10/hackathon-python.git
cd hackathon-python
```

### 2. Avviare il backend Python

Dalla cartella principale del progetto:

```bash
python main.py
```

Si aprirà il menu interattivo di CampusBoard.

### 3. Avviare il frontend web

Aprire un secondo terminale e digitare:

```bash
cd frontend
npm install
node server.js
```

Una volta avviato il server, aprire il browser e visitare:

http://localhost:3000

## 📋 Possibili sviluppi futuri

CampusBoard può essere ulteriormente migliorato attraverso:

- Introduzione di un database più strutturato.
- Implementazione di un sistema di autenticazione.
- Miglioramento della gestione delle notifiche.
- Aggiunta di nuove funzionalità per la comunità universitaria.
- Ottimizzazione dell'interfaccia per dispositivi mobili.

## 👥 Progetto Hackathon

CampusBoard è stato sviluppato nell'ambito del Python Innovation Hackathon, con l'obiettivo di applicare le competenze di programmazione Python alla realizzazione di una soluzione concreta per una comunità intelligente.

---

**CampusBoard — Una bacheca digitale per una comunità universitaria più connessa.**
