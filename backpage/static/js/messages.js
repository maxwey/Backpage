

function addMessage(title, message, type='INFO') {
    const messages_container = document.getElementById('notification-messages');
    const message_template = document.getElementById('notification-message-template');

    const cloned_message = message_template.cloneNode(true);
    // Keep IDs unique
    cloned_message.id = `notification-message-${Date.now()}`;

    // Set the Header and Content text
    cloned_message.getElementsByClassName('notification-message-header')[0].innerText = title;
    cloned_message.getElementsByClassName('notification-message-content')[0].innerText = message;

    // Set Display type of message
    switch(type.toUpperCase()) {
        case 'SUCCESS':
            cloned_message.classList.add('notification-message-success');
            break;
        case 'FAILURE':
            cloned_message.classList.add('notification-message-failure');
            break;
        case 'INFO':
        default:
            cloned_message.classList.add('notification-message-info');
    }

    cloned_message.classList.remove('notification-message-template');

    // Set the timeout for the message to expire after 15 sec
    setTimeout(() => {
        cloned_message.remove();
    }, 10000);

    messages_container.appendChild(cloned_message);
}