import yaml
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from .config import LLM_KEYS_PATH, MODEL_CONFIG_PATH


class LLM:
    def __init__(
        self,
        model_name: str = "deepseek-chat",
        api_key: str = "",
    ):
        if not api_key:
            with open(LLM_KEYS_PATH, "r", encoding="utf-8") as f:
                llm_keys = yaml.safe_load(f)
            api_key = llm_keys.get(model_name, {}).get("api_key", "")
        if not api_key:
            raise ValueError("API key is required. ")
        with open(MODEL_CONFIG_PATH, "r", encoding="utf-8") as f:
            model_configs = yaml.safe_load(f)

        self.model_name = model_name

        self.llm = ChatOpenAI(
            model=model_name,
            api_key=SecretStr(api_key),
            **model_configs.get(model_name, {}),
        )

    def generate(self, prompt: str) -> str:
        try:
            response = self.llm.invoke(prompt)
            content = response.content
            if isinstance(content, str):
                return content
            return str(content)
        except Exception as e:
            raise Exception(f"Failed to generate content: {e!s}") from e

    def __repr__(self) -> str:
        """Return string representation of the agent."""
        return f"Agent(model={self.model_name})"


if __name__ == "__main__":
    llms = LLM()
    prompt = "1 + 1 = ?"
    print(llms.generate(prompt))
