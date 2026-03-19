import requests
import json
import logging
from pathlib import Path
from string import Template
from typing import Optional, Dict, Any

from second_brain_ai.config.settings import get_settings

logger = logging.getLogger(__name__)

# Reliable path to the prompt library
_ROOT = Path(__file__).resolve().parent.parent
_PROMPT_PATH = _ROOT / "PROMPT_LIBRARY.yaml"

def _load_library():
    import yaml
    if not _PROMPT_PATH.exists():
        logger.warning(f"PROMPT_LIBRARY not found at {_PROMPT_PATH}")
        return {}
    with open(_PROMPT_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

class GeminiService:
    """Enhanced Gemini service with robust endpoint selection (v1beta/gemini-2.5-flash)."""

    # Confirmed working end-point: v1beta/models/gemini-2.5-flash
    MODEL = "models/gemini-2.5-flash" 

    def __init__(self):
        settings = get_settings()
        self.api_key = settings.gemini_api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        library = _load_library()
        self.system_prompts = library.get("system_prompts", {})
        self.prefix = self.system_prompts.get("agent_system_prefix", "")
        self.enforcement = self.system_prompts.get("json_enforcement", "")
        self.agent_prompts = library.get("agent_prompts", {})

    def _build_prompt(self, agent: str, action: str, **kwargs) -> str:
        template = self.agent_prompts.get(agent, {}).get(action)
        if not template:
            return f"Agent: {agent}. Action: {action}. Data: {json.dumps(kwargs)}"
        body = Template(template).safe_substitute(**kwargs)
        return f"{self.prefix}\n{self.enforcement}\n{body}"

    async def _call(self, prompt: str, temperature: float = 0.7) -> Optional[str]:
        if not self.api_key:
            return None
        
        # MODEL already has 'models/' prefix string from list_models
        url = f"{self.base_url}/{self.MODEL}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": temperature}
        }

        try:
            # Note: Using requests.post synchronously here for simplicity in this mock-heavy environment,
            # but making the method signature 'async' so agents can 'await' it consistently.
            r = requests.post(url, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            msg = str(e)
            resp = getattr(e, 'response', None)
            if resp is not None:
                if resp.status_code == 429:
                    return '{"error": "AI Rate Limit Reached (15 requests/min). Please wait a moment and try again."}'
                msg += f" | {resp.text}"
            logger.error(f"Gemini call failed: {msg}")
            return None

    def _parse(self, text: Optional[str], key: str = "result") -> Dict[str, Any]:
        if not text:
            return {"error": "No response"}
        cleaned = text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[-1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[-1].split("```")[0].strip()
        
        try:
            return json.loads(cleaned)
        except:
            return {key: text}

    async def generate_research(self, data: Dict[str, Any]):
        p = self._build_prompt("research_agent", "concept_research", **data)
        res = await self._call(p)
        return self._parse(res, "summary")

    async def generate_learning_module(self, data: Dict[str, Any]):
        p = self._build_prompt("learning_agent", "learning_module_generation", **data)
        res = await self._call(p)
        return self._parse(res, "content")

    async def generate_idea(self, concepts: list):
        p = self._build_prompt("idea_synthesizer", "idea_generation", concepts=json.dumps(concepts))
        res = await self._call(p)
        return self._parse(res, "synthesis")

    async def generate_questions(self, data: Dict[str, Any]):
        mastery = data.get("user_mastery_level", "Unknown")
        p = self._build_prompt("question_generator", "question_generation", concept_data=json.dumps(data), mastery_level=mastery)
        res = await self._call(p)
        return self._parse(res, "question")