import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from templates.test_template import TEMPLATE

PROJECT_ROOT = "bigquery_setup"  # Project root directory
TESTS_ROOT = "tests"  # Tests root directory


class TestFileGenerator(FileSystemEventHandler):
    def on_modified(self, event):
        """Rebuild tests when changes are made to Python files."""
        if event.is_directory or event.src_path.endswith(".py"):
            sync_tests()


def get_functions_from_file(file_path):
    """Extracts function names from a Python file."""
    function_names = []
    with open(file_path, "r") as f:
        for line in f:
            if line.strip().startswith("def "):
                function_name = line.split("(")[0].replace("def ", "").strip()
                function_names.append(function_name)
    return function_names


def create_test_file(module_path, module_import):
    """Creates or updates a test file under tests/ directory, mirroring the project structure."""
    # Generate the test file path by replacing the project root with the tests root
    test_path = os.path.join(
        TESTS_ROOT, os.path.relpath(module_path, PROJECT_ROOT)
    ).replace(".py", "_test.py")

    # Ensure the test directory structure is created
    if not os.path.exists(test_path):
        os.makedirs(os.path.dirname(test_path), exist_ok=True)

    # Extract function names from the module
    function_names = get_functions_from_file(module_path)

    # Write the test template with the imported module and function names
    with open(test_path, "w") as f:
        f.write(
            TEMPLATE.format(
                module_import=module_import,
                function_names=", ".join(function_names) or "NoFunctionsFound",
            )
        )
    print(f"Generated or updated test file: {test_path}")


def sync_tests():
    """Sync the tests directory with the project directory structure."""
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Create a mirrored directory structure under tests/
        for file_name in files:
            if file_name.endswith(".py") and not file_name.startswith("__init__"):
                module_path = os.path.join(root, file_name)
                module_import = (
                    module_path.replace(PROJECT_ROOT + "/", "")
                    .replace("/", ".")
                    .replace(".py", "")
                )
                create_test_file(module_path, module_import)


def start_observer():
    """Start the watchdog observer to monitor for changes."""
    event_handler = TestFileGenerator()
    observer = Observer()
    observer.schedule(event_handler, PROJECT_ROOT, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    # Sync tests initially
    sync_tests()
    # Start the observer for continuous monitoring
    start_observer()
