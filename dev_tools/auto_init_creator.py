import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class InitCreator(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            init_path = os.path.join(event.src_path, "__init__.py")
            if not os.path.exists(init_path):
                with open(init_path, 'w') as f:
                    f.write("# Auto-generated __init__.py")
                print(f"Created __init__.py in {event.src_path}")

if __name__ == "__main__":
    path = "."  # Watch the current directory and all subdirectories
    event_handler = InitCreator()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()