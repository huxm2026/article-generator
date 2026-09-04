from .config import *
from transformers import AutoModelForCausalLM, AutoTokenizer,StoppingCriteria
from sentence_transformers import SentenceTransformer, util
from sentence_transformers.models import Transformer, Pooling

#---------------------------------------------------------------------------------------------
# 调试用logit处理器（仅在DEBUG模式启用）
#     功能:
#         在生成过程中打印调试信息
#---------------------------------------------------------------------------------------------
class DebugLogitProcessor(LogitsProcessor):
    def __call__(self, input_ids, scores):
        print("[Debug] Logit processor applied")
        return scores  

#---------------------------------------------------------------------------------------------
# 词汇增强logit处理器
#     参数:
#         bias_tokens (list): 需要偏置的token列表
#         tokenizer (AutoTokenizer): 分词器实例
#         bias (float): 偏置值，默认20.0
#     功能:
#         对指定token添加logit偏置，提升其在生成中的出现概率
#---------------------------------------------------------------------------------------------
class VocabLogitsProcessor(LogitsProcessor):
    def __init__(self, bias_tokens,tokenizer,bias=20.0):
        super().__init__()  # 显式调用父类初始化
        self.tokenizer = tokenizer
        self.bias_dict = {
            int(token): float(bias) 
            for token in bias_tokens
            if 0 <= int(token) < self.tokenizer.vocab_size  # 有效性过滤
            }  # 确保类型安全
        
        print(f"[DEBUG]有效偏置token数量: {len(self.bias_dict)}")  # 调试输出
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        """严格遵循父类方法签名"""
        # 调试信息优化
        if scores.shape[-1] < max(self.bias_dict.keys(), default=0):
            print(f"警告: token_id超出词汇表大小 {scores.shape[-1]}")

        for token_id, bias in self.bias_dict.items():
            if token_id < scores.shape[-1]:
                scores[..., token_id] += bias
        if DEBUG:
            print(f"[Debug]当前偏置token数量: {len(self.bias_dict)}")
            print(f"[Debug]最大偏置值: {max(self.bias_dict.values())}")  
            top_probs = torch.softmax(scores, dim=-1).topk(5)
            print(f"[Debug]当前候选词: {self.tokenizer.decode(top_probs.indices.tolist()[0])}")   
        # 类型转换确保兼容性
        return scores.float() if scores.dtype != torch.float32 else scores
    
