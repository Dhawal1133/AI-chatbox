import pyttsx3

def speak(text):
    """
    Converts text to speech using pyttsx3.
    :param text: The text to be spoken.
    """
    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()

        # Set properties
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.6)  # Volume (0.0 to 1.0)

        # Set voice (0 for male, 1 for female)
        voices = engine.getProperty('voices')
        if len(voices) > 1:  # Ensure there are multiple voice options
            engine.setProperty('voice', voices[1].id)  # Switch to female voice
        else:
            engine.setProperty('voice', voices[0].id)  # Default to first voice

        # Speak the text
        print("Assistant:", text)  # Log text to console for debugging
        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        # Handle any errors during initialization or speech synthesis
        print(f"Error in text-to-speech: {e}")
        print("Falling back to console output:")
        print("Assistant:", text)

# Test the function
if __name__ == "__main__":
    speak("Hello! This is a test of the improved text-to-speech functionality.")
