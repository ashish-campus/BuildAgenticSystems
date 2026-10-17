from dataclasses import dataclass, asdict
from datetime import datetime
import uuid
from src.storage import save_request, load_requests

@dataclass
class FeatureRequest:
    id: str
    description: str
    client: str
    project: str
    timestamp: str

def validate_description(description: str) -> bool:
    """Validates that the description is between 10 and 500 characters."""
    return 10 <= len(description.strip()) <= 500

def create_request(description: str, client: str, project: str) -> bool:
    """Creates, validates, and stores a new feature request."""
    if not validate_description(description):
        print("Error: Description must be between 10 and 500 characters.")
        return False
        
    new_request = FeatureRequest(
        id=str(uuid.uuid4())[:8],
        description=description.strip(),
        client=client.strip(),
        project=project.strip(),
        timestamp=datetime.now().isoformat()
    )
    
    return save_request(asdict(new_request))

def get_all_requests() -> list:
    """Retrieves all stored requests."""
    return load_requests()