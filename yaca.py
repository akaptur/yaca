from flask import Flask, render_template
from flask_sockets import Sockets
import time

app = Flask(__name__)
app.debug = True
sockets = Sockets(app)
app.messages = []

@sockets.route('/echo')
def echo(sock):
    while True:
        msg = sock.receive()
        print msg
        sock.send(msg[::-1])

@sockets.route('/chat')
def chat(sock):
    while True:
        msg = sock.receive()
        time.sleep(10)
        app.messages.append(msg)
        sock.send("".join([msg + "<br>" for msg in app.messages]))

@app.route('/')
def home():
    """ Hitting / invokes the socket method in /echo,
    because that's where the web socket created in echo.html
    is pointing."""
    return render_template('echo.html')

@app.route('/chatter')
def chatter():
    return render_template('chat.html', messages = app.messages)

if __name__ == '__main__':
    print "You must run the app with gevent for socket support"
    app.run(debug = True)
