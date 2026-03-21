import yaml
from pathlib import Path

# Load Prompts from config/prompts.yaml
PROMPT_FILE = Path(__file__).parent.parent / "config" / "prompts.yaml"

def load_prompts():
    if not PROMPT_FILE.exists():
        return {}
    with open(PROMPT_FILE, "r") as f:
        return yaml.safe_load(f)

PROMPTS = load_prompts()

def get_prompt(name: str) -> str:
    return PROMPTS.get(name, "")
