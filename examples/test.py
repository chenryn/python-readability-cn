import sys
import os
import time

# 方便直接运行示例
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from readability_cn import ChineseReadability
from readability_cn.nlp import JiebaNLP, PkuNLP, LtpNLP


def run_with(name, provider):
    print(f"\n=== Running readability analyze with {name} ===")
    readability = ChineseReadability(nlp_provider=provider)
    # add new custom words
    readability.add_custom_words(['日志易', '优特捷'])

    # 加载示例自定义词表（可选）
    readability._load_custom_vocab()
    readability._load_custom_vocab(os.path.join(os.path.dirname(__file__), 'filtered_rizhiyi.vocab'))

    # 对比文件变更前后的可读性指标
    base = os.path.dirname(__file__)
    readability.analyze(os.path.join(base, 'old.adoc'), os.path.join(base, 'new.adoc'))


if __name__ == "__main__":
    # 使用 jieba 提供方
    try:
        start_time = time.time()
        run_with('JiebaNLP', JiebaNLP())
        end_time = time.time()
        print(f"[JiebaNLP] Time taken: {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"[Skip JiebaNLP] {e}")

    # 使用 pkuseg 提供方
    try:
        start_time = time.time()
        run_with('PkuNLP', PkuNLP())
        end_time = time.time()
        print(f"[PkuNLP] Time taken: {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"[Skip PkuNLP] {e}")

    # 使用 LTP 提供方
    try:
        start_time = time.time()
        run_with('LTP', LtpNLP())
        end_time = time.time()
        print(f"[LTP] Time taken: {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"[Skip LTP] {e}")