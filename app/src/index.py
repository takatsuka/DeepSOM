import os
import sys
import threading
import webview

from time import time

from py.som_viz_service import SOMVisualizationService


class Api:

    # Class variables
    services_handle = {
        'SOMVisualizationService': SOMVisualizationService
    }

    services = {}
    services_n = 0

    def launch_service(self, key, params):
        if not key in self.services_handle:
            return
        s = self.services_handle[key](*params)
        self.services[self.services_n] = s
        self.services_n += 1

        return s

    def close_service(self, handle):
        if not handle in self.services:
            return
        s = self.services[handle]

        if callable(getattr(s, 'on_close', None)):
            s.on_close()

        self.services.pop(handle)
        return

    def call_service(self, handle, method, params):
        if not handle in self.services:
            return
        s = self.services[handle]

        md = getattr(s, method, None)
        if not callable(md):
            return

        return md(*params)

    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def save_content(self, content):
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if not filename:
            return

        with open(filename, 'w') as f:
            f.write(content)

    def open_csv_file(self):
        filename = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG)
        if filename == None:
            return None

        if len(filename) < 1:
            return None
        filename = filename[0]
        if not os.path.exists(filename):
            return None

        lines = open(filename).readlines()
        return os.path.basename(filename), [l.strip().split(',') for l in lines]

    def terminate(self):
        webview.windows[0].destroy()
        os.exit(0)


def get_index_page():
    def exists(path):
        if hasattr(sys, '_MEIPASS'):
            print(f"searching {os.path.join(os.getcwd(), path)}")
            return os.path.exists(os.path.join(os.getcwd(), path))
        else:
            return os.path.exists(os.path.join(os.path.dirname(__file__), path))

    if exists('../gui/index.html'):  # unfrozen development
        return '../gui/index.html'

    if exists('./gui/index.html'):
        return './gui/index.html'

    if exists('./gui/index.html'):
        return './gui/index.html'

    raise Exception(f'No index.html found {os.getcwd()} {sys._MEIPASS}')


if hasattr(sys, '_MEIPASS'):
    print("moving to forzen application path: " + sys._MEIPASS)
    os.chdir(sys._MEIPASS)
window = webview.create_window('PySOM Creator', get_index_page(
), js_api=Api(), frameless=True, easy_drag=False)
# gui="cef")
webview.start(debug=(False if hasattr(sys, '_MEIPASS') else True))
