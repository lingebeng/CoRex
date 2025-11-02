# CoRex
CoRex: Comment-based Review and Error Exploration System

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

## 项目运行
```bash
# run main
python -m corex.main --file_path /path/to/code --save_path /path/to/save

# debug
python -m corex.extractor
python -m corex.llms
python -m corex.analyzer
```