from setuptools import setup, find_packages

setup(
    name="bigquery_setup",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-cloud-bigquery",
        "colorama",
    ],
    extras_require={
        "dev": [
            "watchdog",  # For development scripts
            "black",  # Auto code formatter
            "pytest",  # Unit testing
            "schedule",  # For dependency checker
        ],
    },
)
