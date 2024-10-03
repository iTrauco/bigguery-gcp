# test_watchdog.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


class TestHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"File {event.src_path} has been modified.")


observer = Observer()
observer.schedule(TestHandler(), path=".", recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
