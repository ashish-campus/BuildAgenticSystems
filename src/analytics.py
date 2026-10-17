import pandas as pd
import matplotlib.pyplot as plt
import os
from src.storage import load_requests

def run_analytics() -> str:
    """Runs basic analytics on stored requests and generates a chart."""
    requests = load_requests()
    if not requests:
        return "No data available for analytics. Please add some requests first."

    df = pd.DataFrame(requests)
    
    total_requests = len(df)
    df['desc_length'] = df['description'].apply(len)
    avg_length = df['desc_length'].mean()

    keywords = ['login', 'database', 'test', 'payment', 'api', 'user', 'create', 'website']
    all_text = " ".join(df['description'].str.lower())
    
    keyword_counts = {}
    for kw in keywords:
        count = all_text.count(kw)
        if count > 0:
            keyword_counts[kw] = count
            
    keyword_counts = dict(sorted(keyword_counts.items(), key=lambda item: item[1], reverse=True))

    chart_msg = "Not enough keyword matches to generate a chart."
    if keyword_counts:
        plt.figure(figsize=(8, 5))
        plt.bar(keyword_counts.keys(), keyword_counts.values(), color='skyblue')
        plt.title('Keyword Frequency in Feature Requests')
        plt.xlabel('Keywords')
        plt.ylabel('Frequency')
        
        plt.yticks(range(0, max(keyword_counts.values()) + 2)) 
        
        chart_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'keyword_chart.png')
        plt.savefig(chart_path)
        plt.close() # Close the figure to free memory
        chart_msg = f"Chart successfully saved to: {os.path.abspath(chart_path)}"

    report = (
        f"\n--- Analytics Report ---\n"
        f"Total Requests: {total_requests}\n"
        f"Average Description Length: {avg_length:.1f} characters\n"
        f"Keyword Frequency: {keyword_counts}\n"
        f"{chart_msg}\n"
        f"------------------------\n"
    )
    
    return report