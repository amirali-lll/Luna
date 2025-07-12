import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

client = OpenAI(api_key=API_TOKEN)

openai = AsyncOpenAI()

async def main() -> None:
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input="Hi there! How are you doing today?",
        instructions="Speak in Persian with Iranian accent. Use a friendly and engaging tone.Speak casually and naturally.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

if __name__ == "__main__":
    asyncio.run(main())