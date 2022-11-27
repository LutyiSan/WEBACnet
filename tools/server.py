from flask import Flask, render_template
from route_func import who_is, get_object_list, get_object_props, read_select_properties
from env import *


def run_server(ips):
    app = Flask(__name__)
    interfaces = list()
    for i in ips:
        interfaces.append(i)
    print(interfaces)

    @app.route('/')
    def enter():
        return render_template('index_v2.html', interface=interfaces)

    @app.route('/whois')
    def whois():
        return who_is()

    @app.route('/objectlist')
    def object_list():
        return get_object_list()

    @app.route('/object')
    def object_props():
        return get_object_props()

    @app.route('/property')
    def read_props():
        return read_select_properties()

    app.run(host=SERVER_IP, port=SERVER_PORT, debug=False)
