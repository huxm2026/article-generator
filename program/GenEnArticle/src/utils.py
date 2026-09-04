from .config import *
from src.model_handler import VocabLogitsProcessor

import transformers
import language_tool_python
from threading import Lock
import inspect
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox

#---------------------------------------------------------------------------------------------
# 通用工具类
#     功能:
#         提供项目范围内的通用工具方法
#---------------------------------------------------------------------------------------------
class common_utils:
    #---------------------------------------------------------------------------------------------
    # 获取指定层级的父目录路径
    #     参数:
    #         path (str): 原始路径
    #         level (int): 向上追溯的目录层级，默认为1
    #     返回:
    #         str: 计算后的父目录路径
    #---------------------------------------------------------------------------------------------
    @staticmethod
    def get_parent_dir(path, level=1):
        for _ in range(level):
            path = os.path.dirname(path)
        return path
    
    #---------------------------------------------------------------------------------------------
    # 创建并获取输出目录路径
    #     返回:
    #         str: 生成的输出目录绝对路径
    #     异常:
    #         OSError: 目录创建失败时抛出
    #---------------------------------------------------------------------------------------------
    @staticmethod
    def get_output_dir():
        # 创建输出文件夹
        os.makedirs(articles_path, exist_ok=True)
        return articles_path
    
    #---------------------------------------------------------------------------------------------
    # 安全关机函数。
    #     此函数在检测到任务完成后，提示用户是否立即关机。如果用户确认，将根据操作系统类型执行关机命令。
    #     如果用户取消或在60秒内未响应，将不执行关机操作。
    #     Returns:
    #         bool: 成功执行关机命令返回True，否则返回False。
    #---------------------------------------------------------------------------------------------
    @staticmethod
    def safe_shutdown(shutdown_time_range=None):
        if shutdown_time_range:     # 时间段验证
            try:
                if not common_utils._validate_time_range(shutdown_time_range):      # 时间格式检查
                    return False
                if not common_utils._check_current_time_in_range(shutdown_time_range):  # 时间范围检查
                    print("当前不在允许关机的时间段")
                    return False
            except ValueError as e:
                messagebox.showerror("参数错误", f"无效时间格式: {str(e)}")
                return False
        root = tk.Tk()  # 创建隐藏的Tkinter根窗口
        root.withdraw()
        # 修改: 显式捕获 self 参数
        timer = threading.Timer(30, lambda : common_utils._execute_shutdown())   
        timer.start()               # 创建定时器，在30秒后自动执行休眠命令
        if not messagebox.askyesno(  # 移除 timeout 参数
            title="关机确认",
            message="检测到任务完成，是否立即关机？"
        ):
            timer.cancel()          # 用户取消或未响应时，取消定时器
            return False
        timer.cancel()              # 用户确认时，立即执行休眠命令
        return common_utils._execute_shutdown()
    @staticmethod
    def _execute_shutdown():
        """执行休眠命令"""
        try:
            system = platform.system()
            if system == "Windows":
                command = "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"     # 休眠命令
                # command = "shutdown /s /t 0"      # 关机命令
                print(f"执行休眠命令: {command}")
                result = os.system(command)
                if result == 0:
                    print("休眠命令执行成功")
                    return True
                else:
                    print("休眠命令执行失败")
                    return False
            else:
                raise NotImplementedError("仅支持 Windows 系统的休眠操作")
        except Exception as e:
            messagebox.showerror("系统错误", str(e))
        return False

    #---------------------------------------------------------------------------------------------
    # 验证时间范围格式有效性
    # 参数:
    # time_range (list): 包含开始和结束时间的列表
    # 返回:
    # bool: 如果时间范围格式正确，返回True，否则抛出ValueError异常
    #---------------------------------------------------------------------------------------------  
    @staticmethod  
    def _validate_time_range(time_range):
        if len(time_range) != 2:
            raise ValueError("时间范围需要包含开始和结束时间")
        time_format = "%H:%M"
        try:
            datetime.strptime(time_range[0], time_format)
            datetime.strptime(time_range[1], time_format)
        except ValueError:
            raise ValueError("时间格式应为 HH:MM")
        return True
    #---------------------------------------------------------------------------------------------
    # 检查当前时间是否在指定范围内
    #     参数:
    #         time_range -- 时间范围，格式为 ("开始时间", "结束时间")，时间格式为 "HH:MM"
    #     返回:
    #          布尔值，表示当前时间是否在指定范围内
    #---------------------------------------------------------------------------------------------    
    @staticmethod
    def _check_current_time_in_range(time_range):
        now = datetime.now().time()
        start = datetime.strptime(time_range[0], "%H:%M").time()
        end = datetime.strptime(time_range[1], "%H:%M").time()
        # 处理跨午夜情况（如 22:00-02:00）
        if start <= end:
            return start <= now <= end
        else:
            return now >= start or now <= end
    #---------------------------------------------------------------------------------------------
    # 将原始文章内容追加保存到指定文件中
    #       参数:
    #           article (str): 需要保存的原始文章内容文本
    #           current_theme (str): 当前文章对应的主题/分类标识
    #       返回值:
    #           None: 无返回值，直接将内容写入文件
    #---------------------------------------------------------------------------------------------  
    @staticmethod
    def save_original_articles(article,current_theme,current_keywords,rankmin,rankmax):
        def format_rank(r):
            return f"{r//1000}k" if r >= 1000 else str(r)
        if not hasattr(common_utils, "count"):
            common_utils.count = 0
        common_utils.count += 1
        rank_suffix = f"{format_rank(rankmin)}-{format_rank(rankmax)}"
        filename = os.path.join(common_utils.get_output_dir(), f"original_text{rank_suffix}.txt")
        article_content = f"\n{'='*10}Article #{common_utils.count}#{current_theme}#{'='*10}\n"
        article_content +=f"#current_keywords:{current_keywords}#\n</think>\n\n"
        article_content +=f"{article}\n[EOS]\n"
        with open(filename, "a", encoding="utf-8") as f:f.write(article_content)
    #---------------------------------------------------------------------------------------------
    # 测量函数执行时间的装饰器
    # 参数:
    #     func (Callable): 需要被测量执行时间的目标函数
    # 返回:
    #     Callable: 包装后的函数，执行时将输出执行时间信息
    #---------------------------------------------------------------------------------------------
    @staticmethod
    def _measure_time(func, *args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000  # 转换为毫秒
            return result, duration
    
    # #---------------------------------------------------------------------------------------------
    # # 将文本按文章分割
    # #     参数: text (str): 原始文本内容
    # #     返回: tuple[Dict]: 包含内容的字典列表
    # #---------------------------------------------------------------------------------------------
    # @staticmethod
    # def split_articles(text: str) -> tuple:  
    #     article = []
    #     pattern = r'(=+Article #\d+#([^#]+?)#=+)(.*?</think>.*?\[EOS\])'
    #     matches = re.findall(pattern, text, flags=re.DOTALL | re.IGNORECASE)
    #     for i, (header, theme, content) in enumerate(matches, start=1):
    #         current_theme = re.sub(r'\s+', ' ', theme).strip()
    #         keyword_line = ""
    #         keyword_pattern = r'^\s*(#current_keywords:([^#]+)#)\s*'
    #         keyword_match = re.match(keyword_pattern, content)
    #         if keyword_match:
    #             keyword_line = keyword_match.group(1)
    #             keywords = keyword_line.replace("#current_keywords:", "").replace("#", "")
    #             content = content[keyword_match.end():]
    #         # 生成包含主题的标题行
    #         title = f"{'='*10}Article #{i}#{current_theme}#{'='*10}\n"
    #         if keyword_line:        # 如果有关键字行，则在标题后添加
    #             article_content = f"{title}{keyword_line}\n{content}\n"
    #         else:
    #             article_content = f"{title}{content}\n"
    #         article.append(article_content)
    #     return '\n'.join(article)
    
    #---------------------------------------------------------------------------------------------
    # 将文本按文章分割
    #     参数: text (str): 原始文本内容
    #     返回: tuple[Dict]: 包含内容的字典列表
    #---------------------------------------------------------------------------------------------
    @staticmethod
    def split_articles(text: str):  
        pattern = r'(=+Article #\d+#([^#]+?)#=+)(.*?</think>.*?\[EOS\])'
        for matches in re.finditer(pattern, text, flags=re.DOTALL | re.IGNORECASE):
            theme = matches.group(2)
            content = matches.group(3)
            current_theme = re.sub(r'\s+', ' ', theme).strip()
            keyword_line = ""
            keyword_pattern = r'^\s*(#current_keywords:([^#]+)#)\s*'
            keyword_match = re.match(keyword_pattern, content)
            if keyword_match:
                keyword_line = keyword_match.group(1)
                keywords = keyword_line.replace("#current_keywords:", "").replace("#", "")
                content = content[keyword_match.end():]
            yield current_theme,keywords,content
#---------------------------------------------------------------------------------------------
# LanguageTool单例封装类
#     实现说明:
#         使用双检锁模式确保线程安全的单例实例
#     属性:
#         _instance: 单例实例存储
#         _lock: 线程安全锁
#---------------------------------------------------------------------------------------------
class LanguageToolSingleton:
    _instance = None
    _lock = Lock()
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = language_tool_python.LanguageTool(*args, **kwargs)
        return cls._instance 

#---------------------------------------------------------------------------------------------
# 内存监控管理器
#     功能:
#         实时监控内存使用情况并执行清理策略
#     属性:
#         memory_limit (int): 内存限制阈值（单位：字节）
#         enable_swap (bool): 是否启用虚拟内存交换
#---------------------------------------------------------------------------------------------
class MemoryMonitor:
    #---------------------------------------------------------------------------------------------
    # 初始化内存监控参数
    #     参数:
    #         memory_limit (int): 内存限制阈值，默认10GB
    #         enable_swap (bool): 是否启用清理策略，默认True
    #---------------------------------------------------------------------------------------------
    def __init__(self):
        self.memory_limit = 10 * 1024**3  # 10GB限制
        self.enable_swap = True  # 启用虚拟内存交换
        # 内存监控
        self.mem_monitor = psutil.Process(os.getpid())

    #---------------------------------------------------------------------------------------------
    # 内存监控线程函数
    #     功能说明:
    #         1. 持续监控进程内存使用
    #         2. 超过阈值时执行缓存清理
    #         3. 支持PyTorch内存缓存释放
    #     执行频率:
    #         每0.5秒检查一次内存状态
    #---------------------------------------------------------------------------------------------
    def _memory_monitor(self):
        """内存监控线程"""
        while True:
            mem = self.mem_monitor.memory_info().rss
            if mem > self.memory_limit:
                if self.enable_swap:
                    # 触发内存压缩
                    if hasattr(torch, 'empty_cache'):
                        torch.empty_cache()
                    # 清理生成缓存
                    self.past_key_values = None
                    time.sleep(1)
                else:
                    raise MemoryError("内存超出10GB限制")
            time.sleep(0.5)

#---------------------------------------------------------------------------------------------
# 模型测试类
#     功能:
#         提供模型验证相关功能方法
#---------------------------------------------------------------------------------------------
class test_model:
    #---------------------------------------------------------------------------------------------
    # 模型测试类类初始化方法
    #     参数:
    #         tokenizer: 文本分词器对象
    #     属性初始化:
    #         current_rankmax: 当前实际使用的最大词频
    #         expansion_threshold: 词库扩展阈值(0-1)
    #         expansion_step: 扩展步长比例
    #         allowed_words: 允许使用的词汇集合
    #---------------------------------------------------------------------------------------------
    def __init__(self,generator=None):
        self.generator = generator
        self.tokenizer = self.generator.tokenizer    
        self.model = self.generator.model
    #---------------------------------------------------------------------------------------------
    # 执行模型验证流程
    #     返回:
    #         bool: 验证结果
    #     验证内容:
    #         1. 模型文件完整性检查
    #         2. 模型架构参数验证
    #         3. 资源使用情况监控
    #         4. 文本生成质量测试
    #---------------------------------------------------------------------------------------------
    def verify_model(self):
        test_prompt = "Generate an English article about daily life:"
        try:
            processor = VocabLogitsProcessor(
                bias_tokens=[100], 
                tokenizer=self.tokenizer,
                bias=15.0)
            assert isinstance(processor, LogitsProcessor), "类型继承验证失败"
            assert callable(processor), "实例必须可调用"
            # ==================== 模型文件检查 ====================
            model_path = Path(MODEL_PATH)
            model_file = "model.safetensors" if deepseek_model_path else "pytorch_model.bin"
            print(f"模型文件存在: {(model_path / model_file).exists()}")
            print(f"模型结构: {type(self.model).__name__}")
            print(f"Transformers版本: {transformers.__version__}")
            if hasattr(self.model, 'generation_config'):
                print(f"生成配置: {self.model.generation_config}")  # 查看生成配置参数
            else:
                print("当前模型无 generation_config 属性")
            print(f"支持generate方法: {hasattr(self.model, 'generate')}")   # 查看支持的生成模式
            signature = inspect.signature(self.model.generate)
            print("当前模型支持的参数:", list(signature.parameters.keys()))
            print(f"使用设备: {self.model.device}")
            print(f"参数量: {sum(p.numel() for p in self.model.parameters()):,}")
            print(f"量化类型：{next(iter(self.model.parameters())).dtype}")
            print(f"Torch版本: {torch.__version__}")
            print(f"实际硬件: {'GPU' if torch.cuda.is_available() else 'CPU'}")
            print(f"CPU线程数: {torch.get_num_threads()}")
            print(f"当前interop线程数: {torch.get_num_interop_threads()}")

            # ==================== 资源监控 ====================
            print(f"\n内存占用: {psutil.Process().memory_info().rss // 1024**2}MB")
            # ==================== 生成测试封装 ====================
            def run_generation_test(prompt, max_length, use_cache=True):
                """ 支持跨框架的生成测试 """
                inputs = self.tokenizer(
                    prompt.strip(),
                    return_tensors = "pt",
                    padding='max_length',
                    max_length=256,
                    truncation=True
                )
                start_time = time.perf_counter()
                output = self.generator._generate(prompt, max_length=max_length, use_cache=use_cache)
                
                elapsed = time.perf_counter() - start_time
                speed = max_length / elapsed if elapsed > 1e-6 else float('inf')
                print(f"模型验证通过 | 测试输出: {output}")
                print(f"测试输入张量形状: {inputs.input_ids.shape}") 
                print(f"输入长度: {inputs.input_ids.shape[-1]} | 使用缓存: {use_cache}")
                print(f"生成输出类型: {type(output)}")
                print(f"是否含缓存: {hasattr(output, 'past_key_values')}")
                print(f"缓存状态追踪: {type(self.generator.past_key_values)} → 长度: \
                      {len(self.generator.past_key_values) if self.generator.past_key_values else 0}")
                # print(f"缓存层数: {len(self.generator.past_key_values)}")
                # print(f"Key形状: {self.generator.past_key_values.shape} | \
                #       Value形状: {self.generator.past_key_values.shape}")
                return {"output": output, "speed": speed}

            # ==================== 执行测试 ====================
            # 基础测试（所有模型）
            print("\n[测试1] 基础生成")
            cache_time = run_generation_test(test_prompt, max_length=100, use_cache=True)
            print(f"生成速度: {cache_time['speed']:.2f} tokens/秒")

            # print("\n[测试2] 无缓存生成")
            # nocache_time = run_generation_test(test_prompt, max_length=200, use_cache=False)
            # print(f"生成速度: {nocache_time['speed']:.2f} tokens/秒")
            # print(f"缓存加速比: {cache_time['speed'] / nocache_time['speed']:.1f}x")

            return True
        except Exception as e:
            print(f"验证失败: {str(e)}")
            return False


#---------------------------------------------------------------------------------------------
# 测试函数
#        执行   python -m src.utils 
#       或 python -m unittest src.utils.Testutils.test_safe_shutdown             
#       或 python -m unittest src.utils.Testutils.test_save_original_articles             
#---------------------------------------------------------------------------------------------
import unittest
from .themes  import THEME_CONFIGS
class Testutils(unittest.TestCase):
    def test_safe_shutdown(self):
        print("开始测试 safe_shutdown 函数...")
        print("\n测试用例1: 时间范围无效")              # 测试用例1: 时间范围无效
        invalid_time_range = ["25:00", "02:00"]
        result = common_utils.safe_shutdown(invalid_time_range)
        print(f"关机结果: {result}")
        print("\n测试用例2: 当前时间不在允许范围内")    # 测试用例2: 当前时间不在允许范围内
        out_of_range_time = ["03:00", "05:00"]
        result = common_utils.safe_shutdown(out_of_range_time)
        print(f"关机结果: {result}")
        print("\n测试用例3: 用户取消关机")              # 测试用例3: 用户取消关机
        user_cancel_time = ["00:00", "23:59"]
        result = common_utils.safe_shutdown(user_cancel_time)
        print(f"关机结果: {result}")
        print("\n测试用例4: 正常关机")   # 测试用例4: 正常关机
        shutdown_time_range = SHUT_DOWN_TIME
        result = common_utils.safe_shutdown(shutdown_time_range)
        print(f"关机结果: {result}")
        print("\n所有测试完成")
    def test_save_original_articles(self):
        print("开始测试 save_original_articles 函数...")
        for rankmin,rankmax in [(1000,2000),(2000,3000),(3000,4000),(4000,5000)]:
            # rankmin,rankmax = (2000,3000)
            if rankmax in [1000,2000,3000,4000,5000]:
                SELECTED_THEME = f"CHILDHOOD_FUN_THEME{rankmax//1000}K"
                print(f"当前主题集：{SELECTED_THEME}")
            selected_config = THEME_CONFIGS[SELECTED_THEME]
            theme_mapping = selected_config["theme_mapping"]        # 导出给其他模块使用的变量
            theme_starters = selected_config["theme_starters"]
            for theme,keywords in theme_mapping.items():
                text = theme_starters.get(theme, [''])[0]
                common_utils.save_original_articles(text,theme,keywords,rankmin,rankmax)
        print("测试完成,请查看文件\n")

if __name__ == "__main__":    
    unittest.main()
