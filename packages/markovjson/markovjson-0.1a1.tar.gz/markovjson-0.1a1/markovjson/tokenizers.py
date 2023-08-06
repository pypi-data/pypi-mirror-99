from markovjson.mkov import MarkovJson, ReverseMarkovJson


class MarkovCharJson(MarkovJson):
    def tokenize(self, text, wildcards=False):
        sequence = list(text)
        if wildcards:
            sequence = self.replace_wildcards(text)
        return sequence

    def generate_sequence(self, *args, **kwargs):
        seq = super().generate_sequence(*args, **kwargs)
        return "".join([s for s in seq if
                        s != self.START_OF_SEQ and s != self.END_OF_SEQ])


class MarkovWordJson(MarkovJson):
    def generate_sequence(self, *args, **kwargs):
        seq = super().generate_sequence(*args, **kwargs)
        return " ".join([s for s in seq if
                         s != self.START_OF_SEQ and s != self.END_OF_SEQ])


class ReverseMarkovCharJson(ReverseMarkovJson, MarkovCharJson):
    def generate_sequence(self, *args, **kwargs):
        seq = super().generate_sequence(*args, **kwargs)
        return seq[::-1]


class ReverseMarkovWordJson(ReverseMarkovJson, MarkovWordJson):
    def generate_sequence(self, *args, **kwargs):
        seq = super().generate_sequence(*args, **kwargs)
        return seq[::-1]
