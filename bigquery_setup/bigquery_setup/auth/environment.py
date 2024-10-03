import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


def is_colab():
    """
    Detects if the current environment is Google Colab.

    Returns:
        bool: True if running in Colab, False otherwise.
    """
    try:
        import google.colab

        return True
    except ImportError:
        return False


def detect_runtime_environment():
    """Detect the current runtime environment."""
    return os.getenv("RUNTIME_ENV", "development")
