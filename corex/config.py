from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
LLM_CONFIG_DIR = ROOT_DIR / "llm_config"
MODEL_CONFIG_PATH = LLM_CONFIG_DIR / "model_config.yaml"
LLM_KEYS_PATH = LLM_CONFIG_DIR / "llm_keys.yaml"
PROMPT_TEMPLATES_DIR = ROOT_DIR / "prompts"
