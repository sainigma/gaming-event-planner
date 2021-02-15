export default class StateColletor{
    constructor() {
        this.state = new Map()
        window.state = this
    }

    set(key, value) {
        this.state.set(key, value)
    }

    get(key) {
        return this.state.get(key)
    }
}