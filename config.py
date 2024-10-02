import os
import dotenv

dotenv.load_dotenv()

GITHUB_REPO = "mediar-ai/screenpipe" # mediar-ai/screenpipe / m13v/whatsapp2llm
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/stargazers"
LOOPS_API = "https://app.loops.so/api/v1/contacts/create"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
LOOPS_API_KEY = os.environ.get("LOOPS_API_KEY")