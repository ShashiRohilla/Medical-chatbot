/*document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const microphoneIcon = document.createElement('div');

    // Function to add a message to the chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        
        // Auto scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'typing-indicator');
        typingDiv.textContent = 'Typing...';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return typingDiv;
    }

    // Function to remove typing indicator
    function removeTypingIndicator(typingIndicator) {
        if (typingIndicator) {
            chatMessages.removeChild(typingIndicator);
        }
    }

    // Send message function
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage(message, 'user');
        messageInput.value = '';

        // Show typing indicator
        const typingIndicator = showTypingIndicator();

        try {
            // Make API call to backend
            const response = await fetch('http://localhost:5000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            // Remove typing indicator
            removeTypingIndicator(typingIndicator);

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Add bot response
            addMessage(data.message, 'bot');
        } catch (error) {
            // Remove typing indicator
            removeTypingIndicator(typingIndicator);

            // Add error message
            addMessage('Sorry, something went wrong. Please try again.', 'bot');
            console.error('Error:', error);
        }
    }

    // Voice recording functionality
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    // Start audio recording
    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", processAudioRecording);
            mediaRecorder.start();

            // Add recording message
            addMessage('Recording audio...', 'user');
            isRecording = true;
            microphoneIcon.querySelector('svg').style.fill = 'red';
        } catch (error) {
            console.error('Error accessing microphone:', error);
            addMessage('Could not access microphone. Please check permissions.', 'bot');
        }
    }

    function processAudioRecording() {
        const audioBlob = new Blob(audioChunks, { 
            type: 'audio/webm'  // Explicitly set MIME type
        });
        const reader = new FileReader();
        
        reader.onloadend = function() {
            const base64Audio = reader.result.split(',')[1];
            isRecording = false;
            microphoneIcon.querySelector('svg').style.fill = '';
            sendAudioMessage(base64Audio);
        };
    
        reader.readAsDataURL(audioBlob);
    }

    // Send audio message to backend
    async function sendAudioMessage(base64Audio) {
        // Show typing indicator
        const typingIndicator = showTypingIndicator();

        try {
            const response = await fetch('http://localhost:5000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    audio: base64Audio 
                })
            });

            // Remove typing indicator
            removeTypingIndicator(typingIndicator);

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Add bot response
            addMessage(data.message, 'bot');
        } catch (error) {
            // Remove typing indicator
            removeTypingIndicator(typingIndicator);

            // Add error message
            addMessage('Sorry, something went wrong with audio processing.', 'bot');
            console.error('Error:', error);
        }
    }

    // Stop audio recording
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Microphone icon for voice recording
    microphoneIcon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
            <line x1="12" y1="19" x2="12" y2="22" />
        </svg>
    `;
    microphoneIcon.style.cursor = 'pointer';
    microphoneIcon.style.margin = '0 10px';

    // Insert voice recording icon 
    sendButton.parentNode.insertBefore(microphoneIcon, sendButton.nextSibling);

    // Voice recording toggle
    microphoneIcon.addEventListener('click', () => {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    });
});*/