#---------------------------------------------------------------------------------------------
# 模型处理器类
#     功能:
#         封装模型加载、初始化和配置管理
#     属性:
#         model (AutoModelForCausalLM): 语言模型实例
#         tokenizer (AutoTokenizer): 分词器实例
#---------------------------------------------------------------------------------------------
class ModelHandler:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.semantic_model = None

    #---------------------------------------------------------------------------------------------
    # 加载语义模型
    #     功能:
    #         加载SentenceTransformer模型用于语义相似度计算
    #     返回:
    #         SentenceTransformer模型实例
    #---------------------------------------------------------------------------------------------
    def _load_model(self):
        try:
            base_path = Path(SentenceTransformer_path).as_posix()
            # 关键修正：移除显式config参数传递
            transformer = Transformer(
                model_name_or_path=os.path.join(base_path, "0_Transformer"),
                tokenizer_name_or_path=os.path.join(base_path, "0_Transformer")
            )
            pooling = Pooling(
                transformer.get_word_embedding_dimension(),
                pooling_mode='mean'
            )
            sim_model = SentenceTransformer(modules=[transformer, pooling])
            print("[DEBUG]SentenceTransformer模型加载成功 | 维度:", sim_model.get_sentence_embedding_dimension())
            return sim_model
        except Exception as e:
            print(f"[DEBUG]SentenceTransformer加载失败: {str(e)}")
            raise
    #---------------------------------------------------------------------------------------------
    # 初始化语言模型
    #     返回:
    #         AutoModelForCausalLM: 初始化的模型实例
    #     异常:
    #         FileNotFoundError: 模型文件缺失时抛出
    #     功能说明:
    #         1. 配置CPU多线程参数
    #         2. 加载预训练模型和分词器
    #         3. 设置模型评估模式
    #---------------------------------------------------------------------------------------------
    def init_model(self):
        # CPU优化设置
        torch.set_num_interop_threads(4)  # 交错并行，需在模型加载前设置
        torch.set_num_threads(8)
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"模型目录缺失: {MODEL_PATH}")
        # 初始化分词器
        self.tokenizer = AutoTokenizer.from_pretrained(
        # self.tokenizer = QwenTokenizer.from_pretrained(
            MODEL_PATH,
            trust_remote_code=False,
            pad_token='<|endoftext|>',
            # eos_token='<|endoftext|>'
            eos_token='[EOS]'       # 定义结束标记
        )

        # self.test_model_tokens(self.tokenizer)

        # 初始化模型
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            torchscript=True,  # 启用TorchScript优化
            device_map="cpu",   
            torch_dtype=torch.float32,
            load_in_8bit=False, 
            trust_remote_code=False,
            low_cpu_mem_usage=True
        )
        self.model.eval()
        return self.model 

    #---------------------------------------------------------------------------------------------
    # 测试语言模型
        # 测试指定 Unicode 范围内的字符是否被分词器视为单个 Token
        # :param tokenizer: 分词器对象
        # :param unicode_ranges: 要测试的 Unicode 范围列表，如 [(0x0370, 0x03FF)]（希腊字母）
        # :return: 允许的字符列表及其 Token ID
        # unicode_ranges = [
        #     (0xFF20, 0xFF7E),  # ASCII 可打印全角字符
        #     (0x0370, 0x03FF),  # 希腊字母
        #     (0x2200, 0x22FF),  # 数学符号
        #     (0x2600, 0x26FF),  # 杂项符号（如★☺）
        # ]
        # allowed_chars = test_unicode_tokens(self.tokenizer, unicode_ranges) # 运行测试
        # allowed_token_ids = [token_id for (char, token_id) in allowed_chars]    # 输出最终允许的 Token ID 列表
        # print(f"\n最终允许的 Token ID 列表: {allowed_token_ids}")
    #---------------------------------------------------------------------------------------------
    def test_model_tokens(self,tokenizer):
        def test_unicode_tokens(tokenizer, unicode_ranges):
            allowed_chars = []
            for start, end in unicode_ranges:       # 遍历每个 Unicode 范围
                print(f"\n=== 测试范围: U+{start:04X}-U+{end:04X} ===")
                for code_point in range(start, end + 1):   # 遍历范围内的每个字符
                    try:
                        char = chr(code_point)
                        if not char.isprintable():  # 跳过控制字符和非打印字符
                            continue
                        tokens = tokenizer.tokenize(char)       # 使用分词器处理字符
                        # 判断是否为单个 Token 且与原字符一致
                        if len(tokens) == 1 and tokens[0] == char:
                            token_id = tokenizer.convert_tokens_to_ids(tokens[0])
                            allowed_chars.append((char, token_id))
                            print(f"允许: {char} (U+{code_point:04X}) → Token: {tokens[0]} (ID: {token_id})")
                        else:
                            print(f"拒绝: {char} (U+{code_point:04X}) → Tokens: {tokens}")
                    except Exception as e:
                        print(f"错误: U+{code_point:04X} → {str(e)}")
            return allowed_chars
        
        if tokenizer is not None:
            print("[DEBUG]分词器特殊标记:", tokenizer.special_tokens_map) 
            print("[DEBUG]<｜end▁of▁sentence｜> 是否存在:", "<｜end▁of▁sentence｜>" in tokenizer.get_vocab())
            print("[DEBUG]<|end_of_sentence|> 是否存在:", "<|end_of_sentence|>" in tokenizer.get_vocab())
            print("[DEBUG]<｜begin▁of▁sentence｜> 是否存在:", "<｜begin▁of▁sentence｜>" in tokenizer.get_vocab())
            print("[DEBUG]<|begin_of_sentence|> 是否存在:", "<|begin_of_sentence|>" in tokenizer.get_vocab())
        unicode_ranges = [
            # (0xFF20, 0xFF7E),  # ASCII 可打印全角字符
            # (0x0370, 0x03FF),  # 希腊字母
            # (0x2200, 0x22FF),  # 数学符号
            # (0x2600, 0x26FF),  # 杂项符号（如★☺）
            # (0x1F300, 0x1F6FF),  # Emoji扩展
            # (0x1F900, 0x1F9FF)   # 补充符号
        ]
        allowed_chars = test_unicode_tokens(tokenizer, unicode_ranges) # 运行测试
        allowed_token_ids = [token_id for (char, token_id) in allowed_chars]    # 输出最终允许的 Token ID 列表
        print(f"\n最终允许的 Token ID 列表: {allowed_token_ids}")
        sys.exit(1)
    
    #---------------------------------------------------------------------------------------------
    # 初始化MobileLLaMA语言模型
    #     返回:
    #         AutoModelForCausalLM: 初始化的模型实例
    #     异常:
    #         FileNotFoundError: 模型文件缺失时抛出
    #     功能说明:
    #         1. 配置CPU多线程参数
    #         2. 加载预训练模型和分词器
    #         3. 设置模型评估模式
    #---------------------------------------------------------------------------------------------
    def init_Mobile_model(self):
        # 确保模型路径存在
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"模型目录缺失: {MODEL_PATH}")

        # 初始化分词器（此时 self.tokenizer 尚未赋值）
        
        # tokenizer = LlamaTokenizer.from_pretrained(  # pip sentencepiece 
        tokenizer = AutoTokenizer.from_pretrained(  # 先用局部变量 tokenizer
            MODEL_PATH,
            trust_remote_code=False,
            use_fast=True,
            eos_token='</s>',
            bos_token='<s>'
        )
        
        # 检查并添加缺失的 pad_token
        if tokenizer.pad_token is None:
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})  # 或 '<unk>'
        
        # 将局部变量赋给 self.tokenizer
        self.tokenizer = tokenizer
        
        # 继续初始化模型
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            trust_remote_code=False,
            torch_dtype=torch.float32,
            device_map="cpu",
            low_cpu_mem_usage=True
        )
        self.model.eval()
        return self.model
    
