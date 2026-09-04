from .config import *

import pandas as pd
import csv
from PyPDF2 import PdfReader
import pdfplumber
import chardet

#---------------------------------------------------------------------------------------------
# 词库加载器类
#     功能:
#         支持多种文件格式的词库加载与解析
#     支持格式:
#         .xlsx, .csv, .pdf, .txt
#---------------------------------------------------------------------------------------------
class Load_Vocab:
    #---------------------------------------------------------------------------------------------
    # 加载词频文件
    # 根据文件扩展名加载并解析文件，支持xlsx, csv, pdf和txt格式。
    
    # 参数:
    # filename: str - 文件名，包括路径和扩展名。
    # rankmin: int - 排名的最小值，用于筛选数据。
    # rankmax: int - 排名的最大值，用于筛选数据。
    
    # 返回:
    # tuple - 包含三个元素的元组：
    #     data: dict - 文件中所有数据的字典表示，键为排名，值为词元。
    #     target: set - 符合排名范围且只包含字母的词元集合。
    #     allowed: set - 排名在rankmax范围内且只包含字母的词元集合。
    #---------------------------------------------------------------------------------------------
    def load_file(self,wordlistpath,rankmin,rankmax):
        try:
            if wordlistpath == "wordlist_file0":
                filename = wordlist_file0
            elif wordlistpath == "wordlist_file1":
                filename = wordlist_file1
            elif wordlistpath == "wordlist_file2":
                filename = wordlist_file2
            else:
                raise ValueError("Invalid WORDLIST_SOURCE provided.")
            
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension == '.xlsx':
                df = pd.read_excel(filename, names=['rank', 'lemma'], header=0)
                data = df.set_index('rank')['lemma'].to_dict()
            elif file_extension == '.csv':
                with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    data = {int(row[0]): row[1] for row in reader if len(row) >= 2}
            elif file_extension == '.pdf':
                if wordlistpath == "wordlist_file1":
                    data = self.extract_pdf_vocab(filename)
                elif wordlistpath == "wordlist_file2":
                    data = self.read_pdf_vocab(filename)
            elif file_extension == '.txt':
                with open(filename, 'rb') as f:
                    raw_data = f.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding'] if result['encoding'] else 'utf-8'
                    f.seek(0)
                    lines = f.readlines()
                    decoded_lines = [line.decode(encoding, errors='replace').strip() for line in lines]
                data = [line.split() for line in decoded_lines if line.strip()]
            else:
                raise ValueError(f"不支持的文件格式: {file_extension}")

            # data = {rank: str(word) for rank, word in data.items()}
            data = {rank: str(word).strip().lower() for rank, word in data.items()}
            target = set(word for rank, word in data.items() \
                         if rankmin <= rank <= rankmax and word.isalpha())
            allowed = set(word for rank, word in data.items() 
                      if rank <= rankmax and word.isalpha())
            return data, target,allowed
        except Exception as e:
            print(f"加载词频文件时出错: {e}")
            return {}, set(),set()
        
    #---------------------------------------------------------------------------------------------
    # 提取PDF数据并生成与Excel处理结果一致的字典
    # 返回格式：{1: "fitness", 2: "passionate", ...}
    #---------------------------------------------------------------------------------------------
    def extract_pdf_vocab(self,pdf_path) -> dict:
        raw_data = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # 双重解析策略：同时尝试表格提取和文本解析
                try:
                    table = page.extract_table()    # 方法1：表格提取（适用于标准表格结构）
                    if table:
                        for row in table[1:]:  # 跳过表头
                            if len(row) >=5:        # 提取左右两列数据
                                raw_data.append((row[0].strip(), row[1].strip()))
                                raw_data.append((row[3].strip(), row[4].strip()))
                except:
                    text = page.extract_text()      # 方法2：正则解析（适用于非标准表格）
                    matches = re.findall(
                        r'\|\s*(\d+)\s*\|\s*([^\|]+?)\s*\|', 
                        text.replace('\n', ' ')
                    )
                    raw_data.extend(matches)
        data_dict = {}      # 数据标准化处理
        for num, word in raw_data:
            try:
                key = int(num)
                if key in data_dict:  # 处理重复键
                    data_dict[key] = f"{data_dict[key]}/{word}"
                else:
                    data_dict[key] = word.strip()
            except ValueError:
                continue  # 跳过无效编号
        # 生成与Excel完全一致的排序字典
        return dict(sorted(data_dict.items()))

    #  ---------------------------------------------------------------------------------------------
    # 从PDF文件中读取词汇，并根据其重要性等级（五星、四星、三星）进行分类。
    #    参数:
    #         filename (str): PDF文件的路径。
    #    返回:
    #         dict: 包含所有词汇的字典，每个词汇都有一个唯一的排名作为键。
    # ---------------------------------------------------------------------------------------------
    def read_pdf_vocab(self,filename):
        sections = {'五星词汇': [],'四星词汇': [],'三星词汇': []}
        current_section = None
        entry_pattern = re.compile(r'(\d+)\.\s*([a-zA-Z]+)')  
        section_pattern = re.compile(r'^\s*(五星词汇|四星词汇|三星词汇)\s*[:：]?') 
        with pdfplumber.open(filename) as pdf:
            for page in pdf.pages:
                text = page.extract_text(x_tolerance=50, layout=True)  
                if not text:continue
                left_entries = []  # 存储左列词条
                right_entries = []  # 存储右列词条
                lines = text.split('\n')
                for line in lines:
                    if(section_pattern.search(line.strip())):
                        current_section = section_pattern.search(line).group(1)
                        continue
                    if current_section and entry_pattern.findall(line):  
                        for i, (num, word) in enumerate(entry_pattern.findall(line)):   # 按词条位置分列存储
                            if i % 2 == 0:  # 左列词条
                                left_entries.append((int(num), word.strip()))
                            else:           # 右列词条
                                right_entries.append((int(num), word.strip()))
                for num, word in sorted(left_entries, key=lambda x: x[0]):
                    if word.isalpha():sections[current_section].append(word)
                for num, word in sorted(right_entries, key=lambda x: x[0]):
                    if word.isalpha():sections[current_section].append(word)
        all_lemmas = []     # 合并所有section的词汇
        all_lemmas.extend(sections['五星词汇'])
        all_lemmas.extend(sections['四星词汇'])
        all_lemmas.extend(sections['三星词汇'])
        # 生成全局rank字典，rank从1开始
        data = {rank+1: lemma for rank, lemma in enumerate(all_lemmas)}
        return data

