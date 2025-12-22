# Agent Laboratory 项目结构

## 📂 目录说明

```
AgentLaboratory/
│
├── 📄 核心代码文件
│   ├── ai_lab_repo.py          # 主程序入口
│   ├── agents.py               # Agent定义（PhD, Postdoc, Professor等）
│   ├── inference.py            # LLM推理接口
│   ├── mlesolver.py            # 机器学习实验求解器
│   ├── papersolver.py          # 论文撰写求解器
│   ├── tools.py                # 工具函数（数据集搜索、代码执行等）
│   ├── utils.py                # 通用工具函数
│   ├── common_imports.py       # 公共导入
│   └── app.py                  # Flask Web应用（论文管理）
│
├── 📁 docs/                    # 📚 文档目录
│   ├── 改进方案.md             # 系统改进建议
│   ├── 启动说明.md             # 启动和配置指南
│   └── 使用示例.md             # 使用示例
│
├── 📁 experiment_configs/      # ⚙️ 实验配置
│   ├── MATH_agentlab.yaml      # Agent Laboratory配置
│   └── MATH_agentrxiv.yaml     # AgentRxiv配置
│
├── 📁 experiments/             # 🧪 实验结果目录（自动生成）
│   └── YYYYMMDD_HHMMSS_主题/
│       ├── data/               # 数据文件
│       ├── outputs/            # 实验输出
│       ├── logs/               # 日志文件
│       ├── src/                # 生成的代码
│       ├── reports/            # 研究报告
│       └── tex/                # LaTeX文件
│
├── 📁 data/                    # 💾 数据文件（被忽略）
│   ├── math500_experiment_data.json
│   └── mcrcp_results.json
│
├── 📁 scripts/                 # 🔧 测试和工具脚本
│   └── test_directory_structure.py
│
├── 📁 templates/               # 🎨 Flask模板
│   └── index.html
│
├── 📁 media/                   # 🖼️ 媒体资源
│   └── *.png                   # 项目图片
│
├── 📁 readme/                  # 🌍 多语言README
│   ├── README-chinese.md
│   ├── README-japanese.md
│   └── ...
│
├── 📁 uploads/                 # 📤 上传文件（Flask应用）
│
├── 📁 state_saves/             # 💾 状态保存（被忽略）
│
├── 📁 instance/                # 🗄️ Flask实例文件
│   └── papers.db               # 论文数据库
│
├── 📄 配置文件
│   ├── .gitignore              # Git忽略规则
│   ├── requirements.txt        # Python依赖
│   ├── LICENSE                 # 许可证
│   └── README.md               # 项目说明
│
└── 📁 .venv/                   # 🐍 Python虚拟环境

```

## 🚀 快速开始

### 1. 运行主程序
```bash
python ai_lab_repo.py --yaml-location "experiment_configs/MATH_agentlab.yaml"
```

### 2. 启动Web界面
```bash
python app.py
# 访问 http://127.0.0.1:5000
```

## 📝 关键改进

### ✅ 文件组织
- **实验结果** → `experiments/` 目录（带时间戳）
- **文档** → `docs/` 目录
- **数据** → `data/` 目录
- **脚本** → `scripts/` 目录

### ✅ Git管理
- 实验结果和数据文件被忽略
- 保持仓库整洁

### ✅ 目录命名
- 使用时间戳：`YYYYMMDD_HHMMSS_主题`
- 自动清理特殊字符
- 不会覆盖历史实验

## 📖 详细文档

- [改进方案](docs/改进方案.md) - 系统改进建议和实施计划
- [启动说明](docs/启动说明.md) - 详细的启动和配置指南
- [使用示例](docs/使用示例.md) - 使用案例和示例

## 🔍 查找文件

| 你想找... | 位置 |
|----------|------|
| 如何启动 | `docs/启动说明.md` |
| 使用示例 | `docs/使用示例.md` |
| 实验结果 | `experiments/[时间戳]_[主题]/` |
| 配置文件 | `experiment_configs/*.yaml` |
| 测试脚本 | `scripts/` |
| 生成的代码 | `experiments/*/src/` |
| 实验报告 | `experiments/*/reports/` |

## 💡 提示

- 每次运行会创建新的时间戳目录
- 历史实验不会被覆盖
- 所有生成文件都在 `experiments/` 下
- 根目录保持整洁
