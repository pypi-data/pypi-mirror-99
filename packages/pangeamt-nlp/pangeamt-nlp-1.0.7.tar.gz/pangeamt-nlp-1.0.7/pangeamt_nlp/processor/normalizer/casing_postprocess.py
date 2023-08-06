from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg, SegCase
from sacremoses import MosesDetruecaser


class CasingPostprocess(NormalizerBase):
    NAME = "casing_postprocess"

    DESCRIPTION_TRAINING = """"""

    DESCRIPTION_DECODING = """
        Copy the casing of the source
    """

    LATIN_LANGS = [
        'es', 'fr', 'pt', 'it', 'ro', 'ca', 'ga', 'sc', 'oc', ' wa', 'co', 'an'
    ]

    PUNCTS_GENERAL = [
        "'", '"', "‘", '«', "“", '「', '『', '„', '»', '›', '‚', '‹',
        '-', '*', '{', '[', '#'
    ]

    PUNCTS_SPANISH = ['¿', "¡"]

    def __init__(self, src_lang: str, tgt_lang: str) -> None:
        super().__init__(src_lang, tgt_lang)
        self._detruecaser = MosesDetruecaser()

    def process_train(self, seg: Seg) -> None:
        pass

    def process_src_decoding(self, seg: Seg) -> None:
        if seg.src_raw.isupper():
            seg.src = seg.src.lower()

    def process_tgt_decoding(self, seg: Seg) -> None:
        if segment_has_nonempty_values(seg):
            if seg.src_case == SegCase.UPPER:
                seg.tgt = seg.tgt.upper()
            elif (
                is_en_or_latin(self.src_lang)
                and is_latin(self.tgt_lang)
            ):
                if seg.src_case == SegCase.LOWER:
                    seg.tgt = seg.tgt.lower()
                else:
                    detruecased_tgt = " ".join(
                        self._detruecaser.detruecase(seg.tgt)
                    )
                    if seg.src_raw[0] not in CasingPostprocess.PUNCTS_GENERAL \
                            and seg.tgt[0] not in CasingPostprocess.PUNCTS_SPANISH:
                        seg.tgt = process_first_char_casing(
                            seg.src_raw, detruecased_tgt
                        )
                    elif len(seg.src_raw) > 1 and len(seg.tgt) > 1:
                        if seg.tgt[0] in CasingPostprocess.PUNCTS_SPANISH:
                            seg.tgt = seg.tgt[0] + process_first_char_casing(
                                seg.src_raw[:], seg.tgt[1:]
                            )
                        elif seg.tgt[0] in CasingPostprocess.PUNCTS_GENERAL:
                            seg.tgt = seg.tgt[0] + process_first_char_casing(
                                seg.src_raw[1:], seg.tgt[1:]
                            )




def segment_has_nonempty_values(segment: Seg) -> bool:
    return (
        is_not_empty(segment.src_raw)
        and is_not_empty(segment.src)
        and is_not_empty(segment.tgt)
    )


def is_not_empty(s: str) -> bool:
    return s.strip() != ""


def is_en_or_latin(lang: str):
    return lang == "en" or is_latin(lang)


def is_latin(lang: str):
    return lang in CasingPostprocess.LATIN_LANGS


def process_first_char_casing(src_raw: str, tgt: str):
    first_char = tgt[0]
    if src_raw[0].isupper():
        first_char = first_char.upper()
    elif src_raw[0].islower():
        first_char = first_char.casefold()
    return first_char + tgt[1:]


