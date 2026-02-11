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