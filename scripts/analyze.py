#!/usr/bin/env python3

import os
from datetime import datetime, timedelta

# Mapping skill to their log files
logs = {
    'CF': 'codeforces/daily-log.md',
    'Math': 'math/daily-log.md',
    'Workout': 'workout/daily-log.md',
    'Euler': 'euler/daily-log.md',
    'CTF': 'ctf/weekly-log.md',
    'Kaggle': 'kaggle/weekly-log.md',
    'Project': 'hft_projects/project-log.md'
}

# Project start date
project_start = datetime.strptime('2025-07-01', '%Y-%m-%d')
today = datetime.today()
days_since_start = (today - project_start).days
project_week = days_since_start // 7 + 1

def get_entries_for_week(log_path, skill):
    """Returns a set of dates for daily logs, or True if a weekly entry exists."""
    if not os.path.exists(log_path):
        return set()

    entries = set()
    with open(log_path, 'r') as file:
        for line in file:
            if line.startswith('|') and not set(line.strip()) <= {'|', '-'}:
                parts = [p.strip() for p in line.strip().split('|') if p.strip()]
                
                if skill in ['CF', 'Math', 'Workout', 'Euler']:
                    # Daily logs: first column is date
                    try:
                        entry_date = datetime.strptime(parts[0], '%Y-%m-%d')
                        entry_week = (entry_date - project_start).days // 7 + 1
                        if entry_week == project_week:
                            entries.add(entry_date.date())
                    except:
                        continue
                else:
                    # Weekly logs: first column is week number
                    try:
                        week_number = int(parts[0])
                        if week_number == project_week:
                            return True  # Weekly entry exists
                    except:
                        continue

    if skill in ['CF', 'Math', 'Workout', 'Euler']:
        return entries
    else:
        return False

def has_seven_consecutive_days(dates_set):
    """Check if there are 7 consecutive days in the set."""
    if len(dates_set) < 7:
        return False
    sorted_dates = sorted(dates_set)
    for i in range(len(sorted_dates) - 6):
        if (sorted_dates[i + 6] - sorted_dates[i]).days == 6:
            return True
    return False

progress = {}

for skill, path in logs.items():
    week_entries = get_entries_for_week(path, skill)
    
    if skill in ['CF', 'Math', 'Workout', 'Euler']:
        progress[skill] = int(has_seven_consecutive_days(week_entries))
    else:
        progress[skill] = int(bool(week_entries))  # ✅ Safely convert to 0 or 1
        
# Print results as key=value to parse in bash
for skill, completed in progress.items():
    print(f'{skill}={completed}')

print(f'PROJECT_WEEK={project_week}')
