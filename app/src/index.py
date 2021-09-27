import os
import sys
import threading
import webview

from time import time


class Api:
    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def save_content(self, content):
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if not filename:
            return

        with open(filename, 'w') as f:
            f.write(content)

    def ls(self):
        return os.listdir('.')


def get_index_page():
    def exists(path):
        if hasattr(sys,'_MEIPASS'):
            print(f"searching {os.path.join(os.getcwd(), path)}")
            return os.path.exists(os.path.join(os.getcwd(), path))
        else:
            return os.path.exists(os.path.join(os.path.dirname(__file__), path))

    if exists('../gui/index.html'): # unfrozen development
        return '../gui/index.html'

    if exists('./gui/index.html'):
        return './gui/index.html'
    
    if exists('./gui/index.html'):
        return './gui/index.html'

    raise Exception(f'No index.html found {os.getcwd()} {sys._MEIPASS}')



window = webview.create_window('PySOM Creator', get_index_page(), js_api=Api())
webview.start(debug=(False if hasattr(sys,'_MEIPASS') else True))  # gui="cef")
