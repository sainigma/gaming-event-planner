import {listResults} from '/scripts/static/listResults.js'

export default class EventEditor{
    constructor() {
        window.eventeditor = this
        this.div = null
        this.eventId = -1
    }

    async setInnerHTML(target, content) {
        const element = await document.getElementById(target)
        element.innerHTML = content
        return element
    }

    async setVisibility(target, tag) {
        const element = await document.getElementById(target)
        element.style.display = tag
        return element
    }

    async comment() {
        const commentfield = await document.getElementById('commentfield')
        const target = '/api/comment/new'
        const params = {
            eventId:this.eventId,
            targetId:-1,
            content:commentfield.value
        }
        commentfield.disabled = true
        console.log(params)
        const result = await window.services.post(target, params)
        if (result.target.status == 200) {
            commentfield.value = ''
        }
        commentfield.disabled = false
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
        this.div = await this.setVisibility('eventeditor', 'none')
        
        this.eventId = window.state.get('eventid')
        const res = await window.services.get('/api/event/' + this.eventId)
        if (res.target.status !== 200) {
            return
        }
        window.setBlocker(true)

        const responseBody = JSON.parse(res.target.response)
        const info = responseBody.info
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

        console.log(eventInfo)

        if (responseBody.owner === window.login.getUser()) {
            this.setVisibility('eventeditoradminpanel', 'grid')
        } else {
            this.setVisibility('eventeditoradminpanel', 'none')
        }
        this.setVisibility('eventeditorgamelabel', 'none')
        this.setVisibility('eventeditorgameitem', 'none')
        this.setVisibility('eventeditor', 'block')
        if (eventInfo.gameId != -1) {
            this.setVisibility('eventeditorgamelabel', 'inherit')
            this.setVisibility('eventeditorgameitem', 'inherit')
            this.setInnerHTML('eventeditorgameitem', '<i>fetching..</i>')
            const gameRes = await window.services.get('/api/game/' + eventInfo.gameId)
            if (gameRes.target.status == 200) {
                const gameInfo = JSON.parse(gameRes.target.response)
                this.setInnerHTML('eventeditorgameitem', `<a target='_blank' href='https://www.igdb.com/games/${gameInfo.slug}/'>${gameInfo.name}</a>`)
            } else {
                this.setVisibility('eventeditorgamelabel', 'none')
                this.setVisibility('eventeditorgameitem', 'none')
        
            }
        }
    }
}