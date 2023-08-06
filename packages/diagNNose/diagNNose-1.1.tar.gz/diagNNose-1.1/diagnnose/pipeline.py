from typing import Optional

from transformers import PreTrainedTokenizer

from diagnnose.config.config_dict import create_config_dict
from diagnnose.corpus import Corpus
from diagnnose.extract import Extractor
from diagnnose.models import LanguageModel
from diagnnose.models.import_model import import_model
from diagnnose.tokenizer.create import create_tokenizer


class Pipeline:
    def __init__(self):
        config_dict = create_config_dict()

        self.tokenizer: Optional[PreTrainedTokenizer] = None
        self.corpus: Optional[Corpus] = None
        self.model: Optional[LanguageModel] = None
        self.extractor: Optional[Extractor] = None

        if "tokenizer" in config_dict:
            self.tokenizer: Optional[PreTrainedTokenizer] = create_tokenizer(
                **config_dict["tokenizer"]
            )
        if "corpus" in config_dict:
            self.corpus = Corpus.create(
                tokenizer=self.tokenizer, **config_dict["corpus"]
            )
        if "model" in config_dict:
            self.model = import_model(config_dict)
        if "extract" in config_dict:
            self.extractor = Extractor(
                self.model, self.corpus, **config_dict["extract"]
            )

    def run(self):
        if self.extractor is not None:
            self.extractor.extract()
