import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class TestRunner(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.py') and not event.src_path.endswith('_test.py'):
            test_file = event.src_path.replace('.py', '_test.py')
            if os.path.exists(test_file):
                print(f"Running tests for {event.src_path}")
                subprocess.run(['pytest', test_file])

if __name__ == "__main__":
    path = "."  # Watch the current directory and all subdirectories
    event_handler = TestRunner()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
