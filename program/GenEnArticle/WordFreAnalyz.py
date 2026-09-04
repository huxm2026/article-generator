#---------------------------------------------------------------------------------------------
#
#英语文本词频分析工具
#用法:
#  python analyzer.py  文章路径 
#示例:
#  python analyzer.py  test.txt         
#---------------------------------------------------------------------------------------------
from src.config import *
from src.utils import LanguageToolSingleton,common_utils
from src.vocab_processor import VocabProcessor,WordStemmer
from src.analyzearticle import article_analyzer
from src.model_handler import ModelHandler

from nltk import SnowballStemmer
import enchant
import logging
import enum
import PyPDF2
import spacy 

#---------------------------------------------------------------------------------------------
# 按文章进行语言分析
#     参数:
#         articlesfile: 原始文章内容
#         grammar_tool: 语法检查工具实例
#     返回:
#         包含分析结果的字典
#---------------------------------------------------------------------------------------------
def analyze_articles(articlesfile: str, grammar_tool:LanguageToolSingleton,analyze:article_analyzer) -> dict:
    # 初始化分析结果存储
    analysis_results = {
        'articles': [],
        'total_words': 0,
        'total_errors': 0,
        'aggregate_stats': {
            'avg_sentence_length': {'mean': 0, 'std': 0, 'min': 0, 'max': 0},
            'grammar_errors': {'mean': 0, 'std': 0, 'min': 0, 'max': 0},
            'coherence': {'mean': 0, 'std': 0, 'min': 0, 'max': 0},
            'focus_score': {'mean': 0, 'std': 0, 'min': 0, 'max': 0},
            'flesch': {'mean': 0, 'std': 0, 'min': 0, 'max': 0},
            'fkgl': {'mean': 0, 'std': 0, 'min': 0, 'max': 0}
        }
    }

    # 初始化统计指标存储
    metric_accumulator = {
        'sentence_lengths': [],
        'grammar_errors': [],
        'coherence_scores': [],
        'focus_scores': [],
        'flesch_scores': [],
        'fkgl':[]
    }

    # 按文章进行分析
    for idx, (theme,keywords,content) in enumerate(common_utils.split_articles(articlesfile), start=1):
        print(f"\n{'='*40}")
        print(f" 分析文章 {idx}: 主题 {theme}")
        print(f"{'='*40}")
        
        if len(content.split()) < 50:  # 忽略空文章
            print("文章内容过短，跳过分析")
            continue

        # 执行语言检查
        sentences = nltk.sent_tokenize(content)
        avg_length = np.mean([len(s.split()) for s in sentences])
        grammar_errors = grammar_tool.check(content)

        context_coherence, theme_focus, keyword_score = analyze.calculate_text_metrics(
            text = content,  
            current_theme = theme, 
            current_keywords = keywords
            # current_theme = "", 
            # current_keywords = ""
        )

        flesch = textstat.flesch_reading_ease(content)
        fkgl_score = textstat.flesch_kincaid_grade(content)
       
        # 记录分析结果
        article_data = {
            # 'title': article['title'],
            'theme': theme,
            'word_count': len(analyze.tokenize_from_article(content)),
            'sentences': len(sentences),
            'avg_sentence_length': avg_length,
            'grammar_errors': len(grammar_errors),
            'coherence': context_coherence,
            'focus_score': theme_focus,
            'fkgl': fkgl_score,
            'flesch': flesch
        }
        analysis_results['articles'].append(article_data)

        # 记录指标到累加器
        metric_accumulator['sentence_lengths'].append(avg_length)
        metric_accumulator['grammar_errors'].append(len(grammar_errors))
        metric_accumulator['coherence_scores'].append(context_coherence)
        metric_accumulator['focus_scores'].append(theme_focus)
        metric_accumulator['flesch_scores'].append(flesch)
        metric_accumulator['fkgl'].append(fkgl_score)

        def calculate_stats(data: list) -> dict:
            if not data:
                return {'mean': 0, 'std': 0, 'min': 0, 'max': 0}
            arr = np.array(data)
            return {
                'mean': round(np.mean(arr), 2),
                'std': round(np.std(arr), 2) if len(arr) > 1 else 0,
                'min': round(np.min(arr), 2),
                'max': round(np.max(arr), 2)
            }

        # 在所有文章处理完成后更新统计
        if metric_accumulator['sentence_lengths']:  # 仅当有有效数据时更新
            analysis_results['aggregate_stats'] = {
                'avg_sentence_length': calculate_stats(metric_accumulator['sentence_lengths']),
                'grammar_errors': calculate_stats(metric_accumulator['grammar_errors']),
                'coherence': calculate_stats(metric_accumulator['coherence_scores']),
                'focus_score': calculate_stats(metric_accumulator['focus_scores']),
                'flesch': calculate_stats(metric_accumulator['flesch_scores']),
                'fkgl': calculate_stats(metric_accumulator['fkgl'])
            }

        # 打印当前文章结果
        print(f"词数统计：{article_data['word_count']} 词")
        print(f"句子数量：{len(sentences)} 句")
        print(f"平均句长：{avg_length:.1f} 词/句（推荐7-15词）")
        print(f"语法错误：{len(grammar_errors)} 处")
        print(f"上下文一致性: {context_coherence:.1f}%")
        print(f"主题集中度: {theme_focus:.1f}%")
        print(f"Flesch可读性指数: {flesch}%")
        print(f"Fkgl等级: {fkgl_score:.1f}")

    print("\n全局统计指标：")
    for metric, stats in analysis_results['aggregate_stats'].items():
        print(f"{metric}:")
        print(f"  均值: {stats['mean']} ± {stats['std']}")
        print(f"  范围: [{stats['min']} ~ {stats['max']}]")
    print("\n")
    return analysis_results

