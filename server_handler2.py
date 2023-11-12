import pyperclip
from flask_socketio import SocketIO
from flask import Flask, request, render_template, make_response, send_from_directory, jsonify, send_file
import os
from pathlib import Path
import platform

app = Flask(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
MAX_CONTENT_LENGTH = 1024 * 1024 * 1024
socketio = SocketIO(app)

BASE_DIR = Path(__file__).resolve().parent

def copy_file_to_clipboard(file_path):
    if platform.system() == 'Darwin':
        os.system(f"""osascript -e 'tell application "Finder"' -e 'activate' -e 'select ("{file_path}" as POSIX file)' -e 'tell application "System Events" to keystroke "c" using command down' -e 'delay 0.5' -e 'close front window' -e ''end tell """)
    else:
        os.system(f'powershell Set-Clipboard -Path \'{file_path}\'')

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/index.html')
def index():
    return render_template('index.html')


def return_file(name):
    response = make_response(
        # send_from_directory('static', filename=f'static/{name}'))
        send_from_directory('static', filename=f'static/{name}', path=f'static/{name}'))
    response.headers['Content-Type'] = 'application/javascript'
    return response


@app.route('/service-worker.js')
def sw():
    return send_file('static/service-worker.js')


@app.route('/precache-manifest.js')
def precache():
    return send_file('static/precache-manifest.js')


@app.route('/manifest.json')
def manifest():
    return send_file('static/manifest.json')


@app.route('/update', methods=['POST', 'GET'])
def send_clipboard(data=None):
    return jsonify({'clipboard': read_clipboard()})

@app.route('/file-upload', methods=['POST'])
def file_upload(data=None):
    file = request.files['file']
    parent = BASE_DIR / 'tmp'
    if not os.path.exists(parent):
        os.makedirs(parent)

    file.save(parent / file.filename)
    copy_file_to_clipboard(parent / file.filename)
    return jsonify({'status': 'ok'})


@socketio.on('text-copy')
def handle_message(data):
    container = data['container']
    if isinstance(container, str) and container != '':
        pyperclip.copy(container)
        socketio.emit('new-value', {'clipboard': read_clipboard()})


def send_new_clipboard(value):
    socketio.emit('new-value', {'clipboard': read_clipboard()})


def read_clipboard():
    return pyperclip.paste()


def get_ip():
    return


if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', '8000')
