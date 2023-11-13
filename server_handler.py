from fastapi import FastAPI, WebSocket, UploadFile, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, HTMLResponse

import pyperclip
import os
from pathlib import Path
import platform
import json
import shutil

TEMP_FILE_UPLOAD_PATH = ''
app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent


def copy_file_to_clipboard(file_path):
    if platform.system() == 'Darwin':
        os.system(f"""osascript -e 'tell application "Finder"' -e 'activate' -e 'select ("{file_path}" as POSIX file)' -e 'tell application "System Events" to keystroke "c" using command down' -e 'delay 0.5' -e 'close front window' -e ''end tell """)
    else:
        os.system(f'powershell Set-Clipboard -Path \'{file_path}\'')


@app.get('/')
async def index():
    # some rels did not work with FileResponse, so...
    with open('templates/index.html', 'r') as f:
        html = f.read()
    
    return HTMLResponse(html)


@app.get('/service-worker.js')
async def service_worker():
    return FileResponse('static/service-worker.js')


@app.get('/precache-manifest.js')
async def precache():
    return FileResponse('static/precache-manifest.js')

@app.get('/static/{f}')
async def static(f: str):
    return FileResponse(f'static/{f}')


@app.get('/manifest.json')
async def manifest():
    return FileResponse('static/manifest.json')


@app.get('/update')
async def send_clipboard(data=None):
    return JSONResponse({'clipboard': read_clipboard()})


@app.post('/download')
async def download(request: Request):
    try:
        if TEMP_FILE_UPLOAD_PATH == '':
            raise Exception('Path is empty')
        
        filename = os.path.basename(TEMP_FILE_UPLOAD_PATH)
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        return FileResponse(TEMP_FILE_UPLOAD_PATH, headers=headers)
    except Exception as e:
        print(e)
        return RedirectResponse('/')


@app.post('/file-upload')
async def file_upload(file: UploadFile):
    parent = BASE_DIR / 'tmp'
    if not os.path.exists(parent):
        os.makedirs(parent)

    with open(parent / file.filename, 'wb') as f:
        shutil.copyfileobj(file.file, f)

    copy_file_to_clipboard(parent / file.filename)

    return JSONResponse({'status': 'ok'})


async def text_copy(payload, websocket: WebSocket):
    container = payload['container']
    if isinstance(container, str) and container != '':
        pyperclip.copy(container)
        await websocket.send_json({
            'function': 'new-value',
            'payload': {
                'clipboard': read_clipboard()
            }
        })


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    functions = {
        'text-copy': text_copy
    }

    while True:
        try:
            data = await websocket.receive_text()
            data = json.loads(data)
            function = data['function']
            await functions[function](data['payload'], websocket)
        except Exception as e:
            print(e)


def read_clipboard():
    return pyperclip.paste()
