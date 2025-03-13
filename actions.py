from db_handler import engine
from sqlalchemy import text

def add_numbers(number1: int, number2: int) -> int :
    return number1 + number2

def sql_engine_tool(query: str) -> str:
    output = ""
    with engine.connect() as con:
        rows = con.execute(text(query))
        for row in rows:
            output += "\n" + str(row)
    return output
