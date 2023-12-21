// noinspection JSIgnoredPromiseFromCall,JSUnusedGlobalSymbols,JSUnresolvedVariable

function onLoad() {
    replaceLinkMarkers();
    loadFuckingFavicon();
    addListenersToInputs();
    loadThemes();
}

function loadThemes() {
    $.ajax("/request/themes").done(function (data) {
        data.forEach(data => {
            $("#demoThemeSelector").prepend(createDropdownElement(data));
            $("#numberThemeSelector").prepend(createDropdownElement(data));
            $("#imageThemeSelector").prepend(createDropdownElement(data));
        })
        $("#themes").text(function () {
            return JSON.stringify(data);
        })
    })
}

function createDropdownElement(name) {
    const result = document.createElement("option");
    result.innerHTML = name;
    result.value = name;
    return result;
}

function loadFuckingFavicon() {
    fetch('/assets/favicon.png')
        .then(response => response.blob())
        .then(blob => new Promise((resolve, reject) => {
            const reader = new FileReader()
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        })).then(dataUrl => {
            const docHead = document.getElementsByTagName('head')[0];
            const newLink = document.createElement('link');
            newLink.rel = 'shortcut icon';
            newLink.href = dataUrl.toString();
            docHead.appendChild(newLink);
        })
}

function replaceNumber() {
    const theme = $("#numberThemeSelector option:selected").text();
    const value = document.getElementById("numberValue").value;
    const max_length = document.getElementById("numberMaxLength").value
    const lead_zeros = $("#numberLeadZerosSelector option:selected").text();
    const smoothing = $("#numberSmoothingSelector option:selected").text();
    const hard = $("#numberHardSelector option:selected").text();
    $("#number").attr("src", `request/number?theme=${theme}&value=${value}&max_length=${max_length}&lead_zeros=${lead_zeros}&smoothing=${smoothing}&hard=${hard}`)
}

function replaceDemo() {
    const theme = $("#demoThemeSelector option:selected").text();
    const smoothing = $("#demoSmoothingSelector option:selected").text();
    const hard = $("#demoHardSelector option:selected").text();
    $("#demo").attr('src', `request/demo?theme=${theme}&smoothing=${smoothing}&hard=${hard}`);
}


function replaceLinkMarkers() {
    $(".this-href-mark").text(function (index, text) {
        return text.replace("{LINK}", window.location.href);
    })
}

function copy(source) {
    navigator.clipboard.writeText(window.location.href + source);
}

function copyDemoLink() {
    const theme = $("#demoThemeSelector option:selected").text();
    const smoothing = $("#demoSmoothingSelector option:selected").text();
    const hard = $("#demoHardSelector option:selected").text();
    copy(`request/demo?theme=${theme}&smoothing=${smoothing}&hard=${hard}`);
}

function copyThemesLink() {
    copy("request/themes");
}

function copyRegisterLink() {
    const key = document.getElementById("registerKey").value
    const password = document.getElementById("registerPassword").value
    const salt = document.getElementById("registerSalt").value
    copy(`request/take_key?key=${key}&password=${password}&salt=${salt}`);
}

function executeRegister() {
    const key = document.getElementById("registerKey").value
    const password = document.getElementById("registerPassword").value
    const salt = document.getElementById("registerSalt").value
    $.ajax({
        method: "POST", url: `request/take_key?key=${key}&password=${password}&salt=${salt}`,
        success: function (data) {
            $("#register").text(function () {
                return JSON.stringify(data);
            })
        }, error: function (data) {
            $("#register").text(function () {
                return JSON.stringify(data.responseJSON);
            })
        }
    })
}

function executeSet() {
    const key = document.getElementById("setKey").value;
    const value = document.getElementById("setValue").value;
    const password = document.getElementById("setPassword").value;
    const salt = document.getElementById("setSalt").value;
    $.ajax({
        method: "PUT", url: `request/set@${key}?password=${password}&salt=${salt}&value=${value}`,
        success: function (data) {
            $("#set").text(function () {
                return JSON.stringify(data);
            })
        }, error: function (data) {
            $("#set").text(function () {
                return JSON.stringify(data.responseJSON);
            })
        }
    })
}

