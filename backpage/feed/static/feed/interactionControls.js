/*
 * This file contains the logic that controls the interaction buttons such as the like/comment buttons
 */


function like(postId) {
    const data = {
        'action': 'LIKE',
        'user_id': '000',
        'sec_token': '000'
    };
    const endpoint = `post/${postId}/a`;

    // Send the API request
    send(endpoint, JSON.stringify(data))
        .then(response => {
            addMessage('', response.responseText, 'SUCCESS');
        })
        .catch(response => {
            addMessage('', response.responseText, 'FAILURE');
        });
}

function comment(postId, comment) {
    const trimmed_text = comment.trim()
    if (trimmed_text.length == 0) {
        return; // Abort immediately; comment text is empty
    }

    const data = {
        'action': 'COMMENT',
        'content': trimmed_text,
        'user_id': '000',
        'sec_token': '000'
    };
    const endpoint = `post/${postId}/a`;

    // Send the API request
    send(endpoint, JSON.stringify(data))
        .then(response => {
            addMessage('', response.responseText, 'SUCCESS');
        })
        .catch(response => {
            addMessage('', response.responseText, 'FAILURE');
        });
}

function share(postId) {
    const data = {
        'action': 'SHARE',
        'user_id': '000',
        'sec_token': '000'
    };
    const endpoint = `post/${postId}/a`;

    // Send the API request
    send(endpoint, JSON.stringify(data))
        .then(response => {
            addMessage('', response.responseText, 'SUCCESS');
        })
        .catch(response => {
            addMessage('', response.responseText, 'FAILURE');
        });
}