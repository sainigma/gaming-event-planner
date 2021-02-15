import Login from '/scripts/login.js'
import StateColletor from '/scripts/state.js'
import Services from '/scripts/services.js'
import EventCreator from '/scripts/eventcreator.js'

let container, sites

const init = () => {
    const services = new Services()
    
    window.services = services
    window.toggleSite = toggleSite
    window.render = render
    
    const siteList = ['frontpage', 'login', 'eventcreator']
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

function listEvents() {
    const listCategory = (title, events) => {
        const h = document.createElement('h3')
        h.innerHTML = title
        div.appendChild(h)
        if (events.length == 0) {
            const p = document.createElement('p')
            p.innerHTML = 'no events listed'
            div.appendChild(p)
        }
    }
    
    const div = document.getElementById("eventlist")
    console.log(div)
    if (div.children.length == 0) {
        listCategory('Upcoming events', [])
        listCategory('Open invites', [])
        const b = document.createElement('button')
        b.innerHTML = "create event"
        b.onclick = async () => {
            await toggleSite('eventcreator')
            window.eventcreator.initForm()
        }
        div.appendChild(b)
    }
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