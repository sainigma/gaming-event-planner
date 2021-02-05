export default class Services{
    constructor() {
        this.headers = {}
    }

    async _send(method, target, params) {
        return new Promise((response) => {
            let xhr = new XMLHttpRequest()
            xhr.open(method, target, true)
            xhr.setRequestHeader('Content-type', 'application/json;charset=UTF-8')
            for (let header in this.headers) {
                xhr.setRequestHeader(header, this.headers[header])
            }
    
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
        return this._send('POST', target, params)
    }

    setHeader(tag, content) {
        this.headers = {...this.headers, tag: content}
    }
}