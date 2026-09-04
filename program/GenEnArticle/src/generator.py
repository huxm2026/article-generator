
from .config import *
from .utils import common_utils,LanguageToolSingleton
from .model_handler import ModelHandler, VocabLogitsProcessor,DebugLogitProcessor,EOSBooster
from .vocab_processor import VocabProcessor
from .themes  import THEME_CONFIGS
from .textprocessor import NarrativeProcessor
from sentence_transformers import util

class ArticleGenerator:
    #---------------------------------------------------------------------------------------------
    # 初始化文章生成器
    #     参数:
    #         rank_range (tuple): 词频范围 (rankmin, rankmax)
    #---------------------------------------------------------------------------------------------
    def __init__(self, rank_range,TEST = False):
        # 初始化配置
        self.used_themes = deque(maxlen=50)
        self.current_prompt = " "

        self.rankmin, self.rankmax = rank_range
        if self.rankmax in [1000,2000,3000,4000,5000]:
            SELECTED_THEME = f"CHILDHOOD_FUN_THEME{self.rankmax//1000}K"
        narrative_examples = THEME_CONFIGS.get(SELECTED_THEME, {}).get("narrative_examples", {})
        self.current_theme = next(iter(narrative_examples.keys())) if narrative_examples else ""
        print(f"第1个主题{self.current_theme}")

        self.current_keywords = set()
        self.unused_lemmas = set()
        self.past_key_values = None
        self.grammar_tool = LanguageToolSingleton('en-US')
        self.memory_limit = 10 * 1024**3  # 10GB限制
        self.enable_swap = True  # 启用虚拟内存交换

        # 初始化模型
        self.model_handler = ModelHandler()
        self.semantic_model = self.model_handler._load_model()
        if TEST == False : self.model = self.model_handler.init_model()
        # if TEST == False : self.model = self.model_handler.init_Mobile_model()
        self.tokenizer = self.model_handler.tokenizer
        self.vocab_proc = VocabProcessor(
            rank_ranges=rank_range,
            tokenizer=self.tokenizer,
            semantic_model = self.semantic_model
            )
        self.processor = NarrativeProcessor(
            grammar_tool = self.grammar_tool,
            current_theme = self.current_theme,
            rank_ranges = rank_range,
            semantic_model = self.semantic_model
            )
        # 确保tokenizer已经初始化
        if TEST == False : self.allowed_tokens, self.capital_words = self.vocab_proc.prepare_vocab_tokens()  
        # 创建输出文件
        self.output_dir = common_utils.get_output_dir()

    #---------------------------------------------------------------------------------------------
    # 执行文章生成流程
    #     返回:
    #         str: 处理后符合要求的文章内容
    #     功能说明:
    #         1. 执行词库扩展检查
    #         2. 调用生成核心逻辑
    #         3. 进行后处理验证
    #---------------------------------------------------------------------------------------------
    def generate(self) -> str:
        self.vocab_proc.check_expansion()
        article = self._generate(max_length=ARTICLE_LENGTH, use_cache=True)
        # 仅测试用
        common_utils.save_original_articles(article,self.current_theme,self.current_keywords,self.rankmin, self.rankmax)
        
        self.processor.update_current_theme(self.current_theme)
        # processed = self._postprocess(article)
        processed = self.processor.process(article)
            
        if self._validate_coverage(processed):
            return processed
        return ""
    
    #---------------------------------------------------------------------------------------------
    # 验证词汇覆盖率
    #     参数:
    #         text (str): 待验证文本
    #     返回:
    #         bool: 是否包含新词汇
    #     验证逻辑:
    #         通过词形还原检查是否包含未使用词根
    #---------------------------------------------------------------------------------------------
    def _validate_coverage(self, text):
        for word in word_tokenize(text):
            if word.isalpha():
                lemma = self.vocab_proc.lemmatize(word.lower())
                if lemma in self.vocab_proc.unused_lemmas: 
                    return text
        return ""
    
    #---------------------------------------------------------------------------------------------
    # 动态构建生成提示词
    #     参数:
    #         seed_word (str): 核心种子词
    #         word_cluster (list): 关联词群
    #     返回:
    #         str: 结构化提示词模板
    #     构建策略:
    #         1. 基于多维度主题评分选择最佳主题
    #         2. 综合精确匹配、语义相似度、词频加权评分
    #         3. 动态轮换已使用主题
    #---------------------------------------------------------------------------------------------
    def create_prompt(self, seed_word = set(), word_cluster = []):
        def get_semantic_similarity(word, theme_words):      # 语义相似度计算函数
            try:
                similarities = [self.vocab_proc.word_vectors.similarity(word, t) 
                            for t in theme_words if t in self.vocab_proc.word_vectors]
                return np.mean(similarities) if similarities else 0
            except KeyError: return 0
        def topicfirst_select_theme():
            theme_scores = defaultdict(float)
            for theme, keywords in theme_mapping.items():
                available = [w for w in keywords if w in self.vocab_proc.unused_lemmas]
                total_similarity = sum(get_semantic_similarity(w, keywords) for w in word_cluster)
                similarity_score = total_similarity / max(len(word_cluster), 1)  # 防止除以零
                
                availability_ratio = len(available)/len(keywords)
                theme_scores[theme] = (
                    0.47 * availability_ratio + 
                    0.33 * similarity_score + 
                    0.20 * (1 - (self.used_themes.count(theme)/1.0))
                )
            max_score = max(theme_scores.values(), default=0)
            candidates = [t for t in theme_scores 
                if theme_scores[t] >= max_score and self.used_themes.count(t) < 2   ]
            if candidates:
                theme = max(candidates, key=lambda x: theme_scores[x])
                theme_keywords = theme_mapping[theme]
                seed_candidates = [w for w in theme_keywords 
                            if w in self.vocab_proc.unused_lemmas]
                seed = (random.choice(seed_candidates) if seed_candidates 
                            else self.vocab_proc._select_seed_word())
                cluster = list(seed_candidates)
                if len(seed_candidates) < WORD_CLUSTER_LENGTH:
                    remaining = WORD_CLUSTER_LENGTH - len(cluster)
                    expanded = self.vocab_proc._expand_cluster(seed, max_size=remaining)
                    for word in expanded:
                        if word not in cluster and remaining > 0:
                            cluster.append(word)
                            remaining -= 1
                return theme,seed,cluster
            else: return "",set(),[]
        def keywordfirst_select_theme():
            theme_scores = defaultdict(float)       # 多维度主题评分
            for theme, keywords in theme_mapping.items():
                exact_match = len(set(word_cluster).intersection(keywords))     # 维度1：精确匹配（权重40%）
                semantic_sim = sum(get_semantic_similarity(w, keywords) for w in word_cluster)      # 维度2：语义相似度（权重50%）
                freq_score = sum(self.vocab_proc.freq_dist[w] for w in word_cluster if w in keywords)    # 维度3：词频加权（权重10%）
                randomValue = random.uniform(0.8, 1.2)
                theme_scores[theme] = 0.4*exact_match+0.4*semantic_sim+0.1*freq_score+0.1*randomValue      # 综合得分
            sorted_themes = sorted(theme_scores.items(), key=lambda x: -x[1])   # 动态主题选择（设置最低阈值）
            max_score = sorted_themes[0][1] if sorted_themes else 0
            for theme, score in sorted_themes:      # 优先选择未使用的高分主题（得分>最高分60%的）
                if score < max_score * 0.6:continue
                if theme not in self.used_themes:
                    return sorted_themes,theme
            return sorted_themes,""
        
        try:    # 自动选择主题配置
            if self.vocab_proc.rankmax in [1000,2000,3000,4000,5000]:
                SELECTED_THEME = f"CHILDHOOD_FUN_THEME{self.vocab_proc.rankmax//1000}K"
            selected_config = THEME_CONFIGS[SELECTED_THEME]
            theme_mapping = selected_config["theme_mapping"]        # 导出给其他模块使用的变量
            theme_starters = selected_config["theme_starters"]
        except KeyError:
            valid_options = ', '.join(THEME_CONFIGS.keys())
            raise ValueError(f"[ERROR]无效主题集 '{SELECTED_THEME}'，有效选项：{valid_options}")
        
        if len(self.used_themes) >= len(theme_mapping):
            self.used_themes.clear()  
            print("[DEBUG] 主题列表已复位，开始循环使用")
        theme,seed,cluster = topicfirst_select_theme()
        if theme:
            selected_theme = theme
            seed_word = seed
            word_cluster = cluster
            self.used_themes.append(selected_theme)
        else:sorted_themes,selected_theme = keywordfirst_select_theme()
        
        if not selected_theme and len(sorted_themes) >= len(theme_mapping): # 如果所有高分主题都已使用，从前25名中随机选择非最近主题
            candidates = [t[0] for t in sorted_themes[:3] if t[0] not in self.used_themes]
            if candidates:
                selected_theme = random.choice(candidates)
                self.used_themes.append(selected_theme)
        if not selected_theme and sorted_themes:    # 保底逻辑：使用最高分主题（即使重复）
            selected_theme = sorted_themes[0][0]
            self.used_themes.append(selected_theme)
        prompt_template = f"""
            [ROLE] children's story writer 
            [TASK] Write {int(ARTICLE_LENGTH*0.7)}-word narrative about {selected_theme}
            [STRUCTURE]
                Direct story text ({int(ARTICLE_LENGTH*0.7)} words)
            [REQUIREMENTS] 
                1. Use: {', '.join(word_cluster[:WORD_CLUSTER_LENGTH])} 
                2. Flesch-Kincaid ≤{4+self.vocab_proc.current_rankmax//1000} & 70% top-{self.vocab_proc.current_rankmax} words
            [EXAMPLE]
            "{theme_starters.get(selected_theme, [''])[0]}"\n
            """
        self.current_prompt = prompt_template
        self.current_theme = selected_theme
        self.current_keywords = word_cluster
        print(f"[DEBUG]提示词:\n{prompt_template}")
        return prompt_template,seed_word,word_cluster   
    
    #---------------------------------------------------------------------------------------------
    # 生成核心逻辑
    #     参数:
    #         prompts (str/list): 输入提示词
    #         max_length (int): 最大生成长度
    #         use_cache (bool): 是否使用历史缓存
    #     返回:
    #         str: 原始生成文本
    #     关键配置:
    #         - LogitsProcessor: 词汇偏置处理器
    #         - Beam Search: num_beams=3 平衡生成质量与速度
    #         - Sampling: top_p=0.85 + temperature=0.75 保证多样性
    #---------------------------------------------------------------------------------------------
    def _generate(self,prompts = "",max_length=128,use_cache=True)-> str:
        profiler = cProfile.Profile()
        profiler.enable()

        if not prompts:
            seed_word = self.vocab_proc._select_seed_word()
            word_cluster = self.vocab_proc._expand_cluster(seed_word,max_size=WORD_CLUSTER_LENGTH)
            prompt,seed_word,word_cluster = self.create_prompt(seed_word,word_cluster)
            cluster_tokens = self.vocab_proc.get_cluster_tokens(word_cluster)
            print(f"[DEBUG]当前种子词:{seed_word} | 词个数{len(word_cluster)} | 词群:{word_cluster}")
        else:   
            cluster_tokens = self.vocab_proc.get_cluster_tokens(prompts[-1])
            prompt = prompts
        def prefix_allowed_tokens(batch_id, input_ids):     
            last_token = input_ids[-1].item()
            last_text = self.tokenizer.decode([last_token])
            if last_text in ['.', '!', '?','"']:    # 检测到句末标点后，下一个token必须是大写开头
                return [self.tokenizer.encode(' ' + w, add_special_tokens=False)[0] for w in self.capital_words]
            return list(self.allowed_tokens)

        # 创建精准logit处理器
        if VOCAB_LIMITED_LOGITSPROCESSOR==True:
            logitspro_tokens, logitspro_capital_words = self.vocab_proc.prepare_vocab_tokens(self.unused_lemmas,isASCII=False) 
        else:logitspro_tokens = cluster_tokens
        logit_processor = VocabLogitsProcessor(
            bias_tokens=logitspro_tokens,
            tokenizer=self.tokenizer,  # 传入当前tokenizer
            bias=1.8  # 提高目标词偏置
        )
        
        # ------------------上面的是限制词库用的，以下是通用的参数，-------------------------
        inputs = self.tokenizer(
                prompt.strip().replace('\t', ' '),
                return_tensors="pt",
                # padding=True,# padding='max_length',
                max_length=256,
                truncation=True
            ).to('cpu')
        
        think_token_id = self.tokenizer.encode("</think>", add_special_tokens=False)
        input_ids = inputs.input_ids
        force_position = input_ids.shape[1]
        gen_args = {
            "max_new_tokens": max_length,   # "max_length": max_length,
            # "min_length": int(max_length*0.6),
            # "do_sample": True,     # num_beams>1 false
            "top_k": 50,
            "top_p": 0.78,  # 平衡可控性与创造性‌  0.78
            "temperature": 0.4, # 0.4
            "repetition_penalty": 2.5,  # 重复抑制1.2
            "num_beams": 4,  # 连贯性 3
            "length_penalty": 0.1,  # 长度惩罚0.5--0.3
            "no_repeat_ngram_size": 3,    # 禁止词重复,强制句式变化‌
            "early_stopping": True,     # 避免无效搜索
            "penalty_alpha": 0.6,   # 增强提示词相关性
            "pad_token_id": self.tokenizer.pad_token_id,         
            "eos_token_id": self.tokenizer.eos_token_id,          
            "forced_eos_token_id": self.tokenizer.eos_token_id,            # 确保生成结束
            "suppress_tokens": [self.tokenizer.encode("</think>")[0]],   # 抑制特殊标记
            "forced_decoder_ids":[(force_position+1, think_token_id[0])],  # 第0个token必须是 </think>
            "logits_processor": LogitsProcessorList([
                logit_processor,
                EOSBooster(self.tokenizer.eos_token_id),
                ]),
            "prefix_allowed_tokens_fn": prefix_allowed_tokens,
            # "bad_words_ids": [self.tokenizer.encode("meta")],
            "use_cache": use_cache,
            "past_key_values": self.past_key_values if use_cache else None
        }
        if not hasattr(self, '_params_printed'):
            print("[Debug]当前生成参数配置:")
            for k, v in gen_args.items():print(f"{k:20} = {v}")
            self._params_printed = True
        with torch.inference_mode():    # 禁用梯度计算内存占用更低 with torch.no_grad():
            outputs = self.model.generate(**inputs,**gen_args)
        if use_cache and hasattr(outputs, 'past_key_values'):self.past_key_values = outputs.past_key_values
        else: self.past_key_values = None
            
        profiler.disable()
        profiler.dump_stats(os.path.join(self.output_dir, 'generate_profile.prof'))
        if DEBUG:print(f"[Debug]当前use_cache状态: {use_cache} | 输入长度: {inputs.input_ids.shape[-1]}")
        if use_cache and hasattr(outputs, 'past_key_values'):self.past_key_values = outputs.past_key_values
        else:
            self.past_key_values = None
            if DEBUG:print("[Debug]警告: 当前模型未返回缓存状态")

        generated_tokens = outputs[0].tolist()
        matched = [t for t in generated_tokens if t in cluster_tokens]
        print(f"命中目标token数量: {len(matched)}/{len(generated_tokens)}")
        print("具体命中词:", self.tokenizer.decode(matched))

        return self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[-1]:],  # 截取生成部分
            # outputs[0].tolist(), 
            skip_special_tokens=False,
            clean_up_tokenization_spaces=False    
        )
    
     #---------------------------------------------------------------------------------------------
    # 更新生成上下文信息
    #     参数:
    #         unused_lemmas (str): 没有使用的原形词
    #---------------------------------------------------------------------------------------------
    def update_context(self, unused_lemmas):
        self.unused_lemmas = unused_lemmas

    

