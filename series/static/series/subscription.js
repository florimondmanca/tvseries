/** Manage the subscription state.
 * Make use of the Observer pattern to allow other clients to subscribe
 * to "subscribed"/"unsubscribed" events.
 */
class Subscriber {

    constructor(starId, initial) {
        this.starId = starId;
        this._subscribed = initial;
        this._callbacks = {
            subscribe: [],
            unsubscribe: [],
        };
        this.onSubscribe(() => {
            this._toggleClasses();
            this._subscribed = true;
        });
        this.onUnsubscribe(() => {
            this._toggleClasses();
            this._subscribed = false;
        });
    }

    /** Toggle the subscribed state. */
    toggle(showId) {
        if (this._subscribed) {
            this._unSubscribe(showId);
        } else {
            this._subscribe(showId);
        }
    }

    _toggleClasses() {
        const el = this._getElement();
        el.classList.toggle('fas');
        el.classList.toggle('far');
    }

    _getElement() {
        return document.getElementById(this.starId);
    }

    /** Register a new subscribe callback */
    onSubscribe(fn) {
        this._callbacks.subscribe.push(fn);
    }

    /** Register a new unsubscribe callback */
    onUnsubscribe(fn) {
        this._callbacks.unsubscribe.push(fn);
    }

    _notify(event) {
        for (const fn of this._callbacks[event]) {
            fn();
        }
    }

    _makeApiCall(showId, httpMethod, onSuccess) {
        $.ajax({
            type: httpMethod,
            url: `/subscribe/${showId}`,
            dataType: 'json',
            success: () => onSuccess(),
            error: (xhr, status, err) => console.log(err),
        })
    }

    _subscribe(showId) {
        this._makeApiCall(
            showId, 'POST',
            () => this._notify('subscribe')
        );
    }

    _unSubscribe(showId) {
        this._makeApiCall(
            showId, 'DELETE',
            () => this._notify('unsubscribe')
        );
    }
}
