function onLoad() {
    loadFuckingFavicon()
    loadThemesDropDown()
}

function loadThemesDropDown() {
    $.ajax("/request/themes",).done(function (data) {
        data.forEach(data => {
            const element = createDropdownElement(data);
            $("#themeSelector").prepend(element);
        })
    })
}

function createDropdownElement(name) {
    const result = document.createElement("option");
    result.innerHTML = name
    result.value = name
    return result;
}

function loadFuckingFavicon() {
    fetch('/assets/favicon.png')
        .then(response => response.blob())
        .then(blob => new Promise((resolve, reject) => {
            const reader = new FileReader()
            reader.onloadend = () => resolve(reader.result)
            reader.onerror = reject
            reader.readAsDataURL(blob)
        })).then(dataUrl => {
        const docHead = document.getElementsByTagName('head')[0];
        const newLink = document.createElement('link');
        newLink.rel = 'shortcut icon';
        newLink.href = dataUrl.toString();
        docHead.appendChild(newLink);
    })
}

function replaceDemo() {
    const theme = $("#themeSelector option:selected").text()
    $("#demo").attr('src', "/request/demo?theme=" + theme)
}

onLoad()