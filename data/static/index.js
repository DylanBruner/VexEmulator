function addDeviceToList(deviceType, deviceName, deviceId){
    document.getElementById('devices').innerHTML += `<div class='device' id='${deviceType}::${deviceName}(${deviceId})'></div>`
    document.getElementById(`${deviceType}::${deviceName}(${deviceId})`).innerHTML += `<h1>${deviceName}</h1>`
    document.getElementById(`${deviceType}::${deviceName}(${deviceId})`).innerHTML += `<a>Device Type: ${deviceType}</a>`
    document.getElementById(`${deviceType}::${deviceName}(${deviceId})`).innerHTML += `<a>Device ID: ${deviceId}</a>`
    document.getElementById(`${deviceType}::${deviceName}(${deviceId})`).innerHTML += '<span class="attributes"></span>'
}

function generateDeviceAttributes(elementId, deviceId){
    //Make a fetch request to /api/device/attributes/{deviceId}
    //The response will be json
    fetch (`/api/device/attributes/${deviceId}`).then(response => response.json()).then(data => {
        ChildElement = document.getElementById(elementId).children
        TargetSpan   = null;
        for (let i = 0; i < ChildElement.length; i++) {
            if (ChildElement[i].tagName == 'SPAN'){
                ChildElement[i].innerHTML = '<h1>Attributes</h1>'
                TargetSpan = ChildElement[i]
            }
        }

        dataKeys = Object.keys(data)
        for (let i = 0; i < dataKeys.length; i++) {
            attributeData = data[dataKeys[i]];
            if (attributeData['type'] == 'bool')
            {TargetSpan.innerHTML += `<attribute id="${dataKeys[i]}" vartype="bool"><a>${dataKeys[i]}</a><input type="checkbox" value="${attributeData['value']}"></input></attribute>`}
            else if (attributeData['type'] == 'int')
            {TargetSpan.innerHTML += `<attribute id="${dataKeys[i]}" vartype="int"><a>${dataKeys[i]}</a><input type="number" value="${attributeData['value']}"></input></attribute>`}
            else if (attributeData['type'] == 'float')
            {TargetSpan.innerHTML += `<attribute id="${dataKeys[i]}" vartype="float"><a>${dataKeys[i]}</a><input type="number" value="${attributeData['value']}"></input></attribute>`}
            else if (attributeData['type'] == 'string')
            {TargetSpan.innerHTML += `<attribute id="${dataKeys[i]}" vartype="string"><a>${dataKeys[i]}</a><input type="text" value="${attributeData['value']}"></input></attribute>`}
        }

        TargetSpan.innerHTML += `<button onclick="updateDeviceAttributes('${elementId}', '${deviceId}')">Update</button>`
    });

}
function loadDevicesFromServer(){
    //Make a fetch request to /api/devices
    //The response will be json
    fetch ('/api/devices').then(response => response.json()).then(data => {
        devices = data['devices']
        for (let i = 0; i < devices.length; i++) {
            addDeviceToList(devices[i]['type'], devices[i]['name'], devices[i]['id'])
            generateDeviceAttributes(`${devices[i]['type']}::${devices[i]['name']}(${devices[i]['id']})`, devices[i]['id'])
        }
    });
}

function updateDeviceAttributes(elementId, deviceId){
    ChildElements = document.getElementById(elementId).children
    TargetSpan   = null;
    //Get the target span
    for (let i = 0; i < ChildElements.length; i++) {if (ChildElements[i].tagName == 'SPAN'){TargetSpan = ChildElements[i]}}
    SpanChildren = TargetSpan.children
    //Get the attributes
    for (let i = 0; i < SpanChildren.length; i++) {
        if (SpanChildren[i].tagName == 'ATTRIBUTE'){
            AttributeId    = SpanChildren[i].id 
            AttributeType  = SpanChildren[i].outerHTML.split('vartype="')[1].split('"')[0]
            if (AttributeType == 'bool'){AttributeValue = SpanChildren[i].children[1].checked}
            else {AttributeValue = SpanChildren[i].children[1].value}

            fetch(`/api/device/setattribute/${deviceId}/${AttributeId}/${AttributeValue}`)
        }
    }
}

loadDevicesFromServer()