export default class Services{
    constructor() {
        this.headers = new Map()
        this.headers.set('Content-type', 'application/json;charset=UTF-8')
    }
 
    async _send(method, target, params) {
        return new Promise((response) => {
            let xhr = new XMLHttpRequest()
            xhr.open(method, target.replace(' ', '+'), true)
            this.headers.forEach((content, tag) => {
                xhr.setRequestHeader(tag, content)
            })
    
            xhr.onload = (res) => {
                response(res)
            }
            if (params == undefined) {
                xhr.send()
            } else {
                xhr.send(JSON.stringify(params))
            }

        })
    }

    async get(target) {
        return this._send('GET', target)
    }

    async post(target, params) {
        return this._send('POST', target, params, false)
    }

    async sendForm(form, target, next) {
        const data = form instanceof FormData ? form : new FormData(form)
        const formJSON = Object.fromEntries(data.entries())
        const result = await window.services.post(target, formJSON)
        if (result.target.status == 200) {
            next(true)
        }
        next(false)
    }

    setHeader(tag, content) {
        this.headers.set(tag, content)
    }

    removeHeader(tag) {
        this.headers.delete(tag)
    }
}