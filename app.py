from server_handler import socketio, app, send_new_clipboard
from ui_handler import UIApp
import threading
import socket

def _send_new_clipboard():
    send_new_clipboard(None)


def raisingSth():
    try:
        raise Exception()
    except:
        print('ok')



if __name__ == '__main__':
    PORT = 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr, _ = s.getsockname()
    s.close()
    print(ip_addr, PORT)
    socket_thread = threading.Thread(
        target=lambda: socketio.run(app, '0.0.0.0', f'{PORT}')
        )
    socket_thread.daemon = True
    socket_thread.start()

    UIApp(_send_new_clipboard, lambda: raisingSth(), (ip_addr, PORT)).mainloop()

