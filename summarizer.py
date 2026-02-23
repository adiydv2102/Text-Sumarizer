import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from collections import defaultdict

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class FrequencySummarizer:
    def __init__(self, language='english'):
        self.stopwords = set(stopwords.words(language))
        self.word_pattern = re.compile(r"[a-zA-Z0-9']+")

    def _tokenize_words(self, text):
        words = self.word_pattern.findall(text.lower())
        return [w for w in words if w not in self.stopwords]

    def build_frequency_table(self, text):
        freq = defaultdict(int)
        for word in self._tokenize_words(text):
            freq[word] += 1
        if not freq:
            return freq
        max_freq = max(freq.values())
        for w in freq:
            freq[w] /= max_freq
        return freq

    def score_sentences(self, text, freq_table):
        sentences = sent_tokenize(text)
        scores = defaultdict(float)
        for i, sent in enumerate(sentences):
            words = self._tokenize_words(sent)
            if not words:
                continue
            scores[i] = sum(freq_table.get(w,0) for w in words)
        return sentences, scores

    def summarize(self, text, num_sentences=None, percent=None):
        if not text.strip():
            return ""
        freq_table = self.build_frequency_table(text)
        sentences, scores = self.score_sentences(text, freq_table)
        if not scores:
            return ""
        total_sent = len(sentences)
        if percent is not None:
            k = max(1, int(total_sent * percent/100))
        elif num_sentences is not None:
            k = max(1, min(num_sentences, total_sent))
        else:
            k = max(1, int(total_sent*0.2))
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_indices = sorted([i for i,_ in ranked[:k]])
        return " ".join(sentences[i] for i in top_indices)
