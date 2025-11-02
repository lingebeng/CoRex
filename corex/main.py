from pathlib import Path

import typer
from loguru import logger

from .analyzer import Analyzer, AnalyzerWithContext, AnalyzerWithoutContext
from .extractor import CommentExtractor, Extractor, KeywordExtractor
from .llms import LLM


class CoRex:
    """
    Comment-based Review and Error Exploration System
    """

    def __init__(
        self,
        file_path: Path,
        extractor: Extractor,
        analyzer: Analyzer,
        save_path: Path = Path("output.log"),
    ):
        self.file_path = file_path
        self.extractor = extractor
        self.analyzer = analyzer
        self.save_path = save_path

    def run(self):
        """
        运行 CoRex 系统的主流程
        1. 提取代码中的注释
        2. 分析注释，识别潜在问题
        3. 生成分析报告
        """
        logger.info(f"Starting CoRex on file: {self.file_path}")

        extraction_result = self.extractor.parse_file(self.file_path)
        for comment_info in extraction_result:
            filename = comment_info.get("file", "unknown")
            comments_list = comment_info.get("comments", [])
            logger.info(f"Extracted {len(comments_list)} comments from the {filename}.")
            if not comments_list:
                logger.warning(f"No comments found in file: {filename}")
                continue
            for comment_dic in comments_list:
                comment = comment_dic.get("text", "")
                self.analyzer.comments = comment
                response = self.analyzer.analyze()
                if "Normal" not in response:
                    with open(self.save_path, "a") as f:
                        f.write(f"File: {filename}\n")
                        f.write(f"Comment: {comment}\n")
                        f.write(f"Analysis Result:\n{response}\n")
                        f.write("=" * 80 + "\n")
                    logger.info(f"Analysis Result for {filename}:\n{response}")

            # total_comment = []
            # for i, comment_dic in enumerate(comments_list):
            #     comment = comment_dic.get("text", "")
            #     total_comment.append(f"## Case{i}\n### Comment\ncomment:{comment}")
            # all_comments = "\n".join(total_comment)
            # logger.info(f"{all_comments}")
            # self.analyzer.comments = all_comments
            # response = self.analyzer.analyze()
            # logger.info(f"Analysis completed for file: {filename}")
            # logger.info(f"Analysis Result for {filename}:\n{response}")
            # break


def main(
    file_path: Path = typer.Option(
        "/home/haifeng/data/pytorch/torchgen", help="Path to the folder/repo to scan."
    ),
    model_name: str = typer.Option("deepseek-chat", help="LLM model name."),
    language: str = typer.Option(
        "python", help="Programming language of the source code."
    ),
    extractor_type: str = typer.Option("comment", help="Type of extractor to use."),
    analyze_type: str = typer.Option(
        "without_context", help="Type of analysis to perform."
    ),
    save_path: Path = typer.Option(
        "output.log", help="Path to save the analysis report."
    ),
):
    llms = LLM(model_name=model_name)
    if extractor_type == "comment":
        extractor = CommentExtractor(language=language)
    elif extractor_type == "keyword":  # TODO@haifeng
        extractor = KeywordExtractor(language=language)
    else:
        raise ValueError(f"Unsupported extractor type: {extractor_type}")

    if analyze_type == "without_context":
        analyzer = AnalyzerWithoutContext(llms=llms)
    elif analyze_type == "with_context":  # TODO@haifeng
        analyzer = AnalyzerWithContext(llms=llms)
    else:
        raise ValueError(f"Unsupported analyze type: {analyze_type}")

    corex = CoRex(
        file_path=file_path, extractor=extractor, analyzer=analyzer, save_path=save_path
    )
    corex.run()


# python -m corex.main --file_path /path/to/code --model_name deepseek-chat --language python --extractor_type comment --analyze_type without_context
if __name__ == "__main__":
    typer.run(main)
