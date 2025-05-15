document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');


    // form submit post call : user query submit
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        if (message === '') return;
    
        appendMessage('user', message);
        userInput.value = '';
    
        document.getElementById('loaderModal').style.display = 'flex';
        
        // post request to /chat
        fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {

            document.getElementById('loaderModal').style.display = 'none';

            if (data.agent) {
                appendMessage('agent-label', `${data.agent}'s reply:`);
            }
            if (data.response) {
                appendMessage('assistant', data.response);
            } else if (data.error) {
                appendMessage('assistant', data.error);
            }
        })
        .catch(error => {
            document.getElementById('loaderModal').style.display = 'none';
            appendMessage('assistant', 'An error occurred. Please try again.');
        });
    });
    

    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.innerText = message;
        messageDiv.innerHTML = marked.parse(message);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

