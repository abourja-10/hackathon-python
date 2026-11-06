let datiLocali = [];
let filtroCorrente = 'Tutte';

async function caricaBacheca() {
    try {
        const response = await fetch('/api/bacheca');

        if (!response.ok) {
            throw new Error('Errore nel caricamento della bacheca');
        }

        datiLocali = await response.json();
        renderBoard();

    } catch (err) {
        console.error("Errore fetch:", err);
    }
}

function renderBoard() {
    const container = document.getElementById('board');
    container.innerHTML = '';

    const filtrati = filtroCorrente === 'Tutte'
        ? datiLocali
        : datiLocali.filter(d =>
            d.categoria.toLowerCase() === filtroCorrente.toLowerCase()
        );

    if (filtrati.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                Nessuna segnalazione trovata.
            </div>
        `;
        return;
    }

    filtrati.forEach((item, index) => {
        const card = document.createElement('article');

        const catClass = item.categoria
            .toLowerCase()
            .replace(/\s+/g, '-');

        card.className = `card ${catClass}`;

        const emoji = item.categoria === 'Oggetto Trovato'
            ? '🔑'
            : item.categoria === 'Segnalazione'
                ? '📽️'
                : '🎓';

        card.style.animationDelay = `${index * 0.08}s`;

        card.innerHTML = `
            <div class="badge">${item.categoria}</div>

            <div class="card-illustration">${emoji}</div>

            <h3>${item.titolo}</h3>

            <p class="meta">
                📍 <strong>Luogo:</strong> ${item.luogo}
            </p>

            <p class="meta">
                📅 <strong>Data:</strong> ${item.data}
            </p>

            <button class="card-button" type="button">
                Vedi dettagli →
            </button>
        `;

        container.appendChild(card);
    });
}

function filtra(categoria, elemento) {
    filtroCorrente = categoria;

    // Aggiorna pulsanti dei filtri
    document.querySelectorAll('.btn-filter')
        .forEach(btn => btn.classList.remove('active'));

    // Aggiorna pulsanti sidebar
    document.querySelectorAll('.nav-item')
        .forEach(btn => btn.classList.remove('active'));

    // Evidenzia il pulsante cliccato
    if (elemento) {
        elemento.classList.add('active');
    }

    // Sincronizza menu e filtri
    document.querySelectorAll('.btn-filter, .nav-item')
        .forEach(btn => {
            const onclick = btn.getAttribute('onclick');

            if (onclick && onclick.includes(`'${categoria}'`)) {
                btn.classList.add('active');
            }
        });

    renderBoard();
}

// DARK MODE
const themeToggle = document.getElementById('themeToggle');

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');

    themeToggle.textContent =
        document.body.classList.contains('dark-mode')
            ? '🌙'
            : '☀️';
});

// Caricamento iniziale
caricaBacheca();

// Aggiornamento automatico
setInterval(caricaBacheca, 3000);