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
            
            for (let header in this.headers.keys()) {
                console.log(header)
                xhr.setRequestHeader(header, this.headers.get(header))
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
        this.headers.set(tag, content)
    }

    removeHeader(tag) {
        this.headers.delete(tag)
    }
}