#---------------------------------------------------------------------------------------------
#    基础文本预处理,同时支持nltk和spacy工具
#    参数:
#        file_path (str): 输入文件路径，支持txt和pdf格式文件
#        nlp: (spacy): 使用的工具，spacy工具
#    返回:
#        Tuple[List[str], str]: 预处理后的单词列表和原始文本内容
#---------------------------------------------------------------------------------------------
def preprocess_text(file_path: str, nlp: spacy) -> Tuple[List[str], str]:
    if file_path.endswith('.pdf'):
        # 使用PyPDF2读取PDF文件内容
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
    else:
        # 读取文本文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

    nltkwords = [w.lower() for w in word_tokenize(text) if w.isalpha()]
    doc = nlp(text)
    spacylemma = [token.lemma_.lower() for token in doc if token.is_alpha ]

    return nltkwords,spacylemma,text

#---------------------------------------------------------------------------------------------
#    处理英美拼写差异，转换为美式拼写
#    参数: word (str): 输入单词
#    返回: str: 转换后的单词
#---------------------------------------------------------------------------------------------
def normalize_spelling(word: str) -> str:
    """处理英美拼写差异，转换为美式拼写"""
    d_us = enchant.Dict("en_US")
    d_uk = enchant.Dict("en_GB")
    if d_uk.check(word) and not d_us.check(word):
        # 如果是英式拼写，尝试转换为美式
        suggestions = d_us.suggest(word)
        if suggestions:
            return suggestions[0]
    return word

#---------------------------------------------------------------------------------------------
#    增强的词形还原逻辑
#    参数: word_rank (Dict[str, int]): 词频字典
#    参数: word (str): 输入单词
#    返回: str: 还原后的词干
#---------------------------------------------------------------------------------------------
def advanced_lemmatize(word_rank: Dict[str, int], word: str) -> str:
    # 特殊处理规则
    if word.lower() == 'an':  # 处理限定词
        return 'a'
    if word.lower() == 'others':  
        return 'other'
    if word.lower() == 'men':  # 处理不规则复数
        return 'man'
    
    # 初始化工具处理前缀后缀
    coca_set = set(word_rank.keys())  # 提取词频字典的键形成集合
    stemmer = WordStemmer(coca_set, max_loops=3)
    stemmed_word = stemmer.stem(word)
    if stemmed_word is not None:
        return stemmed_word
    return word

