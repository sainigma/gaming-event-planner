import {listResults, listCreator} from '/scripts/static/listResults.js'

export default class EventEditor{
    constructor() {
        window.eventeditor = this
        this.div = null
        this.eventId = -1
        this.initiated = false
    }

    async init() {
        const dateAdderDiv = document.getElementById('dateadder')
        if (dateAdderDiv == null) {
            return
        }

        const getPage = async(label) => {
            const result = await services.get(`./pages/eventeditor/${label}.html?${Date.now()}`)
            if (result.target.status == 200) {
                return result.target.response
            }
            return ''
        }

        dateAdderDiv.innerHTML = await getPage('dateadder')
        this.initiated = true
    }

    updateEvent(form) {
        if (!this.readyForUpdate) {
            return
        }
        const data = new FormData(form)
        data.append('eventId', this.eventId)
        services.sendForm(data, '/api/event/update', () => {})
    }

    updateFormChanged() {
        this.readyForUpdate = true
        const updateButton = document.getElementById('eventupdatebutton')
        updateButton.disabled = false
    }

    collapseHours(hours) {
        let arr1 = []
        let arr2 = []

        let i = 0
        let previous = 0
        arr1.push(hours[0])
        previous = arr1[0]
        hours.forEach(hour => {
            if (hour > previous + 1) {
                arr1.push(hour)
                arr2.push(previous)
            }
            previous = hour
            i++
        })
        arr2.push(previous)

        let result = ''
        for(let j = 0; j < arr1.length; j++) {
            if (arr1[j] == arr2[j]) {
                result += arr1[j]
            } else {
                result += `${arr1[j]} - ${arr2[j]}`
            }
            if (j + 1 < arr1.length) {
                result += ', '
            }
        }
        return result
    }

    dateString(date, precision) {
        const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
        const epoch = parseInt(date)
        const dateObj = epoch > 9999 ? new Date(epoch * 1000) : new Date(Date.parse(date))
        const fields = [`${weekdays[dateObj.getDay()]}`, ` ${dateObj.getDate()}/${months[dateObj.getMonth()]}`, ` ${dateObj.getFullYear()}`]
        
        let result = ''
        for(let i = 0; i < precision; i++) {
            result += fields[i]
        }
        return result
    }

    getDateISOString(time) {
        const date = new Date(time)
        return `${date.getFullYear()}-${('0' + (date.getMonth() + 1)).slice(-2)}-${('0' + date.getDate()).slice(-2)}`
    }

    async activateDateAdder() {

        const dateadderinput = document.getElementById('dateadderdate')
        dateadderinput.min = this.getDateISOString(Date.now())
        dateadderinput.max = this.getDateISOString(parseInt(this.endDate)*1000)

        const dateaddertable = document.getElementById('dateadderdates')
        dateaddertable.innerHTML = ''
        const result = await window.services.get(`/api/vote/date/${this.eventId}`)
        if (result.target.status != 200) {
            return
        }

        if (result.target.response != "[]") {
            const dates = JSON.parse(result.target.response)
            dates.forEach((date) => {
                const tr = document.createElement('tr')
                const buttonfield = document.createElement('td')
                const removebuttonField = document.createElement('td')
                const copybutton = document.createElement('button')
                const removebutton = document.createElement('button')

                const dateInner = `${this.dateString(date.date, 3)} : ${this.collapseHours(date.hours)}`
                
                copybutton.innerHTML = `${dateInner} <span>copy to editor</span>`
                copybutton.onclick = () => {
                    eventeditor.dateCopy(date.date, date.hours)
                }
                copybutton.className = 'button-wide button-expands'
                copybutton.style = 'text-align: left;'
                removebutton.innerHTML = 'remove'
                removebutton.className = 'button-refuse button-wide'
                removebutton.onclick = () => {
                    eventeditor.removeDate(date.date)
                }

                buttonfield.appendChild(copybutton)
                removebuttonField.appendChild(removebutton)
                tr.appendChild(buttonfield)
                tr.appendChild(removebuttonField)
                dateaddertable.appendChild(tr)
            })
        }
        utils.setVisibility('dateadder', 'block')
        utils.setVisibility('eventeditorblocker', 'block')
    }

