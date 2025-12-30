"""
Gradio前端界面 - Agent Laboratory (解耦版本)
只负责配置收集和结果展示，通过调用原有命令行工具来执行实验
"""

import gradio as gr
import os
import subprocess
import threading
import time
from datetime import datetime
import yaml
from pathlib import Path
import queue


class GradioInterface:
    def __init__(self):
        self.running_processes = {}
        self.log_queues = {}
        self.accumulated_logs = {}  # 累积的日志
        
    def load_experiment_configs(self):
        """加载实验配置列表"""
        config_dir = Path("experiment_configs")
        if not config_dir.exists():
            return []
        return [f.name for f in config_dir.glob("*.yaml")]
    
    def load_yaml_config(self, config_file):
        """加载YAML配置文件并返回配置信息"""
        if not config_file:
            return "请选择配置文件"
        
        try:
            config_path = Path("experiment_configs") / config_file
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 格式化显示配置
            config_str = "### 当前配置\n\n"
            for key, value in config.items():
                if key == 'task-notes':
                    config_str += f"**{key}**: [详细任务说明]\n\n"
                else:
                    config_str += f"**{key}**: `{value}`\n\n"
            return config_str
        except Exception as e:
            return f"❌ 加载配置失败: {str(e)}"
    
    def create_config_file(self, research_topic, model_backend, api_key, deepseek_key, 
                          num_papers, max_steps, language, compile_latex, use_agentrxiv):
        """根据用户输入创建临时配置文件"""
        if not research_topic:
            return None, "❌ 请输入研究主题"
        
        # 生成临时配置文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        config_filename = f"temp_config_{timestamp}.yaml"
        config_path = Path("experiment_configs") / config_filename
        
        # 构建配置
        config = {
            'research-topic': research_topic,
            'llm-backend': model_backend,
            'language': language,
            'num-papers-lit-review': int(num_papers),
            'num-papers-to-write': 1,
            'mlesolver-max-steps': int(max_steps / 10),  # 简化配置
            'papersolver-max-steps': int(max_steps / 10),
            'compile-latex': compile_latex,
            'copilot-mode': False,  # 自动模式
            'load-previous': False,
            'parallel-labs': False,
            'except-if-fail': False,
            'agentRxiv': use_agentrxiv,
            'lab-index': 1,
            'task-notes': {
                'plan-formulation': [],
                'data-preparation': [],
                'running-experiments': [],
                'results-interpretation': [],
                'report-writing': []
            }
        }
        
        # 添加API配置
        if api_key:
            config['api-key'] = api_key
        if deepseek_key:
            config['gitee-api-key'] = deepseek_key
            config['gitee-base-url'] = 'https://ai.gitee.com/v1'
        
        # 保存配置文件
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
            return str(config_path), f"✅ 配置文件已创建: {config_filename}"
        except Exception as e:
            return None, f"❌ 创建配置文件失败: {str(e)}"
    
    def start_experiment(self, research_topic, model_backend, api_key, deepseek_key, 
                        num_papers, max_steps, language, compile_latex, use_agentrxiv):
        """启动实验（通过调用原有命令行工具）"""
        # 创建配置文件
        config_path, message = self.create_config_file(
            research_topic, model_backend, api_key, deepseek_key,
            num_papers, max_steps, language, compile_latex, use_agentrxiv
        )
        
        if not config_path:
            return message
        
        # 准备命令
        python_exe = sys.executable
        cmd = [python_exe, "ai_lab_repo.py", "--yaml-location", config_path]
        
        # 在后台线程中运行
        experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_queue = queue.Queue()
        self.log_queues[experiment_id] = log_queue
        
        thread = threading.Thread(
            target=self._run_subprocess,
            args=(cmd, experiment_id, log_queue)
        )
        thread.daemon = True
        thread.start()
        
        return f"""✅ 实验已启动！

**研究主题**: {research_topic}
**模型**: {model_backend}
**配置文件**: {config_path}

实验正在后台运行，请在"实时日志"标签页查看进度。
实验完成后，结果会保存在 `experiments/` 目录。
"""
    
    def _run_subprocess(self, cmd, experiment_id, log_queue):
        """在子进程中运行命令并捕获输出"""
        try:
            log_queue.put("🚀 启动实验进程...\n")
            log_queue.put(f"📝 命令: {' '.join(cmd)}\n\n")
            
            # 设置环境变量，强制使用UTF-8编码
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                env=env,
                encoding='utf-8',
                errors='replace'
            )
            
            self.running_processes[experiment_id] = process
            
            # 实时读取输出
            for line in iter(process.stdout.readline, ''):
                if line:
                    log_queue.put(line)
            
            process.wait()
            
            if process.returncode == 0:
                log_queue.put("\n✅ 实验完成！\n")
            else:
                log_queue.put(f"\n❌ 实验失败，退出码: {process.returncode}\n")
                
        except Exception as e:
            log_queue.put(f"\n❌ 执行出错: {str(e)}\n")
        finally:
            if experiment_id in self.running_processes:
                del self.running_processes[experiment_id]
    
    def get_logs(self):
        """获取实时日志"""
        if not self.log_queues:
            return "暂无运行中的实验"
        
        # 获取最新实验的日志
        latest_id = list(self.log_queues.keys())[-1]
        log_queue = self.log_queues[latest_id]
        
        # 初始化该实验的日志累积器
        if latest_id not in self.accumulated_logs:
            self.accumulated_logs[latest_id] = []
        
        # 从队列中取出新日志并累积
        while not log_queue.empty():
            try:
                line = log_queue.get_nowait()
                self.accumulated_logs[latest_id].append(line)
            except queue.Empty:
                break
        
        # 返回累积的所有日志
        if not self.accumulated_logs[latest_id]:
            return "等待日志输出..."
        
        return "".join(self.accumulated_logs[latest_id])
    
    def list_experiment_results(self):
        """列出所有实验结果"""
        exp_dir = Path("experiments")
        if not exp_dir.exists():
            return "暂无实验结果"
        
        experiments = sorted(
            [d for d in exp_dir.iterdir() if d.is_dir()], 
            key=lambda x: x.stat().st_mtime, 
            reverse=True
        )
        
        if not experiments:
            return "暂无实验结果"
        
        result_str = "## 实验结果目录\n\n"
        for exp in experiments[:10]:
            result_str += f"📁 **{exp.name}**\n"
            
            # 检查关键文件
            report_file = exp / "reports" / "report.txt"
            if report_file.exists():
                result_str += f"   - ✅ 研究报告已生成\n"
            
            code_dir = exp / "src"
            if code_dir.exists() and list(code_dir.glob("*.py")):
                result_str += f"   - ✅ 实验代码已生成\n"
            
            result_str += f"   - 📂 路径: `{exp}`\n\n"
        
        return result_str
    
    def read_experiment_report(self, exp_dir_name):
        """读取实验报告"""
        if not exp_dir_name:
            return "请输入实验目录名"
        
        report_path = Path("experiments") / exp_dir_name / "reports" / "report.txt"
        if not report_path.exists():
            return f"❌ 报告文件不存在: {report_path}"
        
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"# 实验报告\n\n{content}"
        except Exception as e:
            return f"❌ 读取失败: {str(e)}"