#  ---------------------------------------------------------------------------------------------
#   测试： 执行   python -m src.load_vocab 
#               或 python -m unittest test_load_vocab.TestLoadVocab.test_extract_pdf_vocab
#               或 python -m unittest test_load_vocab.TestLoadVocab.test_read_pdf_vocab
#               或 python -m unittest test_load_vocab.TestLoadVocab.test_load_file
# ---------------------------------------------------------------------------------------------    
if __name__ == "__main__":
    import unittest
    class TestLoadVocab(unittest.TestCase):
        def setUp(self):
            self.loader = Load_Vocab()
            self.pdf_path1 = wordlist_file1
            self.pdf_path2 = wordlist_file2
        def test_extract_pdf_vocab(self):
            if os.path.exists(self.pdf_path1):
                print(f"[DEBUG]extract_pdf_vocab函数开始测试,文件路径：{self.pdf_path1}")
                result = self.loader.extract_pdf_vocab(self.pdf_path1)
                print(f"[DEBUG]测试数量: {len(result)}")
                for rankmark,word in list(result.items())[:10]:
                    print(f"[DEBUG]测试结果: rank:{rankmark}---->word:{word}")
                print(f"[DEBUG]输出的数据格式示例：{list(result.items())[:10]}")
                print(f"[DEBUG]输出的数据格式示例：{list(result.items())[-10:]}")
                self.assertIsInstance(result, dict)
                for key, value in result.items():
                    self.assertIsInstance(key, int)
                    self.assertIsInstance(value, str)
            else:
                print(f"跳过 test_extract_pdf_vocab: 未找到测试文件 {self.pdf_path1}")
        def test_read_pdf_vocab(self):
            if os.path.exists(self.pdf_path2):
                print(f"[DEBUG]read_pdf_vocab函数开始测试,文件路径：{self.pdf_path2}")
                result = self.loader.read_pdf_vocab(self.pdf_path2)
                print(f"[DEBUG]测试数量: {len(result)}")
                for rankmark,word in list(result.items())[:10]:
                    print(f"[DEBUG]测试结果: rank:{rankmark}---->word:{word}")
                print(f"[DEBUG]输出的数据格式示例：{list(result.items())[:8]}")
                print(f"[DEBUG]输出的数据格式示例：{list(result.items())[677:682]}")
                print(f"[DEBUG]输出的数据格式示例：{list(result.items())[1705:1711]}")
                print(f"[DEBUG]输出的数据格式示例：{list(result.items())[-8:]}")
                self.assertIsInstance(result, dict)
                for key, value in result.items():
                    self.assertIsInstance(key, int)
                    self.assertIsInstance(value, str)
            else:
                print(f"跳过 test_read_pdf_vocab: 未找到测试文件 {self.pdf_path2}")
        def test_load_file(self):
            print("[DEBUG]load_file函数开始测试")
            full_vocab, target_lemmas, allowed_words = self.loader.load_file(WLF_DIR,1,1000)
            print(f"[DEBUG]输出的数据格式示例full_vocab:{dict(list(full_vocab.items())[:10])}")
            print(f"[DEBUG]输出的数据格式示例target_lemmas:{set(list(target_lemmas)[:10])}")
            print(f"[DEBUG]输出的数据格式示例allowed_words:{set(list(allowed_words)[:10])}")
        
    unittest.main()