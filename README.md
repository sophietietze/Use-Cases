# Automated Content Localization & Transcreation

An e-commerce shop wants to adapt its German product descriptions for the Spanish and French markets—not just translate them, but optimize them culturally.

# Learning effect

**Business**: Understanding scaling effects and transcreation in global e-commerce.

**Computer Science**: API integration, modern package management with uv, and error handling.

**Languages**: Application of localization strategies instead of literal translation.

**Design**: Creating functional AI interfaces with Gradio.

# Key Features
**Cultural Adaptation**: Automatic adjustment of idioms and tone.

**Style Engine**: Choose between Luxurious, Playful, Professional, or Sustainable.

**Smart Retry:** Automatically handles API rate limits (429 errors) with a 35-second cooldown.

**Modern Stack:** Powered by Google Gemini 2.5 Flash and managed via ```bash uv. ```

# Installation & Setup
**1. Prerequisites:** 
Ensure you have the following installed:

1. Installed **uv**(If not: ```bash curl -LsSf https://astral.sh/uv/install.sh | sh or brew install uv```)

2. **Google AI Studio API Key** (Get it at (https://aistudio.google.com/app/api-keys))
   

**2. Initialize Project**
Navigate to your project folder and run:

```bash
#Initialize project structure
uv init
```

```bash
uv venv
```

```bash
# Add required libraries (uv handles venv automatically)
uv add google-genai gradio python-dotenv
```
uv automatically creates a pyproject.toml and a uv.lock file, which guarantees that everyone running your script uses exactly the same versions.

**3. Configuration**
Create a ```bash .env ``` file in the root directory:

```bash
GEMINI_API_KEY=YOUR_API_KEY
```

**4. Application Code**
Copy this code into the file. It contains the logic for the interface and the optimized transcreation prompt.

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
# ROLLE
Du bist ein erfahrener Senior Copywriter und Lokalisierungsexperte für den Zielmarkt {target_lang}. Deine Spezialität ist Transkreation, nicht nur bloße Übersetzung.

# KONTEXT & STIL
- **Zielmarkt:** {target_lang}
- **Gewünschte Tonalität (Vibe):** {vibe}
- **Zielgruppe:** Muttersprachler im Zielmarkt, die Wert auf Authentizität legen.

# AUFGABE
1. Analysiere den Kern der Botschaft des deutschen Textes.
2. Übertrage diese Botschaft in {target_lang}, wobei du lokale Redewendungen, kulturelle Nuancen und den Stil "{vibe}" beachtest.
3. Achte darauf, dass der Text natürlich klingt ("Native-level flow").

### QUELLE (DEUTSCH):
"{text}"

### LOKALISIERTES ERGEBNIS:
"""
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

# 4. Starten des Tools

Once you have saved both files in the folder, start the tool with:

```bash
uv run app.py
```

The terminal will give you a URL (usually **http://127.0.0.1:7860**). Open this in your browser, and you will have your finished interface.

# 5. Troubleshooting

If the tool does not start as expected, check the following:

**Problem Cause Solution**
```bash
ModuleNotFoundError
```
Libraries are missing in the venv. Make sure `(venv)` is displayed in the terminal and run `pip install -U google-genai gradio python-dotenv` again.

```bash
401 Unauthorized
```
API key is incorrect or invalid. Check the `.env` file. The key must not contain quotation marks (e.g., GEMINI_API_KEY=AIza...).

```bash
429 Resource Exhausted
```
Free-tier limit reached. The tool will automatically wait 35 seconds. If this error persists, check your quota in Google AI Studio.

```bash
404 Not Found
```
Incorrect model name. Your key may only support certain models. Replace `gemini-2.5-flash` with `gemini-1.5-flash` in the code.
