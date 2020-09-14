/*
 * This file contains the logic that controls the login logic
 */

function login() {
    startLoginLoading();

    // Get the data from the forms
    const display_name_field = document.forms['loginForm']['display-name-field'].value.trim()
    const user_name_field = document.forms['loginForm']['user-name-field'].value.trim()

    const data = {
        'display_name': display_name_field,
        'user_name': user_name_field
    }

    // Validate the data before completing the request
    if (!validateLoginData(data)) {
        endLoginLoading();
        return false;
    }

    // Send the auth request
    send('/auth', JSON.stringify(data))
        .then(response => {
            // get the page that will be loaded next if the page authenticates successfully
            const qs = window.location.search;
            const urlParams = new URLSearchParams(qs);
            let nextPage = urlParams.get('next');
            // If the query parameter was not defined, go to home page
            if (nextPage === null) {
                nextPage = '/';
            }

            // Login successful, redirect to the following page
            window.location.replace(nextPage);
        })
        .catch(response => {
            const obj = JSON.parse(response.responseText)
            setLoginMessage(obj['error']);
            endLoginLoading();
        });

    return false;
}

/*
 * Validates the login data. 'True' if the data is valid, else return false.
 */
function validateLoginData(data) {
    // Validate data
    if (data['display_name'].length <= 5) {
        setLoginMessage('Display name must be at least 5 characters');
        return false;
    }
    if (data['user_name'].length <= 5) {
        setLoginMessage('Username must be at least 5 characters');
        return false;
    }

    return true;
}

/*
 * Changes the UI to show the loading UI
 */
function startLoginLoading() {
    document.getElementById('login-form-login-button').style.display = 'none';
    document.getElementById('login-form-login-spinner').style.display = 'block';
    for (elem of document.getElementsByClassName('login-form-text-box')) {
        elem.disabled = true;
    }
}

/*
 * Changes the UI to hide the loading UI
 */
function endLoginLoading() {
    document.getElementById('login-form-login-button').style.display = 'block';
    document.getElementById('login-form-login-spinner').style.display = 'none';
    for (elem of document.getElementsByClassName('login-form-text-box')) {
        elem.disabled = false;
    }
}

/*
 * Shows the status message for the login attempt. Usually to show useful
 * information to the user such as reasons why the login attempt failed
 */
function setLoginMessage(message) {
    const login_message = document.getElementById('login-message-display');
    login_message.style.display = 'block';
    login_message.innerText = message;
}
