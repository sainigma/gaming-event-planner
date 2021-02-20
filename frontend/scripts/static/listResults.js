export const listResults = async(res, target, label, next) => {
    let targetUL = document.getElementById(target)
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
        button.innerHTML = label
        button.onclick = () => {
            next(element)
        }
    });
}