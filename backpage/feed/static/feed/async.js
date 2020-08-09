/*
 * This file contains the logic required to submit and retrieve information asynchronously, allowing seamless user
 * interaction without requiring the page to reload entirely.
 */

/*
 * Send the payload to the endpoint. This is always a POST.
 * The payload encoding must be specified if not in JSON format.
 * This function returns a Promise, not the result. The promise must therefore be settled and handled
 */
async function send(endpoint, payload, payloadEncoding = 'application/JSON') {
    return new Promise((resolve, reject) => {
        let xhttp = new XMLHttpRequest();
        // Define the function to handle the server response
        xhttp.onreadystatechange = () => handleReadyStateChange(xhttp, resolve, reject);
        // open and send the request
        xhttp.open('POST', endpoint, true);
        xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhttp.setRequestHeader('Content-Type', payloadEncoding);
        xhttp.send(payload);
    });
}

/*
 * Get the information from the following endpoint, with the payload parameter. This is always a GET.
 * This function returns a Promise, not the result. The promise must therefore be settled and handled
 */
async function get(endpoint, payload, payloadEncoding = 'application/JSON') {
    return new Promise((resolve, reject) => {
        let xhttp = new XMLHttpRequest();
        // Define the function to handle the server response
        xhttp.onreadystatechange = () => handleReadyStateChange(xhttp, resolve, reject);
        // open and send the request
        xhttp.open('GET', endpoint, true);
        xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhttp.setRequestHeader('Content-Type', payloadEncoding);
        xhttp.send(payload);
    });
}


/*
 * This function contains the logic to check that the response was either successful or had an error, and calls either
 * the resolve or reject callbacks.
 */
function handleReadyStateChange(request, resolve, reject) {
    if (request.readyState === XMLHttpRequest.DONE) {
        if (request.status === 200) {
            // 200 HTML code = all ok!
            resolve(request);
        } else {
            reject(request);
        }
    } // else, state changed, but not ready yet. Ignore...
}


/*
 * This function parses the cookies into a Key/Value dictionary
 */
function getCookie(cookieName) {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith(cookieName))
        .split('=')[1];
}