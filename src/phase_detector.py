import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def detect_phase(description: str) -> dict:
    """Uses LLM to detect the SDLC phase and confidence score."""
    prompt = f"""Classify this feature request into one SDLC phase:

"{description}"

Phases: requirements, design, implementation, testing, deployment

Respond with strictly this comma-separated format: phase_name, confidence_percentage
Example: requirements, 90"""

    try:
        response = client.chat.completions.create(
            model="gemini-3.1-pro-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1 
        )
        
        result = response.choices[0].message.content.strip().lower()
        parts = result.split(',')
        
        phase = parts[0].strip()
        confidence = parts[1].strip() if len(parts) > 1 else "unknown"
        
        valid_phases = ["requirements", "design", "implementation", "testing", "deployment"]
        if phase not in valid_phases:
            phase = "unknown"
            
        return {"phase": phase, "confidence": confidence}
        
    except Exception as e:
        print(f"\n[!] LLM API Error: {e}")
        return {"phase": "error", "confidence": "0"}