stage_map = {
    'stage1': '标记词性还原','stage2': '提取词干还原', 'stage3': '前缀后缀还原',
    #'stage4': '拼写差异还原'
}
#---------------------------------------------------------------------------------------------
#    四阶段匹配流程
#    参数: nltkwords (List[str]):  nltk分词的输入单词列表
#    参数: spacylemma (List[str]): spacy分词的输入单词原形列表
#    参数: word_rank (Dict[str, int]): 词频字典
#    参数: snowball_stemmer (SnowballStemmer): 词干提取工具
#    参数: vocab_proc.lemmatize:    nltk词形还原工具
#    参数: nlp:                     spacy词形还原工具
#    返回: Tuple[Dict, List[str]]: 匹配结果和剩余单词列表
#---------------------------------------------------------------------------------------------
def multi_stage_matching(nltkwords: List[str],spacylemma: List[str],word_rank: Dict[str, int], \
        snowball_stemmer: SnowballStemmer,vocab_proc:VocabProcessor) -> Tuple[Dict, List[str]]:
    stage_results = {
        'stage1': {'count':0, 'ranks':set()},
        'stage2': {'count':0, 'ranks':set()},
        'stage3': {'count':0, 'ranks':set()},
        'stage4': {'count':0, 'ranks':set()},
    }
    # remaining = nltkwords.copy()
    remaining = spacylemma.copy()
    seen_lemmas = set()
    for stage in ['stage1', 'stage2', 'stage3']:
        new_remaining = []
        if stage == 'stage1':            # 标记词性还原
            for word in remaining:
                # lemma = vocab_proc.lemmatize(word) 
                lemma = word
                if lemma in word_rank:
                    if lemma not in seen_lemmas:    # 仅当lemma未被当前阶段处理过时计数
                        stage_results[stage]['count'] += 1
                        stage_results[stage]['ranks'].add(word_rank[lemma])
                        seen_lemmas.add(lemma)
                else:
                    new_remaining.append(lemma)
        else:
            for word in remaining:
                if stage == 'stage4':       # 拼写标准化
                    lemma = word
                    # lemma = normalize_spelling(word)
                elif stage == 'stage3':     # 前缀后缀还原
                    lemma = advanced_lemmatize(word_rank, word)
                elif stage == 'stage2':     # 提取词干还原
                    lemma = snowball_stemmer.stem(word)
                if lemma in word_rank:
                    if lemma not in seen_lemmas:    # 仅当lemma未被当前阶段处理过时计数
                        stage_results[stage]['count'] += 1
                        stage_results[stage]['ranks'].add(word_rank[lemma])
                        seen_lemmas.add(lemma)
                else:
                    new_remaining.append(word)
        remaining = list(set(new_remaining))    # 去重
        remaining = [re.sub(r'[^a-zA-Z]','',text).lower() for text in remaining] 
        # 输出阶段匹配信息
        print(f"{stage_map.get(stage, stage)} 匹配 {stage_results[stage]['count']} 词，剩余 {len(remaining)} 词")  # 修改这里，计算剩余词数

    
    total_count = sum(stage_results[f'stage{i}']['count'] for i in range(1,4))  # 计算总匹配
    print(f"总匹配: {total_count} 词，剩余 {len(remaining)} 词")     # 输出总匹配信息，计算剩余词数
    return stage_results, remaining  # 返回时将字符串转换回列表

#---------------------------------------------------------------------------------------------
#    生成各阶段的分布统计
#    参数: stage_data (Dict): 各阶段匹配结果
#    返回: Dict[str, Dict]: 各阶段分布统计和总分布统计
#---------------------------------------------------------------------------------------------
def calculate_stage_distribution(stage_data: Dict) -> Dict[str, Dict]:
    distribution = {} 
    total_distribution = {'1-1000': 0, '1001-1500': 0, '1501-2000': 0,'2001-2500': 0,'2501-3000': 0,\
                           '3001-3500': 0, '3501-4000': 0,'4001-4500': 0,'4501-5000': 0}
    for stage in stage_data.keys():  # 修改这里，使用 stage_data.keys() 获取实际存在的键
        dist = {}
        bins = [(1, 1000), (1001, 1500),(1501, 2000), (2001, 2500),(2501, 3000), \
                (3001, 3500),(3501, 4000), (4001, 4500),(4501, 5000)]
        for low, high in bins:
            key = f"{low}-{high}" if high != float('inf') else f"{low}+"
            count = sum(low <= r <= high for r in stage_data[stage]['ranks'])
            dist[key] = count
            total_distribution[key] += count
        distribution[stage] = dist
    return distribution, total_distribution

#---------------------------------------------------------------------------------------------
#    计算程序运行耗时
#---------------------------------------------------------------------------------------------
def calculate_runtime(start_timeORend_time: enum):
    if start_timeORend_time == 'start_time':
        if not hasattr(calculate_runtime,'start_time'):
            calculate_runtime.start_time = time.time()        # 记录开始时间
    else:
        end_time:float = time.time()          # 记录结束时间
        running_time:float = end_time - calculate_runtime.start_time
        print(f"\n程序运行耗时: {running_time:.2f} 秒")

