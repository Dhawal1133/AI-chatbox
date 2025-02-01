from flask import Flask, jsonify, request,Response
from modules.hotword import listen_for_hotword
from modules.speech_recognition import recognize_speech
from modules.utilities import process_command
from modules.text_to_speech import speak
import time
import threading
import os

# Initialize Flask app

app = Flask(__name__)

@app.route('/')
def index():
    # Open the HTML file and read its content
    html_file_path = os.path.join('src', 'templates', 'index.html')
    with open(html_file_path, 'r') as file:
        html_content = file.read()
    
    # Return the HTML content as a response
    return Response(html_content, mimetype='text/html')

listening = False


# Helper function to speak messages
def speak_message(message):
    speak(message)


# Endpoint to trigger hotword detection and speech recognition
@app.route('/start-listening', methods=['GET'])
def start_listening():
    global listening

    # If already listening, do not trigger again
    if listening:
        return jsonify({"status": "error", "message": "Already listening!"})

    # Start listening in a separate thread to avoid blocking the main thread
    listening = True
    speak_message("Assistant is now active. Say 'HI' to wake me up!")

    # Call function to listen for hotword
    listen_for_hotword()

    # After hotword detection, start speech recognition
    command = recognize_speech()

    if not command:
        speak_message("I didn't catch that. Could you repeat?")
        listening = False
        return jsonify({"status": "error", "message": "No command recognized."})

    # Process command
    command = command.lower()

    # If the command is recognized, process it
    if process_command(command):
        speak_message("Processing command.")
        listening = False
        return jsonify({"status": "success", "message": "Command processed."})

    speak_message("Goodbye!")
    listening = False
    return jsonify({"status": "success", "message": "Exiting."})


# Route to check if the assistant is currently listening
@app.route('/status', methods=['GET'])
def status():
    if listening:
        return jsonify({"status": "listening", "message": "Assistant is listening."})
    else:
        return jsonify({"status": "idle", "message": "Assistant is idle."})


# Error handling route for undefined commands
@app.route('/error', methods=['GET'])
def error():
    return jsonify({"status": "error", "message": "Invalid request."})


# Main entry to start the Flask app
if __name__ == '__main__':
    # Run Flask app
    app.run(debug=True, use_reloader=False)
