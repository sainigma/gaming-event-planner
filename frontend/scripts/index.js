import Login from '/scripts/login.js'
import Services from '/scripts/services.js'

let container, sites, currentSite

const init = () => {
    const login = new Login()
    const services = new Services()
    window.login = login
    window.services = services
    
    window.loadSite = loadSite

    const siteList = ['frontpage', 'login']
    
    container = document.getElementById("container")
    container.innerHTML = ""

    console.log(siteList)
    sites = new Map()
    for (let i in siteList) {
        const site = siteList[i]
        sites.set(site, {content:null, ready:false})        
    }
    loadSite('frontpage')
}

const getSite = async (label) => {
    const response = await services.get(`./pages/${label}.html?${Date.now()}`)
    const div = document.createElement('div')
    div.id = label
    sites.set(label, {content:div, ready:true})
    container.appendChild(div)
    div.innerHTML = response.target.response
    loadSite(label)
}

function loadSite(label) {
    let site = sites.get(label)
    if (!site.ready) {
        console.log(`loading ${label}..`)
        getSite(label)
    } else {
        if (currentSite) {
            currentSite.style.display = 'none'
        }
        site.content.style.display = 'block'
        currentSite = site.content
    }
}

window.onload = () => {
    init()
}