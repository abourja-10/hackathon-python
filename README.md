# 📌 CampusBoard

CampusBoard è un'applicazione ibrida sviluppata per il Python Innovation Hackathon. Permette alla comunità del campus di gestire e visualizzare oggetti trovati, segnalazioni ed eventi in modo semplice e immediato.

## 🏗️ Architettura del Progetto

Il progetto rispetta i vincoli dell'hackathon separando nettamente la logica di inserimento da quella di visualizzazione tramite un approccio file-based (JSON):

1. **Backend (Python CLI):** Uno script a riga di comando (`main.py`) gestisce l'inserimento, la validazione e l'esportazione dei dati.
2. **Database (File JSON):** I dati vengono serializzati in locale sul file `bacheca.json`.
3. **Frontend (Node.js + Web):** Un server Express (`server.js`) espone il JSON a un'interfaccia HTML/CSS/JS reattiva, che si aggiorna in tempo reale mostrando le nuove segnalazioni sotto forma di card filtrabili.

## 🚀 Come avviare l'applicazione

### 1. Avviare il Frontend (Interfaccia Web)
Assicurati di avere Node.js installato. Apri un terminale, entra nella cartella `frontend` e avvia il server:

```bash
cd frontend
npm install
node server.js