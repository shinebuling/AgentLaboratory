# -*- coding: utf-8 -*-
"""
国际化消息配置文件
支持中英文切换，提供统一的消息接口
"""

MESSAGES = {
    'zh_CN': {
        # ==================== 阶段名称 ====================
        'literature review': '文献综述',
        'plan formulation': '计划制定',
        'data preparation': '数据准备',
        'running experiments': '运行实验',
        'results interpretation': '结果解读',
        'report writing': '报告撰写',
        'report refinement': '报告完善',
        
        # ==================== 通用提示信息 ====================
        'beginning_phase': '开始阶段',
        'beginning_subtask': '开始子任务',
        'phase_completed': '阶段完成',
        'subtask_completed': '子任务完成',
        'seconds': '秒',
        'minutes': '分钟',
        'saving_file': '正在保存文件',
        'file_saved': '文件已保存',
        'error_occurred': '发生错误',
        'warning': '警告',
        'info': '信息',
        'duration': '耗时',
        
        # ==================== 实验相关 ====================
        'lab': '实验室',
        'paper': '论文',
        'experiment': '实验',
        'iteration': '迭代',
        'step': '步骤',
        'total_steps': '总步数',
        'current_step': '当前步骤',
        'progress': '进度',
        
        # ==================== 文件操作 ====================
        'loading_file': '加载文件',
        'saving_to': '保存到',
        'file_not_found': '文件未找到',
        'file_exists': '文件已存在',
        'creating_directory': '创建目录',
        'directory_created': '目录已创建',
        
        # ==================== Agent相关 ====================
        'agent_phd': 'PhD学生智能体',
        'agent_postdoc': '博士后智能体',
        'agent_professor': '教授智能体',
        'agent_mle': '机器学习工程师',
        'agent_swe': '软件工程师',
        'agent_response': '智能体响应',
        'agent_thinking': '智能体思考中',
        
        # ==================== LLM相关 ====================
        'llm_model': 'LLM模型',
        'llm_calling': '正在调用LLM',
        'llm_response_received': 'LLM响应已接收',
        'prompt': '提示词',
        'response': '响应',
        'tokens_used': 'Token使用量',
        'cost_estimate': '预估成本',
        
        # ==================== 状态信息 ====================
        'status_running': '运行中',
        'status_completed': '已完成',
        'status_failed': '失败',
        'status_pending': '等待中',
        'status_success': '成功',
        
        # ==================== 分隔符样式 ====================
        'separator_phase': '=' * 80,
        'separator_subtask': '-' * 60,
        'separator_section': '*' * 50,
        'separator_dialogue': '#' * 40,
        'separator_short': '-' * 30,
        
        # ==================== 对话和输出 ====================
        'dialogue': '对话',
        'output': '输出',
        'input': '输入',
        'result': '结果',
        'summary': '摘要',
        'details': '详情',
        'description': '描述',
        
        # ==================== 错误和调试 ====================
        'error': '错误',
        'exception': '异常',
        'traceback': '堆栈跟踪',
        'debug_info': '调试信息',
        'retry': '重试',
        'skip': '跳过',
        'abort': '中止',
    },
    
    'en_US': {
        # ==================== Phase Names ====================
        'literature review': 'Literature Review',
        'plan formulation': 'Plan Formulation',
        'data preparation': 'Data Preparation',
        'running experiments': 'Running Experiments',
        'results interpretation': 'Results Interpretation',
        'report writing': 'Report Writing',
        'report refinement': 'Report Refinement',
        
        # ==================== General Messages ====================
        'beginning_phase': 'Beginning Phase',
        'beginning_subtask': 'Beginning Subtask',
        'phase_completed': 'Phase Completed',
        'subtask_completed': 'Subtask Completed',
        'seconds': 'seconds',
        'minutes': 'minutes',
        'saving_file': 'Saving File',
        'file_saved': 'File Saved',
        'error_occurred': 'Error Occurred',
        'warning': 'Warning',
        'info': 'Info',
        'duration': 'Duration',
        
        # ==================== Experiment Related ====================
        'lab': 'Lab',
        'paper': 'Paper',
        'experiment': 'Experiment',
        'iteration': 'Iteration',
        'step': 'Step',
        'total_steps': 'Total Steps',
        'current_step': 'Current Step',
        'progress': 'Progress',
        
        # ==================== File Operations ====================
        'loading_file': 'Loading File',
        'saving_to': 'Saving to',
        'file_not_found': 'File Not Found',
        'file_exists': 'File Exists',
        'creating_directory': 'Creating Directory',
        'directory_created': 'Directory Created',
        
        # ==================== Agent Related ====================
        'agent_phd': 'PhD Student Agent',
        'agent_postdoc': 'Postdoc Agent',
        'agent_professor': 'Professor Agent',
        'agent_mle': 'ML Engineer Agent',
        'agent_swe': 'Software Engineer Agent',
        'agent_response': 'Agent Response',
        'agent_thinking': 'Agent Thinking',
        
        # ==================== LLM Related ====================
        'llm_model': 'LLM Model',
        'llm_calling': 'Calling LLM',
        'llm_response_received': 'LLM Response Received',
        'prompt': 'Prompt',
        'response': 'Response',
        'tokens_used': 'Tokens Used',
        'cost_estimate': 'Cost Estimate',
        
        # ==================== Status Info ====================
        'status_running': 'Running',
        'status_completed': 'Completed',
        'status_failed': 'Failed',
        'status_pending': 'Pending',
        'status_success': 'Success',
        
        # ==================== Separators ====================
        'separator_phase': '=' * 80,
        'separator_subtask': '-' * 60,
        'separator_section': '*' * 50,
        'separator_dialogue': '#' * 40,
        'separator_short': '-' * 30,
        
        # ==================== Dialogue and Output ====================
        'dialogue': 'Dialogue',
        'output': 'Output',
        'input': 'Input',
        'result': 'Result',
        'summary': 'Summary',
        'details': 'Details',
        'description': 'Description',
        
        # ==================== Error and Debug ====================
        'error': 'Error',
        'exception': 'Exception',
        'traceback': 'Traceback',
        'debug_info': 'Debug Info',
        'retry': 'Retry',
        'skip': 'Skip',
        'abort': 'Abort',
    }
}


