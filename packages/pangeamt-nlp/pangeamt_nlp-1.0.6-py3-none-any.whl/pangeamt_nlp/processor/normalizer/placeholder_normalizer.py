#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import Dict
from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg
from pangeamt_nlp.utils.strip_and_catch_white import strip_and_catch_white


class PlaceholderNormalizer(NormalizerBase):
    NAME = "placeholder_norm"
    DESCRIPTION_TRAINING = """
    """
    DESCRIPTION_DECODING = """
    """

    def __init__(
        self, src_lang: str, tgt_lang: str, placeholder: str, glossary: Dict
    ) -> None:
        self.placeholder = placeholder
        self.glossary = dict(
            (re.escape(k), v) for k, v in glossary.items()
        )
        self.patterns = re.compile("|".join(self.glossary.keys()))
        super().__init__(src_lang, tgt_lang)

    def process_train(self, seg: Seg) -> None:
        pass

    def process_src_decoding(self, seg: Seg) -> None:
        seg.src = self.patterns.sub(
            lambda x: self.glossary[re.escape(x.group(0))], seg.src
        )

    def process_tgt_decoding(self, seg: Seg) -> None:
        pass
