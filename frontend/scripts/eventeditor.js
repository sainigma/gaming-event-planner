export default class EventEditor{
    constructor() {
        window.eventeditor = this
        this.div = null
    }

    setInnerHTML(target, content) {
        const element = document.getElementById(target)
        element.innerHTML = content
        return element
    }

    close() {
        window.toggleSite('eventeditor')
        window.setBlocker(false)
    }

    async update() {
        this.div = await document.getElementById('eventeditor')
        const eventId = window.state.get('eventid')
        const res = await window.services.get('/api/event/' + eventId)
        if (res.target.status !== 200) {
            return
        }
        window.setBlocker(true)

        const info = JSON.parse(res.target.response).info
        const eventInfo = {
            title:info[0],
            description:info[1],
            usergroup:info[2],
            gameId:info[3],
            created:info[4],
            timeout:info[5],
            optupper:info[6],
            optlower:info[7]
        }
        this.setInnerHTML('eventeditortitle', eventInfo.title)
    }
}