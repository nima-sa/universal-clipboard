# Import the required libraries
import tkinter

from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk

TK_SILENCE_DEPRECATION=1
class UIApp:

    def __init__(self, copy_callback, kill, addr):
        self.copy_callback = copy_callback
        self.kill = kill
        self.win = tkinter.Tk()
        self.win.resizable(False, False)

        self.win.title("Universal Clipboard")
        self.win.geometry("250x100")

        self.win.protocol('WM_DELETE_WINDOW', self.hide_window)

        text = tkinter.Text(self.win, height=8)
        text.pack()
        text.insert('1.0', f'{addr[0]}:{addr[1]}')

        self.hide_window()

    def quit_window(self, icon, item):
        self.kill()
        icon.stop()
        self.win.destroy()

    def show_window(self, icon, item):
        icon.stop()
        self.win.after(0, self.win.deiconify())

    def copy_to_clipboard(self, icon, item):
        self.copy_callback()

    def hide_window(self):
        self.win.withdraw()
        image = Image.open('static/icon-512-transparent.png')
        menu = [
            item('Quit', self.quit_window),
            item('Show', self.show_window),
            item('Paste on devices', self.copy_to_clipboard)
        ]
        icon = pystray.Icon("name", image, "My System Tray Icon", menu)
        icon.run()

    def mainloop(self):
        self.win.mainloop()
