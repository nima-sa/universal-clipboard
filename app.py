import asyncio
import uvicorn

import socket
import threading

from ui_handler import UIApp
import server_handler


async def server(host, port):
    config = uvicorn.Config(server_handler.app, host=host, port=port)
    await uvicorn.Server(config).serve()


def _send_new_clipboard():
    send_new_clipboard(None)


def set_file_path_callback(path):
    print('here')
    server_handler.TEMP_FILE_UPLOAD_PATH = path


def raisingSth():
    try:
        raise Exception()
    except:
        print('ok')


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8000

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

    UIApp(_send_new_clipboard, set_file_path_callback, lambda: raisingSth(), (ip_addr, PORT)).mainloop()
