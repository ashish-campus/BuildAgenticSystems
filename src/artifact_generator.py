import os
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Define specific templates for each phase
TEMPLATES = {
    "requirements": """# Requirements Document
Feature: {description}
Project: {project} | Client: {client}
Date: {date}

Expand on the feature description and generate:
1. Detailed Description
2. Basic Requirements (Bullet points)
3. Next Steps (e.g., Review with stakeholders)
""",
    
    "design": """# Technical Design Document
Feature: {description}
Project: {project} | Client: {client}
Date: {date}

Based on the feature, outline:
1. High-level Architecture
2. Key Components / Database Entities
3. Basic API Contracts or Interfaces
""",
    
    "implementation": """# Implementation Task List
Feature: {description}
Project: {project} | Client: {client}
Date: {date}

Break this feature down into developer tasks:
1. Setup & Dependencies
2. Core Logic Tasks
3. UI/API Integration Tasks
""",
    
    "testing": """# Test Plan
Feature: {description}
Project: {project} | Client: {client}
Date: {date}

Generate a basic test plan including:
1. Happy Path Test Cases
2. Edge Cases to Consider
3. Success Criteria
""",
    
    "deployment": """# Deployment Checklist
Feature: {description}
Project: {project} | Client: {client}
Date: {date}

Create a deployment plan outlining:
1. Pre-deployment Prerequisites
2. Deployment Steps
3. Rollback Plan
"""
}

def generate_artifact(description: str, phase: str, project: str, client: str, model_name: str = "gemini-3.5-flash-lite") -> str:
    """Generates an artifact document using LLM and saves it to the correct folder."""
    if phase not in TEMPLATES:
        return "No artifact generated. Phase unknown or unsupported."
        
    print(f"\n[Generator] Creating {phase} artifact via Gemini...")
    
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.2,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        }
        )
    prompt = PromptTemplate.from_template(TEMPLATES[phase])
    chain = prompt | llm | StrOutputParser()
    
    # Generate the content
    try:
        content = chain.invoke({
            "description": description,
            "project": project,
            "client": client,
            "date": datetime.now().strftime("%Y-%m-%d")
        })

        if not content.strip():
            content = f"# {phase.capitalize()} Document\n\n[!] Content generation was blocked by API safety filters. Please review the request description manually.\n\nDescription: {description}"
        # Save the file
        filename = f"{datetime.now().strftime('%H%M%S')}_{phase}_doc.md"
        filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'artifacts', phase, filename)
        
        with open(filepath, 'w') as f:
            f.write(content)
            
        return f"Artifact saved to: {os.path.abspath(filepath)}"
        
    except Exception as e:
        return f"Failed to generate artifact: {e}"