#---------------------------------------------------------------------------------------------
# 强化自然终止logit处理器
# 功能：通过增强EOS（End-of-Sequence）标记的生成概率，促使模型在适当位置自然终止文本生成
# 原理：在每一步生成时，将EOS标记的logits值乘以增强因子，从而提升其被选择概率
# boost_factor	生成效果	        适用场景
# 0.5	        抑制提前终止	    长文本生成任务
# 1.0	        保持原始概率	    基准测试
# 2.0~3.0	    适度增强终止	    对话系统/结构化输出
# 5.0+	        强制快速终止	    测试极端情况
#---------------------------------------------------------------------------------------------
class EOSBooster(LogitsProcessor):
    def __init__(self, eos_token_id, boost_factor=2.1):
        self.eos_token_id = eos_token_id
        self.boost_factor = boost_factor
        
    def __call__(self, input_ids, scores):
        scores[:, self.eos_token_id] *= self.boost_factor
        return scores
    
#---------------------------------------------------------------------------------------------
# 思考抑制logit处理器
#     参数:
#         tokenizer (AutoTokenizer): 分词器实例
#         suppress_tokens (list): 需要抑制的token列表
#     功能:
#         对指定token添加logit惩罚，降低其在生成中的出现概率
#     使用场景:
#         用于抑制与思考过程相关的token，如"首先"、"其次"等
        # gen_args = {
        #     "suppress_tokens": [SuppressThinkingLogits(LogitsProcessor)],
        # }
