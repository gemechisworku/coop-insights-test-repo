import pandas as pd

from model_calls import get_response_mistral

def csv_reader_tool(file_path: str):
    """
    Reads a csv file from data folder with a specified path
 
    Returns
        dataframe: returns data readed from the csv file in dataframe 
    """
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")

async def handle_query(user_query: str, file_path: str):
    """
    Handles user query by fetching data and ensuring insights are generated.
    """

    df = pd.read_csv(file_path)
    data = df.to_dict(orient="records")

    # Ensure we always analyze the data after retrieving it
    insights_query = f"Analyze and generate insights on the following {data} related to: {user_query}"
    
    # Step 2: Generate insights based on the retrieved data
    insights = await generate_insights(insights_query)

    # Step 3: Format and return the final answer
    return f"Final_Answer: \n\n{insights}"

async def generate_insights(updated_user_prompt: str):
    """
    Calls a LLM model to generate insights about the provided query
    
    Args:
        updated_user_prompt: User prompt that the model user use to generate insights
    Returns:
        JSON_BLOB: The model response    

    """
    result = await get_response_mistral(updated_user_prompt)
    return result