/*
document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const microphoneIcon = document.createElement('div');

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'typing-indicator');
        typingDiv.textContent = 'Typing...';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return typingDiv;
    }

    function removeTypingIndicator(typingIndicator) {
        if (typingIndicator) {
            chatMessages.removeChild(typingIndicator);
        }
    }

    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        messageInput.value = '';
        const typingIndicator = showTypingIndicator();


            try {
    console.log("📤 Sending to backend:", message);

    const response = await fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    });


            removeTypingIndicator(typingIndicator);

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.message || 'Server error');
            }

            const data = await response.json();
            console.log("✅ Backend responded with:", data);

            addMessage(data.message || "⚠️ No response from Gemini.", 'bot');

        } catch (error) {
            removeTypingIndicator(typingIndicator);
            console.error("❌ Error from backend:", error);
            addMessage('❌ Error: ' + error.message, 'bot');
        }
    }

    // Voice recording functionality
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", processAudioRecording);
            mediaRecorder.start();

            addMessage('🎙️ Recording...', 'user');
            isRecording = true;
            microphoneIcon.querySelector('svg').style.fill = 'red';
        } catch (error) {
            console.error('Microphone access error:', error);
            addMessage('Could not access microphone. Please check permissions.', 'bot');
        }
    }

    function processAudioRecording() {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const reader = new FileReader();

        reader.onloadend = function () {
            const base64Audio = reader.result.split(',')[1];
            isRecording = false;
            microphoneIcon.querySelector('svg').style.fill = '';
            sendAudioMessage(base64Audio);
        };

        reader.readAsDataURL(audioBlob);
    }

    async function sendAudioMessage(base64Audio) {
        const typingIndicator = showTypingIndicator();

        try {
            console.log("📤 Sending audio to backend");
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ audio: base64Audio })
            });

            removeTypingIndicator(typingIndicator);

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.message || 'Audio processing error');
            }

            const data = await response.json();
            console.log("✅ Audio response:", data);

            addMessage(data.message || "⚠️ No response from Gemini.", 'bot');

        } catch (error) {
            removeTypingIndicator(typingIndicator);
            console.error("❌ Error from audio backend:", error);
            addMessage('🎧 Error processing audio: ' + error.message, 'bot');
        }
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }
    }

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    microphoneIcon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
            <line x1="12" y1="19" x2="12" y2="22" />
        </svg>
    `;
    microphoneIcon.style.cursor = 'pointer';
    microphoneIcon.style.margin = '0 10px';

    sendButton.parentNode.insertBefore(microphoneIcon, sendButton.nextSibling);

    microphoneIcon.addEventListener('click', () => {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    });
});
*/





/*
document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const microphoneIcon = document.createElement('div');
    const connectionStatus = document.getElementById('connectionStatus');
    
    // Check if the backend is available
    async function checkServerStatus() {
        try {
            const response = await fetch('http://127.0.0.1:5000/', { 
                method: 'GET',
                timeout: 3000
            });
            if (response.ok) {
                connectionStatus.textContent = '🟢 Connected';
                connectionStatus.style.color = 'green';
            } else {
                connectionStatus.textContent = '🔴 Server Error';
                connectionStatus.style.color = 'red';
            }
        } catch (error) {
            connectionStatus.textContent = '🔴 Disconnected';
            connectionStatus.style.color = 'red';
            console.error('Backend server not available:', error);
        }
    }
    
    // Check status on load
    checkServerStatus();

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'typing-indicator');
        typingDiv.textContent = 'Typing...';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return typingDiv;
    }

    function removeTypingIndicator(typingIndicator) {
        if (typingIndicator) {
            chatMessages.removeChild(typingIndicator);
        }
    }

    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        messageInput.value = '';
        const typingIndicator = showTypingIndicator();

        try {
            console.log("📤 Sending to backend:", message);

            // Make sure URL is correct - using 127.0.0.1 (localhost)
            const response = await fetch('http://127.0.0.1:5000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            removeTypingIndicator(typingIndicator);

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.message || 'Server error');
            }

            const data = await response.json();
            console.log("✅ Backend responded with:", data);

            addMessage(data.message || "⚠️ No response from AI.", 'bot');

        } catch (error) {
            removeTypingIndicator(typingIndicator);
            console.error("❌ Error from backend:", error);
            addMessage('❌ Error: ' + error.message, 'bot');
        }
    }

    // Voice recording functionality
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", processAudioRecording);
            mediaRecorder.start();

            addMessage('🎙️ Recording...', 'user');
            isRecording = true;
            microphoneIcon.querySelector('svg').style.fill = 'red';
        } catch (error) {
            console.error('Microphone access error:', error);
            addMessage('Could not access microphone. Please check permissions.', 'bot');
        }
    }

    function processAudioRecording() {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const reader = new FileReader();

        reader.onloadend = function () {
            const base64Audio = reader.result.split(',')[1];
            isRecording = false;
            microphoneIcon.querySelector('svg').style.fill = '';
            sendAudioMessage(base64Audio);
        };

        reader.readAsDataURL(audioBlob);
    }

    async function sendAudioMessage(base64Audio) {
        const typingIndicator = showTypingIndicator();

        try {
            console.log("📤 Sending audio to backend");
            // Make sure URL is correct - using 127.0.0.1 (localhost)
            const response = await fetch('http://127.0.0.1:5000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ audio: base64Audio })
            });

            removeTypingIndicator(typingIndicator);

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.message || 'Audio processing error');
            }

            const data = await response.json();
            console.log("✅ Audio response:", data);

            addMessage(data.message || "⚠️ No response from AI.", 'bot');

        } catch (error) {
            removeTypingIndicator(typingIndicator);
            console.error("❌ Error from audio backend:", error);
            addMessage('🎧 Error processing audio: ' + error.message, 'bot');
        }
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }
    }

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    microphoneIcon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
            <line x1="12" y1="19" x2="12" y2="22" />
        </svg>
    `;
    microphoneIcon.style.cursor = 'pointer';
    microphoneIcon.style.margin = '0 10px';

    sendButton.parentNode.insertBefore(microphoneIcon, sendButton.nextSibling);

    microphoneIcon.addEventListener('click', () => {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    });
});
*/





