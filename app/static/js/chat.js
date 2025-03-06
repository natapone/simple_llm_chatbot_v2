document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    // Generate a random user ID and session ID for this chat session
    const userId = 'user_' + Math.random().toString(36).substring(2, 10);
    const sessionId = 'session_' + Math.random().toString(36).substring(2, 10);
    
    // Chat history for context
    let chatHistory = [];
    
    // Function to add a message to the chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user' : 'bot');
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        const messageParagraph = document.createElement('p');
        messageParagraph.textContent = message;
        
        messageContent.appendChild(messageParagraph);
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Add to chat history
        chatHistory.push({
            role: isUser ? 'user' : 'assistant',
            content: message
        });
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('typing-indicator');
        typingDiv.id = 'typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            typingDiv.appendChild(dot);
        }
        
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Function to send a message to the API
    async function sendMessage(message) {
        try {
            showTypingIndicator();
            
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: userId,
                    session_id: sessionId,
                    message: message
                })
            });
            
            if (!response.ok) {
                throw new Error('API request failed');
            }
            
            const data = await response.json();
            removeTypingIndicator();
            
            // Add the bot's response to the chat
            addMessage(data.response, false);
            
        } catch (error) {
            console.error('Error sending message:', error);
            removeTypingIndicator();
            addMessage('Sorry, I encountered an error. Please try again later.', false);
        }
    }
    
    // Function to handle sending a message
    function handleSendMessage() {
        const message = userInput.value.trim();
        
        if (message) {
            // Add the user's message to the chat
            addMessage(message, true);
            
            // Clear the input field
            userInput.value = '';
            
            // Send the message to the API
            sendMessage(message);
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', handleSendMessage);
    
    userInput.addEventListener('keydown', (event) => {
        // Send message on Enter key (without Shift)
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSendMessage();
        }
        
        // Allow new line on Shift+Enter
        if (event.key === 'Enter' && event.shiftKey) {
            // Default behavior (new line) will happen
        }
    });
    
    // Auto-resize the textarea as the user types
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = (userInput.scrollHeight) + 'px';
    });
    
    // Focus the input field when the page loads
    userInput.focus();
}); 