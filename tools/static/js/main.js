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
    hostIP = select('#enter input[name="host-ip"]').value
    port = select('#enter input[name="port"]').value
    if (port === ''){
        port = 47808
    }
    if (validateIP(hostIP) === true){
        select('#enter input[name="host-ip"]').style.color = ("#00ff00");
            if (validateDigitInRange(port,1,65535) === true){
                select('#enter input[name="port"]').style.color = ("#00ff00");
                return true
            }else{
                select('#enter input[name="port"]').value = 0;
                select('#enter input[name="port"]').style.color = ("#ff0000");
                return false
            }
    }else{
        select('#enter input[name="host-ip"]').value = ("invalid HOST-IP address!");
        select('#enter input[name="host-ip"]').style.color = ("#ff0000");
        return false
    }
}

function deviceSelect(){
    selectAll('.device').forEach(item => {
        item.addEventListener('click', event => {
        let deviceData = item.innerText;
        
        if (port === ''){
            port = 47808
       }
        let params = 'objectlist?device='+deviceData+'&host-ip='+hostIP+'&port='+port;
        print(params);
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
        let objectData = item.innerText;
        
        if (port === ''){
            port = 47808
       }
        let params = 'object?object='+objectData+'&host-ip='+hostIP+'&port='+port;
        print(params);
        http_get.open("GET", base_url+params);
        http_get.responseType = 'text';
        http_get.onload  = function() {
        let dataArray = http_get.response;
        select('#objectprops').innerHTML = dataArray;
        
        };
    http_get.send();          
    })
    })
}














select('#whois').addEventListener("click", function(){
    if (validateWhois() === true){
        port = select('#enter input[name="port"]').value
        if (port === ''){
            port = 47808
       }
        let params = 'whois?host-ip='+select('#enter input[name="host-ip"]').value+'&port='+port;
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

