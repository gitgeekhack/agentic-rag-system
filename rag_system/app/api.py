import os
import logging
import aiofiles
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from app.query_agent import process_agent_query, process_query
from app.sarvam_integration import speech_to_text, text_to_speech
from fastapi.staticfiles import StaticFiles

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI()

# Serve static files for audio responses
app.mount("/uploads", StaticFiles(directory="./app/uploads"), name="uploads")

# Ensure uploads directory exists
if not os.path.exists("./app/uploads"):
    os.makedirs("./app/uploads")

class QueryRequest(BaseModel):
    text: str = None  # Optional field
    voice_enabled: bool = False

@app.post("/query")
async def query_api(
    text: str = Form(None),  # Text input
    audio: UploadFile = File(None),  # Audio file input
    microphone: UploadFile = File(None),  # Microphone input (treated as an audio file)
    voice_enabled: bool = Form(False)  # Whether TTS should be enabled
):
    """
    FastAPI endpoint to handle user queries.
    Handles text-based queries, voice-based queries (from uploaded files or microphone).
    """
    user_query = None

    if audio:
        # Read and save uploaded audio file
        audio_data = await audio.read()
        audio_file_path = f"./app/uploads/{audio.filename}"
        async with aiofiles.open(audio_file_path, "wb") as f:
            await f.write(audio_data)

        # Convert speech to text using Sarvam STT
        user_query = speech_to_text(audio_file_path)
        if user_query.startswith("Error"):
            return {"error": user_query}

        # Optionally delete the audio file after processing
        os.remove(audio_file_path)

    elif microphone:
        # Read and save microphone input
        mic_data = await microphone.read()
        mic_file_path = f"./app/uploads/{microphone.filename}"
        async with aiofiles.open(mic_file_path, "wb") as f:
            await f.write(mic_data)

        # Convert speech to text using Sarvam STT
        user_query = speech_to_text(mic_file_path)
        if user_query.startswith("Error"):
            return {"error": user_query}

        # Optionally delete the microphone file after processing
        os.remove(mic_file_path)

    elif text:
        user_query = text

    else:
        return {"error": "No input provided"}

    # Process the user query
    result = process_query(user_query, voice_enabled=voice_enabled)
    logging.info(f"Query Result: {result}")

    audio_response_url = None
    if voice_enabled:
        # Convert response text to speech if voice-enabled is True
        audio_response = text_to_speech(result["response"])
        if isinstance(audio_response, str) and os.path.exists(audio_response):
            audio_response_url = f"./app/uploads/{os.path.basename(audio_response)}"

    return {
        "query": user_query,
        "response": result["response"],
        "audio": audio_response_url  # Return the URL to the audio file if TTS is enabled
    }

@app.post("/query_agent")
async def query_agent_api(
    text: str = Form(None),  # Text input
    audio: UploadFile = File(None),  # Audio file input
    microphone: UploadFile = File(None),  # Microphone input (treated as an audio file)
    voice_enabled: bool = Form(False)  # Whether TTS should be enabled
):
    """
    FastAPI endpoint to handle agent-based queries.
    Handles voice-based queries (from uploaded files or microphone), and text-based queries.
    """
    user_query = None

    if audio:
        # Read and save uploaded audio file
        audio_data = await audio.read()
        audio_file_path = f"./app/uploads/{audio.filename}"
        async with aiofiles.open(audio_file_path, "wb") as f:
            await f.write(audio_data)

        # Convert speech to text using Sarvam STT
        user_query = speech_to_text(audio_file_path)
        if user_query.startswith("Error"):
            return {"error": user_query}

        # Optionally delete the audio file after processing
        os.remove(audio_file_path)

    elif microphone:
        # Read and save microphone input
        mic_data = await microphone.read()
        mic_file_path = f"./app/uploads/{microphone.filename}"
        async with aiofiles.open(mic_file_path, "wb") as f:
            await f.write(mic_data)

        # Convert speech to text using Sarvam STT
        user_query = speech_to_text(mic_file_path)
        if user_query.startswith("Error"):
            return {"error": user_query}

        # Optionally delete the microphone file after processing
        os.remove(mic_file_path)

    elif text:
        user_query = text

    else:
        return {"error": "No input provided"}

    # Process the query using the agent logic
    result = process_agent_query(user_query, voice_enabled=voice_enabled)
    logging.info(f"Agent Query Result: {result}")

    audio_response_url = None
    if voice_enabled:
        # Convert response text to speech if voice-enabled is True
        audio_response = text_to_speech(result["response"])
        if isinstance(audio_response, str) and os.path.exists(audio_response):
            audio_response_url = f"./app/uploads/{os.path.basename(audio_response)}"

    return {
        "query": user_query,
        "response": result["response"],
        "audio": audio_response_url  # Return the URL to the audio file if TTS is enabled
    }
