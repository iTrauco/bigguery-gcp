import sys
import os
import time
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from termcolor import colored

PROJECT_ROOT = "bigquery_setup"
TESTS_ROOT = "tests"

# Dynamically adding the path to the templates directory
try:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.append(project_root)
    from templates.test_template import TEMPLATE
    print(colored("[SUCCESS] TEMPLATE imported successfully.", "green", attrs=["bold"]))
except ModuleNotFoundError:
    print(colored("[ERROR] 'templates/test_template.py' not found.", "red", attrs=["bold"]))
    print(colored("Make sure 'templates/' exists at the project root.", "yellow"))
    print(colored("sys.path: " + str(sys.path), "grey"))
    sys.exit(1)

class TestFileGenerator(FileSystemEventHandler):
    def on_modified(self, event):
        """Rebuild tests when Python files are modified."""
        if event.is_directory or event.src_path.endswith(".py"):
            print(colored(f"[INFO] Detected change in: {event.src_path}", "cyan"))
            try:
                sync_tests()
                print(colored("[SUCCESS] Test sync completed.", "green", attrs=["bold"]))
            except Exception as e:
                print(colored("[ERROR] Failed to sync tests.", "red", attrs=["bold"]))
                print(colored("See full error details below:", "yellow"))
                print(colored(traceback.format_exc(), "grey"))

def get_functions_from_file(file_path):
    """Extracts function names from a Python file."""
    function_names = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                if line.strip().startswith("def "):
                    function_name = line.split("(")[0].replace("def ", "").strip()
                    function_names.append(function_name)
        print(colored(f"[SUCCESS] Extracted functions from: {file_path}", "green", attrs=["bold"]))
    except Exception as e:
        print(colored(f"[ERROR] Failed to read file: {file_path}", "red", attrs=["bold"]))
        print(colored("Ensure the file is readable and correctly formatted.", "yellow"))
        print(colored(traceback.format_exc(), "grey"))
    return function_names

    def create_test_file(module_path, module_import):def create_test_file(module_path, module_import):
        """Creates a test file with basic template for imports and functions."""
        # Correct the file path to ensure test files are named as test_*.py
        test_path = os.path.join(os.path.dirname(module_path.replace(PROJECT_ROOT, TESTS_ROOT)), f"test_{os.path.basename(module_path)}")
        if not os.path.exists(test_path):
            os.makedirs(os.path.dirname(test_path), exist_ok=True)

        # Extract function names for the test
        function_names = get_functions_from_file(module_path)

        # Populate the test template
        with open(test_path, 'w') as f:
            f.write(
                TEMPLATE.format(
                    module_import=module_import, 
                    function_names=', '.join(function_names) or 'NoFunctionsFound'
                )
            )
        print(f"Generated or updated test file: {test_path}")


        print(colored(f"[SUCCESS] Generated/Updated test file: {test_path}", "green", attrs=["bold"]))
    except Exception as e:
        print(colored(f"[ERROR] Could not generate test file for: {module_path}", "red", attrs=["bold"]))
        print(colored("See full error details below:", "yellow"))
        print(colored(traceback.format_exc(), "grey"))

def sync_tests():
    """Syncs the tests/ directory with the project structure."""
    try:
        print(colored("[INFO] Syncing tests with the project...", "cyan"))
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Mirror directory structure in the tests directory
            for file_name in files:
                if file_name.endswith(".py") and not file_name.startswith("__init__"):
                    module_path = os.path.join(root, file_name)
                    module_import = (
                        module_path.replace(PROJECT_ROOT + "/", "")
                        .replace("/", ".")
                        .replace(".py", "")
                    )
                    create_test_file(module_path, module_import)
        print(colored("[SUCCESS] All tests synced.", "green", attrs=["bold"]))
    except Exception as e:
        print(colored("[ERROR] Failed to sync tests.", "red", attrs=["bold"]))
        print(colored("See full error details below:", "yellow"))
        print(colored(traceback.format_exc(), "grey"))

def start_observer():
    """Start the watchdog observer to monitor for changes."""
    event_handler = TestFileGenerator()
    observer = Observer()
    observer.schedule(event_handler, PROJECT_ROOT, recursive=True)
    observer.start()
    try:
        print(colored("[INFO] Starting test generation observer...", "cyan"))
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print(colored("[INFO] Test generation observer stopped.", "yellow"))
    observer.join()

if __name__ == "__main__":
    print(colored("[INFO] Initializing test generation process...", "cyan"))
    try:
        # Sync tests initially
        sync_tests()
        print(colored("[SUCCESS] Initial test sync completed.", "green", attrs=["bold"]))

        # Start the observer for continuous monitoring
        start_observer()
    except Exception as e:
        print(colored("[ERROR] Critical error during initialization.", "red", attrs=["bold"]))
        print(colored("See full error details below:", "yellow"))
        print(colored(traceback.format_exc(), "grey"))
