/** Manage a counter of followers. */
class FollowerCounter {

    constructor(elementId) {
        this.elementId = elementId;
        this._count = +this._getElement().innerText;
    }

    _getElement() {
        return document.getElementById(this.elementId);
    }

    _sync() {
        const el = this._getElement();
        el.innerText = this._count;
    }

    /** Increment the counter. */
    increment() {
        this._count++;
        this._sync();
    }

    /** Decrement the counter. */
    decrement() {
        this._count--;
        this._sync();
    }
}
