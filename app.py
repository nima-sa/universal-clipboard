import asyncio
import uvicorn

import socket
import threading
import shutil

import json
import os

from ui_handler import UIApp
import server_handler
import tkinter.messagebox

async def server(host, port):
    config = uvicorn.Config(server_handler.app, host=host, port=port)
    await uvicorn.Server(config).serve()


def _send_new_clipboard():
    pass


def set_file_path_callback(path):
    print('here')
    server_handler.TEMP_FILE_UPLOAD_PATH = path


def quit():
    exit(0)


if __name__ == '__main__':
    try:

        if os.path.exists('tmp'):
            shutil.rmtree('./tmp', ignore_errors=True)

        if os.path.exists('configs.json'):
            with open('configs.json', 'r') as f:
                configs = json.load(f)
        else:
            configs = {}

        HOST = configs.get('ip', '0.0.0.0')
        PORT = configs.get('port', 8000)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr, _ = s.getsockname()
        s.close()
        print(ip_addr, PORT)

        socket_thread = threading.Thread(
            target=lambda: asyncio.run(server(HOST, PORT))
        )
        socket_thread.daemon = True
        socket_thread.start()

        UIApp(_send_new_clipboard, set_file_path_callback, quit, (ip_addr, PORT)).mainloop()

    except Exception as e:
        print(e)
        tkinter.messagebox.showerror(title='Error', message=str(e))
    
# input('')
