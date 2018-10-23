/** Manage the following state.
 * Make use of the Observer pattern to allow other clients to subscribe
 * to "followed"/"unfollowed" events.
 */

const EVENTS = {
    FOLLOWED: 'followed',
    UNFOLLOWED: 'unfollowed',
};

class FollowManager {

    constructor(starId, initial) {
        this.starId = starId;
        this._following = initial;
        this._callbacks = {
            [EVENTS.FOLLOWED]: [],
            [EVENTS.UNFOLLOWED]: [],
        };
        this.onFollow(() => {
            this._toggleClasses();
            this._following = true;
        });
        this.onUnFollow(() => {
            this._toggleClasses();
            this._following = false;
        });
    }

    /** Toggle the subscribed state. */
    toggle(showId) {
        if (this._following) {
            this._unFollow(showId);
        } else {
            this._follow(showId);
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

    /** Register a new follow callback */
    onFollow(fn) {
        this._callbacks[EVENTS.FOLLOWED].push(fn);
    }

    /** Register a new unfollow callback */
    onUnFollow(fn) {
        this._callbacks[EVENTS.UNFOLLOWED].push(fn);
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

    _follow(showId) {
        this._makeApiCall(
            showId, 'POST',
            () => this._notify(EVENTS.FOLLOWED),
        );
    }

    _unFollow(showId) {
        this._makeApiCall(
            showId, 'DELETE',
            () => this._notify(EVENTS.UNFOLLOWED)
        );
    }
}
