from src.models.summarizer import summarize
from src.models.insights import insights, detect_sentiment
from src.models.router import route


def test_summarize():
    text = (
        "This is a short text. It should not be summarized much. Actually, maybe "
        "it will just return the original text if it's too short."
    )
    summ, count = summarize(text, n=1)
    assert isinstance(summ, str)
    assert isinstance(count, int)

    # Empty text case
    summ, count = summarize("", n=3)
    assert summ == ""
    assert count == 0


def test_insights():
    text = (
        "The new iPhone 14 costs $999.00 and I bought it on Jan 01, 2024. "
        "Contact me at test@example.com."
    )
    ents, kws, sent = insights(text)

    assert isinstance(ents, list)
    assert any(e["type"] == "EMAIL" for e in ents)
    assert any(e["type"] == "MONEY" for e in ents)
    assert any(e["type"] == "DATE" for e in ents)

    assert isinstance(kws, list)
    assert isinstance(sent, str)


def test_sentiment():
    assert detect_sentiment("This is absolutely wonderful and great!") == "positive"
    assert detect_sentiment("This is terrible, broken, and awful.") == "negative"
    assert detect_sentiment("The sky is blue today.") == "neutral"


def test_route_fallback():
    # Empty text should short-circuit to the default fallback without touching the model.
    pipe = "dummy_pipe"
    i2l = {0: "General"}
    cat, conf, probs = route("", pipe, i2l)
    assert cat == "General"
    assert conf == 0.0
    assert probs == {"General": 1.0}
