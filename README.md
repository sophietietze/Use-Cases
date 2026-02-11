# Automatisierte Content-Lokalisierung & "Transcreation"

Ein E-Commerce-Shop möchte seine deutschen Produktbeschreibungen für den spanischen und französischen Markt anpassen – aber nicht nur übersetzen, sondern kulturell optimieren.

**Kulturelle Adaption:** Automatische Anpassung von Maßeinheiten, Währungen und Redewendungen.
**Stil-Engine:** Wähle zwischen Luxuriös, Spielerisch, Professionell, Nachhaltig und mehr.
**Back-Translation:** Erhalte eine deutsche Rückübersetzung zur Qualitätskontrolle.
**Globale Reichweite:** Unterstützung für internationale Zielmärkte

**Voraussetzungen**
Stelle sicher, dass du folgende Dinge installiert hast:

**Python 3.9 oder höher**
**Google AI Studio API Key**

**Installation & Setup**
Folge diesen Schritten, um das Tool in deinem Ordner **use_case** einzurichten:


# 1. Vorbereitung & Setup

Öffne dein **Terminal** (oder CMD), navigiere in deinen Ordner und führe diese Befehle aus, um die notwendigen Pakete zu installieren und die Struktur anzulegen:

```bash
# In den Ordner wechseln
cd use_case
```


```bash
# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate
```

```bash
# Bibliotheken installieren
pip install google-generativeai gradio python-dotenv
```

# 2. Die Dateien erstellen

Erstelle in deinem Ordner use_case zwei Dateien:

**A)** ```bash .env ``` (Deine Zugangsdaten)

Hier speicherst du deinen API-Key sicher ab.
```bash
GEMINI_API_KEY=DEIN_API_KEY_HIER_EINSETZEN
```
Einen **Google AI Studio API Key** kannst du kostenlos unter [aistudio.google.com](https://aistudio.google.com/api-keys?projectFilter=gen-lang-client-0695470617)) erstellen und kopieren.


**B)** ```bash app.py ``` (Das Programm)

Kopiere diesen Code in die Datei. Er enthält die Logik für das Interface und den optimierten Transcreation-Prompt.

```bash
import os
import time
import gradio as gr
from google import genai
from dotenv import load_dotenv

# Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def transcreate_with_retry(text, target_lang, vibe, retries=3):
    if not text:
        return "Bitte gib einen Quelltext ein."
    
    prompt = f"""
    Du bist ein Senior Copywriter für den Markt {target_lang}.
    Aufgabe: Lokalisiere diesen Text. Stilvorgabe: {vibe}.
    Text: {text}
    """
    
    for i in range(retries):
        try:
            # Wir nutzen das Modell aus deiner Liste
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            return response.text
        
        except Exception as e:
            if "429" in str(e) and i < retries - 1:
                wait_time = 35  # Wir warten etwas länger als die geforderten 33s
                print(f"Limit erreicht. Warte {wait_time}s... (Versuch {i+1}/{retries})")
                time.sleep(wait_time)
                continue
            return f"Fehler nach mehreren Versuchen: {str(e)}"

# Modernisiertes Interface
with gr.Blocks(title="Gemini Transcreator 2026") as demo:
    gr.Markdown("# 🚀 AI Content Localizer (Gemini 2.5 Flash)")
    
    with gr.Row():
        with gr.Column(scale=1):
            source = gr.Textbox(label="Deutscher Quelltext", lines=8, placeholder="Füge hier die Produktbeschreibung ein...")
            lang = gr.Dropdown(choices=["Spanisch", "Französisch", "Italienisch", "Englisch (UK)"], label="Zielsprache", value="Spanisch")
            vibe = gr.Dropdown(choices=["Luxuriös/Elegant", "Spielerisch/Jung", "Professionell", "Nachhaltig"], label="Stilrichtung", value="Luxuriös/Elegant")
            btn = gr.Button("Lokalisierung starten", variant="primary")
            
        with gr.Column(scale=1):
            output = gr.Textbox(label="Lokalisierter Text", lines=15, interactive=False)
            gr.Markdown("ℹ️ *Das Tool wartet bei Quota-Limits automatisch 35 Sekunden.*")

    btn.click(fn=transcreate_with_retry, inputs=[source, lang, vibe], outputs=output)

if __name__ == "__main__":
    demo.launch()
```

# 3. Starten des Tools

Wenn du beide Dateien im Ordner und gespeichert hast, startest du das Tool mit:

```bash
python app.py
```

Das Terminal gibt dir eine URL (meist **http://127.0.0.1:7860**). Öffne diese im Browser, und du hast dein fertiges Interface.

# Troubleshooting

Falls das Tool nicht wie erwartet startet, prüfe folgende Punkte:

**Problem	Ursache	Lösung**
```bash
ModuleNotFoundError
```
Bibliotheken fehlen im venv.	Stelle sicher, dass (venv) im Terminal steht und führe pip install -U google-genai gradio python-dotenv erneut aus.

```bash
401 Unauthorized
```
API-Key ist falsch oder ungültig.	Prüfe die .env Datei. Der Key darf keine Anführungszeichen enthalten (z. B. GEMINI_API_KEY=AIza...).

```bash
429 Resource Exhausted
```
Free-Tier Limit erreicht.	Das Tool wartet automatisch 35 Sek. Sollte es dauerhaft auftreten, prüfe im Google AI Studio dein Kontingent.

```bash
404 Not Found
```
Falscher Modellname. Dein Key unterstützt evtl. nur bestimmte Modelle. Ersetze im Code gemini-2.5-flash durch gemini-1.5-flash.
