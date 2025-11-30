import os
import datetime
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool # Correct import for custom tools

# ====================================================
# 1. CONFIGURATION
# ====================================================
# Replace these with your actual API keys
os.environ["SERPER_API_KEY"] = "YOUR_SERPER_KEY_HERE"
os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY_HERE"

# Define the Gemini LLM
# We use the LLM class for robust connection to Google
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash", 
    api_key=os.environ["GOOGLE_API_KEY"]
)

# ====================================================
# 2. CUSTOM TOOL: FILE SAVER (Replaces Gmail)
# ====================================================
class FileSaveTool(BaseTool):
    name: str = "File Saver"
    description: str = "Saves the text to a file named 'facebook_post.txt' on the local computer."

    def _run(self, text_content: str) -> str:
        try:
            filename = "facebook_post.txt"
            # We save it to the current folder
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text_content)
            return f"Successfully saved post to {filename}"
        except Exception as e:
            return f"Error saving file: {e}"

# Instantiate the tools
file_tool = FileSaveTool()
search_tool = SerperDevTool()

# ====================================================
# 3. AGENT DEFINITIONS (Multi-Agent System)
# ====================================================

# Agent 1: The Scout
scout = Agent(
    role='Football Data Scout',
    goal='Find accurate Premier League fixtures for the upcoming week',
    backstory='You are a researcher. You retrieve raw match data from the web.',
    tools=[search_tool],
    llm=gemini_llm,
    verbose=True,
    memory=True
)

# Agent 2: The Selector
selector = Agent(
    role='Bar Manager',
    goal='Select the top 3 matches to show',
    backstory='You manage a sports bar. You prioritize "Big 6" teams and evening games (12pm-10pm).',
    llm=gemini_llm,
    verbose=True,
    memory=True
)

# Agent 3: The Validator
validator = Agent(
    role='Schedule Validator',
    goal='Ensure no time conflicts and correct dates',
    backstory='You check that the selected matches are real and times are correct.',
    llm=gemini_llm,
    verbose=True,
    memory=True
)

# Agent 4: The Writer (Uses the Custom File Tool)
copywriter = Agent(
    role='Social Media Writer',
    goal='Write a Facebook post and SAVE it to a local file',
    backstory='You write exciting posts to get customers into the bar.',
    tools=[file_tool], # Giving access to the File Saver
    llm=gemini_llm,
    verbose=True,
    memory=True
)

# ====================================================
# 4. TASK DEFINITIONS
# ====================================================

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

task_fetch = Task(
    description=f"Search for English Premier League fixtures for the next 7 days starting from {current_date}.",
    expected_output="List of matches with Dates and Times.",
    agent=scout
)

task_select = Task(
    description="Select the 3 best matches based on the Manager's criteria.",
    expected_output="List of 3 selected matches with reasoning.",
    agent=selector
)

task_validate = Task(
    description="Review the selected list for accuracy.",
    expected_output="Confirmed text list of the matches.",
    agent=validator
)

task_draft = Task(
    description="Write a Facebook post for these matches and use the File Saver tool to save it.",
    expected_output="Confirmation that the file was saved.",
    agent=copywriter
)

# ====================================================
# 5. CREW EXECUTION (Sessions & Memory)
# ====================================================

football_crew = Crew(
    agents=[scout, selector, validator, copywriter],
    tasks=[task_fetch, task_select, task_validate, task_draft],
    process=Process.sequential,
    memory=True, # Concept: Sessions & Memory
    verbose=True,
    # Concept: Context Engineering (using Google Embeddings)
    embedder={
        "provider": "google-generativeai",
        "config": {
            "model": "models/embedding-001",
            "task_type": "retrieval_document",
        },
    }
)

print("### STARTING AGENT CREW ###")
result = football_crew.kickoff()
print("\n### FINAL RESULT ###")
print(result)
