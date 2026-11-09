# Phishing Link Detector with Risk Score and Report

A beginner-friendly cybersecurity project. Paste a link and the tool predicts whether it is a phishing scam, assigns a **risk level (Low / Medium / High)**, explains **why**, and generates a **one-page report**.

## Why this project
Phishing is one of the most common ways organizations get breached (MITRE ATT&CK T1566). This tool shows how machine learning can help detect it, and how to communicate the risk in plain language to non-technical users.

## Features
- Extracts 11 features from a URL (length, dots, hyphens, "@", IP address, HTTPS, suspicious words, subdomains, link shortener, and more)
- Random Forest classifier (scikit-learn)
- Risk score with recommended action
- Plain-language explanation of each warning sign
- Downloadable scan report
- Streamlit dashboard: links scanned, high-risk count, risk chart
- Confusion matrix and accuracy report

## Project structure
| File | Purpose |
|---|---|
| `features.py` | Turns a URL into numbers and explains suspicious signs |
| `train.py` | Trains the model, prints accuracy, saves confusion matrix |
| `risk.py` | Risk score and report generation |
| `app.py` | Streamlit web app |
| `sample_data.csv` | Small synthetic demo dataset (for testing only) |

## How to run
```bash
pip install -r requirements.txt
python train.py                  # trains on sample_data.csv
streamlit run app.py             # opens the web app
```

### Use a real dataset (recommended for your resume)
1. Download a phishing URL dataset from Kaggle (search "phishing site URLs" or "malicious URLs dataset").
2. Make sure it has two columns named `url` and `label` (1 = phishing, 0 = safe).
3. Run: `python train.py your_dataset.csv`
4. Put your **real** accuracy numbers in this README and on your resume.

## Results
Add your results here after training on a real dataset:
- Dataset size: ___ URLs
- Accuracy: ___%
- Precision / recall for phishing: ___ / ___
- Screenshot of the confusion matrix and the app

## Limitations (be honest about these in interviews)
- Works on URL text only; it does not check page content, domain age, or reputation databases.
- Attackers can craft links that avoid these patterns.
- Accuracy depends on the training dataset.

## Future improvements
- Add domain age and WHOIS lookup
- Add checks against threat-intelligence feeds
- Email scanning mode and a browser extension
- Log scans to a SIEM-style dashboard
