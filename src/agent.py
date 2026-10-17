from src.phase_detector import detect_phase

class SimpleAgent:
    def __init__(self):
        self.memory = []

    def observe(self, user_input: str) -> dict:
        """Step 1: Collect basic information and context."""
        print("[Agent] Observing input and gathering context...")
        return {
            "description": user_input,
            "previous_context": list(self.memory)
        }

    def reason(self, observations: dict) -> dict:
        """Step 2: Analyze the data using the LLM and memory."""
        print("[Agent] Reasoning about the request...")
        description = observations["description"]

        detection = detect_phase(description)
        phase = detection.get("phase", "unknown")
        confidence = detection.get("confidence", "0")
        
        reasoning_text = f"I identified this as '{phase}' with {confidence}% confidence."
        
        if observations["previous_context"]:
            last_req = observations["previous_context"][-1]
            reasoning_text += f" (Context noted: Following up on previous '{last_req['phase']}' task)."

        return {
            "description": description,
            "phase": phase,
            "confidence": confidence,
            "reasoning": reasoning_text
        }

    def act(self, reasoning: dict) -> dict:
        """Step 3: Determine the best action/advice and update memory."""
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

        self.memory.append({"description": reasoning["description"], "phase": phase})
        if len(self.memory) > 2:
            self.memory.pop(0)

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