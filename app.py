from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from crew.incident_crew import investigate
from tools.log_parser import parse_upload, summarize_events

load_dotenv()
st.set_page_config(page_title="CyberShield", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 1.6rem;}
.hero {padding: 1.4rem 1.6rem; border-radius: 16px; background: linear-gradient(120deg,#10243b,#1e4661); color: white;}
.hero h1 {margin: 0; color: white;} .hero p {margin: .4rem 0 0; color: #d7e8f5;}
</style>
""", unsafe_allow_html=True)

if "reports" not in st.session_state:
    st.session_state.reports = []

st.sidebar.title("🛡️ CyberShield")
page = st.sidebar.radio("Navigate", ["Overview", "Investigate", "Reports"])
st.sidebar.caption("AI-assisted incident triage · Human review required")


def get_secret(name: str, default: str = "") -> str:
    """Read a setting from environment variables or Streamlit secrets."""
    value = os.getenv(name, "")
    if value:
        return value
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return default


if page == "Overview":
    st.markdown('<div class="hero"><h1>CyberShield</h1><p>Turn security events into clear, evidence-backed investigations.</p></div>', unsafe_allow_html=True)
    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.metric("Investigations this session", len(st.session_state.reports))
    high_count = sum(1 for r in st.session_state.reports if r.get("severity", "").lower() in {"high", "critical"})
    c2.metric("High-priority findings", high_count)
    c3.metric("Reports ready", len(st.session_state.reports))
    st.subheader("How it works")
    st.markdown("1. Upload a CSV, JSON, or TXT security log.\n2. CrewAI agents analyze evidence, correlate events, assess risk, and draft a response plan.\n3. Review findings and recommendations before taking any action.")
    st.info("Use synthetic or authorized logs only. CyberShield provides decision support; it does not perform autonomous containment.")
    st.subheader("Quick start")
    st.write("Choose **Investigate** in the sidebar to run your first analysis.")

elif page == "Investigate":
    st.title("Investigate an incident")
    st.write("Upload a security log or try the included synthetic demo dataset.")
    demo_path = Path(__file__).parent / "data" / "sample_logs.csv"
    uploaded = st.file_uploader("Choose a log file", type=["csv", "json", "txt"])
    use_demo = st.checkbox("Use the built-in demo dataset", value=uploaded is None)

    raw = None
    filename = ""
    if uploaded is not None:
        raw, filename = uploaded.getvalue(), uploaded.name
    elif use_demo and demo_path.exists():
        raw, filename = demo_path.read_bytes(), demo_path.name

    if raw is not None:
        try:
            df = parse_upload(raw, filename)
            st.subheader("Data preview")
            st.dataframe(df.head(100), use_container_width=True)
            st.caption(f"{len(df)} rows loaded. Preview is limited to 100 rows.")
            if st.button("🔎 Investigate incident", type="primary", use_container_width=True):
                api_key = get_secret("GROQ_API_KEY")
                if not api_key:
                    st.error("GROQ_API_KEY is not configured. Add it to a local .env file or Streamlit app secrets.")
                else:
                    with st.spinner("CrewAI agents are investigating. This can take a minute or two..."):
                        try:
                            summary = summarize_events(df)
                            result = investigate(summary, api_key=api_key, model_name=get_secret("GROQ_MODEL", "llama-3.3-70b-versatile"))
                            report = {"filename": filename, "summary": summary, **result}
                            st.session_state.reports.insert(0, report)
                            st.session_state.latest = report
                            st.success("Investigation complete. Review the report below.")
                        except Exception as exc:
                            st.error(f"The investigation could not be completed: {exc}")
        except Exception as exc:
            st.error(f"Could not read this file: {exc}")

    if "latest" in st.session_state:
        report = st.session_state.latest
        st.divider()
        st.subheader("Latest investigation")
        st.markdown(report.get("report", "No report was generated."))
        with st.expander("View event summary sent to the AI"):
            st.code(report.get("summary", ""), language="text")
        st.download_button("Download report", data=report.get("report", ""), file_name="cybershield_incident_report.md", mime="text/markdown")

else:
    st.title("Incident reports")
    if not st.session_state.reports:
        st.info("No investigations yet. Run one from the Investigate page.")
    for index, report in enumerate(st.session_state.reports):
        title = f"{index + 1}. {report.get('filename', 'Incident')}"
        with st.expander(title):
            st.markdown(report.get("report", ""))
            st.download_button("Download report", data=report.get("report", ""), file_name=f"cybershield_report_{index + 1}.md", key=f"download_{index}")
