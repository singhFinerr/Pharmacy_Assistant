import os

def load_config():
    return {
        "app_name": "Hopkins Pharmacy Assistant",
        "env": os.getenv("ENV", "dev")
    }
