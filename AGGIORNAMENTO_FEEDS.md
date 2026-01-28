# Aggiornamento Feed News - Gruppo ATIS

## Panoramica

Il sito include due pagine di news che mostrano aggiornamenti in tempo reale:
- **News Sicurezza** (`news/sicurezza.html`) - Notizie su sicurezza sul lavoro
- **News Ambiente** (`news/ambiente.html`) - Notizie su ambiente e normativa

I feed vengono generati dallo script Python `scripts/build_feeds.py` che scarica notizie da fonti RSS e le salva in `feeds.json`.

---

## Aggiornamento manuale dei feed

### Prerequisiti
- Python 3.x installato

### Comando
```bash
cd c:\Users\atisg\sitowebgruppoatis
python scripts/build_feeds.py
```

Questo comando:
1. Scarica le ultime notizie dai feed RSS configurati
2. Genera il file `feeds.json` con le 10 notizie più recenti per categoria
3. Salva una cache in `.cache/feeds_cache.json` (valida 15 minuti)

---

## Configurazione dei feed RSS

Modifica il file `scripts/feeds_config.py`:

```python
FEEDS_SICUREZZA = [
    "https://www.ansa.it/sito/notizie/cronaca/cronaca_rss.xml",
    "https://www.ansa.it/sito/notizie/economia/economia_rss.xml",
]

FEEDS_AMBIENTE = [
    "https://www.ansa.it/sito/notizie/mondo/mondo_rss.xml",
    "https://www.ansa.it/sito/notizie/tecnologia/tecnologia_rss.xml",
]
```

Per aggiungere nuove fonti, inserisci l'URL del feed RSS nella lista appropriata.

---

## Automazione (opzionale)

### Windows Task Scheduler
Per aggiornare automaticamente i feed ogni ora:

1. Apri **Utilità di pianificazione** (Task Scheduler)
2. Crea nuova attività:
   - **Nome**: Aggiorna Feed ATIS
   - **Trigger**: Ogni ora
   - **Azione**: Avvia programma
     - Programma: `python`
     - Argomenti: `scripts/build_feeds.py`
     - Directory: `c:\Users\atisg\sitowebgruppoatis`

### GitHub Actions (per hosting su GitHub Pages)
Aggiungi `.github/workflows/update-feeds.yml`:

```yaml
name: Update Feeds

on:
  schedule:
    - cron: '0 */2 * * *'  # Ogni 2 ore
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      
      - name: Update feeds
        run: python scripts/build_feeds.py
      
      - name: Commit and push
        run: |
          git config --global user.name 'GitHub Actions'
          git config --global user.email 'actions@github.com'
          git add feeds.json
          git diff --staged --quiet || git commit -m "Aggiorna feed news"
          git push
```

---

## Test locale

Per testare le pagine news localmente:

```bash
cd c:\Users\atisg\sitowebgruppoatis
python -m http.server 8080
```

Poi apri nel browser:
- http://localhost:8080/news/sicurezza.html
- http://localhost:8080/news/ambiente.html

> **Nota**: Le pagine news NON funzionano aprendo direttamente il file HTML (`file://...`) a causa delle restrizioni di sicurezza del browser (CORS).

---

## Struttura file

```
sitowebgruppoatis/
├── feeds.json                 # Feed generato (NON modificare manualmente)
├── news/
│   ├── sicurezza.html         # Pagina news sicurezza
│   └── ambiente.html          # Pagina news ambiente
└── scripts/
    ├── build_feeds.py         # Script generazione feed
    ├── feeds_config.py        # Configurazione URL feed RSS
    └── update_pages.py        # Script aggiornamento testi pagine
```

---

## Troubleshooting

### "Aggiornamenti non disponibili al momento"
- Verifica la connessione internet
- Esegui `python scripts/build_feeds.py` manualmente
- Controlla che i feed RSS configurati siano ancora attivi

### Feed vuoti dopo l'aggiornamento
- Alcuni feed RSS potrebbero essere temporaneamente non disponibili
- Prova ad aggiungere feed alternativi in `feeds_config.py`
- Cancella la cache: `del .cache\feeds_cache.json`

### Errore "not a git repository"
Inizializza il repository git:
```bash
git init
git add .
git commit -m "Initial commit"
```

---

## Ultimo aggiornamento
- **Data**: 27 Gennaio 2026
- **Versione feed**: ANSA (Cronaca, Economia, Mondo, Tecnologia)
