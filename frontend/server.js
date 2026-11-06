const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// Espone i file statici contenuti nella cartella public
app.use(express.static(path.join(__dirname, 'public')));

// Percorso per leggere bacheca.json nella radice del progetto
const DATA_FILE = path.join(__dirname, '..', 'bacheca.json');

// Endpoint API per inviare i dati al browser
app.get('/api/bacheca', (req, res) => {
    fs.readFile(DATA_FILE, 'utf8', (err, data) => {
        if (err) {
            return res.json([]);
        }
        try {
            res.json(JSON.parse(data));
        } catch {
            res.status(500).json({ error: 'Errore nel parsing del file JSON' });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server frontend attivo su http://localhost:${PORT}`);
});