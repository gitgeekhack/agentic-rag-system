import gradio as gr
import requests

# FastAPI server URL for the first interface
FASTAPI_URL = "http://localhost:8000/query"

# Function to call the FastAPI endpoint
def query_backend(text=None, audio=None, microphone=None, voice_enabled=False):
    try:
        data = {"voice_enabled": str(voice_enabled).lower()}
        files = {}

        if audio:
            files["audio"] = open(audio, "rb")
        elif microphone:
            files["microphone"] = open(microphone, "rb")
        elif text:
            data["text"] = text

        response = requests.post(FASTAPI_URL, data=data, files=files)

        # Handle API response
        if response.status_code == 200:
            data = response.json()
            print("API Response:", data)  # Debugging line
            response_text = data.get("response")
            audio_path = data.get("audio")
            if audio_path:
                audio_path = f"../{audio_path}"
            return response_text, audio_path
        else:
            return f"Error: {response.status_code}, {response.text}", None

    except Exception as e:
        return f"Error: {str(e)}", None

    finally:
        for file in files.values():
            file.close()

# Create the Gradio interface for the first endpoint
iface = gr.Interface(
    fn=query_backend,
    inputs=[
        gr.Textbox(label="Enter your query (Text)", placeholder="Type your question here..."),
        gr.Audio(label="Upload an audio file (optional)", type="filepath"),
        gr.Microphone(label="Use microphone input (optional)", type="filepath"),
        gr.Checkbox(label="Enable Voice Response (TTS)")
    ],
    outputs=[
        "text",
        gr.Audio(label="Response Audio", type="filepath")
    ],
    title="User Query (Text/Audio)",
    description="Ask a query in text or upload an audio file. The response will be in text and optionally in audio form if voice response is enabled."
)

# Launch the Gradio interface
if __name__ == "__main__":
    iface.launch()
