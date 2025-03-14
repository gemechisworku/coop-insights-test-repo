
import asyncio
import numpy as np
import ollama
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from model_calls import get_response_mistral
from my_actions import csv_reader_tool, generate_insights
from prompts import SYSTEM_PROMPT
from SimplerLLM.tools.json_helpers import extract_json_from_text

app = FastAPI()

available_actions = {
    "generate_insights" : generate_insights,
    "csv_reader_tool": csv_reader_tool 
}

    
@app.get("/process_query/")
async def process_query(user_prompt: str):
    response = await get_response_mistral(user_prompt)
    json_function = extract_json_from_text(response)

    if json_function:
        function_name = json_function[0]['action']
        function_params = json_function[0]['action_input']
        if function_name not in available_actions:
            return {"error": f"Unknown action: {function_name}"}

        action_function = available_actions[function_name]
        result = action_function(**function_params)
        if isinstance(result, np.ndarray):
            result = result.tolist()
        elif isinstance(result, (np.int64, np.int32)): 
            result = int(result)
        elif isinstance(result, (np.float32, np.float64)):
            result = float(result)
        return result
    else:
        return {"response": response}