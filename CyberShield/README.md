# CyberShield — AI-assisted Cyber Incident Response

CyberShield is a hackathon MVP that uses **CrewAI**, **Groq**, and **Streamlit** to turn security event logs into an evidence-led incident triage report. It is designed for defensive analysis and human review; it does not execute containment actions.

## Features
- Upload CSV, JSON, or TXT event logs
- Preview and normalize records
- Four CrewAI agents: log analysis, event correlation, risk assessment, and response planning
- Generate a Markdown report with evidence, uncertainty, and human-reviewed recommendations
- Download reports from the app
- Synthetic demo dataset included

## Requirements
- Python 3.10–3.13 (use a version supported by your installed CrewAI release)
- Groq API key
- Git (for version control and GitHub upload)

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `GROQ_API_KEY` to your own key, then run:

```powershell
streamlit run app.py
```

Open the local URL shown in the terminal (usually http://localhost:8501). Select **Investigate**, keep **Use the built-in demo dataset** enabled, and click **Investigate incident**.

## Run locally (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env to add GROQ_API_KEY
streamlit run app.py
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Deploy with Streamlit Community Cloud
1. Push this project to a GitHub repository.
2. In Streamlit Community Cloud, create an app and select this repository and `app.py`.
3. Open the app's **Settings → Secrets** and add values from `.streamlit/secrets.toml.example`.
4. Deploy and test the public app link.
5. Never commit `.env`, real API keys, or confidential logs.

## Suggested GitHub upload
Upload the project contents (the files and folders in this directory) to the root of your new repository. Do not upload your local `.venv` folder or real `.env` file.

## Safety, privacy, and limitations
- Use synthetic data or logs you are authorized to analyze.
- Uploaded event data is sent to the configured LLM provider as part of analysis. Do not submit confidential data unless your organization has approved that processing.
- Model output can be inaccurate. Validate findings against original logs and trusted sources.
- A severity label is advisory, not a definitive incident determination.
- CyberShield does not block accounts, alter systems, or run commands. A qualified human must verify findings and approve any operational response.
- This prototype is not a replacement for a SIEM, EDR, or professional incident-response team.
