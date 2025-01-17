const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const fileInput = document.getElementById("file-input");
const uploadBtn = document.getElementById("upload-btn");

// Event listener for the Send button (text input)
sendBtn.addEventListener("click", () => {
  const message = userInput.value.trim();
  if (message) {
    appendMessage("user", message);
    sendMessageToBackend(message);
    userInput.value = "";
  } else {
    alert("Please enter a message.");
  }
});

// Event listener for Enter key
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    sendBtn.click();
  }
});

// Event listener for file upload button
uploadBtn.addEventListener("click", () => {
  fileInput.click();
});

// Event listener for file input change (upload)
fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    appendMessage("user", `Uploaded file: ${file.name}`);
    sendFileToBackend(file);
  }
});

// Function to append a message (from user or bot) to the chat
function appendMessage(sender, message) {
  const messageDiv = document.createElement("div");
  messageDiv.className = sender === "user" ? "user-message" : "bot-message";
  messageDiv.textContent = message;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to send text message to backend
function sendMessageToBackend(message) {
  fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
    .then(response => response.json())
    .then(data => {
      if (data.response) {
        appendMessage("bot", data.response);
      } else if (data.error) {
        appendMessage("bot", "An error occurred.");
      }
    })
    .catch(error => {
      console.error("Error:", error);
      appendMessage("bot", "Failed to connect to the server.");
    });
}

// Function to send file to backend
function sendFileToBackend(file) {
  const formData = new FormData();
  formData.append("file", file);

  fetch("http://127.0.0.1:5000/upload", {
    method: "POST",
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.response) {
        appendMessage("bot", `File analyzed: ${data.response}`);
      } else if (data.error) {
        appendMessage("bot", "Failed to analyze the file.");
      }
    })
    .catch(error => {
      console.error("Error:", error);
      appendMessage("bot", "Failed to connect to the server for file upload.");
    });
}
