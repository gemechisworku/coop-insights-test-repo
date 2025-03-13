import ollama

from actions import add_numbers, sql_engine_tool
from prompts import SYSTEM_PROMPT
from SimplerLLM.tools.json_helpers import extract_json_from_text

client = ollama.Client()

def get_response(user_prompt, system_prompt):
    model="hf.co/hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF:latest"
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

user_prompt = "How many customers do we have?"

# test_response = get_response(user_prompt=user_prompt, system_prompt=system_prompt).response
# print(f"test_response: \n ${test_response}")

turn_count = 1
max_turns = 5

# create agentic loop
while turn_count < max_turns:
    print (f"Loop: {turn_count}")
    print("----------------------")
    turn_count += 1

    response = get_response(user_prompt=user_prompt, system_prompt=SYSTEM_PROMPT).response

    print(response)

    json_function = extract_json_from_text(response)

    if json_function:
            function_name = json_function[0]['function_name']
            function_parms = json_function[0]['function_parms']
            if function_name not in available_actions:
                raise Exception(f"Unknown action: {function_name}: {function_parms}")
            print(f" -- running {function_name} {function_parms}")
            action_function = available_actions[function_name]
            #call the function
            result = action_function(**function_parms)
            function_result_message = f"Action_Response: {result}"
            user_prompt.join(function_result_message)
            print(function_result_message)
    else:
         break