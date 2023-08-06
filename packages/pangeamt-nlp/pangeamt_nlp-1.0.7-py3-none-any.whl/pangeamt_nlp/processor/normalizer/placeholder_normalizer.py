#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from functools import partial
from typing import Dict
from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg
from pangeamt_nlp.utils.strip_and_catch_white import strip_and_catch_white


class PlaceholderNormalizer(NormalizerBase):
    NAME = "placeholder_norm"
    DESCRIPTION_TRAINING = """
        Does nothing
    """
    DESCRIPTION_DECODING = """
        For src changes the words in glossary for a placeholder with an index 
        and does the inverse process when processing tgt.
    """

    def __init__(
        self, src_lang: str, tgt_lang: str, placeholder: str, glossary: Dict
    ) -> None:
        self.placeholder = placeholder
        self.glossary = glossary
        self.patterns = re.compile(
            "|".join(map(re.escape, self.glossary.keys()))
        )
        super().__init__(src_lang, tgt_lang)

    def process_train(self, seg: Seg) -> None:
        pass

    def process_src_decoding(self, seg: Seg) -> None:
        helper = Helper()
        seg.src = self.patterns.sub(
            partial(helper.process, self.placeholder), seg.src
        )
        seg.placeholder_dictionary = helper.reverse_glossary

    def process_tgt_decoding(self, seg: Seg) -> None:
        pattern = re.escape(self.placeholder).replace("\\#", r"(?P<index>\d+)")
        seg.tgt = re.sub(pattern, partial(self.postprocess, seg), seg.tgt)

    def postprocess(self, seg: Seg, x: re.Match) -> str:
        key = seg.placeholder_dictionary[int(x.groupdict()["index"])]
        return self.glossary[key]


class Helper:
    def __init__(self):
        self.index = 0
        self.reverse_glossary = {}

    def process(self, placeholder: str, x: re.Match) -> str:
        self.index += 1
        self.reverse_glossary[self.index] = x.group(0)
        return placeholder.replace("#", str(self.index))
