from src.helpdesk import HelpdeskAgent

def test_security_ticket():
    agent = HelpdeskAgent("data/faqs.csv")
    result = agent.analyze("I received a phishing email asking for my password")
    assert result["category"] == "Security"
    assert result["priority"] in {"High", "Critical"}

def test_network_ticket():
    agent = HelpdeskAgent("data/faqs.csv")
    result = agent.analyze("My office wifi is not connecting")
    assert result["category"] == "Network"

def test_faq_returned():
    agent = HelpdeskAgent("data/faqs.csv")
    result = agent.analyze("printer does not print")
    assert result["faq"]["title"]