/*
document.getElementById("sendButton").addEventListener("click", sendMessage);

async function sendMessage() {
  const input = document.getElementById("messageInput");
  const message = input.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  input.value = "";

  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  const data = await response.json();
  appendMessage(data.message, "bot");
}

function appendMessage(message, sender) {
  const msgBox = document.getElementById("chatMessages");
  const msg = document.createElement("div");
  msg.className = `message ${sender}-message`;
  msg.innerText = message;
  msgBox.appendChild(msg);
  msgBox.scrollTop = msgBox.scrollHeight;
}*/






/*
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const micButton = document.getElementById("micButton");
const chatBox = document.getElementById("chatMessages");

sendButton.addEventListener("click", () => sendMessage());
micButton.addEventListener("click", () => startVoice());

function appendMessage(message, sender) {
  const msg = document.createElement("div");
  msg.className = `message ${sender}-message`;
  msg.innerText = message;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(audioBlob = null) {
  const message = messageInput.value.trim();
  const body = {};

  if (audioBlob) {
    const base64 = await blobToBase64(audioBlob);
    body.audio = base64;
  } else if (message) {
    body.message = message;
  } else {
    return;
  }

  appendMessage(message || "🎙️ Voice sent", "user");
  messageInput.value = "";

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    appendMessage(data.message, "bot");
  } catch (error) {
    appendMessage("⚠️ Error connecting to server.", "bot");
    console.error("Fetch error:", error);
  }
}

function blobToBase64(blob) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result.split(',')[1]);
    reader.readAsDataURL(blob);
  });
}

function startVoice() {
  navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
    const mediaRecorder = new MediaRecorder(stream);
    const chunks = [];

    mediaRecorder.start();
    appendMessage("🎤 Listening...", "bot");

    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

    mediaRecorder.onstop = () => {
      const blob = new Blob(chunks, { type: "audio/webm" });
      sendMessage(blob);
    };

    setTimeout(() => {
      mediaRecorder.stop();
    }, 4000); // Stop recording after 4 seconds
  });
}
*/

const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const micButton = document.getElementById("micButton");
const chatBox = document.getElementById("chatMessages");
const pingAudio = new Audio("/static/sounds/ping.mp3");


let mediaRecorder;
let audioChunks = [];
let isRecording = false;

sendButton.addEventListener("click", () => sendMessage());

micButton.addEventListener("click", async () => {
  if (!isRecording) {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: "audio/webm" });
      sendMessage(blob);
    };

    mediaRecorder.start();
    isRecording = true;
    micButton.textContent = "⏹️"; // Change icon to stop
    appendMessage("🎤 Listening... Click mic again to stop.", "bot");
  } else {
    mediaRecorder.stop();
    isRecording = false;
    micButton.textContent = "🎙️"; // Reset icon
  }
});

function appendMessage(message, sender) {
  const msg = document.createElement("div");
  msg.className = `message ${sender}-message`;
  msg.innerText = message;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(audioBlob = null) {
  const message = messageInput.value.trim();
  const body = {};

  if (audioBlob) {
    const base64 = await blobToBase64(audioBlob);
    body.audio = base64;
    appendMessage("🎙️ Voice message sent", "user");
  } else if (message) {
    body.message = message;
    appendMessage(message, "user");
  } else {
    return;
  }

  messageInput.value = "";

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  appendMessage(data.message, "bot");
}

function blobToBase64(blob) {
  return new Promise(resolve => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result.split(",")[1]);
    reader.readAsDataURL(blob);
  });
}
messageInput.addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    event.preventDefault(); // prevent form submission if inside a form
    sendMessage(); // call your sendMessage function
  }
});




