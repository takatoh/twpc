from bottle import route, run


@route('/hello')
def hello():
    return 'Hello, World!'


def run_server():
    run(host='localhost', port=8080, debug=True)