#---------------------------------------------------------------------------------------------
#     处理未匹配词汇的词性标注和词形还原
#     参数: unmatched (List[str]): 未匹配的词汇列表
#     参数: word_rank (Dict[str, int]): 词频字典
#     返回: List[str]: 还原后的词干列表
#---------------------------------------------------------------------------------------------
def process_unmatched_words(unmatched: List[str],word_rank: Dict[str, int]) -> List[str]:
    # 将列表转换为字符串
    unmatch_lemma = []
    for word in unmatched:
        unmatch_lemma.append(advanced_lemmatize(word_rank, word))
    return unmatch_lemma

#---------------------------------------------------------------------------------------------
# # 打印未匹配词汇和未匹配原型
#---------------------------------------------------------------------------------------------
def print_words(words1, words2, label1, label2):
    if label2 == " " and words2 == " ":
        print(f"\n{label1}")
    else:
        print(f"\n{label1} \nvs \n{label2}")
    max_length = max(len(words1), len(words2))
    max_word_length1 = max(len(word) for word in words1) if words1 else 0
    max_word_length2 = max(len(word) for word in words2) if words2 else 0
    for i in range(0, max_length, 10):
        line1 = " ".join(word.ljust(max_word_length1 + 2) for word in words1[i:i+10]).ljust(100)  # 每行10个词，左对齐，总宽度100字符
        if label2 != " ":
            line2 = " ".join(word.ljust(max_word_length2 + 2) for word in words2[i:i+10]).ljust(100)  # 每行10个词，左对齐，总宽度100字符
            print(f"\n{line1} \n{line2}")
        else:
            print(f"{line1}")
    print(f"\n剩余{len(words1)}未能匹配")

#---------------------------------------------------------------------------------------------
#    主函数
#    参数: article_path (str): 文章路径
#    参数: wordlist_path (str): 词表文件路径
#---------------------------------------------------------------------------------------------
def main(article_path: str, wordlist_path: str):
    calculate_runtime('start_time')
    nlp = spacy.load("en_core_web_md")  # 加载SpaCy模型 "en_core_web_sm" "en_core_web_lg"
    snowball_stemmer = SnowballStemmer('english')  # 初始化 SnowballStemmer
    grammar_tool = LanguageToolSingleton('en-US')
    vocab_proc = VocabProcessor(
            rank_ranges=(1,5000),
            tokenizer=None,
            semantic_model = None
            )
    analyzer = article_analyzer(
        vocab_proc=vocab_proc,
        semantic_model = None
        # semantic_model = semantic_model
        )
    word_rank = {str(word).lower(): int(rank) for rank, word in vocab_proc.full_vocab.items()}
    nltkwords,spacylemma,text = preprocess_text(article_path,nlp)   # 预处理文本
    analysis_results = analyze_articles(text, grammar_tool,analyzer)    # 分析文章的连贯性和语法错误
    total_words = (len(nltkwords)+len(spacylemma)) / 2.0
    print(f"文本预处理完成，总词数: {total_words}")
    # 多阶段匹配
    stage_results, unmatched = multi_stage_matching(nltkwords,spacylemma,word_rank, snowball_stemmer,vocab_proc)  # 传递 snowball_stemmer
    stage_dist, total_dist = calculate_stage_distribution(stage_results)
    total_matched = sum(s['count'] for s in stage_results.values()) # 输出结果
    total_words = total_matched + len(unmatched)
    print(f"修正后的总词数: {total_words}")
    print("\n分阶段匹配统计:")
    for stage in ['stage1', 'stage2', 'stage3']:
        data = stage_results[stage]
        print(f"\n{stage_map[stage]}匹配：")
        print(f"- 匹配词数: {data['count']} ({data['count']/total_words*100:.2f}%)")
        print("- 分布情况:")
        for band, count in stage_dist[stage].items():
            print(f"  Rank {band}: {count} 词 ({count/total_words*100:.2f}%)" if data['count'] else "  无匹配")
    print("\n总的分布情况:")
    for band, count in total_dist.items():
        print(f"  Rank {band}: {count} 词 ({count/total_words*100:.2f}%)")
    print(f"\n总匹配率: {total_matched/total_words*100:.2f}%")

    # # 调用 process_unmatched_words 函数来处理未匹配词汇
    # unmatch_lemma = process_unmatched_words(unmatched,word_rank)
    # # 调用 print_words 函数来打印未匹配词汇和未匹配原型
    # print_words(unmatched,unmatch_lemma, "未匹配词汇", "未匹配原型")
    # print_words(unmatched," ", "未匹配词汇", " ")
    
    calculate_runtime('end_time')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Word Frequency Analyzer')
    parser.add_argument('article', type=str, help='Path to article text file')  # 修改为位置参数
    args = parser.parse_args()
    
    main(args.article, WLF_SEL)
