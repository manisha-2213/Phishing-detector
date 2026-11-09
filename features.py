"""Turn a URL into numbers the model can learn from, and explain suspicious signs."""
import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = [
    "login", "signin", "verify", "secure", "update", "account",
    "bank", "confirm", "password", "free", "bonus", "wallet",
]
SHORTENERS = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd"]


def _host(url):
    url = str(url).strip()
    parsed = urlparse(url if "://" in url else "http://" + url)
    return parsed.netloc.lower().split(":")[0]


def extract_features(url):
    url = str(url).strip()
    low = url.lower()
    host = _host(url)
    return {
        "length": len(url),
        "dots": url.count("."),
        "hyphens": url.count("-"),
        "digits": sum(c.isdigit() for c in url),
        "has_at": int("@" in url),
        "has_ip": int(bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host))),
        "https": int(low.startswith("https")),
        "suspicious_words": sum(w in low for w in SUSPICIOUS_WORDS),
        "subdomains": max(host.count(".") - 1, 0),
        "uses_shortener": int(any(s in host for s in SHORTENERS)),
        "host_length": len(host),
    }


FEATURE_NAMES = list(extract_features("http://example.com").keys())


def explain(url):
    """Plain-language reasons why a link looks suspicious."""
    f = extract_features(url)
    reasons = []
    if f["has_ip"]:
        reasons.append("Uses an IP address instead of a website name")
    if f["has_at"]:
        reasons.append("Contains '@', which can hide the real destination")
    if not f["https"]:
        reasons.append("Does not use HTTPS (no secure lock)")
    if f["suspicious_words"]:
        reasons.append(f"Contains {f['suspicious_words']} suspicious word(s) such as login/verify/secure")
    if f["length"] > 75:
        reasons.append("Very long link (often used to hide the real address)")
    if f["subdomains"] >= 3:
        reasons.append("Many subdomains (e.g. bank.login.secure.example.com)")
    if f["uses_shortener"]:
        reasons.append("Uses a link shortener that hides the destination")
    if f["hyphens"] >= 3:
        reasons.append("Many hyphens in the link")
    return reasons
