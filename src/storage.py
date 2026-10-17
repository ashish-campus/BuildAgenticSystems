import json
import os
from typing import List, Dict

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'requests.json')

def load_requests() -> List[Dict]:
    """Loads requests from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_request(request_data: Dict) -> bool:
    """Appends a new request to the JSON file."""
    requests = load_requests()
    requests.append(request_data)
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(requests, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False