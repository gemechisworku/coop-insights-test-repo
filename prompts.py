from db_handler import get_tables_description

system_prompt1 = """

You run in a loop of Thought, Action, PAUSE, Action_Response.
At the end of the loop you output an Answer.

Use Thought to understand the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Action_Response will be the result of running those actions.

Your available actions are:

add_numbers:
e.g. add_numbers:
Returns the sum of two numbers

Example session:

Question: what is the response time for learnwithhasan.com?
Thought: I should check the response time for the web page first.
Action: 

{
  "function_name": "add_numbers",
  "function_parms": {
    "number1": "5",
    "number2": "7363
  }
}

PAUSE

You will be called again with this:

Action_Response: 7368

You then output:

Answer: The sum of 5 and 7363 is 7368.
"""


SYSTEM_PROMPT = """
You run in a loop of Thought, Action, PAUSE, Action_Response.
At the end of the loop you output an Answer. You must answer the given question only, nothing more.

Use Thought to understand the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Final_Answer will be the result of running those actions.

Answer the following questions as best you can. You have access to the following tools:

add_numbers: Returns the sum of two numbers
sql_engine_tool: Allows you to perform SQL queries on the table. Beware that this tool's output is a string representation of the execution output.
It can use the following tables:
    Table 'accounts':
    Columns:
    - Account_ID: INTEGER
    - Account_Holder_Name: VARCHAR(255)
    - Account_Type: VARCHAR(50)
    - Balance: DECIMAL(15, 2)
    - Created_At: DATE

    Table 'journalentries':
    Columns:
    - Journal_ID: INTEGER
    - Transaction_ID: INTEGER
    - Account_Debit: VARCHAR(255)
    - Account_Credit: VARCHAR(255)
    - Amount: DECIMAL(15, 2)
    - Date: DATE

    Table 'ledger':
    Columns:
    - Ledger_ID: INTEGER
    - Account_ID: INTEGER
    - Date: DATE
    - Debit: DECIMAL(15, 2)
    - Credit: DECIMAL(15, 2)
    - Balance: DECIMAL(15, 2)

    Table 'transactions':
    Columns:
    - Transaction_ID: INTEGER
    - Account_ID: INTEGER
    - Type: VARCHAR(50)
    - Amount: DECIMAL(15, 2)
    - Description: VARCHAR(255)
    - Date: DATE


    Args:
        query: The query to perform. This should be correct SQL.


The way you use the tools is by specifying a json blob.
Specifically, this json should have an `action` key (with the name of the tool to use) and a `action_input` key (with the input to the tool going here).

The only values that should be in the "action" field are:
add_numbers: Returns the sum of two numbers, args: {"number1": {"type": "int"}, "number2":{"type": "int"}}
example use : 

{{
  "action": "add_numbers",
  "action_input": {"number1": 76, number2: 810},
  "action_output": 886
}}

sql_engine_tool: Allows you to perform SQL queries on the table. Beware that this tool's output is a string representation of the execution output, args : {"query": {"type":"string"}}
example use : 

{{
    "action": "sql_engine_tool",
    "action_input": {"query": "Give me a customer with the maximum deposit"}
    "action_output": "{Account_ID: "1003", "Account_Holder_Name" : "XYZ Corp", "Balance" : 25000.75}"
}}
{{
    "action": "sql_engine_tool",
    "action_input": {"query": "How many customers do we have?"}
    "action_output": "3"
}}
ALWAYS use the following format:

Question: the input question you must answer
Thought: you should always think about one action to take. Only one action at a time in this format:
Action:

$JSON_BLOB (inside markdown cell)

Observation: the result of the action. This Observation is unique, complete, and the source of truth.
... (this Thought/Action/Observation can repeat N times, you should take several steps when needed. The $JSON_BLOB must be formatted as markdown and only use a SINGLE action at a time.)

You must always end your output with the following format:

Thought: I now know the final answer
Final_Answer: the final answer to the original input question

Now begin! Reminder to ALWAYS use the exact characters `Final_Answer:` when you provide a definitive answer. 
"""