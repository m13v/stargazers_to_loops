import os
import dotenv

dotenv.load_dotenv()

GITHUB_API = "https://api.github.com/repos/mediar-ai/screenpipe/stargazers"
LOOPS_API = "https://app.loops.so/api/v1/contacts/create"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
LOOPS_API_KEY = os.environ.get("LOOPS_API_KEY")