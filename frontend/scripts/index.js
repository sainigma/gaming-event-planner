import Login from '/scripts/login.js'
import Services from '/scripts/services.js'

let container, sites

const init = () => {
    const services = new Services()
    
    window.services = services
    window.toggleSite = toggleSite
    
    const siteList = ['frontpage', 'login']

    container = document.getElementById("container")
    container.innerHTML = ""

    console.log(siteList)
    sites = new Map()
    for (let i in siteList) {
        const site = siteList[i]
        sites.set(site, {content:null, ready:false, visible:false})        
    }
    const login = new Login()
    window.login = login
    
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
    }
}

window.onload = () => {
    init()
}