let container, sites, currentSite

const init = () => {
    const siteList = ['frontpage', 'login']
    
    container = document.getElementById("container")
    container.innerHTML ="js works"

    console.log(siteList)
    sites = new Map()
    for (let i in siteList) {
        const site = siteList[i]
        sites.set(site, {content:null, ready:false})        
    }
    loadSite('frontpage')
}

const getSite = (label) => {
    let xhr = new XMLHttpRequest()
    xhr.open('GET', `./pages/${label}.html?${Date.now()}`)
    xhr.onload = (res) => {
        const div = document.createElement('div')
        div.id = label
        div.innerHTML = res.target.response
        sites.set(label, {content:div, ready:true})
        container.appendChild(div)
        loadSite(label)
    }
    xhr.send()
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