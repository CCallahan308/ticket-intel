import re

_nlp_data = None
_STOP = set(
    """
a an the and or but if while of to in on at by for with about as from up out
over into than then so such no not only own same after before now here there
when where why how all any both each few more most other some such only own
same than too very can will just should could would been being have has had
do does did get got make made take taken go went come came see saw know knew
think thought want wanted need needed use used find found give gave tell told
work seem feel try leave call keep let begin show hear play run move like live
""".lower().split()
)


def _init_nlp():
    global _nlp_data
    if _nlp_data is not None:
        return _nlp_data

    import nltk

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)

    _nlp_data = nltk
    return nltk


def split_sentences(txt: str) -> list[str]:
    nltk = _init_nlp()
    try:
        return nltk.sent_tokenize(txt)
    except:
        return [s.strip() for s in re.split(r"[.!?]+", txt) if s.strip()]


def tokenize(txt: str) -> list[str]:
    nltk = _init_nlp()
    try:
        toks = nltk.word_tokenize(txt.lower())
    except:
        toks = txt.lower().split()
    return [t for t in toks if t.isalpha() and t not in _STOP and len(t) > 2]
