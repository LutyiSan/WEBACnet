# WEBACnet
  This programm implemented BACnet browsing in your browser
  Tested in Windows-10 and Debian-11
# Instalation
  1. cd /opt
  2. git clone https://github.com/LutyiSan/WEBACnet
  3. cd WEBACnet
  4. sudo sh install.sh
# Configuration
   1. Open file WEBACnet/tool/env.py and choice IP and PORT for server, if you need
   2. Open file WEBACnet/tool/static/js/main.js and asign "const base_url = {serverhost}:{serverport}
# Run
  1. Var.1 - pyton3 /opt/WEBACnet/tool/main.py
  2. Var.2 - sudo sh /opt/WEBACnet/run.sh
# Usage
  Open your browser {host}:{port} and enjoy simply usage)
# Dependences
  1. python-3.8 and later
  2. python-lib [loguru~=0.6.0,
                  Flask~=2.2.2,
                  netifaces~=0.11.0,
                    BAC0~=22.9.21]


  
