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
    window.clear = clear
    window.setBlocker = setBlocker

    const siteList = ['frontpage', 'login', 'eventcreator', 'eventeditor', 'newuser']
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

function toggleSite(label, forcedState) {
    let site = sites.get(label)
    if (!site.ready) {
        console.log(`loading ${label}..`)
        getSite(label)
    } else {
        site.visible = forcedState == undefined ? !site.visible : forcedState
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

async function listFriends() {
    const div = document.getElementById("friendslist")

    if (div.children.length != 0) {
        return
    }

    const res = await window.services.get('/api/user/find/?search=*')

    const titlediv = document.createElement('div')
    titlediv.className = 'grid-title-big'
    titlediv.innerHTML = 'My friends'

    const categoryContainer = document.createElement('div')
    categoryContainer.className = 'scrollingfield grid-wide'
    categoryContainer.style.width = '100%'

    const b = document.createElement('button')
    b.className = "button-wide"
    b.innerHTML = "add friend"
    b.style = 'grid-column-start:1; grid-column-end: 4'
    b.onclick = async () => {
        //await toggleSite('eventcreator')
        //window.eventcreator.initForm()
    }

    div.appendChild(titlediv)
    div.appendChild(categoryContainer)
    div.appendChild(b)

    if (res.target.status == 200) {
        const friendsList = JSON.parse(res.target.response)
        console.log(friendsList)
        
        if (friendsList.length == 0) {
            categoryContainer.innerHTML = 'no friends'
            return
        }

        friendsList.forEach(friend => {

        })
    }
}

async function listEvents() {
    const listCategory = (title, events) => {
        const categoryContainer = document.createElement('div')
        categoryContainer.className = 'scrollingfield grid-wide'
        categoryContainer.style.width = '100%'

        const titlediv = document.createElement('div')
        titlediv.className = 'grid-title-big'
        titlediv.innerHTML = title

        div.appendChild(titlediv)
        div.appendChild(categoryContainer)
        
        if (events.length == 0) {            
            const p = document.createElement('div')
            p.className = 'grid-item'
            p.innerHTML = 'no events listed'
            p.style = 'grid-column: 1 / 3'
            div.appendChild(p)
        } else {
            events.forEach(event => {
                const eventTitle = document.createElement('div')
                eventTitle.className = 'grid-event'

                if (title === 'Open invites') {
                    const d = document.createElement('div')
                    d.className = 'grid-title'
                    d.innerHTML = event[1]
                    d.style.background = 'var(--color-background)'
                    d.style.border = 'none'
                    d.style.textAlign = 'left'
                    const acceptButton = document.createElement('button')
                    const ignoreButton = document.createElement('button')
                    acceptButton.innerHTML = 'Accept'
                    ignoreButton.innerHTML = 'Ignore'
                    
                    acceptButton.className = 'button-accept grid-title-button'
                    ignoreButton.className = 'button-refuse grid-title-button'
                    
                    acceptButton.style.right = '8em'
                    ignoreButton.style.right = '0'
                    d.appendChild(acceptButton)
                    d.appendChild(ignoreButton)

                    const target = `/api/event/invitations/${event[0]}`
                    acceptButton.onclick = async () => {
                        await window.services.post(target, {status:1})
                        clear()
                        listEvents()
                    }
                    ignoreButton.onclick = async () => {
                        await window.services.post(target, {status:0})
                        clear()
                        listEvents()
                    }
                    eventTitle.appendChild(d)
                } else {
                    const button = document.createElement('button')
                    button.className = 'button-wide button-expands'
                    button.innerHTML = `${event[1]} <span>expand</span>`
                    button.onclick = () => {
                        toggleSite('eventeditor')
                        window.state.set('eventid', event[0])
                    }
                    eventTitle.appendChild(button)
                }
                categoryContainer.appendChild(eventTitle)
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

        const b = document.createElement('button')
        b.className = "button-wide"
        b.innerHTML = "create event"
        b.style = 'grid-column-start:1; grid-column-end: 4'
        b.onclick = async () => {
            await toggleSite('eventcreator')
            window.eventcreator.initForm()
        }
        div.appendChild(b)

        listCategory('Upcoming events', events['attending'])
        listCategory('Open invites', events['invites'])
    }
    return true
}

function clear() {
    const div = document.getElementById("eventlist")
    const div2 = document.getElementById("friendslist")
    div.innerHTML = ''
    div2.innerHTML = ''
}

function render() {
    console.log('Render')
    if (window.state.get('login')) {
        listEvents()
        listFriends()
        if (window.state.get('current') == 'eventeditor') {
            window.eventeditor.update()
        }
    } else {
        clear()
    }
}

window.onload = () => {
    init()
}