    resetDateAdder() {
        const dateitem = document.getElementById('dateadderdate')
        dateitem.value = ""
        this.dateSetRange(0, 23, false)
        utils.setVisibility('eventeditorcontrols', 'block')
    }

    removeDate(date) {
        this.afterDateSubmit()
    }

    dateCopy(date, hours) {
        const dateitem = document.getElementById('dateadderdate')
        dateitem.value = date
        hours.forEach(hour => {
            const item = document.getElementById(`dateaddervalues${hour}`)
            item.checked = true
        })
        utils.setVisibility('eventeditorcontrols', 'none')
        utils.setVisibility('eventeditordateadderform', 'block')
    }

    dateSetRange(start, end, value) {
        for(let i = start; i <= end; i++) {
            const item = document.getElementById(`dateaddervalues${i}`)
            item.checked = value
        }
    }

    dateToggleRange(start, end) {
        for(let i = start; i <= end; i++) {
            const item = document.getElementById(`dateaddervalues${i}`)
            item.checked = !item.checked
        }
    }

    clearComments() {
        const commentParent = document.getElementById('eventeditorcomments')
        commentParent.innerHTML = ''
    }

    async updateComments() {
        const currentUser = window.login.getUser()
        
        const addComment = (comment) => {
            const commentElement = document.createElement('p')
            const commentDate = new Date(comment.time * 1000)
            const timestamp = `${('0'+commentDate.getHours()).slice(-2)}:${('0'+commentDate.getMinutes()).slice(-2)}:${('0'+commentDate.getSeconds()).slice(-2)}`
            
            let usertag = comment.name
            usertag = comment.name === currentUser ? `<b>${usertag}</b>` : usertag
            commentElement.innerHTML = `[${timestamp}] &#60;${usertag}&#62;: ${comment.content}`
            commentElement.className = 'comment'
            commentParent.appendChild(commentElement)
        }

        const target = `/api/comment/${this.eventId}`
        const commentParent = document.getElementById('eventeditorcomments')
        
        const result = await window.services.get(target)
        if (result.target.status !== 200) {
            return
        }
        const comments = JSON.parse(result.target.response)
        if (comments.length == 0) {
            commentParent.innerHTML = ''
            return
        }
        for (let i = commentParent.childElementCount; i < comments.length; i++) {
            const comment = comments[i]
            addComment(comment)
        }
        commentParent.scrollTop = commentParent.scrollHeight
    }

    afterDateSubmit() {
        utils.setVisibility('eventeditordateadderform', 'none')
        eventeditor.resetDateAdder()
        eventeditor.activateDateAdder()
        eventeditor.updateOverlappingDates()
    }

    async addDate(event, next) {
        const data = new FormData(event.form)
        data.append('eventId', this.eventId)
        const formJSON = Object.fromEntries(data.entries())
        const result = await window.services.post(`/api/vote/date/`, formJSON)
        if (result.target.status == 200) {
            next()
        }
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
        const result = await window.services.post(target, params)
        if (result.target.status == 200) {
            commentfield.value = ''
            this.updateComments()
        }
        commentfield.disabled = false
    }

    close() {
        state.set('current', 'frontpage')
        utils.setVisibility('dateadder', 'none')
        utils.setVisibility('eventeditordateadderform', 'none')
        this.resetDateAdder()
        toggleSite('eventeditor')
        setBlocker(false)
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
        const wrapper = (params, event) => {
            this.inviteUser(params.name)
            event.target.disabled = true
            event.target.innerHTML = 'Invited!'
        }
        const listObject = (params, next) => {
            return listCreator(params, 'Invite', next)
        }
        e.disabled = true
        e.value = ''
        const result = await window.services.get('/api/user/find/?search='+this.usertofind)
        e.disabled = false
        listResults(result.target.response, 'eventeditorinvitelist', listObject, wrapper)
    }

