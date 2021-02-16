export default class Login{
    constructor() {
        this.logindiv = document.getElementById('logindiv')
        window.login = this
    }

    async load() {
        this.credentials = {
            username: undefined,
            token: undefined
        }
        let credentials = localStorage.getItem('credentials')
        if (credentials !== null) {
            let parsedCredentials = JSON.parse(credentials)
            if ('username' in parsedCredentials && 'token' in parsedCredentials) {
                this.credentials.username = parsedCredentials['username']
                this.credentials.token = parsedCredentials['token']    
                window.services.setHeader('Authorization', `Bearer ${this.credentials.token}`)
                
                const res = await window.services.post('/api/login', {null:'null'})
                this.status = res.target.status
                if (this.status == 200) {
                    window.state.set('login', true)
                } else {
                    this.credentials = {}
                    this.save()
                    window.state.set('login', false)
                }
                this.setLoginDiv()
                return
            }
        }
        this.status = 0
        window.state.set('login', false)
        this.setLoginDiv()
    }

    save() {
        localStorage.setItem('credentials', JSON.stringify(this.credentials))
    }

    clearLoginDiv() {
        while (this.logindiv.lastElementChild) {
            this.logindiv.removeChild(this.logindiv.lastElementChild)
        }
    }

    setLoginDiv() {
        this.clearLoginDiv()
        const div = document.createElement('div')
        const p = document.createElement('span')
        const a = document.createElement('a')
        div.className = "loginstatus"
        if (this.status == 0) {
            p.innerHTML = 'not logged in, '
            a.href = '#'
            a.onclick = () => { this.clearLoginDiv(); window.toggleSite('login') }
            a.innerHTML = 'login'
        } else if (this.status == 200){
            p.innerHTML = `logged in as <b>${this.credentials.username}</b>, `
            a.href = '#'
            a.onclick = () => { this.logout() }
            a.innerHTML = 'logout'
            const loginprompt = document.getElementById('loginprompt')
            if (loginprompt) {
                loginprompt.style.backgroundColor = ''
            }
        } else {
            const loginprompt = document.getElementById('loginprompt')
            loginprompt.style.backgroundColor = 'red'
            p.innerHTML = 'login failed'
        }
        this.logindiv.appendChild(div)
        div.appendChild(p)
        p.appendChild(a)
    }

    async login() {
        this.logindiv.innerHTML = ''
        const params = {
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        }
        const res = await window.services.post('/api/login', params)
        this.status = res.target.status
        if (res.target.status === 200) {
            console.log(res.target.response)
            let result = JSON.parse(res.target.response)
            const token = result['bearer']
            
            this.credentials.username = params.username
            this.credentials.token = token
            
            window.services.setHeader('Authorization', `Bearer ${token}`)
            window.toggleSite('login')
            this.save()
        }
        this.setLoginDiv()
        window.state.set('login', true)
        window.render()
    }

    logout() {
        this.credentials = {}
        this.status = 0
        this.save()
        this.setLoginDiv()
        window.services.removeHeader('Authorization')
        window.state.set('login', false)
        window.render()
    }

    verification() {
        return this.verification
    }
}