import Login from '/scripts/login.js'
import StateColletor from '/scripts/state.js'
import Services from '/scripts/services.js'
import EventCreator from '/scripts/eventcreator.js'

let container, sites

const init = async() => {
    const services = new Services()
    
    window.services = services
    window.toggleSite = toggleSite
    window.render = render
    window.listEvents = listEvents
    window.clearEvents = clearEvents

    const siteList = ['frontpage', 'login', 'eventcreator', 'eventeditor']
    container = document.getElementById("container")
    container.innerHTML = ""

    console.log(siteList)
    sites = new Map()
    for (let i in siteList) {
        const site = siteList[i]
        sites.set(site, {content:null, ready:false, visible:false, onload:null})        
    }

    const state = new StateColletor()
    const login = new Login()
    const eventcreator = new EventCreator()

    await login.load()

    toggleSite('frontpage')
}

const getSite = async (label) => {
    const response = await services.get(`./pages/${label}.html?${Date.now()}`)
    const div = document.createElement('div')
    div.id = label
    sites.set(label, {content:div, ready:true})
    container.appendChild(div)
    div.innerHTML = response.target.response
    toggleSite(label)
}

function toggleSite(label) {
    let site = sites.get(label)
    if (!site.ready) {
        console.log(`loading ${label}..`)
        getSite(label)
    } else {
        site.visible = !site.visible
        site.content.style.display = site.visible ? 'block' : 'none'
        if (site.visible) {
            window.state.set('current', label)
            window.render()
        }
    }
}

async function listEvents() {
    const listCategory = (title, events) => {
        const h = document.createElement('h3')
        h.innerHTML = title
        div.appendChild(h)
        if (events.length == 0) {
            const p = document.createElement('p')
            p.className = 'nosell'
            p.innerHTML = 'no events listed'
            div.appendChild(p)
        } else {
            events.forEach(event => {
                const p = document.createElement('p')
                const button = document.createElement('button')
                p.innerHTML = `${event[1]}`
                button.innerHTML = 'expand'
                button.onclick = () => {
                    toggleSite('eventeditor')
                }
                p.appendChild(button)
                div.appendChild(p)
            })
        }
    }
    
    const div = document.getElementById("eventlist")
    const res = await window.services.get('/api/event/all')
    if (res.target.status != 200) {
        return false
    } 
    if (div.children.length == 0) {
        const events = await JSON.parse(res.target.response)
        console.log(events)
        listCategory('My events', events['my'])
        listCategory('Upcoming events', events['attending'])
        listCategory('Open invites', events['invites'])
        const b = document.createElement('button')
        b.innerHTML = "create event"
        b.onclick = async () => {
            await toggleSite('eventcreator')
            window.eventcreator.initForm()
        }
        div.appendChild(b)
    }
    return true
}

function clearEvents() {
    const div = document.getElementById("eventlist")
    div.innerHTML = ''
}

function render() {
    console.log('Render')
    if (window.state.get('login')) {
        listEvents()
    } else {
        clearEvents()
    }
}

window.onload = () => {
    init()
}