// ==========================================
// CAMPUSBOARD - FRONTEND JAVASCRIPT
// ==========================================

let datiTotali = [];
let filtroAttuale = 'Tutte';
let caricamentoInCorso = false;

// ==========================================
// UTILITY
// ==========================================

function escapeHTML(value) {
    return String(value ?? '').replace(/[&<>"']/g, char => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    })[char]);
}

// Icone in base alla categoria
function getCategoriaIcon(categoria) {
    switch (categoria?.toLowerCase()) {
        case 'oggetto trovato':
            return '🔍';
        case 'segnalazione':
            return '🔔';
        case 'evento':
            return '📅';
        default:
            return '📌';
    }
}

// Badge stato
function getStatoBadgeClass(stato) {
    switch (stato?.toLowerCase()) {
        case 'aperta':
        case 'attivo':
        case 'trovato':
            return 'badge-aperto';

        case 'in_corso':
        case 'in corso':
            return 'badge-corso';

        case 'chiusa':
        case 'chiuso':
        case 'restituito':
        case 'archiviato':
            return 'badge-chiuso';

        default:
            return 'badge-default';
    }
}

// ==========================================
// FILTRI
// ==========================================

function filtra(tipo, elemento) {
    filtroAttuale = tipo;

    const pulsanti = document.querySelectorAll(
        '.btn-filter, .nav-item'
    );

    pulsanti.forEach(btn => {
        btn.classList.remove('active');
    });

    // Supporta onclick="filtra('Tutte', event)"
    // e onclick="filtra('Tutte', this)"
    const btnCliccato =
        elemento?.currentTarget ||
        elemento?.target ||
        elemento;

    if (btnCliccato?.classList) {
        btnCliccato.classList.add('active');
    }

    // Sincronizza sidebar e filtri superiori
    pulsanti.forEach(btn => {
        const onclick = btn.getAttribute('onclick') || '';

        if (
            onclick.includes(`'${tipo}'`) ||
            onclick.includes(`"${tipo}"`)
        ) {
            btn.classList.add('active');
        }
    });

    renderCards();
}

// ==========================================
// CARICAMENTO DATI
// ==========================================

async function caricaDati() {

    // Evita richieste sovrapposte
    if (caricamentoInCorso) return;

    caricamentoInCorso = true;

    try {

        // ----------------------------------
        // BACHECA
        // ----------------------------------

        const resBacheca = await fetch('/api/bacheca');

        if (!resBacheca.ok) {
            throw new Error(
                `Errore bacheca: ${resBacheca.status}`
            );
        }

        const datiBacheca = await resBacheca.json();

        let attivi = [];
        let archiviati = [];

        // Supporta API che restituisce un array
        if (Array.isArray(datiBacheca)) {

            attivi = datiBacheca;

        } else {

            attivi = Array.isArray(datiBacheca.attivi)
                ? datiBacheca.attivi
                : [];

            archiviati = Array.isArray(datiBacheca.archiviati)
                ? datiBacheca.archiviati
                : [];
        }

        // ----------------------------------
        // Normalizzazione dati
        // ----------------------------------

        const listaAttivi = attivi.map(item => ({
            ...item,
            isArchiviato: false
        }));

        const listaArchivio = archiviati.map(item => ({
            ...item,
            isArchiviato: true
        }));

        datiTotali = [
            ...listaAttivi,
            ...listaArchivio
        ];

        // ----------------------------------
        // NOTIFICHE
        // ----------------------------------

        const badgeNotifiche =
            document.getElementById('badge-notifiche');

        if (badgeNotifiche) {
            badgeNotifiche.textContent = listaAttivi.length;
        }

        // ----------------------------------
        // CARD
        // ----------------------------------

        renderCards();

        // ----------------------------------
        // STATISTICHE
        // ----------------------------------

        try {

            const resRiepilogo =
                await fetch('/api/riepilogo');

            if (resRiepilogo.ok) {

                const stats = await resRiepilogo.json();

                const statAperti =
                    document.getElementById('stat-aperti');

                const statChiusi =
                    document.getElementById('stat-chiusi');

                if (statAperti) {
                    statAperti.textContent =
                        stats.aperti ?? listaAttivi.length;
                }

                if (statChiusi) {
                    statChiusi.textContent =
                        stats.chiusi ?? listaArchivio.length;
                }

            }

        } catch (erroreStats) {

            console.warn(
                'Statistiche non disponibili:',
                erroreStats
            );

        }

    } catch (err) {

        console.error(
            'Errore caricamento bacheca:',
            err
        );

    } finally {

        caricamentoInCorso = false;

    }
}

// ==========================================
// RENDER CARD
// ==========================================

function renderCards() {

    const container =
        document.getElementById('board');

    if (!container) return;

    container.innerHTML = '';

    // ----------------------------------
    // FILTRAGGIO
    // ----------------------------------

    const filtrati = datiTotali.filter(item => {

        if (filtroAttuale === 'Tutte') {
            return true;
        }

        if (filtroAttuale === 'attivi') {
            return !item.isArchiviato;
        }

        if (filtroAttuale === 'archiviati') {
            return item.isArchiviato;
        }

        return (
            item.categoria?.toLowerCase() ===
            filtroAttuale.toLowerCase()
        );
    });

    // ----------------------------------
    // STATO VUOTO
    // ----------------------------------

    if (filtrati.length === 0) {

        const empty = document.createElement('div');

        empty.className = 'empty-state';

        empty.innerHTML = `
            <span class="empty-icon">📭</span>

            <p>
                Nessuna segnalazione presente
                per questa categoria.
            </p>
        `;

        container.appendChild(empty);

        return;
    }

    // ----------------------------------
    // CREAZIONE CARD
    // ----------------------------------

    filtrati.forEach((item, index) => {

        const card = document.createElement('article');

        const categoria =
            item.categoria || 'Altro';

        const catClass = categoria
            .toLowerCase()
            .replace(/\s+/g, '-');

        card.className = `card ${catClass}`;

        if (item.isArchiviato) {
            card.classList.add('card-archiviata');
        }

        card.style.animationDelay =
            `${index * 0.06}s`;

        const icona =
            getCategoriaIcon(categoria);

        const stato =
            item.stato ||
            (item.isArchiviato ? 'Chiuso' : 'Attivo');

        const statoClass =
            getStatoBadgeClass(stato);

        const storico =
            Array.isArray(item.storico)
                ? item.storico
                : [];

        // ----------------------------------
        // CRONOLOGIA
        // ----------------------------------

        const cronologia = storico.length > 0

            ? storico.map(s => `
                <li>
                    <strong>
                        ${escapeHTML(s.stato)}
                    </strong>

                    <span>
                        - ${escapeHTML(s.data)}
                    </span>
                </li>
            `).join('')

            : `
                <li>
                    Nessuna modifica registrata
                </li>
            `;

        // ----------------------------------
        // CONTENUTO CARD
        // ----------------------------------

        card.innerHTML = `

            <div class="card-header">

                <span class="badge badge-categoria">

                    ${icona}

                    ${escapeHTML(categoria)}

                </span>

                <span class="badge ${statoClass}">

                    ${escapeHTML(stato)}

                </span>

            </div>

            <h3 class="card-title">

                ${escapeHTML(
                    item.titolo || 'Senza titolo'
                )}

            </h3>

            <div class="card-details">

                <p class="meta">

                    📍 <strong>Luogo:</strong>

                    ${escapeHTML(
                        item.luogo || 'Non specificato'
                    )}

                </p>

                <p class="meta">

                    📅 <strong>Data:</strong>

                    ${escapeHTML(
                        item.data || 'N/D'
                    )}

                </p>

            </div>

            <details class="card-history">

                <summary>

                    Cronologia stati (${storico.length})

                </summary>

                <ul>

                    ${cronologia}

                </ul>

            </details>

        `;

        container.appendChild(card);

    });
}

// ==========================================
// MODALITÀ NOTTURNA
// ==========================================

function inizializzaTema() {

    const themeToggle =
        document.getElementById('themeToggle');

    if (!themeToggle) {

        console.warn(
            'Pulsante themeToggle non trovato'
        );

        return;
    }

    // Evita duplicazione degli eventi
    if (
        themeToggle.dataset.themeInitialized === 'true'
    ) {
        return;
    }

    themeToggle.dataset.themeInitialized = 'true';

    function aggiornaTema() {

        const darkMode =
            document.body.classList.contains('dark-mode');

        themeToggle.textContent =
            darkMode ? '🌙' : '☀️';

        themeToggle.setAttribute(
            'aria-label',
            darkMode
                ? 'Attiva modalità chiara'
                : 'Attiva modalità notturna'
        );

        themeToggle.setAttribute(
            'aria-pressed',
            String(darkMode)
        );
    }

    themeToggle.addEventListener('click', () => {

        document.body.classList.toggle('dark-mode');

        aggiornaTema();

    });

    aggiornaTema();
}

// ==========================================
// AVVIO APPLICAZIONE
// ==========================================

function inizializzaCampusBoard() {

    inizializzaTema();

    caricaDati();

    // Aggiornamento automatico ogni 3 secondi
    setInterval(caricaDati, 3000);

}

// Compatibilità con script defer
if (document.readyState === 'loading') {

    document.addEventListener(
        'DOMContentLoaded',
        inizializzaCampusBoard
    );

} else {

    inizializzaCampusBoard();

}