    async updateOverlappingDates() {
        const targetDiv = document.getElementById('eventeditor-overlappingdates')
        targetDiv.innerHTML = ''
        const result = await window.services.get(`/api/vote/date/union/${this.eventId}`)
        if (result.target.status == 200) {
            const dates = JSON.parse(result.target.response).slice(0, 5)
            if (dates.length == 0) {
                targetDiv.innerHTML = '<tr></tr><tr><td>No dates added yet</td></tr>'
                return
            }
            const usersMax = dates[0].overlapMax
            const maxParticipantsSpan = await utils.setVisibility('eventeditor-maxparticipants', 'block')
            maxParticipantsSpan.innerHTML = 'Max participants: ' + usersMax

            const hourGrid = document.createElement('div')
            hourGrid.className = 'hour-grid'
            targetDiv.appendChild(hourGrid)

            const tr = document.createElement('tr')
            const td = document.createElement('td')
            const td2 = document.createElement('td')
            const img = document.createElement('img')
            img.src = './styles/hours.png'
            td.className = 'date-field'
            td2.className = 'hour-field-header'
            td2.appendChild(img)
            tr.appendChild(td)
            tr.appendChild(td2)
            targetDiv.appendChild(tr)

            dates.forEach((date) => {
                const tr = document.createElement('tr')
                const dateField = document.createElement('td')
                const hourField = document.createElement('td')
                
                dateField.innerHTML = this.dateString(date.date, 2)
                dateField.className = 'date-field'

                hourField.className = 'hour-field'

                const canvas = document.createElement('canvas')
                canvas.width = 24
                canvas.height = 1
                canvas.className = 'pixelart'

                const ctx = canvas.getContext('2d')
                ctx.fillStyle = `rgb(0, 0, 164)`
                ctx.fillRect(0, 0, 24, 1)
                date.hours.forEach((hourObj) => {
                    const hour = hourObj.hour
                    const colorCoeff = (hourObj.users / usersMax)
                    const color = `rgb(${0}, ${colorCoeff * 245}, ${-colorCoeff * 164 + 164})`
                    ctx.fillStyle = color
                    ctx.fillRect(hour, 0, 1, 1)
                })


                hourField.appendChild(canvas)
                tr.appendChild(dateField)
                tr.appendChild(hourField)
                targetDiv.appendChild(tr)
            })
        }
    }

    async update() {
        if (!this.initiated) {
            this.init()
        }
        this.div = await utils.setVisibility('eventeditor', 'none')

        const previousEventId = this.eventid
        this.eventId = window.state.get('eventid')
        if (previousEventId != this.eventid) {
            this.clearComments()
        }
        const res = await window.services.get('/api/event/' + this.eventId)
        if (res.target.status !== 200) {

            return
        }
        window.setBlocker(true)

        this.updateComments()

        this.updateOverlappingDates()

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
        this.readyForUpdate = false
        document.getElementById('eventupdatebutton').disabled = true
        utils.setInnerHTML('eventeditorinvitelist', '')
        utils.setInnerHTML('eventeditortitle', eventInfo.title)
        utils.setInnerHTML('eventdescription', eventInfo.description)
        utils.setValue('eventdescriptioneditor', eventInfo.description)
        utils.setInnerHTML('eventenddate', this.dateString(eventInfo.timeout, 3))
        this.endDate = eventInfo.timeout

        utils.setInnerHTML('eventparticipants', responseBody.participants.join(', '))

        if (responseBody.owner === window.login.getUser()) {
            utils.setVisibility('eventeditoradminpanel', 'grid')
        } else {
            utils.setVisibility('eventeditoradminpanel', 'none')
        }
        utils.setVisibility('eventeditorgamelabel', 'none')
        utils.setVisibility('eventeditorgameitem', 'none')
        utils.setVisibility('eventeditor', 'block')
        utils.setVisibility('overlapping-games', 'block')
        utils.setVisibility('votepanelgameadder', 'block')
        if (eventInfo.gameId != -1) {
            utils.setVisibility('votepanelgameadder', 'none')
            utils.setVisibility('overlapping-games', 'none')
            utils.setVisibility('eventeditorgamelabel', 'inherit')
            utils.setVisibility('eventeditorgameitem', 'inherit')
            utils.setInnerHTML('eventeditorgameitem', '<i>fetching..</i>')
            const gameRes = await window.services.get('/api/game/' + eventInfo.gameId)
            if (gameRes.target.status == 200) {
                const gameInfo = JSON.parse(gameRes.target.response)
                utils.setInnerHTML('eventeditorgameitem', `<a target='_blank' href='https://www.igdb.com/games/${gameInfo.slug}/'>${gameInfo.name}</a>`)
            } else {
                utils.setVisibility('eventeditorgamelabel', 'none')
                utils.setVisibility('eventeditorgameitem', 'none')        
            }
        }
    }
}