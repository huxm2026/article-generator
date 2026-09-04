#---------------------------------------------------------------------------------------------
# 英语学习文章生成工具
# 用法: python ArticalGen.py rankmin rankmax
# 示例: python ArticalGen.py 100 200
# 生成文章使用的词汇范围: rankmin到rankmax的词库词 + 小于rankmin的词
# 统计指标: 生成效率 = 已用词库词数 / 总生成词数 * 100%
#---------------------------------------------------------------------------------------------

from src.config import *
from src.generator import ArticleGenerator
from src.analyzearticle import article_analyzer
from src.utils import test_model,common_utils

import argparse

#---------------------------------------------------------------------------------------------
# 运行生成模式
#---------------------------------------------------------------------------------------------
def run_generation_mode(args):
    generator = ArticleGenerator((args.rankmin, args.rankmax))
    # test=test_model(generator)
    # if not test.verify_model():
    #     sys.exit(1)
    analyzer = article_analyzer(generator.vocab_proc,generator.semantic_model)
    while True:
        generator.update_context(analyzer.unused_lemmas)
        article = generator.generate()
        analyzer.update_context(generator.current_prompt,generator.current_theme,generator.current_keywords)
        stats = analyzer.analyze(article)
        analysis_path = analyzer.save_analysis(article,stats)
        if not stats['is_valid']:
            continue
        generator.vocab_proc.update_context(analyzer.unused_lemmas)
        saved_path = analyzer.save_article(article, stats)
        print(f"\n生成文章保存至: {saved_path}")        # 控制台显示摘要
        print(f"\n分析结果保存至: {analysis_path}")
        print(
            f"\n学习统计: 新增词 {stats['new_words']} | 覆盖率" 
            f"{len(analyzer.used_lemmas)}/{len(generator.vocab_proc.target_lemmas)}={stats['coverage']:.2f}%"
        )
        print(
            f"- 生成效率: {stats['new_words']}/{len(analyzer.tokenize_from_article(article))}="
            f"{stats['new_words']/len(analyzer.tokenize_from_article(article))*100:.2f}%"
            f" | {len(analyzer.used_lemmas)}/{analyzer.total_words}={stats['efficiency']:.2f}%"
            f" | 内存占用: {stats['memory_usage']}MB"
        )
        print(f"\n{'='*60}")
        if analyzer.should_stop(stats):  # 终止条件防止死循环
            analyzer.save_progress(is_normal_stop=True)  # 标记正常停止
            print("\n达到停止条件,生成结束")
            common_utils.safe_shutdown(SHUT_DOWN_TIME)
            break

#---------------------------------------------------------------------------------------------
# 运行聊天模式
#---------------------------------------------------------------------------------------------
def run_chat_mode(args):
    from src.chat_processor import ChatProcessor
    print("="*60)
    print("【英语学习助手】输入任意内容开始对话（exit退出）")
    print("="*60)
    generator = ArticleGenerator((args.rankmin, args.rankmax))  
    chat_processor = ChatProcessor(generator)
    session_history = []
    while True:
        user_input = input("\nYou > ").strip()
        if not user_input:
            continue
        if user_input.lower() in ['exit', 'quit']:
            break
        response = chat_processor.generate_response(user_input)
        print(f"\nAI > {response}")
        session_history.append((user_input, response))

#---------------------------------------------------------------------------------------------
# 主函数，负责解析命令行参数并启动文章生成流程
#     参数:
#         rankmin (int): 最小词频排名
#         rankmax (int): 最大词频排名
#     返回:
#         无
#---------------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="英语学习文章生成器")
    parser.add_argument("rankmin", type=int, help="最小词频排名")
    parser.add_argument("rankmax", type=int, help="最大词频排名")
    parser.add_argument("--chat", action="store_true",
                      help="启用交互式聊天模式")
    args = parser.parse_args()

    if args.chat:  # 聊天模式分支
        run_chat_mode(args)
    else:          
        run_generation_mode(args)

#---------------------------------------------------------------------------------------------
#   main()
#---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
