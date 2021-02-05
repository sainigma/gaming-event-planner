export default class Login{
    constructor() {
        this.username, this.password, this.verification = undefined
        this.load()
    }

    load() {
        //lataa keksi
    }

    setUsername(username) {
        this.username = username
    }

    setPassword(password) {
        this.password = password
    }

    async login() {
        const params = {
            username: this.username,
            password: this.password
        }
        const response = await window.services.post('/api/login', params)
        console.log(response)
        //window.services.setHeader('Authorization', `Bearer ${this.verification}`)
        return 200
    }

    verification() {
        return this.verification
    }
}