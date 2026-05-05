# AutoTrack — CLAUDE.md

## Panoramica progetto

**AutoTrack** è una Progressive Web App (PWA) per la gestione delle spese e della manutenzione dell'auto. L'interfaccia è in italiano. Il progetto è monolitico: tutto il codice (HTML, CSS, JS) si trova in `index.html`.

## Struttura file

```
index.html      # App principale — HTML + CSS + JS in un unico file
autotrack.html  # Versione alternativa / prototipo (non in uso attivo)
sw.js           # Service Worker per cache offline (CACHE: 'autotrack-v10')
manifest.json   # Manifest PWA
icon-192.png    # Icona app
icon-512.png    # Icona app
```

## Stack tecnologico

- **Frontend**: HTML/CSS/JS vanilla, nessun framework, nessun bundler
- **Backend/DB**: Firebase Firestore (SDK v10.12.2 caricato da CDN via `import` ES module)
- **PWA**: Service Worker con cache-first strategy
- **Font**: Bebas Neue (titoli), DM Sans (corpo), JetBrains Mono (numeri) — Google Fonts

## Architettura JS

Il codice JS si trova in un `<script type="module">` alla fine di `index.html`.

### Collezioni Firestore
- `cars` — veicoli registrati
- `events` — tutti gli eventi (rifornimenti, manutenzioni, pneumatici, spese generiche)
- `settings` — impostazioni (lista pezzi, categorie spese)

### Wrapper DB
Funzioni uniformi che wrappano Firestore: `dbGetAll(store)`, `dbGet(store, key)`, `dbAdd(store, obj)`, `dbPut(store, obj)`, `dbDelete(store, key)`.

### State globale
```js
let state = {
  cars, events, parts, categories,
  currentCarId, selectedParts,
  editingCarId, editingEventId,
  currentSottoTipo  // 'ordinaria' | 'straordinaria'
}
```

### Viste (navigazione a tab)
- `dashboard` — statistiche e riepilogo
- `movimenti` — lista eventi filtrabili
- `garage` — gestione veicoli
- `settings` — configurazione pezzi e categorie

### Tipi di evento
- `rifornimento` — carburante (litri, prezzo/L, km)
- `manutenzione` — ordinaria o straordinaria (pezzi sostituiti, officina)
- `pneumatici` — cambio gomme (marca, misura, stagione, quantità)
- `altro` — spesa generica (categorie personalizzabili)

## Design system (CSS custom properties)

```css
--bg: #0f1923        /* sfondo principale */
--accent: #e8431a    /* rosso accento */
--gold: #f0a500      /* dorato (manutenzione ordinaria) */
--green: #22c55e     /* verde (rifornimento) */
--blue: #3b82f6      /* blu (manutenzione straordinaria) */
--purple: #8b5cf6    /* viola */
--radius: 14px
--font-head: 'Bebas Neue'
--font-body: 'DM Sans'
--font-mono: 'JetBrains Mono'
```

## Convenzioni

- Lingua interfaccia: **italiano**
- Formati: date `it-IT` (gg mmm aaaa), valute `€ X.XXX,XX`, km con separatore migliaia
- Il Service Worker usa il cache name `autotrack-vN` — incrementare `N` ad ogni deploy che modifica asset cachati
- Non c'e' sistema di build: modificare direttamente `index.html` e ricaricare il browser
- Firebase config hardcoded nel file (progetto: `autotrack-8bb15`)

## Pattern comuni

- Apertura modale: `openModal('modalXxx')` / `closeModal('modalXxx')`
- Toast notifiche: `showToast('messaggio', ms)`
- Loader: `showLoader('msg')` / `hideLoader()`
- Render view: `renderDashboard()`, `renderMovimenti()`, `renderGarage()`, `renderSettings()`
- Salvataggio evento: funzioni `saveRefuel()`, `saveService()`, `saveTyre()`, `saveOther()`
