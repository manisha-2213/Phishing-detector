"""Streamlit demo app.  Run with:  streamlit run app.py"""
import joblib
import pandas as pd
import streamlit as st

from risk import make_report, score_url

st.set_page_config(page_title="Phishing Detector", page_icon="🛡️")
st.title("🛡️ Phishing Link Detector")
st.write("Paste a link. The tool predicts if it is a scam, gives a risk level, and explains why.")


@st.cache_resource
def load_model():
    return joblib.load("model.joblib")


try:
    model = load_model()
except FileNotFoundError:
    st.error("model.joblib not found. Run `python train.py` first.")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = []

url = st.text_input("Link to check", placeholder="http://secure-login-paypal.verify-account.com/update")

if st.button("Scan link") and url.strip():
    result = score_url(model, url.strip())
    st.session_state.history.append(
        {"url": result["url"], "risk": result["level"], "probability": round(result["probability"], 2)}
    )

    colors = {"HIGH": "red", "MEDIUM": "orange", "LOW": "green"}
    st.markdown(f"### Risk level: :{colors[result['level']]}[{result['level']}]")
    st.progress(min(result["probability"], 1.0), text=f"{result['probability']:.0%} chance of phishing")

    st.subheader("Why?")
    if result["reasons"]:
        for r in result["reasons"]:
            st.write(f"- {r}")
    else:
        st.write("No obvious warning signs found.")

    st.info(f"**Recommended action:** {result['action']}")
    st.download_button("Download report", make_report(result), file_name="scan_report.txt")

if st.session_state.history:
    st.divider()
    st.subheader("Dashboard")
    hist = pd.DataFrame(st.session_state.history)
    c1, c2 = st.columns(2)
    c1.metric("Links scanned", len(hist))
    c2.metric("High risk", int((hist["risk"] == "HIGH").sum()))
    st.bar_chart(hist["risk"].value_counts())
    st.dataframe(hist, use_container_width=True)
