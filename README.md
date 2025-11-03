# CoRex

<div align="center">
  <img src=".assets/CoRex.jpg" alt="CoRex Logo" width="400"/>

  <h2>✨ Comment-based Review and Error Exploration ✨</h2>

  <p><em>🤖 智能代码注释分析与错误探索工具 🔍</em></p>
</div>

---

## ✨ 特性

- 🔍 **智能注释分析**: 基于大模型的代码注释质量分析
- 🚨 **错误探索**: 自动识别和分析代码中的潜在问题
- 📊 **上下文理解**: 结合代码上下文进行深度分析
- 🔧 **自动修复**: 提供智能的代码修复建议
- 📝 **多语言支持**: 支持 Python、C++、CUDA 等多种编程语言

## 📋 TODO

- [ ] 完善 `prompts/analysis_comment_without_context.md` 与 `prompts/analysis_comment_with_context.md`
- [ ] 实现 `AnalyzerWithContext` 类
- [ ] 增加 `AutoRectify` 功能

## 🛠️ 工具安装

```bash
# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# sync the dependencies at the root directory
uv sync
# activate the environment
source .venv/bin/activate
```

## ⚙️ 项目配置

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

## 🤖 LLM 配置

在 `llm_config` 文件夹中进行配置

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

## 🚀 项目运行

```bash
# run main
python -m corex.main --file-path /path/to/code --save-path /path/to/save

# debug
python -m corex.extractor
python -m corex.llms
python -m corex.analyzer
```

## 📁 项目结构

```text
CoRex/
├── .assets/             # 项目资源文件
├── corex/               # 核心模块
│   ├── analyzer.py      # 分析器模块
│   ├── config.py        # 配置管理
│   ├── extractor.py     # 代码提取器
│   ├── llms.py          # 大模型接口
│   └── main.py          # 主程序入口
├── experiments/         # 实验脚本
├── llm_config/          # LLM 配置文件
├── prompts/             # 提示词模板
└── README.md            # 项目说明
```
