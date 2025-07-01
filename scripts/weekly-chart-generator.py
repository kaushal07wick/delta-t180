#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime

logs = {
    'codeforces': 'codeforces/daily-log.md',
    'math': 'math/daily-log.md',
    'euler': 'euler/daily-log.md',
    'ctf': 'ctf/weekly-log.md',
    'kaggle': 'kaggle/progress-log.md'
}

# Get the current ISO week and today's date for chart filename
current_week = datetime.now().isocalendar()[1]
today_str = datetime.now().strftime('%Y-%m-%d')

def load_log(file_path):
    dates, values = [], []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('|') and not 'Date' in line and not set(line.strip()) <= {'|', '-'}:
                parts = [x.strip() for x in line.strip().split('|') if x.strip()]
                if len(parts) >= 2:
                    try:
                        # Correctly parse the date
                        date = pd.to_datetime(parts[0], format='%Y-%m-%d', errors='raise')
                        dates.append(date)
                        values.append(float(parts[1].split()[0]))
                    except Exception as e:
                        print(f"Error parsing line: {line.strip()} - {e}")
    return pd.DataFrame({'Date': dates, 'Value': values})

def plot_progress(skill, df):
    df = df.sort_values('Date')
    df['Cumulative'] = df['Value'].cumsum()

    charts_dir = os.path.join(skill, 'charts')
    os.makedirs(charts_dir, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Cumulative'], marker='o', linestyle='-', color='blue')
    plt.title(f'{skill.capitalize()} Progress')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Progress')
    plt.grid(True)

    # Format date axis as '1 Jul, 2025'
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%-d %b, %Y'))  # Linux/macOS
    plt.gcf().autofmt_xdate()

    # Save only the weekly chart
    weekly_chart = os.path.join(charts_dir, f'week_{current_week}_{today_str}.png')
    plt.savefig(weekly_chart)
    plt.close()

if __name__ == '__main__':
    for skill, path in logs.items():
        if os.path.exists(path):
            df = load_log(path)
            if not df.empty:
                plot_progress(skill, df)

    print('✅ Weekly charts generated successfully.')
