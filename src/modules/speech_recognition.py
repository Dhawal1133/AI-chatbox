import vosk
import pyaudio
import json
import os
import time

def recognize_speech():
    # Path to your Vosk model (replace with actual path)
    model_path = r"C:/Users/Dell/voice-assistant/vosk-model-small-en-us-0.15"
    
    # Check if model path exists
    if not os.path.exists(model_path):
        print(f"Error: Model path {model_path} does not exist.")
        return None  # Return None if the model is missing

    try:
        model = vosk.Model(model_path)
        recognizer = vosk.KaldiRecognizer(model, 16000)

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=16000,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=4000
        )
        
        print("Listening for command...")

        start_time = time.time()
        timeout = 10  # Set timeout for command recognition (10 seconds)

        while True:
            data = audio_stream.read(4000)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                command = result.get("text", "").strip()
                
                if command:
                    print(f"Recognized Command: {command}")
                    return command.lower()  # Return recognized command in lowercase

            # Timeout after a certain period of no speech (e.g., 10 seconds)
            if time.time() - start_time > timeout:
                print("No command recognized within timeout. Restarting...")
                return None

    except KeyboardInterrupt:
        print("Speech recognition stopped.")
    except Exception as e:
        print(f"Error during speech recognition: {e}")
    finally:
        # Ensure proper resource cleanup
        audio_stream.close()
        pa.terminate()

    return None  # Return None if no command is recognized
