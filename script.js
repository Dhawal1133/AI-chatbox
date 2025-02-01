function startVoice() {
    document.getElementById('result').innerText = "Voice Assistant Activated!";
    
    // Initialize Speech Recognition API
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US'; // Set language for recognition
    recognition.continuous = false; // Detect a single phrase (not continuous)

    // Start listening to the user's voice
    recognition.start();

    // When speech is detected
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript; // Get the recognized text
        document.getElementById('result').innerText = "You said: " + transcript;

        // You can now add further actions based on the speech input
        if (transcript.toLowerCase().includes("hello")) {
            document.getElementById('result').innerText += "\nHello there! How can I assist you?";
        }
        // Add more commands as needed
    };

    // If there's an error in recognizing speech
    recognition.onerror = function(event) {
        document.getElementById('result').innerText = "Error: " + event.error;
    };

    // When the recognition ends (successfully or with error)
    recognition.onend = function() {
        console.log("Speech recognition ended.");
    };
}