def create_gradio_interface():
    """创建Gradio界面"""
    interface = GradioInterface()
    
    with gr.Blocks(title="Agent Laboratory - AI研究助手") as demo:
        gr.Markdown("""
        # 🔬 Agent Laboratory - AI研究助手
        
        使用LLM驱动的多Agent系统自动执行研究工作流：文献综述、实验设计、代码实现、结果分析和报告撰写。
        
        ---
        """)
        
        with gr.Tabs():
            # Tab 1: 启动实验
            with gr.Tab("🚀 启动实验"):
                gr.Markdown("### 配置你的研究实验")
                
                with gr.Row():
                    with gr.Column(scale=2):
                        research_topic = gr.Textbox(
                            label="研究主题",
                            placeholder="例如: 探索如何将3DGS的致密化操作用强化学习的方式代替",
                            lines=3
                        )
                        
                        with gr.Row():
                            model_backend = gr.Dropdown(
                                choices=["DeepSeek-V3", "DeepSeek-R1", "gpt-4o", "gpt-4o-mini", "deepseek-chat"],
                                value="DeepSeek-V3",
                                label="LLM模型"
                            )
                            language = gr.Dropdown(
                                choices=["Chinese", "English"],
                                value="Chinese",
                                label="语言"
                            )
                        
                        with gr.Row():
                            api_key = gr.Textbox(
                                label="OpenAI API Key (可选)",
                                type="password",
                                placeholder="sk-..."
                            )
                            deepseek_key = gr.Textbox(
                                label="GiteeAI API Key",
                                type="password",
                                placeholder="输入Gitee AI密钥"
                            )
                        
                        with gr.Row():
                            num_papers = gr.Slider(
                                minimum=1, maximum=20, value=5, step=1,
                                label="文献综述论文数量"
                            )
                            max_steps = gr.Slider(
                                minimum=10, maximum=100, value=30, step=10,
                                label="最大步数"
                            )
                        
                        with gr.Row():
                            compile_latex = gr.Checkbox(
                                value=False,
                                label="编译LaTeX"
                            )
                            use_agentrxiv = gr.Checkbox(
                                value=False,
                                label="使用AgentRxiv"
                            )
                        
                        start_btn = gr.Button("▶️ 启动实验", variant="primary", size="lg")
                        status_output = gr.Markdown()
                    
                    with gr.Column(scale=1):
                        gr.Markdown("### 💡 使用提示")
                        gr.Markdown("""
                        1. **输入研究主题**: 详细描述你的研究问题
                        2. **选择模型**: 推荐使用DeepSeek-V3
                        3. **配置API密钥**: 
                           - DeepSeek模型 → 输入Gitee AI密钥
                           - OpenAI模型 → 输入OpenAI密钥
                        4. **调整参数**: 根据需要设置论文数量和步数
                        5. **启动实验**: 点击按钮开始
                        
                        ⚠️ **注意**: 
                        - 实验在后台独立进程中运行
                        - 可能需要较长时间（30分钟到数小时）
                        - 即使关闭浏览器，实验也会继续运行
                        """)
                
                start_btn.click(
                    fn=interface.start_experiment,
                    inputs=[research_topic, model_backend, api_key, deepseek_key, 
                           num_papers, max_steps, language, compile_latex, use_agentrxiv],
                    outputs=status_output
                )
            
            # Tab 2: 实时日志
            with gr.Tab("📊 实时日志"):
                gr.Markdown("### 实验运行日志")
                log_display = gr.Textbox(
                    label="日志输出",
                    lines=25,
                    max_lines=40,
                    interactive=False
                )
                refresh_log_btn = gr.Button("🔄 刷新日志")
                
                refresh_log_btn.click(
                    fn=interface.get_logs,
                    outputs=log_display
                )
                
                # 使用Timer组件实现自动刷新
                timer = gr.Timer(value=2, active=True)
                timer.tick(fn=interface.get_logs, outputs=log_display)
            
            # Tab 3: 实验结果
            with gr.Tab("📁 实验结果"):
                gr.Markdown("### 查看实验结果")
                
                with gr.Row():
                    with gr.Column():
                        results_display = gr.Markdown()
                        refresh_results_btn = gr.Button("🔄 刷新结果列表")
                        
                        refresh_results_btn.click(
                            fn=interface.list_experiment_results,
                            outputs=results_display
                        )
                        
                        demo.load(
                            fn=interface.list_experiment_results,
                            outputs=results_display
                        )
                    
                    with gr.Column():
                        exp_dir_input = gr.Textbox(
                            label="实验目录名",
                            placeholder="例如: 20251225_143812_你的研究主题"
                        )
                        read_report_btn = gr.Button("📖 读取报告")
                        report_display = gr.Markdown()
                        
                        read_report_btn.click(
                            fn=interface.read_experiment_report,
                            inputs=exp_dir_input,
                            outputs=report_display
                        )
            
            # Tab 4: 配置管理
            with gr.Tab("⚙️ 配置管理"):
                gr.Markdown("### 实验配置文件")
                
                config_dropdown = gr.Dropdown(
                    choices=interface.load_experiment_configs(),
                    label="选择配置文件"
                )
                load_config_btn = gr.Button("📂 加载配置")
                config_display = gr.Markdown()
                
                load_config_btn.click(
                    fn=interface.load_yaml_config,
                    inputs=config_dropdown,
                    outputs=config_display
                )
                
                gr.Markdown("""
                ### 创建新配置
                
                你可以在 `experiment_configs/` 目录下创建新的YAML配置文件。
                
                或者在"启动实验"标签页填写参数后，系统会自动生成配置文件。
                """)
        
        gr.Markdown("""
        ---
        ### 📚 相关资源
        - [项目文档](https://github.com/SamuelSchmidgall/AgentLaboratory)
        - [论文](https://arxiv.org/pdf/2501.04227)
        
        **版权所有** © 2025 Agent Laboratory
        """)
    
    return demo


if __name__ == "__main__":
    import sys
    
    print("🚀 启动 Agent Laboratory Gradio 界面 (解耦版本)...")
    print("=" * 60)
    
    # 创建必要的目录
    os.makedirs("experiments", exist_ok=True)
    os.makedirs("experiment_configs", exist_ok=True)
    
    # 创建并启动界面
    demo = create_gradio_interface()
    
    # 启动服务器
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )
