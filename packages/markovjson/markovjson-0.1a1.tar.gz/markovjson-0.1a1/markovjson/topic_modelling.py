from markovjson import MarkovWordJson
from os.path import basename


class MarkovTopic(MarkovWordJson):
    def __init__(self, ignore_case=True, *args, **kwargs):
        self.ignore_case = ignore_case
        super(MarkovTopic, self).__init__(*args, **kwargs)
        self._topics = []

    def register_topic(self, topic_name, samples):
        topic_name = f"[/LABEL={topic_name}]"
        for s in samples:
            if not s.strip():
                continue
            if self.ignore_case:
                s = s.lower()
            s += f" {topic_name}"
            self.add_string(s)

            if topic_name not in self._topics:
                self._topics.append(topic_name)

    def register_topic_from_file(self, path, topic_name=None):
        topic_name = topic_name or basename(path)
        with open(path) as topic:
            samples = [l.strip() for l in topic.readlines()]
        self.register_topic(topic_name, samples)

    def score_topic(self, topic, document):
        if isinstance(document, str):
            tokens = self.tokenize(document, wildcards=True)
        else:
            tokens = document
        return {t: self.calc_approximate_removal_score(t, required_states=[topic])
                for t in tokens}

    def score_tokens(self, document):
        tokens = self.tokenize(document, wildcards=True)
        results = {}
        for topic in self._topics:
            results[topic] = self.score_topic(topic, tokens)
        return results

    def predict_topic(self, document, thresh=0.3):
        topics = {}
        for topic, word_scores in \
                self.score_tokens(document).items():
            scores = [w for k, w in word_scores.items()]
            score = sum(scores) / len(scores)
            if score >= thresh:
                topics[topic] = score
        return topics

