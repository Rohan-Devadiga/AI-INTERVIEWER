import os
import sounddevice as sd
import numpy as np
import threading
import time
import wave
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)

load_dotenv()

API_KEY = os.getenv("STTKEY")
if not API_KEY:
    raise ValueError("Set your Deepgram API key in environment: export STTKEY=your_key")

SAMPLE_RATE = 16000
CHANNELS = 1

# Globals
stop_event = threading.Event()
final_text = None
last_speech_time = None   # ⏱️ track when last speech was detected


def main():
    global final_text, last_speech_time
    final_text = None
    last_speech_time = None
    stop_event.clear()

    try:
        deepgram = DeepgramClient(API_KEY)
        dg_connection = deepgram.listen.websocket.v("1")

        # 🎯 On transcript
        def on_message(self, result, **kwargs):
            global final_text, last_speech_time
            sentence = result.channel.alternatives[0].transcript
            if not sentence:
                return

            if result.is_final:
                final_text = sentence
                last_speech_time = time.time()  # reset silence timer
                print(f"✅ Heard: {final_text}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-3",
            punctuate=True,
            interim_results=False,
            encoding="linear16",
            sample_rate=SAMPLE_RATE
        )

        if not dg_connection.start(options):
            print("❌ Failed to start connection")
            return None
          
        wav_file = wave.open("answer.wav", "wb")
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(SAMPLE_RATE)


        # 🎙️ Mic stream
        def mic_stream():
            def callback(indata, frames, time_info, status):
                if status:
                    print(status)
                audio_data = (indata * 32767).astype(np.int16).tobytes()
                dg_connection.send(audio_data)
                wav_file.writeframes(audio_data)

            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype="float32",
                callback=callback
            ):
                print("🎙️ Speak your answer (auto-stops after 3s of silence)...")

                # 🔄 Keep checking for silence
                while not stop_event.is_set():
                    if last_speech_time and (time.time() - last_speech_time > 3):
                        stop_event.set()  # stop after 3s silence
                    time.sleep(0.2)

        mic_thread = threading.Thread(target=mic_stream)
        mic_thread.start()
        mic_thread.join()
        wav_file.close()
        return final_text

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None

    finally:
        try:
            dg_connection.finish()
        except:
            pass
        


if __name__ == "__main__":
    text = main()
    print("🎤 Final Answer:", text)
