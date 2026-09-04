from .config import *
from .load_vocab import Load_Vocab
from .affix  import affix_rules,prefix_rules,suffix_rules
from .utils import common_utils

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.corpus import brown
from gensim.models import KeyedVectors
from lemminflect import getInflection, getAllInflections, getAllLemmas

nltk.data.path.append(nltk_data_path)                                   # 添加到nltk数据路径
if not os.path.exists(nltk_data_path):
    raise FileNotFoundError(f"请确保 {nltk_data_path} 数据目录存在")

#---------------------------------------------------------------------------------------------
    # 词汇处理器：处理词形还原和词频分析
    
#---------------------------------------------------------------------------------------------
class VocabProcessor:
    #---------------------------------------------------------------------------------------------
    # 类初始化方法
    #     参数:
    #         rank_ranges (tuple): 词频范围 (min, max)
    #         tokenizer: 文本分词器对象
    #     属性初始化:
    #         current_rankmax: 当前实际使用的最大词频
    #         expansion_threshold: 词库扩展阈值(0-1)
    #         expansion_step: 扩展步长比例
    #         allowed_words: 允许使用的词汇集合
    #---------------------------------------------------------------------------------------------
    def __init__(self, rank_ranges=None, tokenizer=None,semantic_model=None):  # 参数顺序调整
        self.rankmin, self.rankmax = rank_ranges
        self.current_rankmax = rank_ranges[1]   # 当前实际使用的最大词频
        self.tokenizer = tokenizer
        self.semantic_model = semantic_model
        self.lemmatizer = WordNetLemmatizer()

        self.word_cache = {}
        self.infl_cache = defaultdict(set)  # 添加变形词缓存
        self.valid_variants_cache = {}
        self.expansion_threshold = EXPANSION_THRESHOLD  # 当未用词比例<x%时触发扩展
        self.expansion_step = 0.3       # 每次扩展30%

        # FreqDist(words.words()+webtext.words()+reuters.words())
        self.freq_dist = FreqDist(brown.words())  # 词频检查
        self.stopwords = set(stopwords.words('english'))
        self.word_vectors = self._load_word_vectors()

        # 加载词频数据
        self.load_vocab=Load_Vocab()
        self.full_vocab, self.target_lemmas, self.allowed_words = \
            self.load_vocab.load_file(WLF_SEL, self.rankmin, self.rankmax)
        
        unused_lemmas = self.load_unused_lemmas()
        self.unused_lemmas = unused_lemmas if unused_lemmas is not None else self.target_lemmas.copy()  
        
        self.valid_variants_cache = self.dynamic_precache_variants(self.allowed_words)
        # self.valid_variants_cache = self.dynamic_precache_variants(self.full_vocab)
        
        # 初始化时预计算词汇嵌入
        self.vocab_graph = self.build_vocab_graph(self.allowed_words)

        self.stemmer = WordStemmer(set(self.target_lemmas), max_loops=3)

    #---------------------------------------------------------------------------------------------
    # 加载上一次未用词
    #     功能:
    #         1. 从JSON文件恢复上一次保存的未用词
    #         2. 更新词汇集合和允许词汇列表
    #     返回:
    #         返回值，上一次未用词
    #---------------------------------------------------------------------------------------------
    def load_unused_lemmas(self):
        def allowed_words_update(saved_unused):
            print(f"[DEBUG]原allowed_words词个数: {len(self.allowed_words)},示例{sorted(list(self.allowed_words))[:5]}")
            print(f"[DEBUG]原target_lemmas词个数: {len(self.target_lemmas)},示例{sorted(list(self.target_lemmas))[:5]}")
            full_vocab_words = set(self.full_vocab.values())
            print(f"[DEBUG]原full_vocab_words词个数: {len(full_vocab_words)},示例{sorted(list(full_vocab_words))[:5]}")
            for word in saved_unused:
                if word in full_vocab_words:
                    self.allowed_words.add(word) 
                    self.target_lemmas.add(word)
            print(f"[DEBUG]更新后allowed_words词个数: {len(self.allowed_words)}")
            print(f"[DEBUG]更新后target_lemmas词个数: {len(self.target_lemmas)}")

        saved_unused = set()
        try:
            self.input_dir = common_utils.get_output_dir()     # 创建输出文件
            with open(os.path.join(self.input_dir, "progress.json"), "r", encoding='utf-8') as f:
                data = json.load(f)
                saved_min, saved_max = data['rankmin'], data['rankmax']
                if saved_min == self.rankmin and saved_max == self.rankmax:           # 检查保存的min/max与当前min/max是否完全相等
                    saved_unused = set(data.get('unused_lemmas', []))                 # 恢复unused_lemmas
                    print(f"[DEBUG]继续最近用词范围: {saved_min}-{saved_max}，未用词汇: {len(saved_unused)},示例{sorted(list(saved_unused))[:5]}")
                    allowed_words_update(saved_unused)
                    return saved_unused
                else:
                    if not(data['normal_stop'] and (saved_max <= self.rankmin < self.rankmax)):
                        return None
                    saved_unused = set(data.get('unused_lemmas', []))                 # 恢复unused_lemmas
                    print(f"[DEBUG]新用词范围{self.rankmin}-{self.rankmax}合并{saved_min}-{saved_max}范围未用词汇:"
                          f"{len(saved_unused)},示例{sorted(list(saved_unused))[:5]}")
                    allowed_words_update(saved_unused)
                    return None
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print("[ERROR]vocab_processor.py提示无有效progress.json文件")
        except KeyError as e:
            print(f"[ERROR]vocab_processor.py提示JSON字段缺失: {str(e)}")
        return None  
    
    

    #---------------------------------------------------------------------------------------------
    # 加载预训练词向量
    #     返回:
    #         KeyedVectors: 预加载的词向量模型
    #     异常:
    #         FileNotFoundError: 词向量文件不存在时抛出
    #         RuntimeError: 加载过程发生错误时抛出
    #---------------------------------------------------------------------------------------------
    def _load_word_vectors(self):
        """加载预转换的二进制词向量"""
        try:
            if not os.path.exists(GloVe_path):
                raise FileNotFoundError(f"词向量文件缺失: {GloVe_path}")
            return KeyedVectors.load(GloVe_path, mmap='r')  # 确保使用正确的加载方法
        except Exception as e:
            raise RuntimeError(f"词向量加载失败: {str(e)}")
        
    #---------------------------------------------------------------------------------------------
    # 构建词汇共现关系图
    #     参数:
    #         lemmas (set): 词根集合
    #     返回:
    #         defaultdict(set): 词汇关系图
    #---------------------------------------------------------------------------------------------
    def build_vocab_graph(self, lemmas):
        """构建词汇共现关系图"""
        graph = defaultdict(set)
        for lemma in lemmas:
            related = self.get_related_words(lemma, top_n=10)
            graph[lemma].update(related)
        return graph
    
    #---------------------------------------------------------------------------------------------
    # 获取语义相关词
    #     参数:
    #         word (str): 查询词
    #         top_n (int): 返回数量，默认10
    #     返回:
    #         set: 相关词集合
    #---------------------------------------------------------------------------------------------
    def get_related_words(self, word, top_n=10):
        try:
            similar = self.word_vectors.most_similar(word, topn=top_n)
            return {w for w, _ in similar if w in self.word_vectors}
        except KeyError:
            return set()

    #---------------------------------------------------------------------------------------------
    # 增强的词形还原
    #     参数:
    #         word: 文本分词器后的词
    #     返回:
    #         lemma: 词原形
    #---------------------------------------------------------------------------------------------
    def enhanced_lemmatize(self, word: str) -> str:
        # 标准词形还原
        lemma = self.lemmatize(word).lower()
        # 词干提取备用方案
        if lemma not in self.target_lemmas:
            stemmed = self.stemmer.stem(word)
            return stemmed if stemmed in self.target_lemmas else lemma
        return lemma
    
    #---------------------------------------------------------------------------------------------
    # 验证单词是否存在于词向量库
    #     参数:
    #         word (str): 待验证单词
    #     返回:
    #         bool: 存在性验证结果
    #---------------------------------------------------------------------------------------------
    def word_exists(self, word):
        try:
            if self.freq_dist[word] < 5 :  
                return False
            if len(wn.synsets(word)) > 0 : 
                return True
        except AttributeError:
            return False

    #---------------------------------------------------------------------------------------------
    # 获取WordNet词性标签
    #     参数:
    #         treebank_tag (str): Penn Treebank词性标签
    #     返回:
    #         nltk.corpus.wordnet: 对应的WordNet词性
    #---------------------------------------------------------------------------------------------
    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return nltk.corpus.wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return nltk.corpus.wordnet.VERB
        elif treebank_tag.startswith('N'):
            return nltk.corpus.wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return nltk.corpus.wordnet.ADV
        else:
            return nltk.corpus.wordnet.NOUN

    #---------------------------------------------------------------------------------------------
    # 带缓存的词形还原
    #     参数:
    #         word (str): 待处理单词
    #     返回:
    #         str: 词元形式
    #---------------------------------------------------------------------------------------------
    def lemmatize(self, word):
        if word not in self.word_cache:
            pos_tag = nltk.pos_tag([word])[0][1]
            pos = self.get_wordnet_pos(pos_tag)
            self.word_cache[word] = self.lemmatizer.lemmatize(word, pos)
        return self.word_cache[word]
    
    #---------------------------------------------------------------------------------------------
    # 获取单词所有屈折变化
    #     参数:
    #         word (str): 原形单词
    #     返回:
    #         set: 所有有效的屈折变化形式集合
    #---------------------------------------------------------------------------------------------
    def get_inflections(self, word):
        if word not in self.infl_cache:
            try:
                # 获取所有屈折形式的字典，格式为 {tag: [forms]}
                all_infls = getAllInflections(word)
                # 定义需要提取的形态标签
                selected_tags = [
                    "VBD","VBN","VBG","VBP","VBZ",       # 动词时态
                    "NNS",                               # 名词复数
                    "JJR", "JJS",                        # 形容词比较级/最高级
                    "RB"                                 # 副词
                ]
                # 合并所有需要的屈折形式
                infls = []
                for tag in selected_tags:
                    infls.extend(all_infls.get(tag, []))  # 若标签不存在则返回空列表
                # 过滤空值并去重
                self.infl_cache[word] = set(filter(None, infls))
            except Exception as e:
                self.infl_cache[word] = set()
        return self.infl_cache[word]

    #---------------------------------------------------------------------------------------------
    # 生成符合英语拼写规则的前缀/后缀变形
    #     参数:
    #         word (str): 原形单词
    #     返回:
    #         set: 有效的前缀/后缀变形集合
    #---------------------------------------------------------------------------------------------
    @staticmethod
    def get_affix_variants(word):
        variants = set()
        # 前缀处理（带语音同化规则）
        for (prefix, rule) in prefix_rules:
            result = rule(word.lower())
            if result and (result not in variants):
                variants.add(result.capitalize() if word.isupper() else result)
        # 后缀处理（多规则链式匹配）
        for (suffix, rules) in suffix_rules:
            candidate = None
            for rule in rules:
                temp = rule(word.lower())
                if temp:    candidate = temp
            if candidate:
                # 保留原始大小写格式
                final = candidate.capitalize() if word.isupper() else candidate
                variants.add(final)

        return variants - {word}
    
    #---------------------------------------------------------------------------------------------
    # 生成合成词变体
    #     参数:
    #         word (str): 原形单词
    #     返回:
    #         set: 有效的合成词集合
    #---------------------------------------------------------------------------------------------
    @staticmethod
    def get_compound_words(word):
        compounds = set()
        # 简单合成规则（可根据需要扩展）
        for connector in ['', '-', '_']:
            parts = split(word)
            if len(parts) > 1:
                compounds.add(connector.join(parts))
        return compounds
    
    #---------------------------------------------------------------------------------------------
    # 获取经过验证的屈折变化
    #     参数:
    #         word (str): 原形单词
    #     返回:
    #         set: 有效屈折变化集合
    #---------------------------------------------------------------------------------------------
    def get_valid_inflections(self, word):
        raw_infls = self.get_inflections(word)
        # return raw_infls
        return {w for w in raw_infls if self.word_exists(w)}
        

    #---------------------------------------------------------------------------------------------
    # 获取合法前缀/后缀变形
    #     参数:
    #         word (str): 原形单词
    #     返回:
    #         set: 有效变形集合
    #---------------------------------------------------------------------------------------------
    def get_valid_affixes(self,word):
        raw_affixes = VocabProcessor.get_affix_variants(word)
        return {w for w in raw_affixes if self.word_exists(w)}

    #---------------------------------------------------------------------------------------------
    # 获取合法合成词
    #     参数:
    #         word (str): 原形单词
    #     返回:
    #         set: 有效合成词集合
    #---------------------------------------------------------------------------------------------
    def get_valid_compounds(self,word):
        raw_compounds = VocabProcessor.get_compound_words(word)
        return {w for w in raw_compounds if self.word_exists(w)}
    
    #---------------------------------------------------------------------------------------------
    # 检查是否需要扩展词库
    #     算法说明:
    #         根据未使用词根比例决定是否扩展词频范围
    #---------------------------------------------------------------------------------------------
    def check_expansion(self):
        if self.expansion_threshold >= 1.0:  # 阈值大于等于1.0时，不进行扩展
            return
        if len(self.unused_lemmas) / len(self.target_lemmas) >= self.expansion_threshold:
            return  # 未用词比例高于阈值时不扩展
        # 计算新的最大词频范围
        # new_max = int(self.rankmax * (1 + self.expansion_step))
        new_max = int(self.rankmax + (self.rankmax - self.rankmin) * self.expansion_step)
        print(f"\n[DEBUG]触发词库扩展: {self.rankmax} → {new_max}")
        # 直接从内存中的完整词库筛选新范围的词
        new_allowed = {
            word for rank, word in self.full_vocab.items()
            if self.rankmax < rank <= new_max and word.isalpha()
        }
        # 更新允许使用的词汇范围
        existing_allowed = set(self.allowed_words)
        self.allowed_words = existing_allowed.union(new_allowed)
        # 仅更新当前最大词频标记
        self.current_rankmax = new_max
        # 更新缓存
        # self.valid_variants_cache = self.dynamic_precache_variants(new_allowed - existing_allowed)
        self.valid_variants_cache = self.dynamic_precache_variants(self.allowed_words)
        # 重建词汇关系图
        self.vocab_graph = self.build_vocab_graph(self.allowed_words)
        # 重新准备词汇token
        self.allowed_tokens, self.capital_words = self.prepare_vocab_tokens()
        self.expansion_threshold = 1.0
        print(f"[DEBUG]允许词库已扩展至 {len(self.allowed_words)} 词 | 新增 {len(new_allowed)} 词")

    #---------------------------------------------------------------------------------------------
    # 动态预缓存单词变体
    #     参数:
    #         vocab (str): 原形词表
    #     返回:
    #         set: 预缓存的变体集合
    #---------------------------------------------------------------------------------------------
    def dynamic_precache_variants(self, vocab):
        allowed_variants={}
        for lemma in vocab:
            allowed_variants[lemma] = self._precache_variants(lemma)
            if lemma == 'a' :
                allowed_variants[lemma].add('an')
        return allowed_variants
    
    #---------------------------------------------------------------------------------------------
    # 预缓存单词变体
    #     参数:
    #         lemma (str): 词根
    #     返回:
    #         set: 预缓存的变体集合
    #---------------------------------------------------------------------------------------------
    def _precache_variants(self, lemma):
        return (
            self.get_valid_inflections(lemma) |
            self.get_valid_affixes(lemma) |
            self.get_valid_compounds(lemma)
        )
    
    #---------------------------------------------------------------------------------------------
    # 预生成词汇变体及对应token
    #     返回:
    #         tuple(set, set): (允许的token集合, 首字母大写的单词集合)
    #---------------------------------------------------------------------------------------------
    def prepare_vocab_tokens(self,allowed_words=set(),isASCII=True):
        if self.tokenizer is None:
            raise ValueError("tokenizer 未提供，无法执行此操作")
        if not allowed_words :
            allowed_words = self.allowed_words     # self.allowed_words | self.full_vocab

        variants = set()
        for lemma in allowed_words:     # 合并预缓存的有效变体
            if lemma not in self.valid_variants_cache:
                self.valid_variants_cache[lemma] = self._precache_variants(lemma)
            variants.update(self.valid_variants_cache[lemma])
        
        capital_words = set()
        word_variants = set()       # 生成大小写变体
        for word in allowed_words | variants:
            capital_word = word[0].upper() + word[1:]
            capital_words.add(capital_word)
            word_variants.update({
                f' {word}', f' {word.lower()}', f' {capital_word}',
                word, word.lower(), capital_word
            })
        
        allowed_tokens = set()      # 预编码token
        for word in word_variants | capital_words :
            word_tokens = self.tokenizer.encode(word, add_special_tokens=False)
            allowed_tokens.update(word_tokens)
        
        if isASCII:
            chinese_chars = {'　','，','。','？','！','；','：','「','」','（','）','【','】','、','“','”','‘','’','—','▁','...'}
            for char in chinese_chars:  # 添加中文字符
                if char in self.tokenizer.vocab:
                    char_tokens = self.tokenizer.encode(char, add_special_tokens=False)
                    allowed_tokens.update(char_tokens)
            
            punctuations = ["'t","'s","'ve", "'d", "'ll", "'re", "'m","'D", "'L", "'Re", "'M"] # 添加特殊符号
            for punc in punctuations:   
                punc_tokens = self.tokenizer.encode(punc, add_special_tokens=False)
                allowed_tokens.update(punc_tokens)
            
            unicode_ranges = [      # 添加Unicode字符
                (0x0370, 0x03FF),   # 希腊字母
                (0x2200, 0x22FF),   # 数学符号
                (0x2600, 0x26FF),   # 杂项符号（如★☺）
                (0x1F300, 0x1F6FF), # Emoji扩展
                (0x1F900, 0x1F9FF)  # 补充符号
            ]
            for start, end in unicode_ranges:
                for codepoint in range(start, end + 1):
                    char = chr(codepoint)
                    char_tokens = self.tokenizer.encode(char, add_special_tokens=False)
                    allowed_tokens.update(char_tokens)

            specific_chars = ['<｜begin▁of▁sentence｜>','<｜end▁of▁sentence｜>', '</think>', self.tokenizer.pad_token,self.tokenizer.eos_token," ", "\n", "\t", "\n\n"]
            for char in specific_chars:
                # if char in self.tokenizer.vocab:
                char_tokens = self.tokenizer.encode(char, add_special_tokens=False)
                allowed_tokens.update(char_tokens)
            
            byte_tokens = set(i for i in range(256) if i < self.tokenizer.vocab_size)   # 字节级token：0-255 
            allowed_tokens.update(byte_tokens)
            
            special_tokens = list(self.tokenizer.special_tokens_map.values())   # 特殊token处理
            # print(f"[DEBUG]验证有效性前special_tokens:{special_tokens}")
            flat_special_tokens = []    # 展开可能存在的嵌套列表并去重
            for token in special_tokens:
                if isinstance(token, list): flat_special_tokens.extend(token)
                else:   flat_special_tokens.append(token)
            unique_special_tokens = list(set(flat_special_tokens))  # 去重处理
            valid_special_tokens = [token for token in unique_special_tokens 
                if token in self.tokenizer.vocab]   # 获取有效token ID
            try:        # 转换token并验证
                # print(f"[DEBUG]验证有效性后valid_special_tokens:{valid_special_tokens}")
                special_ids = self.tokenizer.convert_tokens_to_ids(valid_special_tokens)
            except Exception as e:
                print(f"[ERROR] 特殊token转换失败: {str(e)}")
                special_ids = []
            allowed_tokens.update(special_ids)
        
        print(f"[DEBUG]模型真实词汇表大小: {self.tokenizer.vocab_size}")
        print(f"[DEBUG]候选token_id最大值: {max(allowed_tokens)}")
        print(f"[DEBUG]过滤后有效token数量: {len([t for t in allowed_tokens if t < self.tokenizer.vocab_size])}")
        return allowed_tokens, capital_words
    
    #---------------------------------------------------------------------------------------------
    # 获取当前词群对应的所有token
    #     参数:
    #         word_cluster (set): 词群集合
    #     返回:
    #         set: 对应的token集合
    #---------------------------------------------------------------------------------------------
    def get_cluster_tokens(self, word_cluster):
        if self.tokenizer is None:
            raise ValueError("tokenizer 未提供，无法执行此操作")
        tokens = set()
        for word in word_cluster:
            # 获取单词本体及其变体
            base_tokens = self.tokenizer.encode(f' {word}', add_special_tokens=False)
            # # 获取变形词token（需提前预生成）
            variants = self.valid_variants_cache.get(word, set())
            for v in variants:
                tokens.update(self.tokenizer.encode(f' {v}', add_special_tokens=False))
            tokens.update(base_tokens)
        return tokens
    
    #---------------------------------------------------------------------------------------------
    # 更新未使用的词根集合
    #     参数:
    #         unused_lemmas (set): 新的未使用词根集合
    #---------------------------------------------------------------------------------------------
    def update_context(self, unused_lemmas):
        # 过滤掉无效的词根
        valid_unused = {lemma for lemma in unused_lemmas if lemma in self.target_lemmas}
        # 取交集确保不会引入新词
        self.unused_lemmas = self.unused_lemmas.intersection(valid_unused)

    #---------------------------------------------------------------------------------------------
    # 优化选择最佳种子词
    #     返回:
    #         str: 最佳种子词
    #     算法说明:
    #         综合考虑词汇连接数和未使用次数选择种子词
    #---------------------------------------------------------------------------------------------
    def _select_seed_word(self):
        if not self.unused_lemmas:
            return None
        # 计算词汇权重：连接数 * 未使用次数
        word_weights = {}
        for word in self.unused_lemmas:
            # 计算连接数
            connections = len(self.vocab_graph[word] & self.unused_lemmas)
            # 计算未使用次数（假设每个词初始未使用次数为1）
            unused_count = 1  # 可以根据需要扩展为更复杂的计算
            # 综合权重
            word_weights[word] = connections * unused_count
        # 选择权重最大的词作为种子词
        return max(word_weights, key=word_weights.get)
    

    
    #---------------------------------------------------------------------------------------------
    # 扩展词群
    #     参数:
    #         seed (str): 种子词
    #         max_size (int): 最大词群大小
    #     返回:
    #         list: 扩展后的词群列表
    #     算法说明:
    #         引入多样性系数进行词群扩展
    #---------------------------------------------------------------------------------------------
    def _expand_cluster(self, seed, max_size=WORD_CLUSTER_LENGTH):
        cluster = {seed}
        candidates = self.vocab_graph[seed] & self.unused_lemmas
        if not candidates:      # 添加候选词存在性检查
            print(f"警告: 种子词 '{seed}' 无可用候选词，使用随机扩展")
            candidates = random.sample(list(self.unused_lemmas), min(5, len(self.unused_lemmas)))
        diversity_scores = {            # 多样性评分 = 语义相关度 * 随机因子
            w: len(self.vocab_graph[w]) * np.random.uniform(0.8, 1.2) 
            for w in candidates
        }
        while len(cluster) < max_size and diversity_scores:  # 添加diversity_scores非空检查
            next_word = max(diversity_scores, key=diversity_scores.get)
            cluster.add(next_word)
            del diversity_scores[next_word]
            new_candidates = (self.vocab_graph[next_word] - cluster) & self.unused_lemmas   # 更新候选集时加入新词的关联词（添加存在性过滤）
            for w in new_candidates:
                if w not in diversity_scores:
                    diversity_scores[w] = len(self.vocab_graph[w]) * np.random.uniform(0.8, 1.2)
        return list(cluster)[:max_size]
    
