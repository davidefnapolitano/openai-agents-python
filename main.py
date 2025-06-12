from agents import Agent, Runner

# Definizione agenti
dev = Agent(
    name="Developer",
    instructions=(
        "Agisci come uno sviluppatore web. Ricevi da Project Manager i contenuti e le specifiche di design, "
        "e scrivi codice HTML, CSS (e JS se serve) pronto all’uso, pulito, responsive e ben strutturato. "
        "Restituisci solo i file: index.html, styles.css, script.js (se usato)."
    )
)

designer = Agent(
    name="Designer",
    instructions=(
        "Agisci come un web designer UX/UI. Fornisci layout responsivo, palette colori, font, stile dei bottoni, spaziature. "
        "Scrivi tutto come specifiche CSS da passare al Developer. Non scrivere codice."
    )
)

copywriter = Agent(
    name="Copywriter",
    instructions=(
        "Agisci come un copywriter. Scrivi contenuti chiari e persuasivi per il sito: titoli, testo delle sezioni, bio, contatti. "
        "Non scrivere codice né suggerimenti grafici."
    )
)

pm = Agent(
    name="Project Manager",
    instructions=(
        "Agisci come Project Manager. Ricevi dal cliente la richiesta iniziale e dividi il lavoro tra Developer, Designer e Copywriter. "
        "Organizza i loro risultati, raccoglili e restituiscili in forma di pacchetto completo (HTML, CSS, contenuti). "
        "Non scrivere codice né testi direttamente: coordina il team."
    ),
    handoffs=[dev, designer, copywriter],
)

# Input iniziale dell'utente (cliente)
brief = (
    "Voglio un sito portfolio elegante per un fotografo freelance. Deve avere: "
    "homepage con foto d’impatto, una sezione biografia, una galleria con immagini, una sezione contatti. "
    "Stile moderno, sobrio, mobile-friendly."
)

# Esecuzione
result = Runner.run_sync(pm, brief)
print(result.final_output)
