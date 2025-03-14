import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64
import numpy as np

from test import test_process_query

data = [
    {
        "Transaction_ID": "5040",
        "Account_ID": "1040",
        "Type": "Transfer",
        "Amount": 25000.6,
        "Description": "Warehouse Rent",
        "Date": "2024-06-05"
    },
    {
        "Transaction_ID": "5011",
        "Account_ID": "1011",
        "Type": "Transfer",
        "Amount": 25000.0,
        "Description": "Investment Funding",
        "Date": "2024-04-05"
    },
    {
        "Transaction_ID": "5049",
        "Account_ID": "1049",
        "Type": "Transfer",
        "Amount": 24000.25,
        "Description": "Lease Payment",
        "Date": "2024-06-23"
    },
    {
        "Transaction_ID": "5043",
        "Account_ID": "1043",
        "Type": "Transfer",
        "Amount": 22000.75,
        "Description": "Supplier Payment",
        "Date": "2024-06-11"
    },
    {
        "Transaction_ID": "5034",
        "Account_ID": "1034",
        "Type": "Transfer",
        "Amount": 21000.5,
        "Description": "Vendor Payment",
        "Date": "2024-05-24"
    }
]

def generate_visualization(data: dict) -> str:
    """
    Generates a data visualization based on the given JSON data automatically detecting
    the appropriate chart type.
    
    Parameters:
        data (dict): The data in JSON format.
    
    Returns:
        str: The base64 encoded string of the generated plot image or table.
    """
    df = pd.DataFrame(data)
    df = df.loc[:, ~df.columns.str.endswith('_ID')]

    # print(df)
    print("Columns: \n", df.info)
    
    def encode_plot_to_base64():
        image_stream = io.BytesIO()
        plt.savefig(image_stream, format='png')
        plt.show()
        plt.close()
        image_stream.seek(0)
        encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
        return encoded_image
    
    # 1. Check if data is numeric or categorical, and select visualization
    if df.select_dtypes(include=['number']).shape[1] == 0:
        # If there are no numeric columns, return a table
        plt.figure(figsize=(10, 6))
        plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        plt.axis('off')
        plt.title("Data Table")
        return encode_plot_to_base64()

    # 2. If there are numeric columns, check how many numeric columns there are
    if df.select_dtypes(include=['number']).shape[1] == 1:
        # If there is only one numeric column, consider a bar or pie chart
        if 'category' in df.columns:
            # If there is a category column, we can make a bar chart or pie chart
            plt.figure(figsize=(10, 6))
            plt.pie(df['value'], labels=df['category'], autopct='%1.1f%%', startangle=90)
            plt.title("Pie Chart: Category Distribution")
            return encode_plot_to_base64()
        else:
            # Default to bar chart
            plt.figure(figsize=(10, 6))
            sns.barplot(x=df.columns[0], y=df.columns[1], data=df)
            plt.title("Bar Chart")
            plt.xlabel(df.columns[0])
            plt.ylabel(df.columns[1])
            return encode_plot_to_base64()

    elif df.select_dtypes(include=['number']).shape[1] > 1:
        # If there are multiple numeric columns, create a bar chart
        # We assume this is a scenario for comparing multiple numerical columns
        plt.figure(figsize=(10, 6))
        sns.barplot(x=df.columns[0], y=df.columns[1], data=df)
        plt.title("Bar Chart")
        plt.xlabel(df.columns[0])
        plt.ylabel(df.columns[1])
        return encode_plot_to_base64()
    
    # 3. If the data has numeric columns and categorical columns, create a scorecard
    elif df.select_dtypes(include=['number']).shape[1] > 0 and len(df.columns) > 2:
        # Summary statistics could be used for a scorecard
        summary_stats = df.describe().iloc[0]  # Take summary stats for the first row
        plt.figure(figsize=(8, 4))
        for idx, (column, value) in enumerate(summary_stats.items()):
            plt.text(0.5, 1-idx*0.2, f"{column}: {value:.2f}", fontsize=12, ha='center')
        plt.axis('off')
        plt.title('Scorecard')
        return encode_plot_to_base64()

    # Default: Return a table if we can't decide
    plt.figure(figsize=(10, 6))
    plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    plt.axis('off')
    plt.title("Data Table")
    return encode_plot_to_base64()


generate_visualization(data)