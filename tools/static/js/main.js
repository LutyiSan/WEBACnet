const base_url = 'http://127.0.0.1:90/'
const http_get = new XMLHttpRequest();
var hostIP = ''
var port = 47808


function print(anytext){
    console.log(anytext);
}

function select(selector){
    return document.querySelector(selector)
}

function selectAll(selector){
    return document.querySelectorAll(selector)
}

function validateIP(ip){
    return /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ip);
}

function validateDigitInRange(digit, min, max){
    return min <= digit && digit <= max;
}

function validateWhois(){
    hostIP = select('#enter select[name="action-type"]').value
    port = select('#enter input[name="port"]').value
    if (port === ''){
        port = 47808
        select('#enter input[name="port"]').value = port
    }
    if (validateIP(hostIP) === true){
        select('#enter select[name="action-type"]').style.color = ("#00ff00");
            if (validateDigitInRange(port,1,65535) === true){
                select('#enter input[name="port"]').style.color = ("#00ff00");
                return true
            }else{
                select('#enter input[name="port"]').value = 0;
                select('#enter input[name="port"]').style.color = ("#ff0000");
                return false
            }
    }else{
        select('#enter select[name="action-type"]').value = ("invalid HOST-IP address!");
        select('#enter select[name="action-type"]').style.color = ("#ff0000");
        return false
    }
}

function colorObject(elements){
    selectAll(elements).forEach(elem =>{
        elem.style.color = ('#b6daff');  
    })
}







function deviceSelect(){
    selectAll('.device').forEach(item => {
        item.addEventListener('click', event => {
        print(item);
        colorObject('.device');
        let deviceData = item.innerText;
        let params = 'objectlist?device='+deviceData+'&host-ip='+hostIP+'&port='+port;
        print(params);
        item.style.color = ('#00ff00');
        http_get.open("GET", base_url+params);
        http_get.responseType = 'text';
        http_get.onload  = function() {
        let dataArray = http_get.response;
        
        select('#objectlist').innerHTML = dataArray;
        objectSelect();
        };
    http_get.send();          
    })
    })
}

function objectSelect(){
    selectAll('.object').forEach(item => {
        item.addEventListener('click', event => {
        colorObject('.object');
        let objectData = item.innerText;
        let params = 'object?object='+objectData+'&host-ip='+hostIP+'&port='+port;
        print(params);
        item.style.color = ('#00ff00');
        http_get.open("GET", base_url+params);
        http_get.responseType = 'text';
        http_get.onload  = function() {
        let dataArray = http_get.response;
        
        select('#objectprops').innerHTML = dataArray;
        propertySelect();
        };
    http_get.send();          
    })
    })
}



function propertySelect(){
    selectAll('.property').forEach(item => {
        item.addEventListener('click', event => {
            colorObject('.property');
        print('PROPERTY to read');
        let objectData = item.innerText;
        let params = 'property?property='+objectData+'&host-ip='+hostIP+'&port='+port;
        print(params);
        item.style.color = ('#00ff00');
        http_get.open("GET", base_url+params);
        http_get.responseType = 'text';
        http_get.onload  = function() {
        let dataArray = http_get.response;
        print(dataArray);
        
        select('#props').innerHTML = dataArray;
        };
    http_get.send();
    })
    })
}


select('#whois').addEventListener("click", function(){
    if (validateWhois() === true){
        let params = 'whois?host-ip='+select('#enter select[name="action-type"]').value+'&port='+port;
        print(params+' port: '+port);
        http_get.open("GET", base_url+params);
        http_get.responseType = 'text';
        http_get.onload  = function() {
        let innerData = '<ol>I AM List<br>'
        let dataArray = http_get.response;
        innerData += (dataArray+'</ol>');
        print(innerData);
        print(select('#wi-out'));
        select('#wi-out').innerHTML = dataArray;
        deviceSelect();
        };
    http_get.send();
}})