class I18nManager:
    """国际化管理器"""
    
    def __init__(self, language='zh_CN'):
        """
        初始化国际化管理器
        @param language: 语言代码，'zh_CN' 或 'en_US'
        """
        self.language = language if language in MESSAGES else 'zh_CN'
        self.messages = MESSAGES[self.language]
    
    def get(self, key, default=None):
        """
        获取翻译文本
        @param key: 消息键
        @param default: 默认值（如果键不存在）
        @return: 翻译后的文本
        """
        return self.messages.get(key, default or key)
    
    def set_language(self, language):
        """
        切换语言
        @param language: 语言代码
        """
        if language in MESSAGES:
            self.language = language
            self.messages = MESSAGES[language]
    
    def format_phase_header(self, phase_name):
        """
        格式化阶段标题
        @param phase_name: 阶段名称（英文）
        @return: 格式化后的标题字符串
        """
        separator = self.messages['separator_phase']
        translated_phase = self.messages.get(phase_name, phase_name)
        beginning = self.messages['beginning_phase']
        return f"\n{separator}\n{beginning}: {translated_phase}\n{separator}"
    
    def format_subtask_header(self, subtask_name, lab_index=None, paper_index=None):
        """
        格式化子任务标题
        @param subtask_name: 子任务名称
        @param lab_index: 实验室索引（可选）
        @param paper_index: 论文索引（可选）
        @return: 格式化后的标题字符串
        """
        separator = self.messages['separator_subtask']
        translated_subtask = self.messages.get(subtask_name, subtask_name)
        beginning = self.messages['beginning_subtask']
        
        header = f"\n{separator}\n{beginning}: {translated_subtask}"
        
        if lab_index is not None and paper_index is not None:
            lab = self.messages['lab']
            paper = self.messages['paper']
            header += f" [{lab} #{lab_index} {paper} #{paper_index}]"
        
        header += f"\n{separator}"
        return header
    
    def format_completion(self, task_name, duration):
        """
        格式化完成信息
        @param task_name: 任务名称
        @param duration: 持续时间（秒）
        @return: 格式化后的完成信息
        """
        translated_task = self.messages.get(task_name, task_name)
        completed = self.messages['phase_completed']
        duration_text = self.messages['duration']
        seconds = self.messages['seconds']
        
        return f"{completed}: {translated_task} ({duration_text}: {duration:.2f}{seconds})"
    
    def format_dialogue_header(self, speaker, phase=None):
        """
        格式化对话标题
        @param speaker: 说话者
        @param phase: 阶段名称（可选）
        @return: 格式化后的对话标题
        """
        separator = self.messages['separator_dialogue']
        dialogue = self.messages['dialogue']
        
        phase_info = ""
        if phase:
            translated_phase = self.messages.get(phase, phase)
            phase_info = f" [{translated_phase}]"
        
        return f"\n{separator}\n{speaker}{phase_info} {dialogue}:\n{separator}"
    
    def format_experiment_info(self, lab_index, paper_index):
        """
        格式化实验信息
        @param lab_index: 实验室索引
        @param paper_index: 论文索引
        @return: 格式化后的实验信息
        """
        lab = self.messages['lab']
        paper = self.messages['paper']
        return f"@@ {lab} #{lab_index} {paper} #{paper_index} @@"
    
    def format_file_saved(self, filepath, filetype):
        """
        格式化文件保存信息
        @param filepath: 文件路径
        @param filetype: 文件类型
        @return: 格式化后的保存信息
        """
        file_saved = self.messages['file_saved']
        return f"✓ {file_saved}: {filetype} -> {filepath}"
    
    def format_progress(self, current, total, description=""):
        """
        格式化进度信息
        @param current: 当前进度
        @param total: 总进度
        @param description: 描述（可选）
        @return: 格式化后的进度信息
        """
        progress = self.messages['progress']
        percentage = (current / total * 100) if total > 0 else 0
        
        result = f"{progress}: {current}/{total} ({percentage:.1f}%)"
        if description:
            result += f" - {description}"
        
        return result


# 全局实例（默认中文）
_global_i18n = I18nManager('zh_CN')


def get_i18n():
    """
    获取全局国际化管理器实例
    @return: I18nManager实例
    """
    return _global_i18n


def set_language(language):
    """
    设置全局语言
    @param language: 语言代码
    """
    _global_i18n.set_language(language)


# 便捷函数
def translate(key, default=None):
    """
    快速翻译函数
    @param key: 消息键
    @param default: 默认值
    @return: 翻译后的文本
    """
    return _global_i18n.get(key, default)
