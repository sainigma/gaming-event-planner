import Login from '/scripts/login.js'
import StateColletor from '/scripts/state.js'
import Services from '/scripts/services.js'
import EventCreator from '/scripts/eventcreator.js'
import EventEditor from '/scripts/eventeditor.js'

let container, sites, blocker

const init = async() => {
    const services = new Services()
    
    window.services = services
    window.toggleSite = toggleSite
    window.render = render
    window.listEvents = listEvents
    window.clearEvents = clearEvents
    window.setBlocker = setBlocker

    const siteList = ['frontpage', 'login', 'eventcreator', 'eventeditor']
    container = document.getElementById("container")
    container.innerHTML = ""

    blocker = document.getElementById("blocker")
    setBlocker(false)

    console.log(siteList)
    sites = new Map()
    for (let i in siteList) {
        const site = siteList[i]
        sites.set(site, {content:null, ready:false, visible:false, onload:null})        
    }

    const state = new StateColletor()
    const login = new Login()
    const eventcreator = new EventCreator()
    const eventeditor = new EventEditor()

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
    return true
}

function setBlocker(state) {
    blocker.style.display = state ? 'block' : 'none'
}

async function listEvents() {
    const listCategory = (title, events) => {
        const titlediv = document.createElement('div')
        titlediv.className = 'grid-title-big'
        titlediv.innerHTML = title
        div.appendChild(titlediv)
        
        if (events.length == 0) {            
            const p = document.createElement('div')
            p.className = 'grid-item'
            p.innerHTML = 'no events listed'
            p.style = 'grid-column: 1 / 3'
            div.appendChild(p)
        } else {
            events.forEach(event => {
                const eventTitle = document.createElement('div')
                eventTitle.className = 'grid-title'
                eventTitle.innerHTML = `${event[1]}`

                const buttonDiv = document.createElement('div')
                buttonDiv.className = 'grid-item'
                
                if (title === 'Open invites') {
                    const acceptButton = document.createElement('button')
                    const ignoreButton = document.createElement('button')
                    acceptButton.innerHTML = 'Accept'
                    ignoreButton.innerHTML = 'Ignore'
                    acceptButton.style.width = '40%'
                    acceptButton.style.marginRight = '5%'
                    ignoreButton.style.width = '40%'
                    buttonDiv.appendChild(acceptButton)
                    buttonDiv.appendChild(ignoreButton)

                    const target = `/api/event/invitations/${event[0]}`
                    acceptButton.onclick = async () => {
                        await window.services.post(target, {status:1})
                        clearEvents()
                        listEvents()
                    }
                    ignoreButton.onclick = async () => {
                        await window.services.post(target, {status:0})
                        clearEvents()
                        listEvents()
                    }
                } else {
                    const button = document.createElement('button')
                    button.innerHTML = 'Expand'
                    button.style.width = '80%'
                    button.onclick = () => {
                        toggleSite('eventeditor')
                        window.state.set('eventid', event[0])
                    }
                    buttonDiv.appendChild(button)
                }

                div.appendChild(eventTitle)
                div.appendChild(buttonDiv)
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
        const buttonContainer = document.createElement('div')
        buttonContainer.className = 'grid-title-big'
        const b = document.createElement('button')
        b.innerHTML = "create event"
        b.style.width = '80%'
        b.onclick = async () => {
            await toggleSite('eventcreator')
            window.eventcreator.initForm()
        }
        buttonContainer.appendChild(b)
        div.appendChild(buttonContainer)
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
        if (window.state.get('current') == 'eventeditor') {
            window.eventeditor.update()
        }
    } else {
        clearEvents()
    }
}

window.onload = () => {
    init()
}