# CoRex

CoRex: Comment-based Review and Error Exploration System

## TODO

- [ ] 完善 prompts/analysis_comment_without_context.md 与 prompts/analysis_comment_with_context.md
- [ ] 实现 AnalyzerWithContext 类
- [ ] 增加 AutoRectify 功能

## 工具安装

```bash
# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# sync the dependencies at the root directory
uv sync
# activate the environment
source .venv/bin/activate
```

## 项目配置

```bash
# clone the repo
git clone https://github.com/lingebeng/CoRex.git
cd CoRex
# config
uv sync
source .venv/bin/activate
# install git hook
pre-commit install
```

## LLM 配置

config on the llm_config folder

```bash
# llm_keys.yaml
model_name:
    api_key: "sk-*****"

# model_config.yaml
model_name:
  base_url: "url"
  temperature: 1.0
  max_tokens: 8192
```

## 项目运行

```bash
# run main
python -m corex.main --file-path /path/to/code --save-path /path/to/save

# debug
python -m corex.extractor
python -m corex.llms
python -m corex.analyzer
```
