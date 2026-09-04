from .config import *
from .vocab_processor import VocabProcessor
from .utils import MemoryMonitor,common_utils,LanguageToolSingleton

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.stats import entropy

class article_analyzer:
    #---------------------------------------------------------------------------------------------
    # 文章分析器初始化
    #     参数:
    #         target_lemmas (set): 目标词根集合
    #         current_prompt (str): 当前生成提示词
    #         current_theme (str): 当前文章主题
    #         vocab_proc (VocabProcessor): 词汇处理器实例
    #---------------------------------------------------------------------------------------------
    def __init__(self,vocab_proc=None,semantic_model=None):  
        # 创建输出文件
        self.output_dir = common_utils.get_output_dir()
        # 添加上下文存储属性
        self.current_prompt = ""
        self.current_theme = ""
        self.current_keywords = set()
        # 初始化词汇处理器
        self.vocab_proc = vocab_proc  
        # 初始化语义模型
        self.semantic_model = semantic_model
        # 状态跟踪
        self.target_lemmas = self.vocab_proc.target_lemmas
        self.unused_lemmas = self.vocab_proc.unused_lemmas
        self.used_lemmas = self.target_lemmas - self.unused_lemmas
        self.timestamp_str,self.article_counter,self.generate_count,self.total_words = self.load_progress()
        self.recent_new_words = []
        self.grammar_tool = LanguageToolSingleton('en-US')
        # 创建语法解析器
        self.parser = nltk.RegexpParser('''
            NP: {<DT|PP\$>?<JJ>*<NN.*>+}  # 名词短语
            VP: {<VB.*><NP|PP>}           # 动词短语
            PP: {<IN><NP>}                # 介词短语
        ''')

        # self.validation_thresholds = {
        #     'avg_length': (5, 25),
        #     'grammar_errors': 3,
        #     'coherence': 75,
        #     'theme_focus': 35,
        #     'flesch': 45,
        #     'fkgl': 13,
        #     'keyword_score': 0
        # }

        self.validation_thresholds = {
            'avg_length': (5, 30),
            'grammar_errors': 3,
            'coherence': 75,
            'theme_focus': 0,
            'flesch': 40,
            'fkgl': 13,
            'keyword_score': 0
        }

        self.success_stats_sum = defaultdict(float)
        self.total_stats_sum = defaultdict(float)
        self.success_themes = defaultdict(int)
        self.total_themes = defaultdict(int)
        self.history_stats = defaultdict(list)

        # 内存监控
        self.mem_monitor = psutil.Process(os.getpid())
        # 启动内存监控
        self.memory_monitor = MemoryMonitor()
        threading.Thread(target=self.memory_monitor._memory_monitor, daemon=True).start()
        
    #---------------------------------------------------------------------------------------------
    # 计算基于关键词的文本主题集中度关键指标：TopN占比，信息熵集中度，基尼系数
    #     参数:
    #         text (str): 待分析文本内容
    #         current_keywords (list): 当前关键词列表
    #     返回:
    #         # 综合评分 ：0.4*TopN占比 + 0.4*信息熵集中度 + 0.2*基尼系数
    #---------------------------------------------------------------------------------------------
    def calculate_keyword_metrics(self,text, current_keywords=set(),top_n=5):
        clean_keywords = {kw.lower() for kw in current_keywords if isinstance(kw, str)}
        if not clean_keywords:
            print("[WARNING]No valid keywords found.")
            return 0.0
        vectorizer = TfidfVectorizer(       # 提取主题关键词的TF-IDF向量
                vocabulary=list(current_keywords),
                use_idf=False,  # 单文档不需要IDF
                norm='l1'       # 标准化为概率分布
            )
        tf_matrix = vectorizer.fit_transform([text]).toarray()[0]   # 创建文档列表
        # vocabulary = vectorizer.get_feature_names_out()
        valid_indices = tf_matrix > 0               # 计算关键词集中度指标
        valid_weights = tf_matrix[valid_indices]    
        if len(valid_weights) == 0:     return 0.0  # 过滤非零权重的关键词
        sorted_indices = np.argsort(valid_weights)[::-1]    # TopN占比
        topn_ratio = np.sum(valid_weights[sorted_indices[:top_n]])
        ent = entropy(valid_weights)    # 信息熵集中度
        max_ent = np.log(len(valid_weights))
        normalized_ent = ent / max_ent if max_ent > 0 else 0.0
        concentration_from_entropy = 1 - normalized_ent
        sorted_weights = np.sort(valid_weights)     # 基尼系数
        n = len(sorted_weights)
        cumulative_weights = np.cumsum(sorted_weights)
        gini = 1 - (2 * np.sum(cumulative_weights) / (n * cumulative_weights[-1]) - 1)
        keyword_metrics_score = (       # 综合评分 
            0.4 * topn_ratio + 
            0.4 * concentration_from_entropy +
            0.2 * gini
        ) * 100
        return keyword_metrics_score
    
    #---------------------------------------------------------------------------------------------
    # 计算没有给定关键词的文本主题集中度关键指标：TopN占比，信息熵集中度，基尼系数
    #     参数:
    #         text (str): 待分析文本内容
    #     返回:
    #         # 综合评分 ：0.4*TopN占比 + 0.4*信息熵集中度 + 0.2*基尼系数
    #---------------------------------------------------------------------------------------------
    def calculate_nonkeyword_metrics(self,texts, top_n=5):
        if isinstance(texts, str):texts = [texts]   # 确保输入是字符串列表
        vectorizer = TfidfVectorizer(       # 预处理：创建TF-IDF向量器
            stop_words="english", 
            min_df=1,             
            max_df=1,
            ngram_range=(1, 2)  # 包含双词短语              
        )
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            # vocabulary = vectorizer.get_feature_names_out()
        except ValueError as e:
            return [50.0] * len(texts)      # 无有效词汇时返回默认值
        keyword_metrics_score = []
        for i, doc_vec in enumerate(tfidf_matrix):
            vector = doc_vec.toarray().flatten()    # 获取稠密向量并标准化为概率分布
            total_weight = vector.sum()
            if total_weight <= 0:
                keyword_metrics_score = 50.0  # 默认分值
                continue
            normalized_vec = vector / total_weight
            focus_n = top_n * 3   # 聚焦分析范围,15个核心词
            sorted_weights = normalized_vec.copy()
            sorted_weights.sort()
            sorted_weights = sorted_weights[::-1][:focus_n]  # 取前focus_n个词  
            total_focus_weight = sum(sorted_weights)    # 在focus_n个词上重新归一化
            focus_weights = [w/total_focus_weight for w in sorted_weights]
            topn_ratio = sum(focus_weights[:min(top_n, focus_n)])   # 在这focus_n个词上计算指标
            # top_keywords = [(vocabulary[idx], normalized_vec[idx])      # 获取实际关键词
                            # for idx in sorted_indices[:top_n] if normalized_vec[idx] > 0]
            valid_values = normalized_vec[normalized_vec > 0]       # 信息熵计算 (避免log0错误)
            if len(valid_values) > 1:
                ent = entropy(valid_values)
                max_ent = np.log(len(valid_values))
                normalized_ent = ent / max_ent
                concentration_from_entropy = 1 - normalized_ent
            else:concentration_from_entropy = 1.0 if len(valid_values) > 0 else 0.0 # 只有1个有效词的情况
            sorted_weights = np.sort(normalized_vec)    # 基尼系数计算 ,将权重从小到大排序
            n = len(sorted_weights)
            if n == 0: gini = 0.0
            else:
                index = np.arange(1, n+1)
                gini = (np.sum((2 * index - n - 1) * sorted_weights)) / (n * np.sum(sorted_weights))
            combined_score = (  # 综合评分 
                0.5 * topn_ratio + 
                0.4 * concentration_from_entropy +
                0.1 * gini
            ) * 100
            keyword_metrics_score.append(combined_score)
        return keyword_metrics_score

    #---------------------------------------------------------------------------------------------
    # 计算语法结构差异度
    #     参数:
    #         sent1 (str): 第一句话
    #         sent2 (str): 第二句话
    #     返回:
    #         float: 语法结构差异度（0表示完全相同的结构，1表示完全不同的结构）
    #     功能说明:
    #         通过分析句子的语法结构树，计算两句话的语法结构差异
    #---------------------------------------------------------------------------------------------
    def _syntactic_difference(self, sent1, sent2):
        try:    # 解析语法树
            tree1 = self.parser.parse(sent1.split())
            tree2 = self.parser.parse(sent2.split())
            def simplify_tree(tree):        # 简化树结构（仅保留主干）
                return "|".join([str(child.label()) for child in tree if isinstance(child, nltk.Tree)])
            struct1 = simplify_tree(tree1)      # 计算结构相似度
            struct2 = simplify_tree(tree2)
            seq_matcher = difflib.SequenceMatcher(None, struct1, struct2)   # 使用 difflib 计算字符串差异
            similarity = seq_matcher.ratio()  # 获取相似度比例
            return 1.0 - similarity  # 返回差异度
        except: return 0.5      # 解析失败时默认返回中等差异         
    
    #---------------------------------------------------------------------------------------------
    # 计算文本分析指标
    #     参数:
    #         text (str): 待分析文本内容
    #         current_theme (list): 当前主题词列表
    #         current_keywords (list): 当前关键词列表
    #     返回:
    #         Tuple[float, float, float]: (上下文一致性得分, 主题集中度得分, 关键词匹配度得分)
    #     功能说明:
    #         1. 上下文一致性: 衡量文本内部的连贯性
    #         2. 主题集中度: 衡量文本与主题的相关性
    #         3. 关键词匹配度: 衡量关键词在文本中的覆盖率
    #---------------------------------------------------------------------------------------------
    def calculate_text_metrics(self, text, current_theme="", current_keywords=set()):
        sentences = nltk.sent_tokenize(text)
        words = [w.lower() for w in word_tokenize(text) if w.isalpha()]
        
        if isinstance(current_keywords,str):
            cleaned_str = re.sub(r'[^a-zA-Z,]', '', current_keywords)
            current_keywords = {kw.strip().strip("'").strip('"') for kw in cleaned_str.split(",")}
        else: current_keywords = set(current_keywords)
        valid_keywords = {kw for kw in current_keywords if self.vocab_proc.word_exists(kw) }
        
        valid_theme_words = {w for w in current_theme.split() if w.isalpha() and self.vocab_proc.word_exists(w)}
        keyword_set = valid_keywords | valid_theme_words
        
        matched = set()
        for w in words:
            lemma = self.vocab_proc.lemmatize(w)
            if lemma in keyword_set:
                matched.add(lemma)
        keyword_score = len(matched) / len(keyword_set) * 100 if keyword_set else 0.0
        if len(sentences) < 2:
            context_coherence = 0.0
        else:
            diversity_factor = min(1.0, len(set(sentences)) / len(sentences))   # 多样性惩罚因子
            vectors = []        
            for sent in sentences:  # 句向量计算
                words = [w.lower() for w in word_tokenize(sent) if w.isalpha() and w not in self.vocab_proc.stopwords]
                if not words:   continue
                word_vecs = []
                for w in words:     # 词向量加权平均
                    try:word_vecs.append(self.vocab_proc.word_vectors[w])
                    except KeyError:    continue
                if word_vecs:    vectors.append(np.mean(word_vecs, axis=0))
            similarities = []
            for i in range(len(vectors)-1):     # 防止重复语句的虚高得分
                syntax_diff = self._syntactic_difference(sentences[i], sentences[i+1])  # 添加句法结构相似性检测
                cos_sim = np.dot(vectors[i], vectors[i+1]) / (
                    np.linalg.norm(vectors[i]) * np.linalg.norm(vectors[i+1]) + 1e-8)
                adjusted_sim = max(0, min(cos_sim, 1)) * diversity_factor       # 应用多样性惩罚
                if syntax_diff < 0.3:  # 高度相似的句子结构
                    adjusted_sim *= 0.7  # 降低30%的相似度评分
                similarities.append(adjusted_sim)
            context_coherence = np.mean(similarities) * 100 if similarities else 0.0
        
        if not current_theme:       #  主题集中度计算
            theme_focus = self.calculate_nonkeyword_metrics(text)[0] * 2.5
            # print(f"[DEBUG]无theme主题集中度得分:{theme_focus:.4f}")
        else:                       # 主题向量计算
            theme_vectors = []
            for word in current_theme:
                try:theme_vectors.append(self.vocab_proc.word_vectors[word.lower() 
                    if word.isalpha() and word not in self.vocab_proc.stopwords else ""])
                except KeyError:    continue
            if not theme_vectors:   theme_focus = self.calculate_nonkeyword_metrics(text)[0] * 2.5
            else:
                theme_center = np.mean(theme_vectors, axis=0)
                text_vectors = []
                for sent in sentences:  # 文本向量计算
                    words = [w.lower() for w in word_tokenize(sent) 
                             if w.isalpha() and w not in self.vocab_proc.stopwords]
                    if not words:  continue
                    word_vecs = []
                    for w in words:     # 词向量平均
                        try:    word_vecs.append(self.vocab_proc.word_vectors[w])
                        except KeyError:    continue
                    if word_vecs:   text_vectors.append(np.mean(word_vecs, axis=0))
                theme_scores = []   # 添加主题演化检测
                for i, vec in enumerate(text_vectors):  # 计算与主题中心的相似度
                    similarity = np.dot(vec, theme_center) / (
                        np.linalg.norm(vec) * np.linalg.norm(theme_center) + 1e-8)
                    similarity = np.clip(similarity, 0.0, 1.0)  # 负值归零
                    theme_scores.append(similarity)
                unique_content_score = min(1.0, len(set(sentences)) / len(sentences)) \
                                        * np.mean(theme_scores) * 100   # 防止重复内容的高分   
            keyword_metrics_score = self.calculate_keyword_metrics(text,keyword_set) if keyword_set else 0.0
            theme_focus = (             # 最终主题集中度公式
                0.80 * keyword_metrics_score +
                0.15 * unique_content_score +
                0.05 * keyword_score
            )
        def clamp(value):       return max(0.0, min(round(value, 2), 100.0))
        return (
            clamp(context_coherence),
            clamp(theme_focus),
            clamp(keyword_score)
        )
    
    #---------------------------------------------------------------------------------------------
    # 分析生成文本的学习效果
    #     参数:
    #         text (str): 待分析文本内容
    #     返回:
    #         Dict: 包含各项质量指标的字典
    #---------------------------------------------------------------------------------------------
    def analyze(self, text: str) -> dict:
        stats = {
            'avg_length': 0.0,
            'grammar_errors': 0,
            'coherence': 0.0,
            'theme_focus': 0.0,
            'flesch': 0,
            'fkgl': 0.0,
            'keyword_score': 0.0,
            'is_valid': False
        }
        # 参数类型校验和空值处理
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            print(f"[DEBUG]无效输入文本,类型:{type(text)},长度{len(text)if type(text)==str else 1 }")
            stats["is_valid"] = False
            self.generate_count += 1
            return stats

        def _check_validation(stats):
            """统一验证逻辑"""
            t = self.validation_thresholds
            return all([
                t['avg_length'][0] <= stats['avg_length'] <= t['avg_length'][1],
                stats['grammar_errors'] <= t['grammar_errors'],
                stats['coherence'] >= t['coherence'],
                stats['theme_focus'] >= t['theme_focus'],
                stats['flesch'] >= t['flesch'],
                stats['fkgl'] <= t['fkgl'],
                stats['keyword_score'] >= t['keyword_score']
            ])

        sentences = nltk.sent_tokenize(str(text))  
        avg_length = np.mean([len(s.split()) for s in sentences])
        print(f"平均句长: {avg_length:.1f} (标准7-15)")
        
        # 语法正确性检查
        grammar_errors = []
        if len(text.split()) > ARTICLE_LENGTH*0.3:
            grammar_errors = self.grammar_tool.check(text)
            print(f"语法错误数: {len(grammar_errors)}")
        else:   print(f"文章过短，无法检查语法")

        # 计算文本指标
        context_coherence, theme_focus, keyword_score = self.calculate_text_metrics(
            text, 
            self.current_theme, 
            self.current_keywords
        )
        print(f"上下文一致性: {context_coherence:.1f}%")
        print(f"主题集中度: {theme_focus:.1f}%")
        print(f"关键词匹配度: {keyword_score:.1f}%")

        flesch = textstat.flesch_reading_ease(text)
        print(f"Flesch可读性指数: {flesch}%")
        fkgl_score = textstat.flesch_kincaid_grade(text)
        print(f"Flesch-Kincaid等级: {fkgl_score:.1f}")
        stats = {
            "avg_length": avg_length,
            "grammar_errors": len(grammar_errors),
            "coherence": context_coherence,
            "theme_focus": theme_focus,
            "flesch": flesch,
            "fkgl": fkgl_score,
            "keyword_score": keyword_score,
        }
        stats["is_valid"] = _check_validation(stats)
        self.generate_count += 1

        params = ['avg_length', 'grammar_errors', 'coherence', 'theme_focus', 'flesch','fkgl','keyword_score' ]
        for param in params:
            self.total_stats_sum[param] += stats[param]
            if stats['is_valid']:
                self.success_stats_sum[param] += stats[param]
        self.total_themes[self.current_theme] += 1
        if stats['is_valid']:
            self.success_themes[self.current_theme] += 1
        for param in ['avg_length', 'grammar_errors', 'coherence', 'theme_focus', 'flesch', 'fkgl','keyword_score']:
            self.history_stats[param].append(stats[param])

        if not stats['is_valid']:
            print(f"\n文章未通过验证.")
            return stats

        tokens = word_tokenize(text)
        new_lemmas = set()
        
        # 使用依存句法分析增强覆盖检测
        doc = nltk.ne_chunk(nltk.pos_tag(tokens))
        for chunk in doc:
            if isinstance(chunk, nltk.Tree):
                words = [w[0].lower() for w in chunk.leaves()]
            else:
                words = [chunk[0].lower()]
            for word in words:
                if not word.isalpha():
                    continue
                # lemma = self.vocab_proc.lemmatize(word)  
                lemma = self.vocab_proc.enhanced_lemmatize(word)
                # print(f"[DEBUG]原始词: {word} → 词根: {lemma} (是否在目标词库: {lemma in self.target_lemmas})")
                if lemma in self.target_lemmas:
                    self.total_words += 1  # 确保总词数统计
                    if lemma not in self.used_lemmas:
                        new_lemmas.add(lemma)
                        new_lemmas = set(new_lemmas)
        # 更新词库状态
        if new_lemmas:
            self.used_lemmas.update(new_lemmas)
            self.used_lemmas = set(self.used_lemmas)
            self.unused_lemmas = self.unused_lemmas.difference(new_lemmas)
            self.unused_lemmas = set(self.unused_lemmas)
        if len(self.unused_lemmas) + len(self.used_lemmas) != len(self.target_lemmas):
            print(f"! 状态异常: 总词数={len(self.target_lemmas)} 已用={len(self.used_lemmas)} 未用={len(self.unused_lemmas)}")
            self.unused_lemmas = set(self.target_lemmas) - self.used_lemmas
        
        # 计算统计指标
        efficiency = (len(self.used_lemmas)/self.total_words)*100 if self.total_words else 0.0
        target_lemma_count = len(self.target_lemmas)
        coverage_percent = (len(self.used_lemmas) / target_lemma_count * 100) if target_lemma_count > 0 else 0.0
        stats["new_words"] = len(new_lemmas)
        stats["new_lemmas"] = new_lemmas
        stats["efficiency"] = efficiency
        stats["coverage"] = coverage_percent
        stats["memory_usage"] = self.mem_monitor.memory_info().rss // 1024**2
        return stats
    #---------------------------------------------------------------------------------------------
    # 判断是否达到停止条件
    #     参数:
    #         stats (Dict): 分析统计数据
    #     功能:
    #         1. 检查最近3次迭代的新增词汇量是否持续低于阈值
    #         2. 维护最近3次迭代结果的队列
    #     返回:
    #         bool: 如果连续3次新增词汇数低于阈值返回True，否则返回False
    #---------------------------------------------------------------------------------------------
    def should_stop(self, stats):
        if not hasattr(self, 'recent_new_words'):   # 初始化历史记录队列
            self.recent_new_words = []
        current_count = stats.get('new_words', 0)   # 获取当前统计数据
        coverage_percent = stats.get('coverage', 0.0)
        if coverage_percent >= 99.99: return True   # 1. 如果覆盖率 >= 99.99% 直接结束
        
        if len(self.recent_new_words) >= 6:         # 维护最近新增单词记录
            self.recent_new_words.pop(0)
        self.recent_new_words.append(current_count)
        reset_threshold = WORD_CLUSTER_LENGTH       # 根据覆盖率决定重置条件
        if coverage_percent <= 80.00:               # 2. 当覆盖率较低时（≤80%），降低重置阈值
            reset_threshold *= 0.5
        if current_count >= reset_threshold:         # 3. 当覆盖率较高时（>80%），保持正常重置阈值
            self.recent_new_words.clear()
            return False
        return (    # 检查连续三次不达标
            len(self.recent_new_words) >= 6 and 
            all(cnt < WORD_CLUSTER_LENGTH for cnt in self.recent_new_words)
        )

    #---------------------------------------------------------------------------------------------
    # 保存进度到文件
    #     参数:
    #         is_normal_stop (bool): 是否为正常停止，默认为False
    #     功能:
    #         1. 将当前状态保存到JSON文件
    #         2. 记录已学习词汇、词汇范围和时间戳
    #         3. 支持后续恢复进度
    #---------------------------------------------------------------------------------------------
    def save_progress(self, is_normal_stop=False):
        progress_data = {
            'timestamp': datetime.now().isoformat(),
            'rankmin': self.vocab_proc.rankmin,
            'rankmax': self.vocab_proc.rankmax,
            'unused_lemmas': list(self.unused_lemmas),
            'article_counter': self.article_counter,
            'generate_count': self.generate_count,
            'total_words': self.total_words,
            'normal_stop': is_normal_stop
        }
        with open(os.path.join(self.output_dir, "progress.json"), "w",encoding='utf-8') as f:
            json.dump(progress_data, f)

    #---------------------------------------------------------------------------------------------
    # 加载上一次进度
    #     功能:
    #         1. 从JSON文件恢复之前保存的状态
    #         2. 加载上一次时间戳
    #     返回:
    #         返回值，timestamp_str时间标签
    #---------------------------------------------------------------------------------------------
    def load_progress(self):
        timestamp_str = ""  # 初始化时间标签为空字符串
        article_counter = 1
        generate_count = 1
        total_words = 1
        try:
            with open(os.path.join(self.output_dir, "progress.json"), "r", encoding='utf-8') as f:
                data = json.load(f)
                saved_min, saved_max = data['rankmin'], data['rankmax']
                current_min, current_max = self.vocab_proc.rankmin, self.vocab_proc.rankmax
                if saved_min == current_min and saved_max == current_max:           # 1. 检查保存的min/max与当前min/max是否完全相等
                    saved_timestamp = datetime.fromisoformat(data['timestamp'])     # 2. 恢复时间标签并转换格式
                    timestamp_str = saved_timestamp.strftime('%Y%m%d')
                    article_counter =  data['article_counter']
                    generate_count = data['generate_count']
                    total_words = data['total_words']
                    print(f"[DEBUG]上一次时间标签:{timestamp_str},文章序号:{article_counter},总序号:{generate_count},总词数:{total_words}")
                    return timestamp_str,article_counter,generate_count,total_words   
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print("[ERROR]analyzearticle.py提示无有效progress.json文件")
        except KeyError as e:
            print(f"[ERROR]analyzearticle.py提示JSON字段缺失: {str(e)}")
        return timestamp_str,article_counter,generate_count,total_words  
    
    #---------------------------------------------------------------------------------------------
    # 从文章文本中提取词汇
    #     参数:
    #         text (str): 原始文章文本内容
    #     返回:
    #         List[Tuple[str, str]]: 包含(原始词, 词根)的元组列表
    #     功能说明:
    #         1. 使用NLTK进行句子分割和词汇标记化
    #         2. 过滤非字母词汇和短于min_length的词汇
    #---------------------------------------------------------------------------------------------
    def tokenize_from_article(self,text: str) -> List[str]:
        words = [w.lower() for w in word_tokenize(text) if w.isalpha()]
        return words
    #---------------------------------------------------------------------------------------------
    # 保存分析结果到文件
    #     参数:
    #         stats (Dict): 分析统计数据
    #     返回:
    #         str: 保存的文件路径
    #---------------------------------------------------------------------------------------------
    def save_analysis(self, text, stats):
        #---------------------------------------------------------------------------------------------
        # 保存分析结果到文件
        #     参数:
        #         stats (Dict): 分析统计数据
        #     返回:
        #         str: 保存的文件路径
        #---------------------------------------------------------------------------------------------
        def _calc_avg(param, success=False):
            source_sum = self.success_stats_sum if success else self.total_stats_sum
            count = self.article_counter if success else self.generate_count
            if count == 0:
                return 0.0
            return source_sum[param] / count
        def format_rank(r):
            return f"{r//1000}k" if r >= 1000 else str(r)
        if not self.timestamp_str:
            self.timestamp_str = datetime.now().strftime('%Y%m%d')
        rank_suffix = f"{format_rank(self.vocab_proc.rankmin)}-{format_rank(self.vocab_proc.rankmax)}"
        if stats['is_valid']:
            filename = f"analysis_{rank_suffix}_{self.timestamp_str}.txt"
        else:
            filename = f"failanalysis_{rank_suffix}_{self.timestamp_str}.txt"
        text_len = len(self.tokenize_from_article(text))
        filepath = os.path.join(self.output_dir, filename)
        success_rate = (self.article_counter/self.generate_count)*100 if self.generate_count > 0 else 0.0
        content = [
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "【当前文章质量】",
            f"- 平均句长: {stats['avg_length']:.1f}(标准7-15)",
            f"- 语法错误数: {stats['grammar_errors']}",
            f"- 上下文一致性: {stats['coherence']:.1f}%",
            f"- 主题集中度: {stats['theme_focus']:.1f}%",
            f"- Flesch可读性指数: {stats['flesch']}%",
            f"- Flesch-Kincaid等级: {stats['fkgl']:.1f}",
            f"- 关键词匹配度: {stats['keyword_score']:.1f}%"
        ]
        if stats['is_valid']:
            content += [
                "【生成统计】",
                f"- 生成成功率: {self.article_counter}/{self.generate_count}={success_rate:.1f}%",
                f"- 新增词汇: {stats['new_words']}",
                f"- 生成效率: '{stats['new_words']}/{text_len}={100*stats['new_words']/text_len:.2f}%'"
                f" | {len(self.used_lemmas)}/{self.total_words}={stats['efficiency']:.2f}%"
                f" | 内存占用: {stats['memory_usage']}MB",
                f"- 覆盖率: {len(self.used_lemmas)}/{len(self.target_lemmas)}={stats['coverage']:.2f}%",
                f"【Article #{self.article_counter}生成提示词】",
                f"{self.current_prompt}"
            ]
            content += [
                "【质量参数统计】",
                "成功文章平均值:",
                f"- 平均句长: {_calc_avg('avg_length', success=True):.1f}",
                f"- 语法错误: {_calc_avg('grammar_errors', success=True):.1f}",
                f"- 上下文一致性: {_calc_avg('coherence', success=True):.1f}%",
                f"- 主题集中度: {_calc_avg('theme_focus', success=True):.1f}%",
                f"- 关键词匹配: {_calc_avg('keyword_score', success=True):.1f}%",
                f"- 可读性: {_calc_avg('flesch', success=True):.1f}%",
                f"- Flesch-Kincaid等级: {_calc_avg('fkgl', success=True):.1f}"
            ]
        content += [
            "全部文章平均值:",
            f"- 平均句长: {_calc_avg('avg_length'):.1f}",
            f"- 语法错误: {_calc_avg('grammar_errors'):.1f}", 
            f"- 上下文一致性: {_calc_avg('coherence'):.1f}%",
            f"- 主题集中度: {_calc_avg('theme_focus'):.1f}%",
            f"- 关键词匹配: {_calc_avg('keyword_score'):.1f}%",
            f"- 可读性: {_calc_avg('flesch'):.1f}%",
            f"- Flesch-Kincaid等级: {_calc_avg('fkgl'):.1f}"
        ]
        theme_report = [
            "【主题类型统计】",
            "成功文章主题分布:",
            *[f"- {k}: {v}次" for k,v in self.success_themes.items() if v > 0],
            "全部文章主题分布:", 
            *[f"- {k}: {v}次" for k,v in self.total_themes.items() if v > 0],
            "【主题类型统计】",
            f"成功主题覆盖率: {len(self.success_themes)}/{len(self.total_themes)}种",
            "高频成功主题(top5):",
            *[f"- {k}: {v}次" for k,v in sorted(self.success_themes.items(), 
                                      key=lambda x:-x[1])[:5]]
        ]
        content += theme_report
        fluctuation_report = ["【参数离散度分析】"]
        for param in ['avg_length', 'grammar_errors', 'coherence',
                    'theme_focus', 'flesch', 'fkgl','keyword_score']:
            values = self.history_stats[param]
            if len(values) > 1:
                std_dev = np.std(values)
                mean_val = np.mean(values)
                fluctuation_report.append(
                    f"- {param}: 均值={mean_val:.2f} 标准差={std_dev:.2f} " 
                    f"(范围[{min(values):.2f}-{max(values):.2f}])"
                )
            else:fluctuation_report.append(f"- {param}: 数据不足(需至少2次生成)")
        fluctuation_report += ["\n\n"]
        content += fluctuation_report
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write('\n'.join(content))
        return filepath

    #---------------------------------------------------------------------------------------------
    # 保存生成文章到文件
    #     参数:
    #         text (str): 文章内容
    #         stats (Dict): 分析统计数据
    #     返回:
    #         str: 保存的文件路径
    #---------------------------------------------------------------------------------------------
    def save_article(self, text, stats):
        def format_rank(r):
            return f"{r//1000}k" if r >= 1000 else str(r)
        if not self.timestamp_str:
            self.timestamp_str = datetime.now().strftime('%Y%m%d')
        rank_suffix = f"{format_rank(self.vocab_proc.rankmin)}-{format_rank(self.vocab_proc.rankmax)}"
        filename = f"articles_{rank_suffix}_{self.timestamp_str}.txt"
        filepath = os.path.join(self.output_dir, filename)
        header = f"\n{'='*26}Article #{self.article_counter}#{self.current_theme}#{'='*25}"
        if self.current_keywords:
            keyword_part = f"#current_keywords:{self.current_keywords}#"
        content = [header,keyword_part,"</think>" + text + "\n[EOS]\n"]
        # 首次写入时创建文件并添加标题
        mode = 'a' if os.path.exists(filepath) else 'w'
        with open(filepath, mode, encoding='utf-8') as f:
            if mode == 'w':
                f.write(f"{'='*30} 英语学习文章合集 {'='*25}\n\n")
            f.write('\n'.join(content))
        self.article_counter += 1
        return filepath

    #---------------------------------------------------------------------------------------------
    # 更新生成上下文信息
    #     参数:
    #         new_prompt (str): 新提示词
    #         new_theme (str): 新主题
    #---------------------------------------------------------------------------------------------
    def update_context(self, new_prompt="", new_theme="",new_keywords=set()):
        """更新生成上下文信息"""
        self.current_prompt = new_prompt
        self.current_theme = new_theme
        self.current_keywords = new_keywords

