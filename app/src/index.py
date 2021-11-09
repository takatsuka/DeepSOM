import os
import sys
import threading
import webview
import json
from time import time

from py.som_datastore_service import SOMDatastoreService
from py.som_scatterview_service import SOMScatterviewService
from py.som_viz_service import SOMVisualizationService
from py.model_service import ModelService
from py.som_view_service import SomViewService
from py.animal_service import AnimalService

class Api:

    # Class variables
    services_handle = {
        'SOMScatterviewService': SOMScatterviewService,
        'SOMVisualizationService': SOMVisualizationService,
        "ModelService": ModelService,
        "SomViewService": SomViewService,
        "AnimalService": AnimalService
    }

    global_services = {
        'SOMDatastoreService': -1
    }

    def __init__(self):
        self.datastore = SOMDatastoreService()
        self.services = {-1: self.datastore}
        self.services_n = 0

    def launch_service(self, key):
        if key in self.global_services:
            return self.global_services[key]

        if key not in self.services_handle:
            return

        s = self.services_handle[key](self.datastore)

        sid = self.services_n
        self.services[sid] = s
        self.services_n += 1

        return sid

    def close_service(self, handle):
        if handle not in self.services:
            return
        s = self.services[handle]

        if callable(getattr(s, 'on_close', None)):
            s.on_close()

        self.services.pop(handle)
        return

    def call_service(self, handle, method, params):
        if handle not in self.services:
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

    def open_csv_file_at(self, path):
        filename = path
        if not os.path.exists(filename):
            return None

        lines = open(filename).readlines()
        return os.path.basename(filename), [l.strip().split(',') for l in lines]

    def open_json_file(self):
        filename = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG)
        if filename == None:
            return None

        if len(filename) < 1:
            return None
        filename = filename[0]
        if not os.path.exists(filename):
            return None

        fields = json.loads(open(filename).read())
        return fields

    def open_json_file_at(self, path):
        filename = path
        if not os.path.exists(filename):
            return None

        fields = json.loads(open(filename).read())
        return fields

    def save_json_file(self, obj):
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if filename == None:
            return None

        open(filename, 'w').write(json.dumps(obj))
        return os.path.basename(filename)

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


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        print("moving to forzen application path: " + sys._MEIPASS)
        os.chdir(sys._MEIPASS)

    index_page = get_index_page()
    width, height = (1440, 900)

    if len(sys.argv) == 2:
        if sys.argv[1] == "--runtest":
            # maximise window for testing
            width, height = (2560, 1440)
            index_page = index_page.replace("index.html", "index-testing.html")
        elif sys.argv[1] == "--sudo":
            index_page = index_page.replace("index.html", "index-superuser.html")

    window = webview.create_window('PySOM Creator', index_page, js_api=Api(),
                frameless=True, easy_drag=False, width=width, height = height)
# gui="cef")

    # webview.start(debug=(False if hasattr(sys, '_MEIPASS') else True))
    webview.start(debug=True) # work around the debuging bug in pywebview for now.
