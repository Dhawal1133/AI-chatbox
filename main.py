from modules.hotword import listen_for_hotword
from modules.speech_recognition import recognize_speech
from modules.utilities import process_command
from modules.text_to_speech import speak
import time
import signal
import sys

def main():
    speak("Assistant is now active. Say 'HI' to wake me up!")

    listening = False  # State to track if we're in listening mode
    
    while True:
        if not listening and listen_for_hotword():  # Listen for hotword only when not already listening
            listening = True  # Set the listening state to True after hotword is detected
            speak("I'm listening!")
            time.sleep(1)  # Add a small delay to avoid multiple activations

            command = recognize_speech()
            
            if not command:  # Skip if no valid command is detected
                speak("I didn't catch that. Could you repeat?")
                listening = False  # Reset listening state to allow another hotword detection
                continue

            command = command.lower()

            # Process the command and ensure it doesn’t trigger again
            if not process_command(command):  # Exit if command is "exit" or "quit"
                break

            listening = False  # Reset the listening state after processing the command



if __name__ == "__main__":
    main()
