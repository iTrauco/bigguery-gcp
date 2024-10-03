import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class CodeFormatter(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.py'):
            print(f"Formatting {event.src_path}")
            subprocess.run(['black', event.src_path])

if __name__ == "__main__":
    path = "."  # Watch the current directory and all subdirectories
    event_handler = CodeFormatter()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
