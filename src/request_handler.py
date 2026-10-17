from dataclasses import dataclass, asdict
from datetime import datetime
import uuid
import re
from src.storage import save_request, load_requests
from src.agent import LangChainAgent
from src.artifact_generator import generate_artifact

sdlc_agent = LangChainAgent()

@dataclass
class FeatureRequest:
    id: str
    description: str
    client: str
    project: str
    timestamp: str
    phase: str = "pending"
    confidence: str = "0"
    agent_advice: str = ""
    artifact_path: str = ""

def validate_description(description: str) -> bool:
    clean_desc = description.strip()

    if not (10 <= len(clean_desc) <= 500):
        print("Error: Description must be between 10 and 500 characters.")
        return False

    forbidden_patterns = r'(<script>|system:|ignore previous|you are now)'
    if re.search(forbidden_patterns, clean_desc, re.IGNORECASE):
        print("Error: Unsafe characters or command overrides detected in the request.")
        return False
        
    return True

def create_request(description: str, client: str, project: str) -> bool:
    """Creates, validates, and stores a new feature request."""
    if not validate_description(description):
        print("Error: Description must be between 10 and 500 characters.")
        return False
    
    print("Analyzing request with LLM...")
    agent_result = sdlc_agent.process(description)

    artifact_msg = generate_artifact(
        description=description, 
        phase=agent_result["phase"],
        project=project,
        client=client,
        model_name="gemini-3.5-flash-lite"
    )
    print(f">> {artifact_msg}")
    print("------------------------\n")
        
    new_request = FeatureRequest(
        id=str(uuid.uuid4())[:8],
        description=description.strip(),
        client=client.strip(),
        project=project.strip(),
        timestamp=datetime.now().isoformat(),
        phase=agent_result["phase"],
        confidence=agent_result["confidence"],
        agent_advice=agent_result["advice"],
        artifact_path=artifact_msg
    )
    
    return save_request(asdict(new_request))

def get_all_requests() -> list:
    """Retrieves all stored requests."""
    return load_requests()