#---------------------------------------------------------------------------------------------
# 仅用于测试的代码段 
#   测试： 执行   python -m src.generator 
#---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import unittest
    from src.vocab_processor import WORD_CLUSTER_LENGTH
    class TestCreoateprmpt(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls.generator = ArticleGenerator((1000, 2000), TEST=True)
        def test_createprompt(self):
            print("开始测试 test_createprompt()函数...")
            for index in range(1,27):
                seed_word, seed_time = common_utils._measure_time(self.generator.vocab_proc._select_seed_word)
                word_cluster, cluster_time = common_utils._measure_time(self.generator.vocab_proc._expand_cluster, 
                                                                seed_word, max_size=WORD_CLUSTER_LENGTH)
                prompt_data, prompt_time = common_utils._measure_time(self.generator.create_prompt,seed_word,word_cluster)
                prompt, seed_word, word_cluster = prompt_data
                print(f"[_select_seed_word]耗时:{seed_time:.2f}ms,  [_expand_cluster]耗时:{cluster_time:.2f}ms"
                    f"[create_prompt]耗时:{prompt_time:.2f}ms,[总耗时]:{seed_time + cluster_time + prompt_time:.2f}ms")
                self.generator.vocab_proc.unused_lemmas -= set(word_cluster)
                print(f"[DEBUG]当前种子词:{seed_word}|词个数{len(word_cluster)}|词群:{word_cluster}|剩余词数：{len(self.generator.vocab_proc.unused_lemmas)}")
                print(f"[DEBUG]第{index}个主题:{self.generator.current_theme}")
            self.assertIsInstance(prompt, str)
            self.assertIsInstance(seed_word, str)
            self.assertIsInstance(word_cluster, list)
            print("\n测试结束")  
            
    unittest.main(argv=[''], exit=False)

    
    