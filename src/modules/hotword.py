import vosk
import pyaudio
import json
import logging
import sys
import time
import signal

logging.basicConfig(level=logging.INFO)

def signal_handler(sig, frame):
        print("KeyboardInterrupt detected. Exiting gracefully...")
        sys.exit(0)
        
     # Register the keyboard interrupt handler
        signal.signal(signal.SIGINT, signal_handler)

def listen_for_hotword():
    model_path = r"C:/Users/Dell/voice-assistant/vosk-model-small-en-us-0.15"
    try:
        model = vosk.Model(model_path)
    except Exception as e:
        logging.error(f"Failed to load Vosk model: {e}")
        return False

    recognizer = vosk.KaldiRecognizer(model, 16000)
    pa = pyaudio.PyAudio()

    # Start listening to the microphone
    sample_rate = 16000
    try:
        audio_stream = pa.open(
            rate=sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=4000
        )
    except Exception as e:
        logging.error(f"Error initializing audio stream: {e}")
        pa.terminate()
        return False

    logging.info("Listening for hotword...")

    timeout = 30  # Stop listening after 30 seconds
    start_time = time.time()
    
    try:
        while time.time() - start_time < timeout:
            try:
                data = audio_stream.read(4000, exception_on_overflow=False)
            except OSError as e:
                logging.warning(f"Audio stream error: {e}")
                continue

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip().lower()
                logging.info(f"Recognized: {text}")
                if "hi" in text:
                    logging.info("Hotword detected!")
                    audio_stream.stop_stream()  # Stop listening after hotword is detected
                    return True
    except KeyboardInterrupt:
        logging.info("Stopping hotword detection.")
    finally:
        if audio_stream.is_active():
            audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        logging.info("Audio resources released.")

    logging.info("Listening timed out.")
    return False


