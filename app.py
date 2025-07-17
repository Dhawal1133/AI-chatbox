from flask import Flask, jsonify, request,Response
from modules.hotword import listen_for_hotword
from modules.speech_recognition import recognize_speech
from modules.utilities import process_command
from modules.text_to_speech import speak
import time
import threading
import os

# Initializimg Flask app

app = Flask(__name__)

@app.route('/')
def index():
    
    html_file_path = os.path.join('src', 'templates', 'index.html')
    with open(html_file_path, 'r') as file:
        html_content = file.read()
    
    
    return Response(html_content, mimetype='text/html')

listening = False


# Helper function to speak messages
def speak_message(message):
    speak(message)



@app.route('/start-listening', methods=['GET'])
def start_listening():
    global listening

    
    if listening:
        return jsonify({"status": "error", "message": "Already listening!"})

   
    listening = True
    speak_message("Assistant is now active. Say 'HI' to wake me up!")

    # Call function
    listen_for_hotword()

    # After hotword detection, start speech recognition
    command = recognize_speech()

    if not command:
        speak_message("I didn't catch that. Could you repeat?")
        listening = False
        return jsonify({"status": "error", "message": "No command recognized."})

    
    command = command.lower()

    
    if process_command(command):
        speak_message("Processing command.")
        listening = False
        return jsonify({"status": "success", "message": "Command processed."})

    speak_message("Goodbye!")
    listening = False
    return jsonify({"status": "success", "message": "Exiting."})



@app.route('/status', methods=['GET'])
def status():
    if listening:
        return jsonify({"status": "listening", "message": "Assistant is listening."})
    else:
        return jsonify({"status": "idle", "message": "Assistant is idle."})


# Error handling 
@app.route('/error', methods=['GET'])
def error():
    return jsonify({"status": "error", "message": "Invalid request."})


# Main entry to start the Flask app
if __name__ == '__main__':
    # Run Flask app
    app.run(debug=True, use_reloader=False)
