import torch
from ltp import LTP, StnSplit


class LtpNLP:
    """
    LTP 封装：提供分句、分词、词性、依存等能力，并保持与现有调用一致的接口形态。
    - pipeline(sentence, tasks=[...])：透传 LTP 的 pipeline，返回对象具有 cws/pos/dep 属性
    - add_words(words, freq)：添加自定义词
    - split_sentences(text)：使用 LTP 的 StnSplit 进行分句
    """

    def __init__(self, model_path: str = "LTP/small", use_gpu: bool = True):
        self.ltp = LTP(model_path)
        self.stnsplit = StnSplit()

        if use_gpu and torch.cuda.is_available():
            self.ltp.to("cuda")

    def add_words(self, words, freq: int = 2):
        """向分词器添加自定义词。支持 list 或 dict。"""
        if isinstance(words, list):
            words_dict = {word: freq for word in words}
        elif isinstance(words, dict):
            words_dict = words
        else:
            raise ValueError("Words should be a list or a dictionary.")

        for word, f in words_dict.items():
            self.ltp.add_words([word], freq=f)

    def pipeline(self, sentence: str, tasks=None):
        """透传 LTP 的 pipeline 调用，返回对象包含 cws/pos/dep 等属性。"""
        tasks = tasks or ["cws", "pos", "dep"]
        return self.ltp.pipeline(sentence, tasks=tasks)

    def split_sentences(self, text: str):
        """使用 LTP 的 StnSplit 分句并去除空白。"""
        return [s.strip() for s in self.stnsplit.split(text) if s.strip()]


class PipelineOutput:
    """统一的 pipeline 返回对象，包含 cws/pos/dep 属性。"""
    def __init__(self, cws=None, pos=None, dep=None):
        self.cws = cws or []
        self.pos = pos or []
        self.dep = dep or []


class JiebaNLP:
    """
    基于 jieba 的 NLP 提供方：支持分词与词性，依存关系不提供（返回空）。
    - pipeline(sentence, tasks=[...])：当包含 pos 时使用 posseg 的切分以保证 cws 与 pos 对齐
    - add_words(words, freq)：通过 jieba.add_word 添加自定义词
    - split_sentences(text)：使用规则分句
    """

    def __init__(self):
        import jieba
        import jieba.posseg as pseg
        self.jieba = jieba
        self.pseg = pseg

    def add_words(self, words, freq: int = 2):
        if isinstance(words, list):
            words_dict = {word: freq for word in words}
        elif isinstance(words, dict):
            words_dict = words
        else:
            raise ValueError("Words should be a list or a dictionary.")

        for word, f in words_dict.items():
            self.jieba.add_word(word, freq=f)

    def pipeline(self, sentence: str, tasks=None):
        tasks = tasks or ["cws"]
        has_pos = "pos" in tasks
        if has_pos:
            tokens = list(self.pseg.lcut(sentence))  # 保证与词性对齐的切分
            cws = [t.word for t in tokens]
            pos = [t.flag for t in tokens]
        else:
            cws = list(self.jieba.lcut(sentence))
            pos = []
        dep = []  # jieba 不支持依存，返回空
        return PipelineOutput(cws=cws, pos=pos, dep=dep)

    def split_sentences(self, text: str):
        import re
        # 按句末标点分句，不按逗号分，以接近 LTP 默认行为
        parts = re.split(r'[。！？!?；;：:]+\s*', text)
        return [s.strip() for s in parts if s and s.strip()]


class PkuNLP:
    """
    基于 pkuseg 的 NLP 提供方：支持分词与词性，依存关系不提供（返回空）。
    - 通过 postag=True 获取词性，cws 与 pos 天然对齐
    - add_words(words, freq)：通过维护 user_dict 重建分词器以注入自定义词
    - split_sentences(text)：使用规则分句
    """

    def __init__(self):
        import pkuseg
        self.pkuseg = pkuseg
        self.user_dict = set()
        self._build_segmenter()

    def _build_segmenter(self):
        # 注意：重建分词器可能较慢，但能在运行时注入自定义词
        self.seg = self.pkuseg.pkuseg(postag=True, user_dict=list(self.user_dict))

    def add_words(self, words, freq: int = 2):
        # pkuseg 不使用词频，这里仅维护词典
        if isinstance(words, list):
            for w in words:
                self.user_dict.add(w)
        elif isinstance(words, dict):
            for w in words.keys():
                self.user_dict.add(w)
        else:
            raise ValueError("Words should be a list or a dictionary.")
        self._build_segmenter()

    def pipeline(self, sentence: str, tasks=None):
        tasks = tasks or ["cws"]
        tagged = self.seg.cut(sentence)  # list of (word, pos)
        cws = [w for w, _ in tagged]
        pos = [p for _, p in tagged] if "pos" in tasks else []
        dep = []  # pkuseg 不支持依存，返回空
        return PipelineOutput(cws=cws, pos=pos, dep=dep)

    def split_sentences(self, text: str):
        import re
        parts = re.split(r'[。！？!?；;：:]+\s*', text)
        return [s.strip() for s in parts if s and s.strip()]