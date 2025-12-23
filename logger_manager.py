"""
Agent Laboratory 日志管理系统
提供多级日志记录功能，包括完整执行日志、LLM交互日志、错误日志和阶段日志
"""

import logging
import sys
import os
from datetime import datetime


class TeeOutput:
    """同时输出到终端和文件的流"""
    
    def __init__(self, file_handle, original_stream):
        self.file = file_handle
        self.stream = original_stream
    
    def write(self, data):
        """写入数据到终端和文件"""
        self.stream.write(data)
        self.file.write(data)
        self.file.flush()  # 立即刷新到文件
    
    def flush(self):
        """刷新两个流"""
        self.stream.flush()
        self.file.flush()
    
    def __getattr__(self, name):
        """代理其他属性到原始流"""
        return getattr(self.stream, name)
    
    def __getstate__(self):
        """序列化时排除文件句柄"""
        return {'stream': self.stream}
    
    def __setstate__(self, state):
        """反序列化时恢复（文件句柄将在 AgentLabLogger 中重新设置）"""
        self.__dict__.update(state)
        self.file = None  # 临时设置为 None


class AgentLabLogger:
    """统一的日志管理系统"""
    
    def __init__(self, log_dir="logs"):
        """
        初始化日志管理器
        @param log_dir: 日志目录路径
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # 重定向stdout和stderr到文件（同时保留终端输出）
        self.full_log_file = open(f"{log_dir}/full_execution.log", "a", encoding="utf-8")
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        
        # 使用TeeOutput同时输出到终端和文件
        sys.stdout = TeeOutput(self.full_log_file, self.original_stdout)
        sys.stderr = TeeOutput(self.full_log_file, self.original_stderr)
        
        # 清除所有现有的handlers，避免重复
        for logger_name in ['full_execution', 'llm_interactions', 'errors', 'phases']:
            logger = logging.getLogger(logger_name)
            logger.handlers.clear()
        
        # 1. 完整执行日志（所有输出）
        self.full_logger = self._create_logger(
            'full_execution',
            f'{log_dir}/full_execution.log',
            logging.DEBUG
        )
        
        # 2. LLM交互日志（对话记录）
        self.llm_logger = self._create_logger(
            'llm_interactions',
            f'{log_dir}/llm_interactions.log',
            logging.INFO
        )
        
        # 3. 错误日志（仅错误和警告）
        self.error_logger = self._create_logger(
            'errors',
            f'{log_dir}/errors.log',
            logging.WARNING
        )
        
        # 4. 阶段日志（各阶段完成情况）
        self.phase_logger = self._create_logger(
            'phases',
            f'{log_dir}/phases.log',
            logging.INFO
        )
        
        self.current_phase = None
        self.phase_start_time = None
    
    def _create_logger(self, name, filename, level):
        """
        创建单个logger
        @param name: logger名称
        @param filename: 日志文件名
        @param level: 日志级别
        @return: logger对象
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False  # 防止传播到root logger
        
        # 文件处理器（UTF-8编码支持中文）
        fh = logging.FileHandler(filename, encoding='utf-8', mode='a')
        fh.setLevel(level)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        return logger
    
    def info(self, message):
        """记录普通信息"""
        self.full_logger.info(message)
    
    def debug(self, message):
        """记录调试信息"""
        self.full_logger.debug(message)
    
    def warning(self, message):
        """记录警告信息"""
        self.full_logger.warning(message)
        self.error_logger.warning(message)
    
    def error(self, message, exception=None):
        """
        记录错误信息
        @param message: 错误消息
        @param exception: 异常对象（可选）
        """
        self.full_logger.error(message)
        self.error_logger.error(message)
        if exception:
            self.error_logger.exception(exception)
            self.full_logger.exception(exception)
    
    def log_llm_interaction(self, model, phase, prompt, response, step=None):
        """
        记录LLM交互
        @param model: 模型名称
        @param phase: 阶段名称
        @param prompt: 提示词
        @param response: 模型响应
        @param step: 步骤号（可选）
        """
        separator = "=" * 80
        step_info = f" | 步骤: {step}" if step is not None else ""
        
        self.llm_logger.info(f"\n{separator}")
        self.llm_logger.info(f"模型: {model} | 阶段: {phase}{step_info}")
        self.llm_logger.info(f"{separator}")
        
        # 记录提示词（截断过长的内容）
        prompt_preview = prompt[:1000] + "..." if len(prompt) > 1000 else prompt
        self.llm_logger.info(f"提示词:\n{prompt_preview}")
        
        # 记录响应（截断过长的内容）
        response_preview = response[:1000] + "..." if len(response) > 1000 else response
        self.llm_logger.info(f"\n响应:\n{response_preview}")
        self.llm_logger.info(f"{separator}\n")
        
        # 同时记录到完整日志
        self.full_logger.debug(f"LLM调用 [{phase}] - 模型: {model}")
    
    def log_phase_start(self, phase_name):
        """
        记录阶段开始
        @param phase_name: 阶段名称
        """
        self.current_phase = phase_name
        self.phase_start_time = datetime.now()
        
        # 如果有i18n实例，使用国际化格式
        if hasattr(self, 'i18n'):
            msg = self.i18n.format_phase_header(phase_name)
            log_msg = f"开始: {self.i18n.get(phase_name, phase_name)}"
        else:
            separator = "*" * 50
            msg = f"\n{separator}\n开始阶段: {phase_name}\n{separator}"
            log_msg = f"开始: {phase_name}"
        
        self.full_logger.info(msg)
        self.phase_logger.info(log_msg)
    
    def log_subtask_start(self, subtask_name, lab_index=None, paper_index=None):
        """
        记录子任务开始
        @param subtask_name: 子任务名称
        @param lab_index: 实验室索引（可选）
        @param paper_index: 论文索引（可选）
        """
        # 如果有i18n实例，使用国际化格式
        if hasattr(self, 'i18n'):
            msg = self.i18n.format_subtask_header(subtask_name, lab_index, paper_index)
            translated = self.i18n.get(subtask_name, subtask_name)
            log_msg = f"  → 子任务: {translated}"
        else:
            separator = "&" * 30
            if lab_index is not None and paper_index is not None:
                msg = f"\n{separator}\n[实验室 #{lab_index} 论文 #{paper_index}] 开始子任务: {subtask_name}\n{separator}"
            else:
                msg = f"\n{separator}\n开始子任务: {subtask_name}\n{separator}"
            log_msg = f"  → 子任务: {subtask_name}"
        
        self.full_logger.info(msg)
        self.phase_logger.info(log_msg)
    
    def log_phase_end(self, phase_name, duration):
        """
        记录阶段结束
        @param phase_name: 阶段名称
        @param duration: 持续时间（秒）
        """
        # 如果有i18n实例，使用国际化格式
        if hasattr(self, 'i18n'):
            msg = self.i18n.format_completion(phase_name, duration)
            translated = self.i18n.get(phase_name, phase_name)
            log_msg = f"完成: {translated} (耗时: {duration:.2f}秒)"
        else:
            msg = f"阶段 '{phase_name}' 完成，耗时: {duration:.2f} 秒"
            log_msg = f"完成: {phase_name} (耗时: {duration:.2f}秒)"
        
        self.full_logger.info(msg)
        self.phase_logger.info(log_msg)
    
    def log_subtask_end(self, subtask_name, duration, steps=None):
        """
        记录子任务结束
        @param subtask_name: 子任务名称
        @param duration: 持续时间（秒）
        @param steps: 步骤数（可选）
        """
        step_info = f", 步骤数: {steps}" if steps is not None else ""
        msg = f"子任务 '{subtask_name}' 完成，耗时: {duration:.2f} 秒{step_info}"
        self.full_logger.info(msg)
        self.phase_logger.info(f"  ✓ 完成: {subtask_name} ({duration:.2f}秒{step_info})")
    
    def log_file_saved(self, filepath, filetype="文件"):
        """
        记录文件保存
        @param filepath: 文件路径
        @param filetype: 文件类型描述
        """
        msg = f"✓ 已保存{filetype}: {filepath}"
        self.full_logger.info(msg)
    
    def log_agent_response(self, agent_name, response, phase=None):
        """
        记录Agent响应
        @param agent_name: Agent名称
        @param response: 响应内容
        @param phase: 阶段名称（可选）
        """
        # 所有输出已经通过stdout重定向到full_execution.log
        # 这里只需要记录到专门的日志文件
        phase_info = f" [{phase}]" if phase else ""
        self.full_logger.debug(f"\n{'='*60}")
        self.full_logger.debug(f"{agent_name}{phase_info} 响应:")
        self.full_logger.debug(f"{'='*60}")
        self.full_logger.debug(response)
        self.full_logger.debug(f"{'='*60}\n")
        self.full_logger.debug(f"{'='*60}\n")
    
    def log_code_execution(self, code_preview, result_preview):
        """
        记录代码执行
        @param code_preview: 代码预览
        @param result_preview: 结果预览
        """
        self.full_logger.info(f"执行代码:\n{code_preview}")
        self.full_logger.info(f"代码执行结果:\n{result_preview}")
    
    def log_experiment_info(self, lab_index, paper_index):
        """
        记录实验信息
        @param lab_index: 实验室索引
        @param paper_index: 论文索引
        """
        msg = f"@@ 实验室 #{lab_index} 论文 #{paper_index} @@"
        self.full_logger.info(msg)
    
    def log_dialogue(self, speaker, dialogue, phase=None):
        """
        记录对话
        @param speaker: 说话者
        @param dialogue: 对话内容
        @param phase: 阶段名称（可选）
        """
        separator = "#" * 40
        phase_info = f" [{phase}]" if phase else ""
        msg = f"\n{separator}\n{speaker}{phase_info} 对话:\n{dialogue}\n{separator}"
        self.full_logger.info(msg)
    
    def log_reward_score(self, phase, score):
        """
        记录奖励分数
        @param phase: 阶段名称
        @param score: 分数
        """
        msg = f"{phase} 完成，奖励函数分数: {score}"
        self.full_logger.info(msg)
    
    def log_review_complete(self):
        """记录审查完成"""
        separator = "*" * 40
        msg = f"\n{separator}\n审查完成\n{separator}"
        self.full_logger.info(msg)
    
    def __getstate__(self):
        """
        序列化时调用，排除不可序列化的文件句柄和日志对象
        """
        state = self.__dict__.copy()
        # 移除不可序列化的对象
        state.pop('full_log_file', None)
        state.pop('original_stdout', None)
        state.pop('original_stderr', None)
        state.pop('full_logger', None)
        state.pop('llm_logger', None)
        state.pop('error_logger', None)
        state.pop('phase_logger', None)
        return state
    
    def __setstate__(self, state):
        """
        反序列化时调用，重新初始化文件句柄和日志对象
        """
        self.__dict__.update(state)
        
        # 重新打开文件和创建日志对象
        log_dir = self.log_dir
        
        # 重新打开重定向文件
        self.full_log_file = open(f"{log_dir}/full_execution.log", "a", encoding="utf-8")
        
        # 获取真正的原始流（防止重复嵌套 TeeOutput）
        if isinstance(sys.stdout, TeeOutput):
            self.original_stdout = sys.stdout.stream
        else:
            self.original_stdout = sys.stdout
            
        if isinstance(sys.stderr, TeeOutput):
            self.original_stderr = sys.stderr.stream
        else:
            self.original_stderr = sys.stderr
        
        # 使用TeeOutput同时输出到终端和文件
        sys.stdout = TeeOutput(self.full_log_file, self.original_stdout)
        sys.stderr = TeeOutput(self.full_log_file, self.original_stderr)
        
        # 重新创建日志对象
        self.full_logger = self._create_logger(
            'full_execution',
            f'{log_dir}/full_execution.log',
            logging.DEBUG
        )
        
        self.llm_logger = self._create_logger(
            'llm_interactions',
            f'{log_dir}/llm_interactions.log',
            logging.INFO
        )
        
        self.error_logger = self._create_logger(
            'errors',
            f'{log_dir}/errors.log',
            logging.WARNING
        )
        
        self.phase_logger = self._create_logger(
            'phases',
            f'{log_dir}/phases.log',
            logging.INFO
        )
    
    def close(self):
        """关闭所有日志处理器"""
        # 恢复原始stdout和stderr
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        
        # 关闭文件
        if hasattr(self, 'full_log_file') and not self.full_log_file.closed:
            self.full_log_file.close()
        
        # 关闭所有日志处理器
        for logger in [self.full_logger, self.llm_logger, self.error_logger, self.phase_logger]:
            for handler in logger.handlers:
                handler.close()
                logger.removeHandler(handler)


# 全局日志实例（用于简化调用）
_global_logger = None


def get_logger(log_dir=None):
    """
    获取全局日志实例
    @param log_dir: 日志目录（仅在首次调用时有效）
    @return: AgentLabLogger实例
    """
    global _global_logger
    if _global_logger is None and log_dir:
        _global_logger = AgentLabLogger(log_dir)
    return _global_logger


def set_logger(logger):
    """
    设置全局日志实例
    @param logger: AgentLabLogger实例
    """
    global _global_logger
    _global_logger = logger
