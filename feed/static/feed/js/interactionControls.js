/*
 * This file contains the logic that controls the interaction buttons such as the like/comment buttons
 */


function like(postId) {
    const data = {
        'action': 'like',
        'user_id': '000'
    };
    const endpoint = `/post/${postId}/a`;

    // Send the API request
    send(endpoint, JSON.stringify(data))
        .then(response => {
            const json_response = JSON.parse(response.responseText);
            addMessage('', json_response.message, 'SUCCESS');
        })
        .catch(response => {
            addMessage('Oops!', 'A problem happened: ' + response.responseText, 'FAILURE');
        });
}

function comment(postId, comment) {
    const trimmed_text = comment.trim()
    if (trimmed_text.length == 0) {
        return; // Abort immediately; comment text is empty
    }

    const data = {
        'action': 'comment',
        'content': trimmed_text
    };
    const endpoint = `/post/${postId}/a`;

    // Send the API request
    send(endpoint, JSON.stringify(data))
        .then(response => {
            const comment_container = document.getElementById(`feed-post-comment-${postId}`);
            const comment_template = document.getElementById('feed-post-comment-template');
            const new_comment = comment_template.cloneNode(true);

            new_comment.classList.remove('feed-post-comment-placeholder');
            new_comment.removeAttribute('id');

            const comment_post_date = new_comment.querySelector('.feed-post-comment-userbadge-date');
            const comment_post_content = new_comment.querySelector('.feed-post-comment-content');
            insertDatetime(comment_post_date, moment.utc());
            comment_post_content.innerText = trimmed_text;

            // Insert to before last entry
            comment_container.insertBefore(new_comment, comment_container.lastElementChild);
            document.getElementById(`comment-input-${postId}`).value = '';

            const json_response = JSON.parse(response.responseText);
            addMessage('', json_response.message, 'SUCCESS');
        })
        .catch(response => {
            addMessage('Oops!', 'A problem happened: ' + response.responseText, 'FAILURE');
        });
}

function share(postId) {
    const data = {
        'action': 'share',
        'user_id': '000'
    };
    const endpoint = `/post/${postId}/a`;

    // Send the API request
    send(endpoint, JSON.stringify(data))
        .then(response => {
            const json_response = JSON.parse(response.responseText);
            addMessage('', json_response.message, 'SUCCESS');
        })
        .catch(response => {
            addMessage('Oops!', 'A problem happened: ' + response.responseText, 'FAILURE');
        });
}
