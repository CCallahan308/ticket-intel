import pytest
from unittest.mock import MagicMock
from src.models.summarizer import summarize
from src.models.insights import insights, extract_entities, extract_keywords, detect_sentiment
from src.models.router import route

@pytest.fixture(autouse=True)
def mock_spacy_nlp(monkeypatch):
    import src.models.insights as insights_module
    
    class DummyToken:
        def __init__(self, text, pos, is_stop):
            self.text = text
            self.pos_ = pos
            self.is_stop = is_stop
            
    class DummyEnt:
        def __init__(self, text, label):
            self.text = text
            self.label_ = label
            
    class DummyDoc:
        def __init__(self, text):
            self.text = text
            self.tokens = [
                DummyToken("iPhone", "PROPN", False),
            ]
            self.ents = [
                DummyEnt("$999.00", "MONEY"),
                DummyEnt("Jan 01, 2024", "DATE")
            ]
        def __iter__(self):
            return iter(self.tokens)
            
    dummy_nlp = MagicMock()
    dummy_nlp.return_value = DummyDoc("text")
    monkeypatch.setattr(insights_module, "get_nlp", lambda: dummy_nlp)

def test_summarize():
    text = "This is a short text. It should not be summarized much. Actually, maybe it will just return the original text if it's too short."
    summ, count = summarize(text, n=1)
    assert isinstance(summ, str)
    assert isinstance(count, int)
    
    # Empty text case
    summ, count = summarize("", n=3)
    assert summ == ""
    assert count == 0

def test_insights():
    text = "The new iPhone 14 costs $999.00 and I bought it on Jan 01, 2024. Contact me at test@example.com."
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
    # If text is totally empty, route should return a default fallback
    pipe = "dummy_pipe"
    i2l = {0: "General"}
    cat, conf, probs = route("", pipe, i2l)
    assert cat == "General"
    assert conf == 0.0
    assert probs == {"General": 1.0}
