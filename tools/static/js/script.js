const base_url = 'http://127.0.0.1:90/protocol/'
const http_get = new XMLHttpRequest();


function select(selector){
    return document.querySelector(selector)
}

function validateIP(ip){
    return /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ip);

}

function validateDigitInRange(digit, min, max){
    return min <= digit && digit <= max;
}

function validateModbus(){
    let ip = select('#modbus-read input[name="device-ip"]').value
    let port = select('#modbus-read input[name="port"]').value
    if (port === ''){
        port = '502'
    }
      console.log(port);
    let address = select('#modbus-read input[name="instance"]').value
    let quantity = select('#modbus-read input[name="quantity"]').value
    if (validateIP(ip) === true){
        select('#modbus-read input[name="device-ip"]').style.color = ("#00ff00"); 
        if (validateDigitInRange(port,1,65535)){
            select('#modbus-read input[name="port"]').style.color = ("#00ff00"); 
            if (validateDigitInRange(address,1,65535) === true){
                select('#modbus-read input[name="instance"]').style.color = ("#00ff00"); 
                if (validateDigitInRange(quantity,1,125) === true){
                    select('#modbus-read input[name="quantity"]').style.color = ("#00ff00"); 
                    return true
                }else{
                    select('#modbus-read input[name="quantity"]').value = 0;
                    select('#modbus-read input[name="quantity"]').style.color = ("#ff0000"); 
                    return false
                }
            }else{
                select('#modbus-read input[name="instance"]').value = 0;
                select('#modbus-read input[name="instance"]').style.color = ("#ff0000"); 
                return false
            }
        }else{
            select('#modbus-read input[name="port"]').value = 0; 
            select('#modbus-read input[name="port"]').style.color = ("#ff0000"); 
            return false
        }  
    }else{
        select('#modbus-read input[name="device-ip"]').value = ("invalid IP address!"); 
        select('#modbus-read input[name="device-ip"]').style.color = ("#ff0000"); 
        return false
    }
}

function validateBacnetRead(){
    let host_ip = select('#bacnet-read input[name="host-ip"]').value
    let device_ip = select('#bacnet-read input[name="device-ip"]').value
    let bport = select('#bacnet-read input[name="port"]').value
    if (bport === ''){
        bport = 47808
    }
    let baddress = select('#bacnet-read input[name="instance"]').value
    console.log(host_ip, device_ip, bport, baddress)
    if (validateIP(host_ip) === true){
        select('#bacnet-read input[name="host-ip"]').style.color = ("#00ff00"); 
        if (validateIP(device_ip)=== true){
            select('#bacnet-read input[name="device-ip"]').style.color = ("#00ff00"); 
            if (validateDigitInRange(bport,1,65535) === true){
                select('#bacnet-read input[name="port"]').style.color = ("#00ff00");
                if (validateDigitInRange(baddress,1,4194303) === true){
                    select('#bacnet-read input[name="instance"]').style.color = ("#00ff00");  
                    return true
                }else{
                    select('#bacnet-read input[name="instance"]').value = 0; 
                    select('#bacnet-read input[name="instance"]').style.color = ("#ff0000");  
                    return false
                }
            }else{
                select('#bacnet-read input[name="port"]').value = 0; 
                select('#bacnet-read input[name="port"]').style.color = ("#ff0000");  
                return false
            }
        }else{
            select('#bacnet-read input[name="device-ip"]').value = ("invalid Device-IP address!"); 
            select('#bacnet-read input[name="device-ip"]').style.color = ("#ff0000"); 
            return false
        }  
    }else{
        select('#bacnet-read input[name="host-ip"]').value = ("invalid HOST-IP address!"); 
        select('#bacnet-read input[name="host-ip"]').style.color = ("#ff0000"); 
        return false
    }
}

