import asyncio
import os

from dotenv import load_dotenv
from mistralai import Mistral
import ollama

from prompts import SYSTEM_PROMPT

load_dotenv()

def get_response(user_prompt, system_prompt):
    client = ollama.Client()
    model="hf.co/hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF:latest"
    # model="deepseek-r1:latest"
    response = client.generate(
         model=model, 
         prompt=user_prompt, 
         system=system_prompt
    )
    return response



async def get_response_mistral(query: str) -> str:
    await asyncio.sleep(0)  # Ensures it yields execution
    api_key = os.getenv("MISTRAL_API_KEY")
    model = "mistral-large-latest"
    client = Mistral(api_key=api_key)

    chat_response = await asyncio.to_thread(client.chat.complete,  # Runs in thread
        model=model,
        messages=[
            {"role": "user", "content": query},
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    )
    return chat_response.choices[0].message.content