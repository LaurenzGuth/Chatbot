const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

sendButton.addEventListener("click", () => {
    const message = userInput.value;
    if (message.trim()) {
        addMessage("user", message);
        userInput.value = "";

        fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sender: "user123",  // Sender ID
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                data.forEach(msg => addMessage("bot", msg.text));
            } else {
                addMessage("bot", "Das habe ich nicht verstanden. Kannst du das anders formulieren?");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            addMessage("bot", "Error communicating with the server.");
        });
    }
});

userInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        sendButton.click();
    }
});

function addMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.className = sender;

    const messageBox = document.createElement("div");
    messageBox.className = "message-box";
    messageBox.textContent = text;

    messageDiv.appendChild(messageBox);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}