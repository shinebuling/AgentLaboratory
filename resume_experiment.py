"""
从之前中断的实验恢复执行
"""
import pickle
import sys
import os
import yaml
from pathlib import Path

# 导入必要的类定义以支持pickle反序列化
sys.path.insert(0, os.path.dirname(__file__))
from ai_lab_repo import LaboratoryWorkflow

def list_experiments():
    """列出所有可恢复的实验"""
    experiments_dir = Path("experiments")
    if not experiments_dir.exists():
        print("未找到experiments目录")
        return []
    
    experiments = []
    for exp_dir in sorted(experiments_dir.iterdir(), reverse=True):
        if exp_dir.is_dir():
            logs_dir = exp_dir / "logs"
            if logs_dir.exists():
                state_files = list(logs_dir.glob("state_*.pkl"))
                if state_files:
                    # 找到最新的状态文件
                    latest_state = max(state_files, key=lambda p: p.stat().st_mtime)
                    experiments.append({
                        'dir': exp_dir,
                        'name': exp_dir.name,
                        'latest_state': latest_state.name,
                        'time': latest_state.stat().st_mtime
                    })
    return experiments

def resume_experiment(exp_dir):
    """从指定实验目录恢复执行"""
    exp_path = Path(exp_dir)
    logs_dir = exp_path / "logs"
    
    if not logs_dir.exists():
        print(f"错误: {logs_dir} 不存在")
        return False
    
    # 查找所有状态文件
    state_files = sorted(logs_dir.glob("state_*.pkl"), 
                        key=lambda p: p.stat().st_mtime, 
                        reverse=True)
    
    if not state_files:
        print(f"错误: 在 {logs_dir} 中未找到状态文件")
        return False
    
    latest_state_file = state_files[0]
    print(f"\n正在加载状态: {latest_state_file}")
    
    try:
        # 重新设置环境变量（从当前环境变量或配置文件加载）
        import yaml
        config_files = list(Path("experiment_configs").glob("temp_config_*.yaml"))
        if config_files:
            # 使用最新的配置文件
            latest_config = max(config_files, key=lambda p: p.stat().st_mtime)
            print(f"✓ 从配置文件加载API密钥: {latest_config.name}")
            with open(latest_config, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                if 'gitee-api-key' in config and not os.getenv('GITEE_API_KEY'):
                    os.environ['GITEE_API_KEY'] = config['gitee-api-key']
                    print(f"✓ 设置 GITEE_API_KEY 环境变量")
                if 'gitee-base-url' in config and not os.getenv('GITEE_BASE_URL'):
                    os.environ['GITEE_BASE_URL'] = config['gitee-base-url']
                if 'api-key' in config and not os.getenv('OPENAI_API_KEY'):
                    os.environ['OPENAI_API_KEY'] = config['api-key']
                if 'deepseek-api-key' in config and not os.getenv('DEEPSEEK_API_KEY'):
                    os.environ['DEEPSEEK_API_KEY'] = config['deepseek-api-key']
        
        # 加载状态
        with open(latest_state_file, "rb") as f:
            lab = pickle.load(f)
        
        print(f"✓ 成功加载实验状态")
        print(f"  研究主题: {lab.research_topic}")
        print(f"  实验目录: {lab.lab_dir}")
        print(f"\n阶段状态:")
        for phase, completed in lab.phase_status.items():
            status = "✓ 已完成" if completed else "○ 未完成"
            print(f"  {status} {phase}")
        
        # 继续执行研究
        print(f"\n继续执行实验...")
        lab.perform_research()
        
        return True
        
    except Exception as e:
        print(f"错误: 加载或执行失败 - {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("实验恢复工具")
    print("=" * 60)
    
    # 列出可恢复的实验
    experiments = list_experiments()
    
    if not experiments:
        print("\n未找到可恢复的实验")
        sys.exit(1)
    
    print(f"\n找到 {len(experiments)} 个可恢复的实验:\n")
    for i, exp in enumerate(experiments, 1):
        import datetime
        time_str = datetime.datetime.fromtimestamp(exp['time']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{i}. {exp['name']}")
        print(f"   最新状态: {exp['latest_state']} ({time_str})")
        print()
    
    # 选择实验
    if len(sys.argv) > 1:
        # 从命令行参数获取
        exp_dir = sys.argv[1]
    else:
        # 交互式选择
        try:
            choice = input(f"请选择要恢复的实验 (1-{len(experiments)}) 或按Enter选择最新的: ").strip()
            if not choice:
                choice = "1"
            idx = int(choice) - 1
            if idx < 0 or idx >= len(experiments):
                print("无效的选择")
                sys.exit(1)
            exp_dir = experiments[idx]['dir']
        except (ValueError, KeyboardInterrupt):
            print("\n已取消")
            sys.exit(0)
    
    # 恢复执行
    success = resume_experiment(exp_dir)
    sys.exit(0 if success else 1)
