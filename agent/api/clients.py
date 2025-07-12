from openai import OpenAI, AsyncOpenAI
from config import OPENAI_API_KEY,GROQ_API_KEY

openai_client = OpenAI(api_key=OPENAI_API_KEY)
async_openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

groq_client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)