#---------------------------------------------------------------------------------------------
class SuppressThinkingLogits(LogitsProcessor):
    def __init__(self, tokenizer, suppress_tokens):
        suppressed_tokens = ["首先", "其次", "因此", "<think>"]
        self.suppress_ids = [tokenizer.convert_tokens_to_ids(t) for t in suppress_tokens]

    def __call__(self, input_ids, scores):
        for idx in self.suppress_ids:
            scores[:, idx] -= 10  # 大幅降低指定token概率
        return scores

#---------------------------------------------------------------------------------------------
# 快速切换停止条件
#     参数:
#         tokenizer (AutoTokenizer): 分词器实例
#         max_thinking_steps (int): 最大思考步数，默认3
#     功能:
#         检测生成文本中的思考模式，在超过最大步数时停止生成
#     使用场景:
#         用于控制模型在生成过程中的思考深度，避免过度分析
        # gen_args = {
        #     "stopping_criteria": [FastSwitchCriteria(tokenizer)],
        # }
#---------------------------------------------------------------------------------------------
class FastSwitchCriteria(StoppingCriteria):
    def __init__(self, tokenizer, max_thinking_steps=3):
        self.tokenizer = tokenizer
        self.max_steps = max_thinking_steps
        self.step_count = 0
        self.thinking_triggers = ["分析", "因为", "所以"]

    def __call__(self, input_ids, scores, **kwargs):
        current_text = self.tokenizer.decode(input_ids[0][-20:])  # 检测最近20个token
        # 判断是否处于思考阶段
        if any(trigger in current_text for trigger in self.thinking_triggers):
            self.step_count +=1
            return self.step_count > self.max_steps  # 超过最大步数则停止
        return False


#---------------------------------------------------------------------------------------------
# 模型处理器类
#     功能:
#         封装模型加载、初始化和配置管理
#     属性:
#         model (AutoModelForCausalLM): 语言模型实例
#         tokenizer (AutoTokenizer): 分词器实例
#---------------------------------------------------------------------------------------------

# | 参数名称                  | 当前值   | 功能说明                                                                 |
# |--------------------------|----------|--------------------------------------------------------------------------|
# | `max_new_tokens`         |max_length| 控制生成的最大新 token 数量（优先于旧参数 `max_length`）                 |
# | `top_k`                  | 30       | 保留概率最高的前30个候选词进行采样                                       |
# | `top_p`                  | 0.85     | 使用核采样(nucleus sampling)，累计概率超过85%的词会被过滤                |
# | `temperature`            | 0.75     | 控制采样随机性：0.75平衡创造性与可控性（值越低输出越确定）                 |
# | `repetition_penalty`     | 4.2      | 抑制重复惩罚系数：4.2表示对重复内容施加较强惩罚                           |
# | `num_beams`              | 2        | 使用束搜索(beam search)时的束宽为2，平衡生成质量与速度                    |
# | `length_penalty`         | 0.2      | 长度惩罚系数：0.2鼓励生成更长文本（>1鼓励长文本，<1鼓励短文本）             |
# | `no_repeat_ngram_size`   | 3        | 禁止3-gram重复出现，强制句式变化                                         |
# | `penalty_alpha`          | 0.7      | 对比搜索(contrastive search)的惩罚系数，增强提示词相关性                  |
# | `pad_token_id`           | 动态获取  | 使用分词器的pad_token_id作为填充标记                                     |
# | `forced_eos_token_id`    | 动态获取  | 强制在生成结束时添加eos_token                                            |
# | `suppress_tokens`        | [ids]    | 抑制特定token生成（包含". </think>"、"Note:"、"(" 的token ID）            |
# | `forced_decoder_ids`     |[[1,eos_id]| 在第2个token位置强制生成结束标记                                         |
# | `use_cache`              | use_cache | 是否使用键值缓存加速生成（True时复用历史计算结果）                         |
# | [past_key_values]        | 动态获取  | 缓存的历史键值对，用于加速长文本生成（当use_cache=True时生效）              |

# ### 注释参数说明
# - `"do_sample": True`（当前已注释）：当与`num_beams`同时使用时需设为False
# - `"max_length": max_length`（旧参数）：建议优先使用`max_new_tokens`