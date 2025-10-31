# 中文文本可读性指标 Chinese Readability Score

Evaluate the readability of Chinese text using word segmentation, part-of-speech analysis, and syntactic dependency analysis capabilities. Supports multiple NLP providers including LTP, Jieba, and PKU.
利用分词、词性分析和句法依存分析能力，对中文文本的可读性进行评估。支持多种 NLP 提供方，包括 LTP、Jieba 和 PKU。

The code is implemented based on several papers I know, with the scoring metric named after the first author of each paper.
代码根据我已知的几篇论文分别进行实现，评分指标名称即论文第一作者姓名。

## Installation

It's easy using pip, just run:
直接使用 pip 命令安装即可：

```shell
$ pip install readability_cn
```

Optional NLP providers:
可选的 NLP 提供方依赖：

```shell
# Install with Jieba support
$ pip install readability_cn[jieba]

# Install with PKU support
$ pip install readability_cn[pkuseg]

# Install with all optional providers
$ pip install readability_cn[all]
```

## Usage

```python
    import readability_cn
    from readability_cn.nlp import JiebaNLP, PkuNLP, LtpNLP

    # use LTP as default NLP provider
    readability = ChineseReadability()
    # or use other NLP providers
    # readability = ChineseReadability(nlp_provider=JiebaNLP())  # use Jieba
    # readability = ChineseReadability(nlp_provider=PkuNLP())    # use PKU
    # readability = ChineseReadability(nlp_provider=LtpNLP())    # explicitly use LTP

    # add new custom words
    readability.add_custom_words(['日志易', '优特捷'])

    # Compare readability metrics before and after file changes
    readability.analyze('old.adoc', 'new.adoc')

    # use your own preprocess functions
    import markdown
    import re
    with open(file_name, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    text = markdown.markdown(markdown_content)
    text = re.sub(r'\n+', '\n', content)
    ... # do other remove and replace here
    sentences = [sentence.strip() for sentence in readability.stnsplit.split(text) if sentence.strip()]
    readability.chengyong_gf0025_readability(sentences)

```

### Use Custom Vocab

You can use the sentencepiece tool to extract a vocabulary from specific domain documents, referring to the `custom_vocab.py` implementation in the `examples` directory. Then merge it into the top-level vocabulary for use:
您可以通过 sentencepiece 工具，对特定领域文档提取词表，可以参考 `examples` 目录中的 `custom_vocab.py` 实现。然后合并到甲级词汇表中使用：

```python
    # Load the top 16% of custom vocabulary as common words in specific fields
    # 可以加载自定义词表的前16%词汇作为特定领域的常用词汇
    # Default to the vocabulary from Fudan University's computer science corpus
    # 默认提供复旦大学计算机领域语料库的词表
    readability._load_custom_vocab()
    readability._load_custom_vocab("rizhiyi.vocab")
```

## Note

1. The research in this field in China is mainly concentrated in the area of teaching Chinese as a foreign language. The research data primarily consists of a small number of textbook passages and Chinese proficiency test outlines. The coefficients obtained from polynomial linear regression fitting may not be effective for native speakers or technical documents.
   国内进行相关研究的学者主要集中在对外汉语教育领域，研究数据集中为少量教材课文和汉语等级考试大纲等材料。多项式线性回归拟合的系数可能未必对母语用户、理工科文档等情况有效。

2. Some formulas are sensitive to the number of clauses. In this implementation, we simply use Chinese commas, semicolons, and colons for sentence splitting, without considering the mixed use of Chinese and English punctuation.
   部分公式对分句数量敏感。本实现中简单使用中文的逗号、分号、冒号进行切分，并未考虑中英文标点混用的情况。

3. This implementation currently only provides preprocessing for asciidoc format text. For other formats, please refer to the `preprocess_asciidoc()` method to remove various markups.
   本实现中暂时只提供了对 asciidoc 格式文本的预处理，其他格式请参照处理去除各种标记。

## Thanks

1. [LTP](https://github.com/HIT-SCIR/ltp)
2. [Lexi](https://github.com/Rebilly/lexi)
3. [Cursor](https://cursor.sh/) IDE and [Claude AI](https://www.anthropic.com)
