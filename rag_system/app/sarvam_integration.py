import os
import base64
import requests

SARVAM_API_KEY = os.getenv('SARVAM_API_KEY')
SARVAM_TTS_URL = "https://api.sarvam.ai/text-to-speech"
SARVAM_STTT_URL = "https://api.sarvam.ai/speech-to-text-translate"


def text_to_speech(text, language_code="en-IN", speaker="meera", pitch=0, pace=1.65, loudness=1.5,
                   speech_sample_rate=8000, model="bulbul:v1"):
    """
    Converts text to speech using Sarvam's TTS API.
    The API response returns a base64-encoded .wav audio file.
    """
    try:
        payload = {
            "inputs": [text],
            "target_language_code": language_code,
            "speaker": speaker,
            "pitch": pitch,
            "pace": pace,
            "loudness": loudness,
            "speech_sample_rate": speech_sample_rate,
            "enable_preprocessing": True,
            "model": model
        }
        headers = {
            "Content-Type": "application/json",
            "api-subscription-key": SARVAM_API_KEY
        }
        response = requests.post(SARVAM_TTS_URL, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()

            # Extract the base64-encoded audio from the response
            if 'audios' in result and len(result['audios']) > 0:
                base64_audio = result['audios'][0]

                # Decode the base64 string
                audio_data = base64.b64decode(base64_audio)

                # Save the decoded audio data to a .wav file
                output_file_path = "./app/uploads/output_speech.wav"
                with open(output_file_path, "wb") as f:
                    f.write(audio_data)

                return output_file_path  # Return path to the audio file
            else:
                return "Error: No audio data found in the response"
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


def speech_to_text(audio_file_path, model="saaras:v1"):
    """
    Converts speech to text using Sarvam's STT API.
    """
    try:
        # Open the audio file
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
        files = {
            'file': (os.path.basename(audio_file_path), audio_data, 'audio/wav')
        }
        data = {
            "model": model
        }
        headers = {
            "api-subscription-key": SARVAM_API_KEY
        }

        response = requests.post(SARVAM_STTT_URL, headers=headers, files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            # Extract the transcript from the response
            return result.get("transcript", "")
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"
