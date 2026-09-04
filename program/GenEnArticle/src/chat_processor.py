# src/chat_processor.py
import time
from collections import deque

class ChatProcessor:
    #---------------------------------------------------------------------------------------------
    # 初始化对话处理器
    #     参数:
    #         generator (ArticleGenerator): 文章生成器实例
    #     初始化内容:
    #         1. 复用生成器配置（模型/tokenizer）
    #         2. 设置对话上下文队列
    #         3. 配置对话专用生成参数（继承自文章生成逻辑）
    #---------------------------------------------------------------------------------------------
    def __init__(self, generator):
        # 复用现有生成器配置
        self.generator = generator
        # 对话上下文队列（保留最近3轮）
        self.context = deque(maxlen=3) 
        
        # 继承原始生成参数（来自ArticleGenerator._generate）
        self.chat_gen_args = {
            "max_new_tokens": 500,   # "max_length": max_length,
            "top_k": 50,
            "top_p": 0.78,  # 平衡可控性与创造性‌  0.95--0.85
            "temperature": 0.2, # 0.75
            "repetition_penalty": 4.2,  # 重复抑制4.2
            "num_beams": 2,  # 连贯性 3
            "length_penalty": 0.2,  # 长度惩罚0.5--0.3
            "no_repeat_ngram_size": 3,    # 禁止词重复,强制句式变化‌
            "penalty_alpha": 0.7,   # 增强提示词相关性
            "pad_token_id": self.generator.tokenizer.eos_token_id,
            "eos_token_id": self.generator.tokenizer.eos_token_id
        }

        # self.chat_gen_args = {
        #     # 长度控制
        #     "max_new_tokens": 512,               # 最大生成长度（根据任务动态调整）
        #     "min_new_tokens": 32,                # 最小生成长度（避免过早截断）
            
        #     # 采样策略
        #     "do_sample": True,                   # 启用随机采样（提高生成多样性）
        #     "temperature": 0.4,                  # 平衡确定性与创造性（值越低输出越确定）
        #     "top_k": 40,                         # 保留最可能的40个候选词
        #     "top_p": 0.6,                       # 累积概率85%的词汇参与采样
            
        #     # 重复与惩罚
        #     "repetition_penalty": 1.15,          # 抑制重复短语（>1.0生效）
        #     "no_repeat_ngram_size": 3,           # 禁止3-gram重复出现
            
        #     # 设备与效率
        #     "num_beams": 1,                      # 禁用Beam Search（移动端推荐单束）
        #     "use_cache": True,                    # 启用KV缓存加速推理
        #     "pad_token_id": 0,                   # 填充符ID（需与分词器对齐）
        #     "eos_token_id": 2                    # 结束符ID（LLaMA标准为</s>，ID通常为2）
        # }
    #---------------------------------------------------------------------------------------------
    # 生成对话响应
    #     参数:
    #         user_input (str): 用户输入内容
    #     返回:
    #         str: 生成的回复内容或错误信息
    #     处理流程:
    #         1. 构建包含历史上下文的提示词
    #         2. 调用模型生成响应（禁用词汇限制）
    #         3. 处理生成结果并更新上下文
    #     关键配置:
    #         - max_length=512 允许更长上下文
    #         - logits_processor=None 关闭词汇过滤
    #         - 保留最近3轮对话历史
    #---------------------------------------------------------------------------------------------
    def generate_response(self, user_input):
        """基于现有模型生成对话回复"""
        try:
            # 构建对话提示词（保留2轮历史）
            prompt = "\n".join([
                "[对话历史]" if self.context else "",
                *self.context,
                f"User: {user_input}",
                "Assistant:"
            ])
            
            # 复用原始生成逻辑
            inputs = self.generator.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=512,  # 增加上下文长度
                truncation=True
            ).to('cpu')
            
            # 生成时关闭词汇限制
            outputs = self.generator.model.generate(
                **inputs,
                **self.chat_gen_args,
                logits_processor=None  # 禁用原有词汇处理器
            )
            
            response = self.generator.tokenizer.decode(
                outputs[0][inputs.input_ids.shape[-1]:], 
                # outputs[0].tolist(), 
                clean_up_tokenization_spaces=False,  
                skip_special_tokens=False
            )
            # ).split("User:")[0].strip()  # 截断到新用户输入前
            
            # 更新上下文
            self.context.extend([f"User: {user_input}", f"Assistant: {response}"])
            
            return response
            
        except Exception as e:
            return f"生成错误：{str(e)}"
