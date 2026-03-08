from ai.gemini_service import GeminiService
from core.memory_system import MemoryStorageService
from core.logging.logger import LoggerFactory


class PromptManager:
    """
    Central prompt orchestration system.
    """

    def __init__(self):
        self.logger = LoggerFactory.create_logger("prompt_manager")
        self.llm = GeminiService()
        self.memory = MemoryStorageService()

    def build_prompt(self, system_prompt: str, user_prompt: str, context: str = ""):
        """
        Construct a structured prompt.
        """

        prompt = ""

        if system_prompt:
            prompt += f"System:\n{system_prompt}\n\n"

        if context:
            prompt += f"Context:\n{context}\n\n"

        prompt += f"User:\n{user_prompt}\n"

        return prompt

    def generate_response(self, system_prompt: str, user_prompt: str, context: str = ""):
        """
        Build prompt and request AI response.
        """

        prompt = self.build_prompt(system_prompt, user_prompt, context)

        self.logger.info("Sending prompt to Gemini")

        response = self.llm.generate(prompt)

        return response

    def build_memory_prompt(self, user_prompt: str, memory_items: list):
        """
        Build prompt including memory context.
        """

        memory_context = "\n".join(memory_items)

        system_prompt = "Use the provided memory context when answering."

        return self.build_prompt(system_prompt, user_prompt, memory_context)