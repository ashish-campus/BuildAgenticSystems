import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class LangChainAgent:
    def __init__(self):
        # 1. Initialize the Google Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            temperature=0.1,
             safety_settings={
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    }
        )
        self.memory = [] 
        
        # 2. Setup Prompt Template (langchain_core)
        self.prompt = PromptTemplate.from_template(
            """Classify this feature request into one of these exact SDLC phases: requirements, design, implementation, testing, deployment.

Examples:
- "We need a user profile page" -> requirements, 95
- "Plan the database structure" -> design, 90
- "Write the API code for payments" -> implementation, 85
- "Create automated unit tests for the login module" -> testing, 90
- "Set up the production AWS environment" -> deployment, 80

Previous interactions (for context):
{chat_history}

Current Request: "{description}"

IMPORTANT: Respond ONLY with the exact phase name and confidence score separated by a comma. Do not include quotes, markdown formatting, or any other words.
Format: phase_name, confidence_percentage"""
        )
        
        # 3. Modern LCEL Chain 
        self.chain = self.prompt | self.llm | StrOutputParser()

    def observe(self, user_input: str) -> dict:
        """Step 1: Collect basic information."""
        print("[Agent] Observing input...")
        return {"description": user_input}

    def reason(self, observations: dict) -> dict:
        print("[Agent] Reasoning about the request using Gemini LCEL...")
        description = observations["description"]
        
        chat_history = "\n".join([f"Previous Task: {m['req']} -> Phase: {m['phase']}" for m in self.memory])
        if not chat_history:
            chat_history = "None"
            
        try:
            response_string = self.chain.invoke({
                "chat_history": chat_history,
                "description": description
            })

            if not response_string.strip():
                print("[Agent Debug] Gemini returned an empty string (API block).")
                print("[Agent Debug] Using fallback classification to maintain workflow.")
                response_string = "testing, 50"

            # Print exactly what the LLM returned so we can see its tricks
            print(f"[Agent Debug] Raw LLM text: '{response_string.strip()}'")
            
            # --- Bulletproof Keyword Parsing ---
            result = response_string.lower()
            phase = "unknown"
            valid_phases = ["requirements", "design", "implementation", "testing", "deployment"]
            
            # Just look for the word in the text, ignoring format
            for p in valid_phases:
                if p in result:
                    phase = p
                    break
                    
            # Extract the first set of digits it finds for the confidence score
            import re
            numbers = re.findall(r'\d+', result)
            confidence = numbers[-1] if numbers else "0"
            
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