import os
import json

def load_config():
    # Detect the current environment (default to 'development')
    environment = os.getenv("ENVIRONMENT", "development")
    
    # Build the path to the config file for the detected environment
    config_file = f"config/{environment}.json"
    
    try:
        # Load the configuration file
        with open(config_file) as f:
            config = json.load(f)
        print(f"Loaded {environment} configuration.")
        return config
    except FileNotFoundError:
        print(f"[ERROR] Config file for {environment} not found!")
        raise
    except Exception as e:
        print(f"[ERROR] Failed to load config for {environment}: {e}")
        raise

# Example usage
if __name__ == "__main__":
    config = load_config()
    print(config)
