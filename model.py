import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline

# Load pre-trained LLM for text-to-SQL
query_pipeline = pipeline("text2text-generation", model="mrm8488/t5-base-finetuned-wikiSQL")

# Generate SQL query from natural language question
def generate_sql_query(question, columns):
    prompt = f"Generate a SQL query for the following question based on the columns {', '.join(columns)}: {question}"
    result = query_pipeline(prompt)
    sql_query = result[0]['generated_text']
    return sql_query

# Perform the data analysis based on SQL query and return visualization
def perform_data_analysis(sql_query, data):
    try:
        # Execute the SQL query on the pandas dataframe
        result = pd.read_sql_query(sql_query, data)
        
        # Generate visualization (e.g., for numeric data, we can plot)
        plot_path = 'visualizations/plot.png'
        if not os.path.exists('visualizations'):
            os.makedirs('visualizations')
        
        # Generate a simple plot (e.g., distribution of a column or correlation heatmap)
        if len(result.columns) == 1:
            plt.figure(figsize=(8, 6))
            sns.histplot(result[result.columns[0]], kde=True)
        else:
            plt.figure(figsize=(10, 8))
            sns.heatmap(result.corr(), annot=True, cmap="coolwarm")
        
        plt.savefig(plot_path)
        plt.close()

        return result.head().to_html(), plot_path

    except Exception as e:
        return f"Error in query or data processing: {e}", None
