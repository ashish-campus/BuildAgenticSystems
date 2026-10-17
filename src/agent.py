import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class LangChainAgent:
    def __init__(self):
        # 1. Initialize the Google Gemini LLM
        self.llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash-tts", temperature=0.1)
        self.memory = [] 
        
        # 2. Setup Prompt Template (langchain_core)
        self.prompt = PromptTemplate.from_template(
            """Classify this feature request into one SDLC phase.
Phases: requirements, design, implementation, testing, deployment

Previous interactions (for context):
{chat_history}

Current Request: "{description}"

Respond with strictly this comma-separated format: phase_name, confidence_percentage
Example: requirements, 90"""
        )
        
        # 3. Modern LCEL Chain 
        self.chain = self.prompt | self.llm | StrOutputParser()

    def observe(self, user_input: str) -> dict:
        """Step 1: Collect basic information."""
        print("[Agent] Observing input...")
        return {"description": user_input}

    def reason(self, observations: dict) -> dict:
        """Step 2: Analyze data using LangChain and Gemini."""
        print("[Agent] Reasoning about the request using Gemini...")
        description = observations["description"]
        
        # Format our memory context
        chat_history = "\n".join([f"Previous Task: {m['req']} -> Phase: {m['phase']}" for m in self.memory])
        if not chat_history:
            chat_history = "None"
            
        try:
            # Use LCEL .invoke()
            response_string = self.chain.invoke({
                "chat_history": chat_history,
                "description": description
            })
            
            # Parse Gemini's response
            result = response_string.strip().lower()
            parts = result.split(',')
            phase = parts[0].strip()
            confidence = parts[1].strip() if len(parts) > 1 else "0"
            
            valid_phases = ["requirements", "design", "implementation", "testing", "deployment"]
            if phase not in valid_phases:
                phase = "unknown"
                
            self.memory.append({"req": description, "phase": phase})
            if len(self.memory) > 2:
                self.memory.pop(0)
                
            reasoning_text = f"Identified as '{phase}' with {confidence}% confidence via Gemini."
            
            return {
                "description": description,
                "phase": phase,
                "confidence": confidence,
                "reasoning": reasoning_text
            }
            
        except Exception as e:
            print(f"\n[!] LangChain/Gemini Error: {e}")
            return {"description": description, "phase": "error", "confidence": "0", "reasoning": "Error processing request."}

    def act(self, reasoning: dict) -> dict:
        """Step 3: Determine the best action/advice."""
        print("[Agent] Formulating action and advice...")
        phase = reasoning["phase"]
        
        advice = "Let's proceed with standard SDLC practices."
        if phase == "requirements":
            advice = "Advice: Document detailed user stories and stakeholder acceptance criteria."
        elif phase == "design":
            advice = "Advice: Create architecture diagrams and define API contracts."
        elif phase == "implementation":
            advice = "Advice: Ensure adherence to coding standards and write unit tests."
        elif phase == "testing":
            advice = "Advice: Execute test cases and ensure all edge cases are covered."
        elif phase == "deployment":
            advice = "Advice: Review deployment checklists and verify rollback plans."

        return {
            "phase": phase,
            "confidence": reasoning["confidence"],
            "agent_reasoning": reasoning["reasoning"],
            "advice": advice
        }

    def process(self, user_input: str) -> dict:
        """The core agent loop."""
        observations = self.observe(user_input)
        reasoning = self.reason(observations)
        return self.act(reasoning)