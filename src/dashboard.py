import os
import pandas as pd
import matplotlib.pyplot as plt
from src.storage import load_requests

def generate_dashboard():
    requests = load_requests()
    if not requests:
        print("\n[!] No data found. Please submit some feature requests first.")
        return

    df = pd.DataFrame(requests)

    df['confidence'] = pd.to_numeric(df['confidence'], errors='coerce').fillna(0)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    print("\n" + "="*40)
    print("📊 SDLC AGENT ANALYTICS DASHBOARD")
    print("="*40)
    print(f"Total Feature Requests Processed: {len(df)}")
    
    phase_counts = df['phase'].value_counts()
    print("\n--- Volume by Phase ---")
    for phase, count in phase_counts.items():
        print(f"- {phase.capitalize()}: {count} requests")
        
    avg_confidence = df.groupby('phase')['confidence'].mean()
    print("\n--- Agent Confidence by Phase ---")
    for phase, conf in avg_confidence.items():
        print(f"- {phase.capitalize()}: {conf:.1f}% average confidence")

    print("\n[Dashboard] Generating visual charts...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    phase_counts.plot(kind='bar', ax=ax1, color='#4A90E2', edgecolor='black')
    ax1.set_title('Feature Requests by Phase')
    ax1.set_xlabel('SDLC Phase')
    ax1.set_ylabel('Number of Requests')
    ax1.tick_params(axis='x', rotation=45)

    avg_confidence.plot(kind='bar', ax=ax2, color='#50E3C2', edgecolor='black')
    ax2.set_title('Average AI Confidence by Phase')
    ax2.set_xlabel('SDLC Phase')
    ax2.set_ylabel('Confidence (%)')
    ax2.set_ylim(0, 105) # Cap at 100% (with a little padding)
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()

    os.makedirs(os.path.join('data', 'dashboards'), exist_ok=True)
    filepath = os.path.join('data', 'dashboards', 'latest_dashboard.png')
    
    plt.savefig(filepath)
    plt.close() # Free up memory
    
    print(f"[Dashboard] Visual dashboard saved to: {os.path.abspath(filepath)}")
    print("="*40 + "\n")