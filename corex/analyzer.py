from abc import ABC, abstractmethod

from loguru import logger

from .config import PROMPT_TEMPLATES_DIR
from .llms import LLM


class Analyzer(ABC):
    def __init__(self, llms: LLM):
        self.llms = llms
        self.prompt = ""
        self.comments = ""
        self.context = ""

    @abstractmethod
    def load_prompt_template(self):
        raise NotImplementedError()

    @abstractmethod
    def analyze(self):
        raise NotImplementedError()


class AnalyzerWithContext(Analyzer):
    def __init__(self, llms: LLM):
        super().__init__(llms=llms)

        self.load_prompt_template()

    def load_prompt_template(self):
        prompt_path = PROMPT_TEMPLATES_DIR / "analysis_comment_with_context.md"
        with open(prompt_path, "r") as f:
            self.prompt = f.read()

    def analyze(self):
        prompt_filled = self.prompt.replace("{{comment}}", self.comments).replace(
            "{{context}}", self.context
        )
        response = self.llms.generate(prompt_filled)
        return response


class AnalyzerWithoutContext(Analyzer):
    def __init__(self, llms: LLM):
        super().__init__(llms=llms)
        self.load_prompt_template()

    def load_prompt_template(self):
        prompt_path = PROMPT_TEMPLATES_DIR / "analysis_comment_without_context.md"
        with open(prompt_path, "r") as f:
            self.prompt = f.read()

    def analyze(self):
        prompt_filled = self.prompt.replace("{{comment}}", self.comments)
        response = self.llms.generate(prompt_filled)
        return response


# python -m corex.analyzer
if __name__ == "__main__":
    llms = LLM()
    comments = "# This is a sample code comment with a typo."
    analyzer = AnalyzerWithoutContext(llms=llms)
    analyzer.comments = comments
    result = analyzer.analyze()
    logger.info(f"Analysis Result:\n{result}")
