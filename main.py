
import ollama
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from actions import add_numbers, sql_engine_tool
from prompts import SYSTEM_PROMPT
from SimplerLLM.tools.json_helpers import extract_json_from_text

from mistralai import Mistral

load_dotenv()
app = FastAPI()

def get_response_mistral(query: str) -> str:
    model = "mistral-large-latest"
    api_key = os.getenv("MISTRAL_API_KEY")
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": query,
            },
            {
                 "role": "system",
                 "content": SYSTEM_PROMPT
            }
        ]
    )
    response_content = chat_response.choices[0].message.content
    return response_content


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


available_actions = {
    "add_numbers" : add_numbers,
    "sql_engine_tool": sql_engine_tool
}

    
@app.get("/process_query/")
def process_query(user_prompt: str):
    response = get_response_mistral(user_prompt)
    json_function = extract_json_from_text(response)

    if json_function:
        function_name = json_function[0]['action']
        function_params = json_function[0]['action_input']
        if function_name not in available_actions:
            return {"error": f"Unknown action: {function_name}"}

        action_function = available_actions[function_name]
        result = action_function(**function_params)
        function_result_message = f"Action_Response: {result}"
        return function_result_message
    else:
        return {"response": response}