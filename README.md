# 🍺 The Pub Promoter: Autonomous Sports Bar Agent

**Track:** Enterprise Agents
**Status:** Complete

## 🚀 Project Overview
This project solves a real-world problem for Sports Bar owners: the weekly drudgery of checking football schedules, cross-referencing them with business hours, and writing social media copy. 

**The Pub Promoter** is a Multi-Agent System that autonomously:
1.  **Scouts:** Searches the web for live Premier League fixtures (Serper Tool).
2.  **Strategizes:** Selects the top 3 matches based on "Big 6" popularity and Bar Opening Hours.
3.  **Validates:** checks dates/times to prevent hallucinations.
4.  **Executes:** Writes a Facebook post and saves it to a local file (Custom Tool).

## 🔑 Key Concepts Applied
*   **Multi-Agent System:** Sequential workflow using specialized roles (Scout, Selector, Validator, Copywriter).
*   **Tools:** 
    *   *Built-in:* Google Search (Serper) for real-time fixture data.
    *   *Custom:* `FileSaveTool` to persist the final marketing copy to disk.
*   **Sessions & Memory:** Agents share context (Short-term memory) to refine the match list as it passes through the chain.

## 🛠️ How to Run
1.  Clone the repository.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Set API Keys:
    *   `export GOOGLE_API_KEY='your_key'`
    *   `export SERPER_API_KEY='your_key'`
4.  Run the agent: `python main.py`