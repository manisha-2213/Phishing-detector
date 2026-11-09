"""Risk scoring + one-page report for a scanned URL."""
from datetime import datetime

from features import explain, extract_features, FEATURE_NAMES
import pandas as pd


def score_url(model, url):
    """Return probability of phishing (0-1), risk level, and reasons."""
    row = pd.DataFrame([extract_features(url)])[FEATURE_NAMES]
    prob = float(model.predict_proba(row)[0][1])
    if prob >= 0.7:
        level, action = "HIGH", "Do not open. Report to the security team and block the link."
    elif prob >= 0.4:
        level, action = "MEDIUM", "Be careful. Verify the sender and website before clicking."
    else:
        level, action = "LOW", "Looks normal, but stay alert for unexpected requests."
    return {
        "url": url,
        "probability": prob,
        "level": level,
        "action": action,
        "reasons": explain(url),
    }


def make_report(result):
    reasons = result["reasons"] or ["No obvious warning signs found"]
    lines = [
        "PHISHING SCAN REPORT",
        "=" * 40,
        f"Date:        {datetime.now():%Y-%m-%d %H:%M}",
        f"URL:         {result['url']}",
        f"Risk level:  {result['level']}  ({result['probability']:.0%} chance of phishing)",
        "",
        "Why:",
        *[f"  - {r}" for r in reasons],
        "",
        f"Recommended action: {result['action']}",
        "",
        "Reference: MITRE ATT&CK T1566 (Phishing)",
    ]
    return "\n".join(lines)
