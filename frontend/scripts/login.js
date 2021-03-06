export default class Login{
    constructor() {
        this.logindiv = document.getElementById('logindiv')
        window.login = this
        this.initLoginEvents()
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
                    state.set('login', true)
                    this.setLoginDiv('loginsuccess')
                } else {
                    this.credentials = {}
                    this.save()
                    this.status = 0
                    state.set('login', false)
                    this.setLoginDiv()
                }
                return
            }
        }
        this.status = 0
        state.set('login', false)
        this.setLoginDiv()
    }

    cancel() {
        this.setLoginDiv()
        const a = document.getElementById('login')
        const b = document.getElementById('newuser')
        console.log(a, b)
        if (a != undefined && a.style.display != 'none') {
            toggleSite('login')
        }
        if (b != undefined && b.style.display != 'none') {
            toggleSite('newuser')
        }
    }

    save() {
        localStorage.setItem('credentials', JSON.stringify(this.credentials))
    }

    clearLoginDiv() {
        while (this.logindiv.lastElementChild) {
            this.logindiv.removeChild(this.logindiv.lastElementChild)
        }
    }

    initLoginEvents() {
        this.events = {}
        this.events['default'] = (span) => {
            span.innerHTML = `<button class='button-login' onclick="login.clearLoginDiv(); toggleSite('login')">Login</button> <button class='button-login' onclick="login.clearLoginDiv(); toggleSite('newuser')">Sign up</up>`
        }
        this.events['loginfailed'] = () => {
            const errorSpan = document.getElementById('loginerrorspan')
            const loginprompt = document.getElementById('loginprompt')
            if (loginprompt != null) {
                loginprompt.style.backgroundColor = 'red'
                errorSpan.innerHTML = 'login failed'
            }
        }
        this.events['newuserfailed'] = () => {
            const errorSpan = document.getElementById('newusererrorspan')
            const loginprompt = document.getElementById('newuserprompt')
            if (loginprompt != null) {
                loginprompt.style.backgroundColor = 'red'
                errorSpan.innerHTML = 'username already taken'
                state.set('login', false)
            }
        }
        this.events['loginsuccess'] = (span) => {
            this.status = 200
            span.innerHTML = `logged in as <b>${this.credentials.username}</b>, <a href='#' onclick="login.logout()">logout</a>`
            const loginprompt = document.getElementById('loginprompt')
            if (loginprompt) {
                loginprompt.style.backgroundColor = ''
            }
        }
        this.events['newusersuccess'] = (span) => {
            this.status = 200
            toggleSite('newuser')
            span.innerHTML = `logged in as <b>${this.credentials.username}</b>, <a href='#' onclick="login.logout()">logout</a>`
            const loginprompt = document.getElementById('newuserprompt')
            if (loginprompt) {
                loginprompt.style.backgroundColor = ''
            }
        }
    }

    setLoginDiv(event) {
        let key = event == undefined ? 'default' : event

        this.clearLoginDiv()
        const div = document.createElement('div')
        const span = document.createElement('span')
        div.className = 'loginstatus'

        this.events[key](span)

        div.appendChild(span)
        this.logindiv.appendChild(div)
    }

    setLoginDivOld() {
        this.clearLoginDiv()
        const div = document.createElement('div')
        const p = document.createElement('span')
        const a = document.createElement('a')
        div.className = "loginstatus"
        if (this.status == 0) {
            p.innerHTML = `<button class='button-login' onclick="login.clearLoginDiv(); toggleSite('login')">Login</button> <button class='button-login' onclick="login.clearLoginDiv(); toggleSite('newuser')">Sign up</up>`
        } else if (this.status == 200){
            p.innerHTML = `logged in as <b>${this.credentials.username}</b>, <a href='#' onclick="login.logout()">logout</a>`
            const loginprompt = document.getElementById('loginprompt')
            if (loginprompt) {
                loginprompt.style.backgroundColor = ''
            }
        } else {
            const loginprompt = document.getElementById('loginprompt')
            if (loginprompt != null) {
                loginprompt.style.backgroundColor = 'red'
                p.innerHTML = 'login failed'
            }
        }
        this.logindiv.appendChild(div)
        div.appendChild(p)
        p.appendChild(a)
    }

    getLoginParams(usernameTag, passwordTag) {
        return {
            username: document.getElementById(usernameTag).value,
            password: document.getElementById(passwordTag).value
        }
    }

    async new() {
        this.logindiv.innerHTML = ''
        const params = this.getLoginParams('newusername', "newpassword")
        const res = await services.post('/api/login/new', params)
        const success = this.completeLogin(res, params)
        console.log(res, success)
        if (success) {
            state.set('login', true)
            this.setLoginDiv('newusersuccess')
        } else {
            state.set('login', false)
            this.setLoginDiv('newuserfailed')
        }
        window.render()
    }

    async login() {
        this.logindiv.innerHTML = ''
        const params = this.getLoginParams('username', 'password')
        
        const res = await window.services.post('/api/login', params)
        const success = this.completeLogin(res, params)
        if (success) {
            window.state.set('login', true)
            this.setLoginDiv('loginsuccess')
            toggleSite('login')
        } else {
            window.state.set('login', false)
            this.setLoginDiv('loginfailed')
        }
        
        window.render()
    }

    completeLogin(res, params) {
        if (res.target.status == 200) {
            console.log(res.target.response)
            let result = JSON.parse(res.target.response)
            const token = result['bearer']

            this.credentials.username = params.username
            this.credentials.token = token
            
            window.services.setHeader('Authorization', `Bearer ${token}`)
            this.save()
            
            return true
        }
        return false
    }

    logout() {
        this.credentials = {}
        this.status = 0
        this.save()
        this.setLoginDiv()
        friends.clear()
        window.services.removeHeader('Authorization')
        window.state.set('login', false)
        window.render()
        window.setBlocker(false)
    }

    verification() {
        return this.verification
    }

    getUser() {
        return this.credentials.username
    }
}