function executeRecord() {
    const key = document.getElementById("recordKey").value;
    const do_inc = $("#recordDoIncSelector option:selected").text();
    $.ajax({
        method: "GET", url: `request/record@${key}?do_inc=${do_inc}`,
        success: function (data) {
            $("#record").text(function () {
                return JSON.stringify(data);
            })
        }, error: function (data) {
            $("#record").text(function () {
                return JSON.stringify(data.responseJSON);
            })
        }
    })
}

function copySetLink() {
    const key = document.getElementById("setKey").value;
    const value = document.getElementById("setValue").value;
    const password = document.getElementById("setPassword").value;
    const salt = document.getElementById("setKey").value;
    copy(`request/set@${key}?password=${password}&salt=${salt}&value=${value}`)
}

function copyRecordLink() {
    const key = document.getElementById("recordKey").value;
    const do_inc = $("#recordDoIncSelector option:selected").text();
    copy(`request/record@${key}?do_inc=${do_inc}`)
}

function executeImage() {
    const theme = $("#imageThemeSelector option:selected").text();
    const key = document.getElementById("imageKey").value;
    const max_length = document.getElementById("imageMaxLength").value
    const lead_zeros = $("#imageLeadZerosSelector option:selected").text();
    const smoothing = $("#imageSmoothingSelector option:selected").text();
    const do_inc = $("#imageDoIncSelector option:selected").text();
    const hard = $("#imageHardSelector option:selected").text();
    $("#image").attr("src", `request/image@${key}?theme=${theme}&max_length=${max_length}&lead_zeros=${lead_zeros}&smoothing=${smoothing}&do_inc=${do_inc}&hard=${hard}`)

}

function copyImageLink() {
    const theme = $("#imageThemeSelector option:selected").text();
    const key = document.getElementById("imageKey").value;
    const max_length = document.getElementById("imageMaxLength").value
    const lead_zeros = $("#imageLeadZerosSelector option:selected").text();
    const smoothing = $("#imageSmoothingSelector option:selected").text();
    const do_inc = $("#imageDoIncSelector option:selected").text();
    const hard = $("#imageHardSelector option:selected").text();
    copy(`request/image@${key}?theme=${theme}&max_length=${max_length}&lead_zeros=${lead_zeros}&smoothing=${smoothing}&do_inc=${do_inc}&hard=${hard}`);
}

function copyDeleteLink() {
    const key = document.getElementById("deleteKey").value
    const password = document.getElementById("deletePassword").value
    const salt = document.getElementById("deleteSalt").value
    copy(`request/revoke_key?key=${key}&password=${password}&salt=${salt}`);
}

function executeDelete() {
    const key = document.getElementById("deleteKey").value
    const password = document.getElementById("deletePassword").value
    const salt = document.getElementById("deleteSalt").value
    $.ajax({
        method: "DELETE", url: `request/revoke_key?key=${key}&password=${password}&salt=${salt}`,
        success: function (data) {
            $("#delete").text(function () {
                return JSON.stringify(data);
            })
        }, error: function (data) {
            $("#delete").text(function () {
                return JSON.stringify(data.responseJSON);
            })
        }
    })
}

function addListenersToInputs() {
    document.getElementById("numberValue").addEventListener('change', replaceNumber);
    document.getElementById("numberMaxLength").addEventListener('change', replaceNumber);
}

function copyNumberLink() {
    const theme = $("#numberThemeSelector option:selected").text();
    const value = document.getElementById("numberValue").value;
    const max_length = document.getElementById("numberMaxLength").value
    const lead_zeros = $("#numberLeadZerosSelector option:selected").text();
    const smoothing = $("#numberSmoothingSelector option:selected").text();
    const hard = $("#numberHardSelector option:selected").text();
    copy(`request/number?theme=${theme}&value=${value}&max_length=${max_length}&lead_zeros=${lead_zeros}&smoothing=${smoothing}&hard=${hard}`);
}

onLoad()
