from sqlalchemy import create_engine, text, inspect

database = "demo_bank_db"
username = "root"
password = "root"
host = "localhost"
port = "3306"
db_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(db_uri)

with engine.connect() as con:
    rows = con.execute(text("""SELECT * FROM accounts"""))
    # for row in rows:
    #     print(row)

def get_tables_description() -> str:
    description = """Allows you to perform SQL queries on the table. Beware that this tool's output is a string representation of the execution output.
    It can use the following tables:"""

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    for table in tables:
        columns_info = [(col["name"], col["type"]) for col in inspector.get_columns(table)]

        table_description = f"Table '{table}':\n"

        table_description += "Columns:\n" + "\n".join([f"  - {name}: {col_type}" for name, col_type in columns_info])
        description += "\n\n" + table_description
        

    output = """
    Args:
        query: The query to perform. This should be correct SQL.
    """

    description += "\n\n" + output
    return description

# table_description = get_tables_description()


# print(table_description)