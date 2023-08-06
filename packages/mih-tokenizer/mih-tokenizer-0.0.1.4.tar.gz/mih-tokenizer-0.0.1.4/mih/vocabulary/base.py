# encoding: utf-8

import os
import numpy as np
import pandas as pd

from typing import List, Union, Tuple, Optional
from collections import OrderedDict
from collections.abc import Iterable

from ..util import logging
logger = logging.getLogger(__name__)

# Define type aliases
Text = str
TextInput = List[Text]

Token = str
TokenInput = List[Token]

Vocab = OrderedDict

VOCAB_FILES_NAMES = {"vocab_file": "vocab.txt"}


class VocabularyBase:

    def __init__(self, vocab_file=None, **kwargs):
        self.vocab = OrderedDict() if vocab_file is None else self.load_vocab(vocab_file)
        self.special_tokens = []
        self.unk_token = '[UNK]'
        self.add_tokens(self.unk_token, special_tokens=True)

    def __contains__(self, token: Token) -> bool:
        return token in self.vocab

    def __eq__(self, other):
        if isinstance(other, OrderedDict):
            return self.vocab == other
        return self == other

    def items(self):
        return self.vocab.items()

    def is_special(self, token: Token) -> bool:
        return token in self.special_tokens

    @property
    def vocab_size(self):
        return len(self.vocab)

    def add_tokens(self, tokens: Union[Token, TokenInput], special_tokens: bool = False):

        def _add_tokens(token: Token, special_tokens: bool = False):
            if special_tokens:
                self.special_tokens.append(token)
            self.vocab[token] = self.vocab_size

        if isinstance(tokens, str):
            _add_tokens(tokens, special_tokens=special_tokens)
            logger.debug(f'vocab size: {self.vocab_size}')
        elif isinstance(tokens, (list, tuple, Iterable, np.ndarray, pd.Series)):
            for token in tokens:
                _add_tokens(token, special_tokens=special_tokens)
            logger.debug(f'vocab size: {self.vocab_size}')
        else:
            raise ValueError(
                f"type of tokens unknown: {type(tokens)}. "
                f"Should be one of a str, list, tuple, set, Iterable, np.ndarray or pd.Series."
            )   

    def create_vocab(self, texts_or_path: Union[TextInput, os.PathLike], **kwargs):
        # TODO: support from counter

        def _create_vocab_with_special(texts, **kwargs):
            new_texts = []
            for text in texts:
                if isinstance(text, str):
                    new_texts.append(text)
                elif isinstance(text, (list, tuple, np.ndarray, pd.Series)):
                    for t in text:
                        if not self.is_special(t):
                            new_texts.append(t)
                else:
                    raise ValueError(
                        f"type of text unknown: {type(text)}. "
                        f"Should be one of a str, list, tuple, np.ndarray, pd.Series."
                    )   
            self._create_vocab(new_texts, **kwargs)

        def _create_vocab_byfile(p, **kwargs):
            with p.open() as f:
                texts = f.readlines()
            _create_vocab_with_special(texts, **kwargs)

        if isinstance(texts_or_path, (list, tuple, np.ndarray, pd.Series)):
            _create_vocab_with_special(texts_or_path, **kwargs)
        else:
            p = Path(texts_or_path)
            if p.is_file():
                self._create_vocab_byfile(p, **kwargs)
            elif p.is_dir():
                # TODO: in 1 file
                for _ in p.iterdir(): self._create_vocab_byfile(_, **kwargs)
            else:
                raise ValueError(
                    f"type of texts_or_path unknown: {type(texts_or_path)}. "
                    f"Should be one of a str, list, tuple, np.ndarray, pd.Series, os.PathLike."
                )   

    def _create_vocab(self, texts: TextInput, **kwargs):
        raise NotImplementedError

    def save_vocabulary(self, save_directory: str, filename_prefix: Optional[str] = None) -> Tuple[str]:
        index = 0
        os.makedirs(save_directory, exist_ok=True)
        vocab_file = os.path.join(
            save_directory, (filename_prefix + "-" if filename_prefix else "") + VOCAB_FILES_NAMES["vocab_file"]
        )
        with open(vocab_file, "w", encoding="utf-8") as writer:
            for token, token_index in self.vocab.items():
                if index != token_index:
                    logger.warning(
                        "Saving vocabulary to {}: vocabulary indices are not consecutive."
                        " Please check that the vocabulary is not corrupted!".format(vocab_file)
                    )
                    index = token_index
                writer.write(token + "\n")
                index += 1
        return (vocab_file,)

    def load_vocab(self, save_directory: str, filename_prefix: Optional[str] = None) -> Vocab:
        """Loads a vocabulary file into a dictionary."""
        vocab_file = os.path.join(
            save_directory, (filename_prefix + "-" if filename_prefix else "") + VOCAB_FILES_NAMES["vocab_file"]
        )
        with open(vocab_file, "r", encoding="utf-8") as reader:
            tokens = reader.readlines()
        for index, token in enumerate(tokens):
            token = token.rstrip("\n")
            self.vocab[token] = index
