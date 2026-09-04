# program/src/config.py

import os
import sys
# 系统环境配置
os.environ.update({
    "BITSANDBYTES_NOWELCOME": "1",
    "ACCELERATE_USE_CPU": "True",
    "CUDA_VISIBLE_DEVICES": "-1",
    "KMP_DUPLICATE_LIB_OK": "TRUE",
    "BITSANDBYTES_CPU_ONLY": "1",
    "ACCELERATE_ENABLE_RICH": "0",
    "TRANSFORMERS_NO_ADVISORY_WARNINGS": "1",
    "TRANSFORMERS_OFFLINE": "1"
})
if sys.platform == "win32":
    sys.path.append(os.path.join(sys.base_prefix, 'Library', 'bin'))

import re
import argparse
import time
import json
import difflib
import numpy as np
from collections import defaultdict,deque,Counter
import psutil
from datetime import datetime
import cProfile
from pathlib import Path
from wordninja import split
import threading
import textstat
import random
import torch
from transformers import LogitsProcessor,LogitsProcessorList,BitsAndBytesConfig
import nltk
from nltk import word_tokenize,sent_tokenize
import spacy
from typing import Dict, List, Tuple
from sklearn.metrics.pairwise import cosine_similarity


# 路径配置
current_dir = os.path.dirname(os.path.abspath(__file__)) if not getattr(sys, 'frozen', False) else os.path.dirname(sys.executable)
MODEL_DIR = os.path.abspath(os.path.join(current_dir, "..\..", "models"))
DATA_DIR = os.path.abspath(os.path.join(current_dir, "..\..", "GloVe6B"))
WLF_DIR = os.path.abspath(os.path.join(current_dir, "..", "data"))
NLTK_DIR = os.path.abspath(os.path.join(current_dir, "..\..", "nltk_data"))

# 模型路径
wordlist_file0  = os.path.join(WLF_DIR, "ShortWordFrequency.xlsx")   # 组合成wordlist_file路径
wordlist_file1 = os.path.join(WLF_DIR, "ScallopEnFreq.pdf")          # 组合成wordlist_file路径
wordlist_file2 = os.path.join(WLF_DIR, "GradedOCvocab.pdf")          # 组合成wordlist_file路径
nltk_data_path = os.path.abspath(os.path.join(current_dir,"..\..","nltk_data"))   # 组合成nltk_data路径

deepseek_model_path = os.path.join(MODEL_DIR, "DeepSeek-R1-Distill-Qwen-1.5B")
Qwen_model_path = os.path.join(MODEL_DIR, "Qwen2.5-1.5B-Instruct")
deepseek_Q5_model_path = os.path.join(MODEL_DIR, "DeepSeek-R1-Distill-Qwen-1.5B-Q5_K_M-GGUF")
MobileLLaMA_model_path = os.path.join(MODEL_DIR, "MobileLLaMA-1_4B-Chat")

SentenceTransformer_path = os.path.join(MODEL_DIR, "sentence-transformers")

articles_path = os.path.abspath(\
    os.path.join(current_dir,"..\..\..","articles"))                   # articles_path路径
GloVe_path = os.path.join(DATA_DIR, "glove6B.gensim.bin")                 # 直接使用二进制文件

# 生成参数
SELECTED_THEME = 'CHILDHOOD_FUN_THEME1K'  # 可选项,GENERAL_THEME, CHILDHOOD_FUN_THEME1K,CHILDHOOD_FUN_THEME2K,OTHER_THEME，
WLF_SEL = "wordlist_file0"              #可选"wordlist_file0"，"wordlist_file1"，"wordlist_file2"
SHUT_DOWN_TIME = ["21:00", "07:00"]     # #格式为 ("开始时间", "结束时间")，时间格式为 "HH:MM"
# SHUT_DOWN_TIME = ["00:00", "23:59"]     # #格式为 ("开始时间", "结束时间")，时间格式为 "HH:MM"
VOCAB_LIMITED_LOGITSPROCESSOR = True
WORD_CLUSTER_LENGTH = 20
ARTICLE_LENGTH = 400
EXPANSION_THRESHOLD = 0.5
MODEL_PATH = deepseek_model_path
# MODEL_PATH = Qwen_model_path
# MODEL_PATH = deepseek_Q5_model_path
# MODEL_PATH = MobileLLaMA_model_path
DEBUG = False

