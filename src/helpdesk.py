import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity


CATEGORY_KEYWORDS = {
    "Network": ["wifi", "wi-fi", "internet", "network", "vpn", "ethernet", "connection", "connectivity"],
    "Hardware": ["laptop", "desktop", "keyboard", "mouse", "monitor", "screen", "printer", "battery", "charger", "hardware"],
    "Software": ["software", "application", "app", "crash", "install", "update", "excel", "word", "outlook", "browser"],
    "Account & Access": ["password", "login", "log in", "account", "access", "permission", "locked", "authentication", "mfa"],
    "Email": ["email", "mailbox", "gmail", "mail", "attachment", "outlook"],
    "Security": ["phishing", "malware", "virus", "suspicious", "security", "breach", "ransomware"],
    "Other": []
}

URGENT_TERMS = [
    "ransomware", "malware", "breach", "phishing", "hacked", "data loss",
    "production down", "server down", "entire team", "cannot work",
    "critical", "urgent", "immediately"
]

class HelpdeskAgent:
    def __init__(self, faq_path):
        self.faqs = pd.read_csv(faq_path).fillna("")
        self._train_classifier()
        self._build_retriever()

    @staticmethod
    def clean(text):
        text = str(text).lower()
        text = re.sub(r"[^a-z0-9\s\-]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def _train_classifier(self):
        # Lightweight embedded training set makes the demo reproducible offline.
        rows = [
            ("wifi not connecting to office network", "Network"),
            ("vpn connection fails from home", "Network"),
            ("internet is very slow", "Network"),
            ("ethernet cable has no connection", "Network"),
            ("laptop screen is broken", "Hardware"),
            ("keyboard is not working", "Hardware"),
            ("printer is not printing", "Hardware"),
            ("battery is not charging", "Hardware"),
            ("application crashes when I open it", "Software"),
            ("cannot install required software", "Software"),
            ("browser keeps crashing", "Software"),
            ("microsoft excel is not responding", "Software"),
            ("forgot my password", "Account & Access"),
            ("my account is locked", "Account & Access"),
            ("need permission to access a folder", "Account & Access"),
            ("mfa authentication is failing", "Account & Access"),
            ("email is not sending", "Email"),
            ("outlook mailbox is full", "Email"),
            ("email attachment cannot be opened", "Email"),
            ("received suspicious phishing email", "Security"),
            ("computer may have malware", "Security"),
            ("possible security breach", "Security"),
            ("ransomware warning appeared", "Security"),
            ("need help with an unusual issue", "Other"),
        ]
        x = [self.clean(t) for t, _ in rows]
        y = [c for _, c in rows]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
        X = self.vectorizer.fit_transform(x)
        self.classifier = LogisticRegression(max_iter=1000, random_state=42)
        self.classifier.fit(X, y)

    def _build_retriever(self):
        texts = [
            self.clean(f"{r['title']} {r['category']} {r['solution']}")
            for _, r in self.faqs.iterrows()
        ]
        self.retriever = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
        self.faq_matrix = self.retriever.fit_transform(texts)

    def predict_category(self, text):
        cleaned = self.clean(text)
        X = self.vectorizer.transform([cleaned])
        probs = self.classifier.predict_proba(X)[0]
        classes = self.classifier.classes_
        order = np.argsort(probs)[::-1]
        top_idx = order[0]
        scores = {classes[i]: round(float(probs[i]), 4) for i in order[:5]}

        # Keyword override for high-signal security language.
        if any(term in cleaned for term in ["ransomware", "malware", "phishing", "breach"]):
            category = "Security"
            confidence = max(float(probs[top_idx]), 0.90)
        else:
            category = classes[top_idx]
            confidence = float(probs[top_idx])

        return category, min(confidence, 0.99), scores

    def predict_priority(self, text):
        cleaned = self.clean(text)
        factors = []
        score = 0

        for term in URGENT_TERMS:
            if term in cleaned:
                score += 2
                factors.append(f"urgent term: '{term}'")

        if any(x in cleaned for x in ["entire team", "everyone", "all users", "production"]):
            score += 2
            factors.append("broad business impact")

        if any(x in cleaned for x in ["cannot", "unable", "blocked", "down", "failed"]):
            score += 1
            factors.append("service disruption")

        if score >= 5:
            priority = "Critical"
        elif score >= 3:
            priority = "High"
        elif score >= 1:
            priority = "Medium"
        else:
            priority = "Low"

        if not factors:
            factors.append("no strong urgency or broad-impact signals detected")

        return priority, factors

    def retrieve_faq(self, text, category):
        q = self.retriever.transform([self.clean(text)])
        sims = cosine_similarity(q, self.faq_matrix)[0]

        # Small category bonus improves relevance without hiding similarity.
        adjusted = sims.copy()
        for i, (_, row) in enumerate(self.faqs.iterrows()):
            if row["category"] == category:
                adjusted[i] += 0.08

        idx = int(np.argmax(adjusted))
        row = self.faqs.iloc[idx].to_dict()
        return row, float(sims[idx])

    def analyze(self, text):
        category, confidence, category_scores = self.predict_category(text)
        priority, factors = self.predict_priority(text)
        faq, faq_score = self.retrieve_faq(text, category)

        reason = (
            f"The model classified the request as '{category}' with "
            f"{confidence*100:.1f}% confidence. Priority was set to '{priority}' "
            f"based on the detected signals: {', '.join(factors)}."
        )

        response = self._draft_response(text, category, priority, faq)

        return {
            "category": category,
            "priority": priority,
            "confidence": confidence,
            "category_scores": category_scores,
            "priority_factors": factors,
            "faq": faq,
            "faq_score": round(faq_score, 4),
            "reason": reason,
            "response": response,
        }

    def _draft_response(self, ticket, category, priority, faq):
        greeting = "Hello,\n\nThanks for contacting IT Support."
        urgency = (
            "Because this appears to be a high-impact or security-related issue, "
            "please avoid making further changes to the affected system and contact the IT/security team immediately."
            if priority in ["Critical", "High"]
            else "We have reviewed your request and identified a relevant troubleshooting article."
        )
        return (
            f"{greeting}\n\n"
            f"Ticket category: {category}\n"
            f"Priority: {priority}\n\n"
            f"{urgency}\n\n"
            f"Recommended guidance — {faq['title']}:\n"
            f"{faq['solution']}\n\n"
            "If the issue continues, please reply with a screenshot or the exact error message "
            "and the approximate time the problem started. An IT support engineer can then investigate further.\n\n"
            "Regards,\nIT Support"
        )