function validateBacnetGetList(){
    let host_ip = select('#bacnet-object-list input[name="host-ip"]').value
    let device_ip = select('#bacnet-object-list input[name="device-ip"]').value
    let bport = select('#bacnet-object-list input[name="port"]').value
    if (bport === ''){
        bport = 47808
    }
    let baddress = select('#bacnet-object-list input[name="instance"]').value
    console.log(host_ip, device_ip, bport, baddress)
    if (validateIP(host_ip) === true){
        select('#bacnet-object-list input[name="host-ip"]').style.color = ("#00ff00"); 
        if (validateIP(device_ip)=== true){
            select('#bacnet-object-list input[name="device-ip"]').style.color = ("#00ff00");
            if (validateDigitInRange(bport,1,65535) === true){
                select('#bacnet-object-list input[name="port"]').style.color = ("#00ff00");
                if (validateDigitInRange(baddress,1,4194303) === true){
                    select('#bacnet-object-list input[name="instance"]').style.color = ("#00ff00");
                    return true
                }else{
                    select('#bacnet-object-list input[name="instance"]').value = 0; 
                    select('#bacnet-object-list input[name="instance"]').style.color = ("#ff0000");
                    return false
                }
            }else{
                select('#bacnet-object-list input[name="port"]').value = 0; 
                select('#bacnet-object-list input[name="port"]').style.color = ("#ff0000");
                return false
            }
       }else{
            select('#bacnet-object-list input[name="device-ip"]').value = ("invalid Device-IP address!"); 
            select('#bacnet-object-list input[name="device-ip"]').style.color = ("#ff0000");
            return false
        }  
   }else{
        select('#bacnet-object-list input[name="host-ip"]').value = ("invalid HOST-IP address!"); 
        select('#bacnet-object-list input[name="host-ip"]').style.color = ("#ff0000"); 
        return false
    }
}

function validateWhois(){
    let host_ip = select('#bacnet-whois input[name="host-ip"]').value
    let bport = select('#bacnet-whois input[name="port"]').value
    if (bport === ''){
        bport = 47808
    }

    if (validateIP(host_ip) === true){
        select('#bacnet-whois input[name="host-ip"]').style.color = ("#00ff00");
            if (validateDigitInRange(bport,1,65535) === true){
                select('#bacnet-read input[name="port"]').style.color = ("#00ff00");
                return true
            }else{
                select('#bacnet-read input[name="port"]').value = 0;
                select('#bacnet-read input[name="port"]').style.color = ("#ff0000");
                return false
            }
    }else{
        select('#bacnet-read input[name="host-ip"]').value = ("invalid HOST-IP address!");
        select('#bacnet-read input[name="host-ip"]').style.color = ("#ff0000");
        return false
    }
}

select('#protocol-submit').addEventListener("click", function(){
    console.log(select('#start-form select').value)
    if (select('#start-form select').value === 'bacnet') {
        select('#bacnet-form').style.display = "block";
        select('#modbus-read').style.display = "none";
        select('#response-data').innerHTML = '';
    } else {
          select('#modbus-read').style.display = "block";
          select('#bacnet-form').style.display = "none";
          select('#bacnet-object-list').style.display = "none";
          select('#bacnet-read').style.display = "none";
          select('#bacnet-whois').style.display = "none";
          select('#response-data').innerHTML = '';

      }
    }
)

select('#bacnet-submit').addEventListener("click", function(){
    if (select('#bacnet-form select').value === 'object-list') {
        select('#bacnet-object-list').style.display = "block";
        select('#modbus-read').style.display = "none";
        select('#bacnet-read').style.display = "none";
        select('#bacnet-whois').style.display = "none";
        select('#response-data').innerHTML = '';
    } else if (select('#bacnet-form select').value === 'read-property'){
          select('#bacnet-read').style.display = "block";
          select('#bacnet-object-list').style.display = "none";
          select('#bacnet-whois').style.display = "none";
          select('#modbus-read').style.display = "none";
          select('#bacnet-form #bacnet-submit').type = 'button';
          select('#response-data').innerHTML = '';
    } else{
        select('#bacnet-whois').style.display = "block";
        select('#bacnet-read').style.display = "none";
        select('#bacnet-object-list').style.display = "none";
        select('#modbus-read').style.display = "none";
        select('#response-data').innerHTML = '';
      }
    }
)

