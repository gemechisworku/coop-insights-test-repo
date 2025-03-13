from db_handler import engine
from sqlalchemy import text
from tabulate import tabulate

def add_numbers(number1: int, number2: int) -> int :
    """
    
    """
    return number1 + number2

def sql_engine_tool(query: str):
    """
    Allows you to perform SQL queries on the table. Beware that this tool's output is a string representation of the execution output.
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
    Returns: 
        list(dict): The result of the query after executing in list of dictionaries format
    """
    with engine.connect() as con:
        result = con.execute(text(query))
        columns = result.keys()  # Get column names
        return [dict(zip(columns, row)) for row in result]



def display_table(data):
    """
    Displays a list of dictionaries as a table.
    
    :param data: List of dictionaries, where keys are column names.
    """
    if not data:
        print("No data to display.")
        return

    headers = data[0].keys()
    rows = [list(row.values()) for row in data]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