#---------------------------------------------------------------------------------------------
# 仅用于测试的代码段 
#   测试： 执行   python -m src.analyzearticle 
#       或 python -m unittest src.analyzearticle.TestAnalyzer.test_analyze
#---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import unittest
    from .textprocessor import NarrativeProcessor
    from .vocab_processor import VocabProcessor
    from .utils import common_utils,LanguageToolSingleton
    from .model_handler import ModelHandler
    from .narrative_features import THEME_CONFIGS

    class TestAnalyzer(unittest.TestCase):
        def setUp(self):
            # 模拟初始化参数
            # self.quickly = True
            self.quickly = False
            self.rank_ranges = (1000, 2000)

            self.rankmin, self.rankmax = self.rank_ranges
            if self.rankmax in [1000,2000,3000,4000,5000]:
                SELECTED_THEME = f"CHILDHOOD_FUN_THEME{self.rankmax//1000}K"
                print(f"选择的主题集SELECTED_THEME={SELECTED_THEME}")
            narrative_examples = THEME_CONFIGS.get(SELECTED_THEME, {}).get("narrative_examples", {})
            self.current_theme = next(iter(narrative_examples.keys())) if narrative_examples else "default_theme"
            print(f"第1个主题{self.current_theme}")
            
            if not self.quickly:  
                self.model_handler = ModelHandler()  
                self.semantic_model = self.model_handler._load_model()
                self.grammar_tool = LanguageToolSingleton('en-US')
                self.processor = NarrativeProcessor(
                    grammar_tool = self.grammar_tool,
                    current_theme = self.current_theme,
                    rank_ranges = self.rank_ranges,
                    semantic_model = self.semantic_model
                )
            else :self.semantic_model = None

            self.vocab_proc = VocabProcessor(
                rank_ranges=self.rank_ranges,
                tokenizer = None,
                semantic_model = self.semantic_model
            )
            
            self.analyze = article_analyzer(
                vocab_proc = self.vocab_proc,
                semantic_model = self.semantic_model
                )
            self.output_dir = common_utils.get_output_dir()      # 获取输入和输出目录
            # self.input_file = os.path.join(self.output_dir, "COCA1000.txt")
            # self.input_file = os.path.join(self.output_dir, "original_text1-1k.txt")
            self.input_file = os.path.join(self.output_dir, "original_text1k-2k.txt")
        def test_analyze(self):
            print("开始测试 test_analyze()函数...")
            with open(self.input_file, "r", encoding="utf-8") as f:
                input_text = f.read()
            for idx,(theme,keywords,content) in enumerate(common_utils.split_articles(input_text),start=1):
                if not self.quickly:
                    self.processor.update_current_theme(theme)
                    content, process_time = common_utils._measure_time(self.processor.process,content)
                    print(f"[DEBUG]self.processor.process耗时: {process_time:.4f}ms")
                
                if len(content.split()) < ARTICLE_LENGTH*0.3:continue
                else:
                    self.analyze.update_context("",theme,keywords)
                    # self.analyze.update_context("","","")
                    stats,analyze_time = common_utils._measure_time(self.analyze.analyze,content)
                    # stats = self.analyze.analyze(article)
                    self.analyze.save_analysis(content,stats)
                    self.analyze.save_article(content,stats)
                    print(f"[DEBUG]self.analyze耗时: {analyze_time:.4f}ms")
                    # print(f"内存占用: {stats['memory_usage']}MB\n\n") 
            print("\n测试结束")  
            
    unittest.main()

