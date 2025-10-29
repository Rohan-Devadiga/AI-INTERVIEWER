import os
import queue
import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from deepgram import DeepgramClient, SpeakWebSocketEvents

load_dotenv()
API_KEY = os.getenv("STTKEY")
if not API_KEY:
    raise ValueError("Deepgram API key not found in .env")

def speak(text: str):
    """Speak text sequentially using Deepgram TTS."""
    # New client per call
    dg = DeepgramClient(API_KEY)
    audio_queue = queue.Queue()
    ws = dg.speak.websocket.v("1")  # new websocket

    def on_open(self, open, **kwargs):
        print("[TTS] Connection opened")

    def on_audio(self, data, **kwargs):
        audio = np.frombuffer(data, dtype=np.int16)
        audio_queue.put(audio)

    def on_close(self, close, **kwargs):
        audio_queue.put(None)
        print("[TTS] Connection closed")

    ws.on(SpeakWebSocketEvents.Open, on_open)
    ws.on(SpeakWebSocketEvents.AudioData, on_audio)
    ws.on(SpeakWebSocketEvents.Close, on_close)

    # Start websocket
    if not ws.start({
        "voice": "aura-2-thalia-en",
        "encoding": "linear16",
        "sample_rate": 48000
    }):
        print("[TTS] Failed to start connection")
        return

    # Open audio stream before sending text
    with sd.OutputStream(samplerate=48000, channels=1, dtype='int16') as stream:
        ws.send_text(text)
        ws.flush()

        # Playback loop with timeout
        while True:
            try:
                chunk = audio_queue.get(timeout=5)  # timeout ensures no hang
            except queue.Empty:
                print("[TTS] No audio received, ending stream")
                break
            if chunk is None:
                break
            stream.write(chunk)

    ws.finish()  # ensure websocket is closed
