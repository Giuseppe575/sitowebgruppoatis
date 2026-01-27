from pathlib import Path

REPLACEMENTS = {
    'Se vuoi, posso inserirti un form “vero” (con endpoint) oppure integrare WhatsApp/Calendly.':
        'Compila il form per una richiesta rapida: ti rispondiamo entro 24-48 ore lavorative.'
}

TARGETS = [
    'sito_restyling_ATIS_con_immagini.html',
    'servizi.html',
    'metodo.html',
    'laboratorio.html',
    'faq.html',
    'contatti.html',
    'preventivo.html',
]

for name in TARGETS:
    path = Path(name)
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    path.write_text(text, encoding='utf-8')

print('Update complete.')
