/*
 * This file contains the logic that controls the login logic
 */

function login() {
    const submit_button = document.getElementById('login-form-login-button');
    const submit_spinner = document.getElementById('login-form-login-spinner');
    submit_button.style.display = 'none';
    submit_spinner.style.display = 'block';

    // Get the data from the forms
    const display_name_field = document.forms['loginForm']['display-name-field'].value.trim()
    const user_name_field = document.forms['loginForm']['user-name-field'].value.trim()

    // Validate data
    if (display_name_field.length <= 5) {
        setLoginMessage('Display name must be at least 5 characters');
        submit_button.style.display = 'block';
        submit_spinner.style.display = 'none';
        return false;
    }
    if (user_name_field.length <= 5) {
        setLoginMessage('Username must be at least 5 characters');
        submit_button.style.display = 'block';
        submit_spinner.style.display = 'none';
        return false;
    }

    const data = {
        'display_name': display_name_field,
        'user_name': user_name_field
    }

    // Send the auth request
    send('/auth', JSON.stringify(data))
        .then(response => {
            // get the page that will be loaded next if the page authenticates successfully
            const qs = window.location.search;
            const urlParams = new URLSearchParams(qs);
            const nextPage = urlParams.get('next');

            window.location.replace(nextPage);

            submit_button.style.display = 'block';
            submit_spinner.style.display = 'none';
        })
        .catch(response => {
            const obj = JSON.parse(response.responseText)
            setLoginMessage(obj['error']);

            submit_button.style.display = 'block';
            submit_spinner.style.display = 'none';
        });

    return false;
}


function setLoginMessage(message) {
    const login_message = document.getElementById('login-message-display');
    login_message.style.display = 'block';
    login_message.innerText = message;
}