select('#modbus-read-submit').addEventListener('click', function(){
    select('#response-data').innerHTML = '';
    if (validateModbus() === true){
        let port = select('#modbus-read input[name="port"]').value
        if (port === ''){
          port = 502
        }
        let params = 'modbus/read?device-ip='+select('#modbus-read input[name="device-ip"]').value+
                  '&port='+port+
                    '&object-type='+select('#modbus-read select[name="object-type"]').value+
                      '&instance='+select('#modbus-read input[name="instance"]').value+
                        '&quantity='+select('#modbus-read input[name="quantity"]').value+
                        '&value-type='+select('#modbus-read select[name="value-type"]').value
        http_get.open("GET", base_url+params);
        http_get.responseType = 'text';
        http_get.onload  = function() {
            let inner_data = '<ol>Registers<br>'
            let data_array = http_get.response.split(',');
            data_array.forEach(element => {
            console.log(element);
            inner_data += '<li>'+element+'</li>' 
        });
        inner_data += '</ol>'
        select('#response-data').innerHTML = inner_data;
        };
      http_get.send();
}})

select('#bacnet-read-submit').addEventListener('click', function(){
    select('#response-data').innerHTML = '';
    if(validateBacnetRead() === true){
        let port = select('#bacnet-read input[name="port"]').value
        if (port === ''){
            port = 47808
         }
        let params = 'bacnet/read?host-ip='+select('#bacnet-read input[name="host-ip"]').value+
                '&device-ip='+select('#bacnet-read input[name="device-ip"]').value+
                '&port='+port+
                  '&object-type='+select('#bacnet-read select[name="object-type"]').value+
                    '&instance='+select('#bacnet-read input[name="instance"]').value
                     
        http_get.open("GET", base_url+params);
        http_get.responseType = 'text';
        http_get.onload  = function() {
        let inner_data = '<ol>Properties<br><li>'
        inner_data += http_get.response+'</li></ol>'
        select('#response-data').innerHTML = inner_data;
        };
        http_get.send();
}})

select('#obj-list-submit').addEventListener('click', function(){
    select('#response-data').innerHTML = '';
    if (validateBacnetGetList() === true){
        let port = select('#bacnet-object-list input[name="port"]').value
        if (port === ''){
            port = 47808
       }
        let params = 'bacnet/gol?host-ip='+select('#bacnet-object-list input[name="host-ip"]').value+
                '&device-ip='+select('#bacnet-object-list input[name="device-ip"]').value+
                '&port='+port+
                    '&instance='+select('#bacnet-object-list input[name="instance"]').value
                     
        http_get.open("GET", base_url+params);
        http_get.responseType = 'text';
        http_get.onload  = function() {
        let inner_data = '<ol>Object List<br>'
        let data_array = http_get.response.split(',');
        data_array.forEach(element => {
        console.log(element);
        inner_data += '<li>'+element+'</li>' 
    });
inner_data += '</ol>'
select('#response-data').innerHTML = inner_data;
};
http_get.send();
}})

select('#whois-submit').addEventListener('click', function(){
    select('#response-data').innerHTML = '';
    if (validateWhois() === true){
        let port = select('#bacnet-whois input[name="port"]').value
        if (port === ''){
            port = 47808
       }
        let params = 'bacnet/whois?host-ip='+select('#bacnet-whois input[name="host-ip"]').value+'&port='+port
        console.log(params)

        http_get.open("GET", base_url+params);
        http_get.responseType = 'text';
        http_get.onload  = function() {
        let inner_data = '<ol>I AM List<br>'
        let data_array = http_get.response.split(',');
        data_array.forEach(element => {
        console.log(element);
        inner_data += '<li>'+element+'</li>'
    });
inner_data += '</ol>'
select('#response-data').innerHTML = inner_data;
};
http_get.send();
}})

