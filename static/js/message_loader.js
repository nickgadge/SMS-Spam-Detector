document.getElementById('loadMsgs').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/messages', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) throw new Error('Failed to load messages');

        const messages = await response.json();
        displayMessages(messages);

    } catch (error) {
        alert(error.message);
        console.error('Error:', error);
    }
});

function displayMessages(messages) {
    const container = document.getElementById('messageContainer');
    container.innerHTML = '';

    messages.forEach(msg => {
        const msgElement = document.createElement('div');
        msgElement.className = `message-card ${msg.is_spam ? 'spam' : 'ham'}`;

        msgElement.innerHTML = `
            <div class="message-content">${msg.content}</div>
            <div class="message-meta">
                <span class="badge ${msg.is_spam ? 'bg-danger' : 'bg-success'}">
                    ${msg.is_spam ? 'SPAM' : 'HAM'} (${msg.confidence}%)
                </span>
                <small class="text-muted">${new Date(msg.timestamp).toLocaleString()}</small>
            </div>
        `;

        container.appendChild(msgElement);
    });
}