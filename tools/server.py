from flask import Flask, render_template
from route_func import who_is, get_object_list, get_object_props

app = Flask(__name__)


@app.route('/')
def enter():
    return render_template('index.html')


@app.route('/whois')
def whois():
    return who_is()


@app.route('/objectlist')
def object_list():
    return get_object_list()


@app.route('/object')
def object_props():
    print('IN route props')
    return get_object_props()


app.run(host='127.0.0.1', port=90, debug=True)
