from .registry import Registry


class TokeniserRegistry(Registry):
    def add_predefines(self):
        ...
        # This class will be updated in the coming PR
        # self.add_item(nltk_word_tokenizer)
