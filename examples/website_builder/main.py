import html
import os

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from agents import Agent, Runner, gen_trace_id, handoff, trace

DEVELOPER_PROMPT = """Agisci come uno sviluppatore web senior. Ricevi task dal Project Manager e scrivi codice funzionante, ordinato e moderno in HTML, CSS e JavaScript. Il codice deve essere pronto all'uso e separato logicamente in:
- index.html
- styles.css
- script.js (se necessario)

Assicurati che:
- Il sito sia responsive e compatibile con i browser moderni
- I riferimenti ai contenuti e al design siano corretti
- Il codice sia commentato nei punti chiave

Non occuparti di testi o design. Aspettati che quei contenuti ti siano forniti dal Copywriter e dal Designer."""

DESIGNER_PROMPT = """Agisci come un web designer esperto in UX/UI. Il tuo compito è creare lo stile visivo del sito seguendo le richieste del Project Manager. Fornisci:
- Scelte di colori e palette
- Tipografia consigliata
- Layout per desktop e mobile
- Eventuali elementi UI (bottoni, moduli, spacing)

Scrivi le specifiche in modo che il Developer possa implementarle facilmente nel CSS. Non creare immagini o mockup grafici, ma descrivi lo stile visivo in modo preciso.

Non occuparti del codice o dei testi: solo design."""

COPYWRITER_PROMPT = """Agisci come un copywriter professionista per siti web. Scrivi tutti i contenuti testuali su richiesta del Project Manager, inclusi:
- Titoli e sottotitoli
- Sezioni \"Chi sono\", \"Servizi\", \"Contatti\"
- Call to action e testi per bottoni
- Testi per moduli e footer

Usa uno stile coerente con il tipo di sito (es. portfolio creativo, aziendale, elegante). Assicurati che il linguaggio sia chiaro, persuasivo e adatto al target.

Non occuparti del codice o dello stile visivo."""

PM_PROMPT = """Agisci come un Project Manager esperto nello sviluppo di siti web. Ricevi richieste dal cliente (utente) e suddividi il lavoro in task per il team, che comprende:
- Developer: scrive codice HTML, CSS, JavaScript.
- Designer: propone lo stile visivo, UI/UX, colori, layout responsivo.
- Copywriter: scrive tutti i contenuti testuali del sito.

Il tuo obiettivo è coordinare il team per produrre un sito web completo. Assicurati che:
- Ogni agente riceva task chiari
- I file finali siano completi: .html, .css, ed eventuale JS
- I contenuti siano coerenti tra loro

Quando il lavoro è completato, raccogli tutto il materiale e invialo all'utente in modo ordinato (anche come codice incorporato o allegati, se possibile).

Non eseguire tu stesso i task tecnici. Comunica con l'utente solo per definire il progetto e restituire l'output finale."""


developer_agent = Agent(name="Developer", instructions=DEVELOPER_PROMPT)

designer_agent = Agent(name="Designer", instructions=DESIGNER_PROMPT)

copywriter_agent = Agent(name="Copywriter", instructions=COPYWRITER_PROMPT)

project_manager_agent = Agent(
    name="Project Manager",
    instructions=PM_PROMPT,
    handoffs=[handoff(developer_agent), handoff(designer_agent), handoff(copywriter_agent)],
)


PAGE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset=\"UTF-8\">
    <title>Website Builder</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 2rem; }}
        textarea {{ width: 100%; height: 10rem; }}
        pre {{ white-space: pre-wrap; background-color: #f4f4f4; padding: 1rem; }}
    </style>
</head>
<body>
    <h1>Website Builder</h1>
    <form method=\"post\" action=\"/generate\">
        <textarea name=\"prompt\" placeholder=\"Descrivi il sito che desideri\">{prompt}</textarea>
        <button type=\"submit\">Avvia</button>
    </form>
    {result_block}
</body>
</html>"""


app = FastAPI()


def render_page(prompt: str = "", result: str | None = None) -> HTMLResponse:
    result_block = ""
    if result:
        result_block = f"<h2>Risultato</h2><pre>{html.escape(result)}</pre>"
    content = PAGE_TEMPLATE.format(prompt=html.escape(prompt), result_block=result_block)
    return HTMLResponse(content)


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return render_page()


@app.post("/generate", response_class=HTMLResponse)
async def generate(prompt: str = Form(...)) -> HTMLResponse:
    trace_id = gen_trace_id()
    with trace(workflow_name="Website builder", trace_id=trace_id):
        result = await Runner.run(project_manager_agent, prompt)
    final_output = (
        f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n\n"
        f"{result.final_output}"
    )
    return render_page(prompt, final_output)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
