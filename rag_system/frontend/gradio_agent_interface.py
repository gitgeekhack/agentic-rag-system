import gradio as gr
import requests

# FastAPI server URL for the second interface
FASTAPI_AGENT_URL = "http://localhost:8000/query_agent"

# Function to call the FastAPI agent endpoint
def query_agent_backend(text=None, audio=None, microphone=None, voice_enabled=False):
    try:
        data = {"voice_enabled": str(voice_enabled).lower()}
        files = {}

        if audio:
            files["audio"] = open(audio, "rb")
        elif microphone:
            files["microphone"] = open(microphone, "rb")
        elif text:
            data["text"] = text

        response = requests.post(FASTAPI_AGENT_URL, data=data, files=files)

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

# Create the Gradio interface for agent query
iface_agent = gr.Interface(
    fn=query_agent_backend,
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
    title="Agent Query Interface",
    description="Ask a query, and the agent will process it using different tools. The response will be in text and audio form."
)

# Launch the Gradio interface
if __name__ == "__main__":
    iface_agent.launch()
