/*
We need to cache locally if the user is subscribed or not so he can
toggle his subscription without reloading the page every time
*/
var is_subscribed = null;

function toggle_subscribe(show_id, is_subbed) {
    /*
    Function that will toggle the user's subscription
     */

    //The first time the user toggles subscription, we use his current subscription state
    //After that we use the cached value
    if (is_subscribed == null) {
        is_subscribed = is_subbed;
    }
    if (is_subscribed) {
        unsubscribe(show_id)
    } else {
        subscribe(show_id)
    }
}

function subscribe(show_id) {
    /*
    Function that subscribes the user to the show by making a POST request to the SubscriptionShow view
     */
    const subscriptionUrl = "/subscribe/" + show_id;
    $.ajax({
        type: 'POST',
        url: subscriptionUrl,
        dataType: "json",
        success: toggleSubscriptionDone,
        error: onError,
    })
}

function unsubscribe(show_id) {
    /*
    Function that unsubscribes the user to the show by making a DELETE request to the SubscriptionShow view
     */
    const subscriptionUrl = "/subscribe/" + show_id;
    $.ajax({
            type: 'DELETE',
            url: subscriptionUrl,
            dataType: "json",
            success: toggleSubscriptionDone,
            error: onError,
        })
}

function toggleSubscriptionDone() {
    /*
    Function called when the API request is a success
    We need to internally remember current state of subscription
     */
    is_subscribed = !is_subscribed;
    toggleStar();
}

function toggleStar() {
    /*
    Change the star aspect whether the user is subscribed or not
     */
    el = document.getElementById('star')
    el.classList.toggle('fas');
    el.classList.toggle('far');
}

function onError(jqXHR, textStatus, errorThrown) {
    console.error(errorThrown);
}


/*
Utilities functions to allow csrf token
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
