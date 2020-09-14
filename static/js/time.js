/*
 * This file contains all the logic related to the incredibly complex problem of showing and formatting dates and
 * times according to the locales and other complicated issues. Fun.
 */

 /*
  * Insert the given datetime into the container with the correct formatting for the locale.
  * Now is assumed to be specified in UTC time. If now is omitted, current time is used.
  *
  * Please use this function when displaying dates to keep a consistent appearance across the application for
  * showing datetimes
  */
 function insertDatetime(container, now) {
    const time = moment.utc(now).local();

    container.innerText = time.format('ll, LT');
 }

/*
 * This function goes through the DOM of the pages, replacing UTC formatted dates into appropriate local time
 * and formats. This depends on all dates to be in a container of the class `utc-date-container`.
 *
 * This function should be run before the page is displayed to the user.
 */
 function fixAllUTCDates() {
    const elementsToFix = document.getElementsByClassName("utc-date-container");

    for (let i=0; i < elementsToFix.length|0; i++) {
        const value = elementsToFix[i].innerText.trim();
        if (value.length > 0) {
            insertDatetime(elementsToFix[i], value);
        }
    }
 }

// Add the listener to run once DOM has fully loaded
 document.addEventListener('DOMContentLoaded', fixAllUTCDates);