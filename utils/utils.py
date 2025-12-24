from pathlib import Path


def path_exists(location: str) -> bool:
    """determines if the path exists"""
    path = Path(location)
    if not path.exists():
        print("Configuration file not found at {filename}")
        return False
    return True


def load_config(filename: str) -> dict:
    """Load config from text file to dictionary. Originally meant for http headers."""
    configuration = {}
    try:
        with open(filename, "r", encoding="utf8") as f:
            for line in f:
                if not line.strip() or ":" not in line:
                    continue
                key, value = line.split(":", 1)
                configuration[key.strip()] = value.strip()
        return configuration
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {filename}")
