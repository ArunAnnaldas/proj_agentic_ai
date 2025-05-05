# Agentic AI - Dynamic Web Automation Agent

This project showcases an intelligent agent workflow using Google's Gemini model and Playwright. The agent dynamically reads a task prompt, generates automation steps using LLM, executes the scenario in a browser, and generates a structured report.

## 📁 Project Structure

- `agentcreation_with_tokens.py` – Main driver script that:
  - Reads task from `task.txt`
  - Initializes the Gemini LLM and Controller
  - Executes the dynamic automation using Playwright
  - Generates an HTML report (`result.html`)
  - Logs token usage using the Gemini API

- `task.txt` – A text file with the user instruction (e.g., "Navigate to google.com and search for 'LangChain AI'")

- `agentRun.json` – Stores the result history from the agent execution.

- `result.html` – A clean HTML report containing scenario results such as browser type, title, validation status, action count, and success indicator.

## ✅ Requirements

- Python 3.8+
- `playwright`
- `langchain-google-genai`
- `pydantic`

Install all dependencies:

```bash
pip install -r requirements.txt
```

Also install and set up Playwright browsers:

```bash
playwright install
```

## 🚀 Running the Agent

Make sure you have a valid `GOOGLE_API_KEY` set in your environment:

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

Then run the script:

```bash
python agentcreation_with_tokens.py
```

## 📊 Output

- `result.html`: Clean report summarizing what actions were performed and whether the title validation passed.
- `agentRun.json`: Full context history from the agent.
- Console output shows the total token usage.

---

## 📌 Example task in `task.txt`

```
Go to https://google.com and search for "LangChain Playwright".
```

---

## 🙏 Credits

Special thanks to **Anjali Jha** for creating the original sample code and contributions to the dynamic agent design.

