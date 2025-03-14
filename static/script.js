document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const typingIndicator = document.getElementById("typing-indicator");

    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add(sender === "bot" ? "bot-message" : "user-message");
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage("user", message);
        userInput.value = "";

        // Show typing indicator
        typingIndicator.style.display = "flex";

        fetch("/get", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            typingIndicator.style.display = "none";
            appendMessage("bot", data.response);
        })
        .catch(() => {
            typingIndicator.style.display = "none";
            appendMessage("bot", "Sorry, I couldn't process that. Try again.");
        });
    }

    // Handle Enter key
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});
