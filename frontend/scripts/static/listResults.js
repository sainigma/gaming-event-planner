export const buttonCreator = (element, next) => {
    const button = document.createElement('button')
    button.className = 'button-expands'
    button.innerHTML = `${element.name} <span>select</span>`
    button.onclick = (event) => {
        next(element, next)
    }
    return button
}

export const listCreator = (element, buttonlabel, next) => {
    const li = document.createElement('li')
    const title = document.createElement('span')
    const button = document.createElement('button')
    li.appendChild(title)
    li.appendChild(button)
    title.innerHTML = element.name
    button.innerHTML = buttonlabel
    button.onclick = (event) => {
        next(element, event)
    }
    return li
}

export const listResults = async(res, target, contentGenerator, next) => {
    let targetElement = document.getElementById(target)
    targetElement.innerHTML = ''
    const arr = await JSON.parse(res)
    arr.forEach(element => {
        const child = contentGenerator(element, next)
        targetElement.appendChild(child)
    });
}