from click import BOOL
from .config import *
from .narrative_features import THEME_CONFIGS
from sentence_transformers import util
from .utils import common_utils

#---------------------------------------------------------------------------------------------
# # 使用示例
# processor = NarrativeProcessor()
# original_text = """您的原始文本内容..."""
# output = processor.process(original_text)
#---------------------------------------------------------------------------------------------
class NarrativeProcessor:
    #---------------------------------------------------------------------------------------------
    # 类初始化方法
    #     参数:
    #         semantic_threshold: float, 语义相似度阈值，默认值为0.7
    #         narrative_examples: list, 叙事类文本示例列表，可选
    #         non_narrative_examples: list, 非叙事类文本示例列表，可选
    #---------------------------------------------------------------------------------------------
    def __init__(self,grammar_tool,current_theme,rank_ranges,semantic_model):
        self.nlp = spacy.load("en_core_web_md")     # 加载 NLP 模型
        self.current_theme = current_theme
        self.rankmin, self.rankmax = rank_ranges
        if self.rankmax in [1000,2000,3000,4000,5000]:
            SELECTED_THEME = f"CHILDHOOD_FUN_THEME{self.rankmax//1000}K"
            # print(f"[DEBUG]textprocessor.py中__init__()当前主题集 {SELECTED_THEME}")
        self.theme_config = THEME_CONFIGS.get(
            SELECTED_THEME, 
            THEME_CONFIGS[SELECTED_THEME]
        )

        # 初始化语义模型和示例嵌入
        self.grammar_tool=grammar_tool
        self.semantic_model = semantic_model
        self._init_semantic_examples()
        self.alpha = 3.5                    # 锐化强度参数
        self.top_k = 0.25                   # 使用前k%最具叙事性的句子
        self.semantic_threshold = 0.35
        self.min_similarity = 0.75          # 相似度阈值
        
    #---------------------------------------------------------------------------------------------
    # 预计算语义示例的嵌入向量
    #     参数:
    #         narrative_examples: list, 叙事类文本示例列表，可选
    #         non_narrative_examples: list, 非叙事类文本示例列表，可选
    #     功能:
    #         1. 初始化默认的叙事类和非叙事类示例文本
    #         2. 使用语义模型将文本转换为嵌入向量
    #         3. 将嵌入向量转换为半精度以加速计算
    #     返回:
    #         无返回值，结果存储在类属性中
    #---------------------------------------------------------------------------------------------
    def _init_semantic_examples(self):
        NARRATIVE_EXAMPLES_ALL = self.theme_config.get('narrative_examples', {})
        themes = list(NARRATIVE_EXAMPLES_ALL.keys())
        if not themes:
            print("[ERROR]没有可用主题,退出_init_semantic_examples()函数")
            return 
        
        if self.current_theme not in themes:
            print(f"[ERROR]遍历叙事性示例文本，没有找到{self.current_theme}主题对应的示例文本,退出_init_semantic_examples()函数")
            return 
        # else:print(f"[DEBUG]textprocessor.py中_init_semantic_examples()遍历叙事性示例文本,找到相对应的主题:{self.current_theme}")
        if isinstance(NARRATIVE_EXAMPLES_ALL, dict):
            self.narrative_examples = NARRATIVE_EXAMPLES_ALL.get(self.current_theme, [])
        elif isinstance(NARRATIVE_EXAMPLES_ALL, list):    # 备用逻辑：如果 narrative_examples 是列表，转换为字典
            NARRATIVE_EXAMPLES_ALL = dict(NARRATIVE_EXAMPLES_ALL)
            self.narrative_examples = NARRATIVE_EXAMPLES_ALL.get(self.current_theme, [])
        self.non_narrative_examples = self.theme_config.get('non_narrative_examples', [])
        # print(f"[DEBUG]当前主题 {self.current_theme} 的叙事示例: {', '.join(self.narrative_examples[:1]) + '...'}")
        # print(f"[DEBUG]当前主题 {self.current_theme} 的非叙事示例: {', '.join(self.non_narrative_examples[:1]) + '...'}")
        try:
            self.narrative_embeddings = self.semantic_model.encode(
                self.narrative_examples, convert_to_tensor=True,truncation=True, max_length=512,padding='max_length')
            self.non_narrative_embeddings = self.semantic_model.encode(
                self.non_narrative_examples, convert_to_tensor=True,truncation=True, max_length=512,padding='max_length')
        except Exception as e:
            print(f"[ERROR] 编码失败: {str(e)}")
            print(f"当前示例数量 - 叙事: {len(self.narrative_examples)}, 非叙事: {len(self.non_narrative_examples)}")
            self.narrative_embeddings = torch.empty(0)      # 初始化空张量作为备用
            self.non_narrative_embeddings = torch.empty(0)
        
    #---------------------------------------------------------------------------------------------
    # 分割文本为句子
    #     参数:
    #         text: str, 待分割的文本
    #     功能:
    #         使用spaCy的句子分割器将文本分割为句子
    #     返回:
    #         list: 句子列表，每个句子为一个字符串
    #---------------------------------------------------------------------------------------------
    def _split_sentences(self, text):
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 0]
   
    #---------------------------------------------------------------------------------------------
    # 基于语义相似度的去重
    #     参数:
    #         sentences: List[str], 待去重的句子列表
    #         window_size: int, 对比的最近保留句子窗口大小 
    #         min_similarity: float, 相似度阈值，低于则视为不重复
    #     功能:
    #         1. 计算句子嵌入向量
    #         2. 构建相似度矩阵
    #         3. 使用滑动窗口进行去重
    #     返回:
    #         list: 去重后的句子列表
    #---------------------------------------------------------------------------------------------
    def _deduplicate(self, sentences, window_size=5):
        if len(sentences) < 2:
            return sentences.copy()
        embeddings = self.semantic_model.encode(sentences,convert_to_tensor=True)
        # 计算所有句子与其他句子的平均相似度
        sim_matrix = util.pytorch_cos_sim(embeddings, embeddings)
        mask = torch.eye(sim_matrix.size(0), dtype=torch.bool)  # 创建对角线掩码
        sim_matrix = sim_matrix.masked_fill(mask, -1)  # 用PyTorch方法填充
        avg_similarities = torch.mean(sim_matrix, dim=1)
        keep_indices = [torch.argmin(avg_similarities).item()]
        for i in range(len(sentences)):
            if i in keep_indices:
                continue
            compare_indices = keep_indices[-window_size:] if len(keep_indices)>=window_size else keep_indices
            if not compare_indices:
                keep_indices.append(i)
                continue
            current_embed = embeddings[i].unsqueeze(0)
            compare_embeds = embeddings[compare_indices]
            similarities = util.pytorch_cos_sim(current_embed, compare_embeds)
            if similarities.max().item() < self.min_similarity:
                keep_indices.append(i)
        
        keep_indices = sorted(list(set(keep_indices)))
        return [sentences[i] for i in keep_indices]
    
    #---------------------------------------------------------------------------------------------
    # 句子差异计算（语义空间比对） 计算单个句子的原始叙事差异
    #   sentence 输入参数：
    #       需要分析的单个句子
    #   关键操作：
    #       与预设叙事/非叙事嵌入空间进行相似度比对
    #   返回：
    #       叙事性差异分数（[-1.0, 1.0]区间）
    #---------------------------------------------------------------------------------------------
    def _calculate_sentence_diff(self, sentence: str) -> float:
        try:
            # Add explicit padding and better tokenization control
            sent_embedding = self.semantic_model.encode(
                sentence, 
                convert_to_tensor=True, 
                truncation=True, 
                max_length=512,
                padding='max_length'  # Ensure consistent tensor dimensions
            )
            
            narrative_sim = util.pytorch_cos_sim(
                sent_embedding, self.narrative_embeddings).max().item()
            non_narrative_sim = util.pytorch_cos_sim(
                sent_embedding, self.non_narrative_embeddings).max().item()
                
            return narrative_sim - non_narrative_sim
            
        except Exception as e:  # Catch all exceptions for debugging
            print(f"[ERROR] Failed to process sentence: {sentence[:50]}...")
            print(f"Exception type: {type(e).__name__}, Message: {str(e)}")
            return 0.0 
    
    #---------------------------------------------------------------------------------------------
    # 对比度增强函数（分段优化）, 增强型分段锐化函数，特别优化0值附近表现
    #   diff 输入参数：
    #       原始叙事差异值
    #   核心逻辑：
    #       - 零值附近使用立方增强
    #       - 其他区域使用双曲正切函数
    #   返回：
    #       锐化后的差异值（[-2.8, 2.8]区间）
    #---------------------------------------------------------------------------------------------
    def _sharpen_contrast(self, diff: float) -> float:
        # 针对0值附近的特殊增强
        if -0.15 < diff < 0.15:
            # 立方增强：在0值附近创造更强对比
            return np.sign(diff) * (abs(diff) ** 0.7) * 2.8
        else:
            # 双曲正切函数增强其他区域
            return np.tanh(self.alpha * diff)
    
    #---------------------------------------------------------------------------------------------
    # 加权叙事评分（聚焦关键句子）,加权叙事性评分：聚焦最具叙事性的句子
    #   diffs 输入参数：
    #       锐化后的差异值列表
    #   核心算法：
    #       1. 筛选前k%高差异值
    #       2. 指数衰减权重分配
    #   返回：
    #       加权叙事评分（无量纲）
    #---------------------------------------------------------------------------------------------
    def _weighted_narrative_score(self, diffs: list) -> float:
        # 选择前k%最具叙事性的句子
        if not diffs:  
            return 0.0
        
        k = max(1, int(len(diffs) * self.top_k))
        top_diffs = sorted(diffs, reverse=True)[:k]
        
        # 指数加权：更具叙事性的句子权重更高
        weights = np.exp(np.linspace(0, 1, k))
        weights /= weights.sum()
        
        return np.dot(top_diffs, weights)
    
    #---------------------------------------------------------------------------------------------
    # 叙事主导度计算（复合指标）,叙事主导度：衡量段落被叙事内容主导的程度
    #   diffs 输入参数：
    #       锐化后的差异值列表
    #   计算逻辑：
    #       - 正差异值比例
    #       - 正差异值强度
    #   返回：
    #       几何平均数（[0.0, 1.0]区间）
    #---------------------------------------------------------------------------------------------
    def _narrative_dominance(self, diffs: list) -> float:
        positive_diffs = [d for d in diffs if d > 0]
        if not positive_diffs: 
            return 0.0
        
        # 基于叙事句的比例和强度
        proportion = len(positive_diffs) / len(diffs)
        intensity = np.mean(positive_diffs)
        
        # 几何平均平衡比例和强度
        return np.sqrt(proportion * intensity)
    
    #---------------------------------------------------------------------------------------------
    # 对比度指数计算（方差增强）,对比度指数：量化段落内叙事性变化程度
    #   diffs 输入参数：
    #       原始差异值列表
    #   核心算法：
    #       指数加权移动方差
    #   返回：
    #       放大后的标准差（≥0.0）
    #---------------------------------------------------------------------------------------------
    def _contrast_index(self, diffs: list) -> float:
        # 计算指数加权移动方差
        weights = np.exp(np.linspace(0, 1, len(diffs)))
        weights /= weights.sum()
        
        mean = np.average(diffs, weights=weights)
        variance = np.average((diffs - mean)**2, weights=weights)
        
        return np.sqrt(variance) * 3.0  # 放大对比度
    
    #---------------------------------------------------------------------------------------------
    # 段落分类器（二元决策）,基于锐化分数分类段落是否为叙事性
    #   diffs 输入参数：
    #       锐化后的差异值列表
    #   决策逻辑：
    #       加权分数（70%）+ 主导度（30%）> 0.35
    #   返回：
    #       combined_score 综合评分
    #       True/False 表示是否具有叙事性
    #---------------------------------------------------------------------------------------------
    def _classify_paragraph(self, weighted, dominance) -> bool:
        # 组合指标：0.35是经验阈值
        combined_score = 0.7 * weighted + 0.3 * dominance
        return combined_score,combined_score > self.semantic_threshold
    
    #---------------------------------------------------------------------------------------------
    # 段落分类器（三元决策）,基于锐化分数分类段落是否为叙事性
    #   diffs 输入参数：
    #       锐化后的差异值列表
    #   决策逻辑：
    #       加权分数（70%）+ 主导度（30%）+ 对比度指数调整
    #   返回：
    #       combined_score 综合评分
    #       True/False 表示是否具有叙事性
    #---------------------------------------------------------------------------------------------
    def _enhanced_classify(self, weighted, dominance, contrast) -> bool:
        # 基础组合分数
        base_score = 0.7 * weighted + 0.3 * dominance
        
        # 使用对比度指数调整：高对比度降低分数，低对比度保持或略微提升
        if contrast < 0.2:  # 低对比度文本
            adjusted_score = base_score * 1.1  # 低对比度奖励
        elif contrast > 0.6: # 高对比度文本
            # 高对比度需验证叙事主导性
            if dominance > 0.4: 
                adjusted_score = base_score * 0.9
            else:
                adjusted_score = base_score * 0.7
        else: # 中等对比度
            adjusted_score = base_score
        
        return adjusted_score,adjusted_score > self.semantic_threshold

    #---------------------------------------------------------------------------------------------
    # 段落分析主方法（核心逻辑）,分析整个段落的叙事性特征
    #   text 输入参数：
    #       text: str, 待判断的文本
    #   返回值：
    #       叙事性综合评分
    #       True/False 表示是否具有叙事性
    #---------------------------------------------------------------------------------------------
    def analyze_paragraph(self, text: str) -> bool:
        sentences = self._split_sentences(text)
        
        if not sentences:
            print("[WARNING]空段落输入")
            return 0.0, False  # 返回默认评分和False

        # 1. 计算每个句子的原始叙事差异
        raw_diffs = [self._calculate_sentence_diff(sent) for sent in sentences]
        
        # 2. 锐化每个句子的差异值
        sharpened_diffs = [self._sharpen_contrast(d) for d in raw_diffs]
        
        # 3. 计算段落整体指标
        # mean_raw            = np.mean(raw_diffs)
        # mean_sharpened      = np.mean(sharpened_diffs)
        weighted_mean       = self._weighted_narrative_score(sharpened_diffs)
        narrative_dominance = self._narrative_dominance(sharpened_diffs)
        contrast_index      = self._contrast_index(raw_diffs)

        # print (f"[DEBUG]原始叙事差异Mean Raw: {mean_raw:.4f},锐化叙事差异Mean Sharpened: {mean_sharpened:.4f}")
        # print (f"[DEBUG]加权叙事评分Weighted Narrative Score: {weighted_mean:.4f}")
        # print (f"[DEBUG]叙事主导度Narrative Dominance:        {narrative_dominance:.4f}")
        # print (f"[DEBUG]对比度指数Contrast Index:             {contrast_index:.4f}")

        return self._enhanced_classify(weighted_mean,narrative_dominance,contrast_index) 
        # return self._classify_paragraph(weighted_mean,narrative_dominance)  

    #---------------------------------------------------------------------------------------------
    # 处理文本主函数
    #     参数:
    #         text: str, 原始生成文本
    #     功能:
    #         1. 编码规范化
    #         2. 全角字符转半角
    #         3. 提取正文内容
    #         4. 过滤非ASCII字符
    #         5. 格式化段落和缩进
    #         6. 语法纠错
    #     返回:
    #         str: 规范化处理后的文本
    #---------------------------------------------------------------------------------------------
    def process(self, text: str) -> str:
        def full_to_half(text)-> str:
            result = []
            for char in text:
                code_point = ord(char)
                if code_point == 0x3000:    # 处理全角空格（U+3000 → U+0020）
                    result.append(' ')
                elif 0xFF01 <= code_point <= 0xFF5E:    # 处理全角 ASCII 可打印字符（0xFF01-0xFF5E → 0x21-0x7E）
                    result.append(chr(code_point - 0xFEE0))
                else:        # 处理其他特殊全角符号（如“”、‘’等）# 补充特殊符号的映射
                    special_map = {
                        '“': '"', '”': '"', '‘': "'", '’': "'", '—': '-','▁': '_', '...': '…'
                    }
                    result.append(special_map.get(char, char))
            return ''.join(result)
        def extract_think_eos(text)-> str:    # 截取 </think> 到 [EOS] 之间的内容
            story_text = ""
            start_markers = [r'\*\*Direct Story Text\*\*',r'\*\*Title: .*?\*\*',r'</think>']    # [r'</p>',r'</s>']   # Qwen 模型用
            end_markers = [r'\[EOS\]']    #  r'<\|begin_of_sentence\|>',r'<\|end_of_sentence\|>',已省略
            for start in start_markers:
                for end  in end_markers:
                    pattern = re.compile(f"({start}.*?){end}", re.DOTALL)
                    match = pattern.search(text)
                    if match:
                        story_text = match.group(1).strip() +  "[EOS]"
                        # print(f"[DEBUG]{start}-->{end}之间提取正文部分成功。") 
                        print("[DEBUG]{}-->{}之间提取正文部分成功。".format(re.sub(r'\\(.)', r'\1', start), re.sub(r'\\(.)', r'\1', end)))
                        if len(story_text.split()) > int(ARTICLE_LENGTH*0.3):break
                        else:continue
                    # else:print("[DEBUG]{}-->{}之间提取正文部分失败。".format(re.sub(r'\\(.)', r'\1', start), re.sub(r'\\(.)', r'\1', end)))
                if story_text:break
            return story_text
        def select_best_segment(split_text = []):
            max_score = -float('inf')
            best_segment = ''
            is_narrative_last = False
            for i, segment in enumerate(split_text, start=1):
                if not segment.strip() :                    continue   # 跳过空段落
                if len(segment.split()) < int(ARTICLE_LENGTH*0.3):  continue   # 跳过过短段落
                score, is_narrative = self.analyze_paragraph(segment)
                print(f"[DEBUG]段落{i}评分：{score:.4f} 叙事性：{is_narrative} 内容：{segment[:100].lstrip()}...")
                if is_narrative and score > max_score:
                    is_narrative_last = is_narrative
                    max_score = score
                    best_segment = segment
            return is_narrative_last,best_segment
        # text = re.sub(r'[#*\-_]{2,}|$.*?$|<.*?>', '', text)     # 清理文本    
        if not isinstance(text, str):       # 确保输入是字符串
            text = str(text) if text is not None else print(f"输入文本错误，请检查输入。")
        text = text.encode('utf-8', 'ignore').decode('utf-8')   # 编码规范化
        text = full_to_half(text)
        text = extract_think_eos(text)
        
        markers = ['</think>','<|begin_of_sentence|>','<|end_of_sentence|>','---']
        pattern = '|'.join(re.escape(m) for m in markers)
        split_text = re.split(pattern, text)
        segment_total = len(split_text)
        print(f"[DEBUG]分割文本，得到{segment_total}个段落")

        story_text=''
        is_narrative = False
        is_narrative,text = select_best_segment(split_text)
        if is_narrative and text: 
            story_text = text
            print(f"[DEBUG]选择的正文内容是：{story_text[:100].lstrip()}")
        else:print("[DEBUG]没有叙事性文本！！！")

        # 剔除start_marker表示的特定内容
        markers = [r'</think>',r'[EOS]',r'---',r'**Direct Story Text**']
        for  marker in markers:
            story_text = re.sub(f"{re.escape(marker)}.*?(\n|$)", '', story_text)
        if len(story_text.split()) > int(ARTICLE_LENGTH*0.3) :
            story_text = self.grammar_tool.correct(story_text) # 语法纠错
        story_text = re.sub(r'[^\x00-\x7F]+', ' ', story_text)  # 过滤非ASCII字符
        story_text = re.sub(r'(?:^|\n\s*\n)\s*(?=\S)', '\n\n    ', story_text)
        return story_text
    
    #---------------------------------------------------------------------------------------------
    # 更新当前主题信息
    #     参数:
    #         new_theme (str): 新主题
    #---------------------------------------------------------------------------------------------
    def update_current_theme(self, new_theme):
        self.current_theme = new_theme
        self._init_semantic_examples()

