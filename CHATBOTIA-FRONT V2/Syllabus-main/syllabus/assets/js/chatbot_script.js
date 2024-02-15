function sendMessage() {
    const userInput = document.getElementById('userInput');
    const chatBox = document.getElementById('chatBox');

    const userMessage = userInput.value;
    appendMessage('user', userMessage);

    // Appel à l'API du chatbot
    // Ici, nous supposons une réponse simple du chatbot
    const botMessage = simulateChatbotResponse(userMessage);
    appendMessage('bot', botMessage);

    userInput.value = '';
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById('chatBox');
    const messageElement = document.createElement('div');
    messageElement.classList.add(sender);
    messageElement.innerHTML = message;
    chatBox.appendChild(messageElement);
}

function simulateChatbotResponse(userMessage) {
    // Simulation simple de la réponse du chatbot
    return "Réponse de Syllabus : " + userMessage, "Je suis incapable de répondre à cette question.";
}