#---------------------------------------------------------------------------------------------
#    词干提取器类
#---------------------------------------------------------------------------------------------
class WordStemmer:
    def __init__(self, coca_set, max_loops=3):
        self.coca_set = coca_set          # COCA词表集合（小写）
        self.max_loops = max_loops        # 最大处理层数
        self.visited = set()              # 防重复处理
        # 定义按优先级排序的词缀规则（副词 → 形容词 → 名词 → 动词 → 前缀）
        self.rules = affix_rules
    def stem(self, word: str) -> str:
        queue = deque([(word.lower(), 0)])
        self.visited.clear()
        
        while queue:
            current, depth = queue.popleft()
            
            if current in self.coca_set:return current      # 匹配COCA
            
            if depth >= self.max_loops:             # 达到最大深度时
                continue
            #     return word          
            # else: # 当没有达到最大深度，而且队列非空，继续处理队列
            #     if queue:continue                           # 继续处理队列
            # 生成所有可能的变形
            for rule in self.rules:
                pos, affix, length, transform = rule
                candidate = None
                # 检查是否匹配词缀
                if pos == 'suffix' and current.endswith(affix):
                    candidate = transform(current)
                elif pos == 'prefix' and current.startswith(affix):
                    candidate = transform(current)
                # 验证候选词合法性
                if candidate and candidate not in self.visited:
                    self.visited.add(candidate)
                    queue.append((candidate, depth + 1))
        return word