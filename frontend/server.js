const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'public')));

// Legge sia gli elementi attivi sia quelli archiviati
app.get('/api/bacheca', (req, res) => {
  const campusPath = path.join(__dirname, '..', 'dati', 'campus.json');
  const archivioPath = path.join(__dirname, '..', 'dati', 'archivio.json');

  let attivi = [];
  let archiviati = [];

  if (fs.existsSync(campusPath)) {
    try {
      attivi = JSON.parse(fs.readFileSync(campusPath, 'utf8'));
    } catch (e) {
      console.error("Errore lettura campus.json:", e);
    }
  }

  if (fs.existsSync(archivioPath)) {
    try {
      archiviati = JSON.parse(fs.readFileSync(archivioPath, 'utf8'));
    } catch (e) {
      console.error("Errore lettura archivio.json:", e);
    }
  }

  res.json({ attivi, archiviati });
});

// Endpoint per le statistiche aggregate
app.get('/api/riepilogo', (req, res) => {
  const riepilogoPath = path.join(__dirname, '..', 'output', 'riepilogo.json');
  if (fs.existsSync(riepilogoPath)) {
    try {
      const data = JSON.parse(fs.readFileSync(riepilogoPath, 'utf8'));
      return res.json(data);
    } catch (e) {
      console.error("Errore lettura riepilogo.json:", e);
    }
  }
  res.json({});
});

app.listen(PORT, () => {
  console.log(`Server frontend attivo su http://localhost:${PORT}`);
});