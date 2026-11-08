# Valutazione finale

## 1. Obiettivi

| ID | Raggiunto (sì / parziale / no) | Prova |
|---|---|---|
| O1 | Sì | Il backend Python permette di gestire le funzionalità previste per gli oggetti trovati e le segnalazioni. |
| O2 | Sì | I dati vengono salvati nei file JSON. Node.js, tramite Express, legge i dati e li rende disponibili al frontend. |
| O3 | Sì | La dashboard permette di visualizzare e gestire le informazioni attraverso l'interfaccia web. |

## 2. Test

Esito: PASS, FAIL o NON ESEGUITO.

| # | Test | Atteso | Osservato | Esito |
|---|---|---|---|---|
| 1 | Avvio e uscita | Avvio corretto del backend Python, del server Node.js e caricamento del frontend. | Tutti i componenti si avviano correttamente e la pagina viene caricata nel browser. | PASS |
| 2 | Le tre operazioni con un dato valido | Le operazioni principali devono funzionare con dati corretti. | Le operazioni di inserimento, ricerca e aggiornamento degli elementi funzionano correttamente. | PASS |
| 3 | Input non valido | I valori non consentiti devono essere bloccati; gli input errati dovrebbero essere gestiti con controlli adeguati. | I valori non consentiti vengono rifiutati, ma non sono presenti controlli completi per tutte le tipologie di input. | PASS PARZIALE |
| 4 | Campo vuoto | Il programma deve impedire l'inserimento se mancano dati obbligatori. | I campi obbligatori vengono controllati e l'inserimento viene impedito se sono vuoti. | PASS |
| 5 | Elemento assente | La ricerca senza risultati deve mostrare un messaggio informativo. | Viene mostrato un messaggio che comunica l'assenza di risultati. | PASS |
| 6 | Dataset vuoto | Il progetto deve funzionare anche senza elementi registrati. | La bacheca viene mostrata correttamente anche quando il dataset è vuoto. | PASS |
| 7 | File mancante o malformato | Il sistema dovrebbe gestire file mancanti o con formato non valido. | Il comportamento non è stato verificato attraverso un test specifico. | NON ESEGUITO |
| 8 | Esportazione e rilettura dell'output | I dati devono essere esportati in CSV e il file generato deve poter essere letto correttamente. | L'esportazione CSV e la successiva lettura dei dati sono state verificate. | PASS |
| 9 | Dashboard: file valido e file non valido | Con un JSON valido i dati devono essere visualizzati; con un JSON non valido deve comparire un messaggio di errore. | Entrambi i casi sono stati verificati: i dati vengono visualizzati correttamente e, in caso di JSON non valido, viene mostrato un messaggio di errore. | PASS |

## 3. Riflessione

| Domanda | Risposta |
|---|---|
| Problema principale e come l'avete risolto | Il problema principale è stato integrare la gestione dei dati JSON e CSV con il frontend. È stato risolto utilizzando Node.js ed Express: il server legge i dati dai file JSON e li rende disponibili all'interfaccia frontend, che li visualizza correttamente. |
| Un miglioramento futuro | Aggiungere controlli più completi sugli input per impedire l'inserimento di dati non validi e rendere l'applicazione più robusta. |

## 4. Uso dell'AI

| Strumento | Richiesta/parte assistita | Decisione del gruppo | Prova con cui avete controllato |
|---|---|---|---|
| ChatGPT | Aiuto nella scrittura, correzione e comprensione del codice. | I suggerimenti sono stati valutati e utilizzati quando ritenuti utili. | Il codice suggerito è stato sempre verificato attraverso prove pratiche nel progetto. |
| Gemini | Chiarimenti, curiosità e risposte a domande emerse durante lo sviluppo. | Le informazioni sono state utilizzate come supporto durante il lavoro. | Le informazioni utili sono state confrontate con le necessità del progetto. |

## 5. Contributi

| Componente | Cosa ha fatto | Funzione che sa spiegare |
|---|---|---|
| Achraf Bourja | Project Manager, coordinamento del gruppo, supporto frontend e integrazione tra Node.js ed Express. | Organizzazione del progetto, funzionamento del frontend e integrazione tra Node.js ed Express. |
| Giuseppe Bizzoca | Sviluppo del backend. | Funzionamento del backend Python e gestione delle operazioni principali. |
| Giovanni Dellicarri | Testing e verifica delle funzionalità. | Test delle funzionalità e verifica dei risultati. |
| Marco Felcini | Gestione e organizzazione dei dati JSON. | Struttura dei file JSON e gestione dei dati. |

## Pronto per la consegna?

- [x] Ogni test ha un esito e un osservato.
- [x] Ogni obiettivo ha un esito e una prova.
- [x] La dichiarazione AI è compilata.
- [x] Nessun segnaposto è rimasto nel file.