#---------------------------------------------------------------------------------------------
# 测试程序
#       python -m src.textprocessor 
#    或 python -m unittest textprocessor.py -v 
#    或 python -m unittest src.textprocessor.Test_prog.test_split_articles
#     
#---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import unittest
    from .utils import common_utils,LanguageToolSingleton
    from .model_handler import ModelHandler
    class Test_prog(unittest.TestCase):
        def setUp(self):
            self.rank_ranges = (1, 1000)
            self.rankmin, self.rankmax = self.rank_ranges
            if self.rankmax in [1000,2000,3000,4000,5000]:
                SELECTED_THEME = f"CHILDHOOD_FUN_THEME{self.rankmax//1000}K"
                print(f"选择的主题集SELECTED_THEME={SELECTED_THEME}")
            narrative_examples = THEME_CONFIGS.get(SELECTED_THEME, {}).get("narrative_examples", {})
            self.current_theme = next(iter(narrative_examples.keys())) if narrative_examples else "default_theme"
            print(f"第1个主题{self.current_theme}")
            # themes = list(narrative_examples.keys())
            # if not themes:print("没有可用主题")
            # for i, theme in enumerate(themes, start=1):
            #     examples = narrative_examples.get(theme, [])
            #     examples_str = ', '.join(examples[:1]) + '...' 
            #     print(f"第{i}个主题{theme}")
            #     print(f"主题{theme}示例文本: {examples_str}\n")
            self.grammar_tool = LanguageToolSingleton('en-US')
            self.model_handler = ModelHandler()
            self.semantic_model = self.model_handler._load_model()
            self.processor = NarrativeProcessor(
                grammar_tool = self.grammar_tool,
                current_theme = self.current_theme,
                rank_ranges = self.rank_ranges,
                semantic_model = self.semantic_model
                )
            self.output_dir = common_utils.get_output_dir()      # 获取输入和输出目录
            # self.input_file = os.path.join(self.output_dir, "COCA1000.txt")
            # self.input_file = os.path.join(self.output_dir, "original_text1-1k.txt")
            self.input_file = os.path.join(self.output_dir, "original_text1k-2k.txt")
            # self.input_file = os.path.join(self.output_dir, "original_text2k-3k.txt")
            # self.input_file = os.path.join(self.output_dir, "original_text3k-4k.txt")
            # self.input_file = os.path.join(self.output_dir, "original_text4k-5k.txt")
            self.output_file = os.path.join(self.output_dir, "split_articles_output.txt")
        
        def test_process_articles(self):
            print("开始测试 test_process_articles()函数...")
            if not os.path.exists(self.input_file):
                print(f"输入文件 {self.input_file} 不存在，请确保文件存在并包含要处理的文本。")
                exit(1)
            with open(self.input_file, "r", encoding="utf-8") as f:
                input_text = f.read()
            articles = []
            for idx,(theme,keywords,content) in enumerate(common_utils.split_articles(input_text),start=1):
                self.processor.update_current_theme(theme)
                article, process_time = common_utils._measure_time(self.processor.process,content)
                print(f"[DEBUG]self.processor.process耗时: {process_time:.4f}ms\n")  
                title = f"{'='*15}Article #{idx}#{theme}#{'='*15}\n"   # 生成包含主题的标题行
                if keywords:article_content = f"{title}#current_keywords:{keywords}#\n</think>{article}\n[EOS]\n"    # 如果有关键字行，则在标题后添加      
                else:article_content = f"{title}</think>{article}\n[EOS]\n"
                articles.append(article_content)
            articles_file = '\n'.join(articles)
            with open(self.output_file, "w", encoding="utf-8") as f:
                    f.write(f"{articles_file}\n")
            print("\n测试结束") 
                   
    unittest.main()
