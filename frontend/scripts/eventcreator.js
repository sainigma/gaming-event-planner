export default class EventCreator{
    constructor() {
        this.name = ''
        this.game = ''
        this.gameId = -1
        this.groupId = -1
        window.eventcreator = this
    }

    async saveEvent() {
        const eventstatus = document.getElementById('eventcreationstatus')
        const savebutton = document.getElementById('eventsavebutton')
        const groups = document.getElementById('eventusergroups')
        savebutton.disabled = true

        const groupId = await groups.value

        const target = '/api/event/new'
        const params = {
            name:this.name,
            gameId:this.gameId,
            groupId:groupId
        }
        const result = await window.services.post(target, params)
        if (result.target.status == 200) {
            this.cancel()
            window.clearEvents()
            await window.listEvents()
            window.setBlocker(false)
            window.render()
        } else {
            savebutton.disabled = false
            eventstatus.innerHTML = 'creation failed'
        }
    }

    setName(e) {
        this.name = e
        const savebutton = document.getElementById('eventsavebutton')
        if (this.name.length > 3) {
            savebutton.disabled = false
        } else {
            savebutton.disabled = true
        }
    }

    setSearch(e) {
        this.game = e
    }

    showDiv(tag, state) {
        const div = document.getElementById(tag)
        if (div != null) {
            div.style.display = state ? 'block' : 'none'
        }
    }

    initForm() {
        window.setBlocker(true)
        
        this.showDiv('eventtypeselector', true)
        this.showDiv('eventgameselector', false)
        this.showDiv('eventfinalform', false)
        
        this.game = ''
        this.gameId = -1
        this.name = ''

        const nameInput = document.getElementById('eventnameinput')
        if (nameInput != null) {
            nameInput.value = ''
        }

        const savebutton = document.getElementById('eventsavebutton')
        if (savebutton != null) {
            savebutton.disabled = true
        }

        const status = document.getElementById('eventcreationstatus')
        if (status != null) {
            status.innerHTML = ''
        }
    }

    showFinalForm() {
        const addGroupOption = (label, id) => {
            const option = document.createElement('option')
            option.value = id
            option.innerHTML = label
            groups.appendChild(option)
        }
        const groups = document.getElementById('eventusergroups')
        groups.innerHTML = ''
        addGroupOption('friends', -1)

        const gametitle = document.getElementById('eventgametitle')
        gametitle.innerHTML = this.game
        this.showDiv('eventfinalform', true)
    }

    setGame(title, id) {
        this.game = title
        this.gameId = id
        
        this.showDiv('eventtypeselector', false)
        this.showDiv('eventgameselector', false)

        this.showFinalForm()
    }

    setGameOriented(status) {
        this.showDiv('eventtypeselector', false)
        if (status) {
            this.showDiv('eventgameselector', true)
        } else {
            this.game = 'user vote'
            this.showFinalForm()
        }
    }

    cancel() {
        let targetUL = document.getElementById('eventcreatorgamepicker')
        targetUL.innerHTML = ''
        this.game = ''
        this.gameId = -1
        window.toggleSite('eventcreator')
    }

    async listResults(res) {
        let targetUL = document.getElementById('eventcreatorgamepicker')
        targetUL.innerHTML = ''
        const arr = await JSON.parse(res)
        console.log(arr)
        arr.forEach(element => {
            const li = document.createElement('li')
            const title = document.createElement('span')
            const button = document.createElement('button')
            li.appendChild(title)
            li.appendChild(button)
            targetUL.appendChild(li)
            title.innerHTML = element.name
            button.innerHTML = 'Select'
            button.onclick = () => {
                this.setGame(element.name, element.id)
            }
            console.log(element)
        });
    }

    async searchGame(e) {
        e.disabled = true
        e.value = ''
        const result = await window.services.get('/api/game/find/'+this.game)
        e.disabled = false
        this.listResults(result.target.response)
    }
}
