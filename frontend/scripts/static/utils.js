export default class Utils {
    constructor() {}

    setInnerHTML(target, content) {
        const element = document.getElementById(target)
        if (element) {
            element.innerHTML = content
            return element
        }
        return false
    }

    setValue(target, value) {
        const element = document.getElementById(target)
        if (element) {
            element.value = value
            return element
        }

    }

    setVisibility(target, tag) {
        const element = document.getElementById(target)
        element.style.display = tag
        return element
    }
}
