
from krwordrank.word import KRWordRank

class BaseKeywordExtraction:
    IN_TYPE = [str]
    OUT_TYPE = [str]

class TextRankExtractor(BaseKeywordExtraction):
    def __init__(self, pos_tagger_name=None, mecab_path=None,
                 lang='ko', max=10,
                 stopwords=[], combined_keywords=False):
        import treform.keyword.textrank as tr
        self.inst = tr.TextRank(pos_tagger_name=pos_tagger_name,mecab_path=mecab_path,lang=lang,stopwords=stopwords)
        self.max=max
        self.combined_keywords = combined_keywords
    def __call__(self, *args, **kwargs):
        import nltk.tokenize
        sents = nltk.tokenize.sent_tokenize(*args)
        for sent in sents:
            self.inst.build_keywords(sent)
        return self.inst.get_keywords(self.max,self.combined_keywords)

class MRAKUNExtractor(BaseKeywordExtraction):
    def __init__(self):
        from mrakun import RakunDetector
        from nltk.corpus import stopwords
        hyperparameters = {"distance_threshold": 2,
                           "distance_method": "editdistance",
                           "num_keywords": 10,
                           "pair_diff_length": 2,
                           "stopwords": stopwords.words('english'),
                           "bigram_count_threshold": 2,
                           "num_tokens": [1, 2],
                           "max_similar": 3,  ## n most similar can show up n times
                           "max_occurrence": 3}  ## maximum frequency overall

        self.keyword_detector = RakunDetector(hyperparameters)

    def __call__(self, *args, **kwargs):
        keywords = self.keyword_detector.find_keywords(*args, input_type="text")

        return keywords

class TextRankSummarizer(BaseKeywordExtraction):
    def __init__(self,pos_tagger_name=None,mecab_path=None,max=3):
        import treform.keyword.textrank as tr
        self.inst=tr.TextRank(pos_tagger_name=pos_tagger_name,mecab_path=mecab_path)
        self.max=max

    def __call__(self, *args, **kwargs):
        return self.inst.summarize(args[0],self.max)

class KeywordExtractionKorean(BaseKeywordExtraction):
    def __init__(self, min_count=2, max_length=10,
                 beta=0.85, max_iter=10, verbose=True, num_words=20):
        self.min_count=min_count
        self.max_length=max_length
        self.beta=beta
        self.max_iter=max_iter
        self.verbose=verbose
        self.num_words=num_words

        self.inst=KRWordRank(min_count, max_length,self.verbose)

    def __call__(self, *args, **kwargs):
        _num_keywords=10
        #print(str(args[0]) + "\n")
        keywords, rank, graph = self.inst.extract(args[0], self.beta, self.max_iter, self.num_words)

        return keywords