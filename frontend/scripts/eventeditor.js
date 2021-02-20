import {listResults} from '/scripts/static/listResults.js'

export default class EventEditor{
    constructor() {
        window.eventeditor = this
        this.div = null
        this.eventId = -1
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

    setSearch(e) {
        this.usertofind = e
    }

    async inviteUser(username) {
        const target = '/api/user/invite/'
        const params = {'targetuser':username, 'eventid': this.eventId}
        const result = await window.services.post(target, params)
    }

    async searchUser(e) {
        const wrapper = (params) => {
            this.inviteUser(params.name)
        }
        e.disabled = true
        e.value = ''
        const result = await window.services.get('/api/user/find/?search='+this.usertofind)
        e.disabled = false
        listResults(result.target.response, 'eventeditorinvitelist', 'Invite', wrapper)
    }

    async update() {
        this.div = await document.getElementById('eventeditor')
        this.eventId = window.state.get('eventid')
        const res = await window.services.get('/api/event/' + this.eventId)
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
        this.setInnerHTML('eventdescription', eventInfo.description)
        this.setInnerHTML('eventdescriptioneditor', eventInfo.description)
    }
}