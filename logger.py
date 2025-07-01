#!/usr/bin/env python3

import os
from datetime import datetime

# Log file paths
log_paths = {
    'Codeforces': 'codeforces/daily-log.md',
    'Math': 'math/daily-log.md',
    'Euler': 'euler/daily-log.md',
    'Workout': 'workout/daily-log.md',
    'CTF': 'ctf/weekly-log.md',
    'Kaggle': 'kaggle/weekly-log.md',
    'Project': 'hft_projects/project-log.md'
}

today = datetime.now().strftime('%Y-%m-%d')
current_week = datetime.now().isocalendar()[1]

def log_codeforces():
    print('\n📄 Logging: CODEFORCES')
    problems_solved = input('Problems solved today: ').strip()
    contests = input('Contests today? (Yes/No): ').strip()
    rating = input('Current rating: ').strip()
    notes = input('Brief progress/notes: ').strip()

    log_entry = f'| {today} | {problems_solved} | {contests} | {rating} | {notes} |\n'
    with open(log_paths['Codeforces'], 'a') as f:
        f.write(log_entry)

    print('✅ Codeforces log updated.')

def log_math():
    print('\n📄 Logging: MATH')
    topic = input('Topic studied today: ').strip()
    duration = input('Duration (e.g. 1 hr, 30 min): ').strip()
    notes = input('Brief progress/notes: ').strip()

    log_entry = f'| {today} | {topic} | {duration} | {notes} |\n'
    with open(log_paths['Math'], 'a') as f:
        f.write(log_entry)

    print('✅ Math log updated.')

def log_euler():
    print('\n📄 Logging: EULER')
    problems_solved = input('Problems solved today: ').strip()
    total_solved = input('Running total solved: ').strip()

    log_entry = f'| {today} | {problems_solved} | {total_solved} |\n'
    with open(log_paths['Euler'], 'a') as f:
        f.write(log_entry)

    print('✅ Euler log updated.')

def log_workout():
    print('\n📄 Logging: WORKOUT')
    workout_type = input('Workout type (e.g. Cardio, Weights, Yoga): ').strip()
    duration = input('Duration (e.g. 1 hr, 30 min): ').strip()
    notes = input('Brief progress/notes: ').strip()

    log_entry = f'| {today} | {workout_type} | {duration} | {notes} |\n'
    with open(log_paths['Workout'], 'a') as f:
        f.write(log_entry)

    print('✅ Workout log updated.')

def log_ctf():
    print('\n📄 Logging: CTF')
    platform = input('CTF platform (e.g. picoCTF, HackTheBox): ').strip()
    challenges_solved = input('Challenges solved this week: ').strip()
    topics_covered = input('Topics covered (comma separated): ').strip()
    notes = input('Brief progress/notes: ').strip()

    log_entry = f'| {current_week} | {platform} | {challenges_solved} | {topics_covered} | {notes} |\n'
    with open(log_paths['CTF'], 'a') as f:
        f.write(log_entry)

    print('✅ CTF log updated.')

def log_kaggle():
    print('\n📄 Logging: KAGGLE')
    competition = input('Competition name: ').strip()
    rank = input('Current rank (e.g. Top 10%): ').strip()
    lb_score = input('Leaderboard score: ').strip()
    notes = input('Brief progress/notes: ').strip()

    log_entry = f'| {current_week} | {competition} | {rank} | {lb_score} | {notes} |\n'
    with open(log_paths['Kaggle'], 'a') as f:
        f.write(log_entry)

    print('✅ Kaggle log updated.')

def log_project():
    print('\n📄 Logging: PROJECT')
    project_name = input('Project name: ').strip()
    focus_area = input('Focus area this week: ').strip()
    hours_spent = input('Hours spent: ').strip()
    key_progress = input('Key progress this week: ').strip()
    notes = input('Any notes/blockers: ').strip()

    log_entry = f'| {current_week} | {project_name} | {focus_area} | {hours_spent} | {key_progress} | {notes} |\n'
    with open(log_paths['Project'], 'a') as f:
        f.write(log_entry)

    print('✅ Project log updated.')

def is_recent_entry(log_path, field_index=1, days=7):
    """Check if there is a recent entry within N days or the same week for weekly logs."""
    if not os.path.exists(log_path):
        return False
    with open(log_path, 'r') as file:
        for line in file:
            if line.startswith('|') and not set(line.strip()) <= {'|', '-'}:
                parts = [p.strip() for p in line.strip().split('|') if p.strip()]
                if not parts:
                    continue
                try:
                    value = parts[field_index]
                    if log_path in [log_paths['CTF'], log_paths['Kaggle'], log_paths['Project']]:
                        # Weekly logs: Check by week number
                        if int(value) == current_week:
                            return True
                    else:
                        # Daily logs: Check by date
                        entry_date = datetime.strptime(value, '%Y-%m-%d').date()
                        if (datetime.now().date() - entry_date).days < days:
                            return True
                except:
                    continue
    return False

def main():
    print(f'\n🟢 Logging for {today} (Week {current_week}):\n')

    log_codeforces()
    log_math()
    log_euler()
    log_workout()

    if not is_recent_entry(log_paths['CTF']):
        log_ctf()

    if not is_recent_entry(log_paths['Kaggle']):
        log_kaggle()

    if not is_recent_entry(log_paths['Project']):
        log_project()

    print('\n✅ All logs updated. You can now commit and push.\n')

if __name__ == '__main__':
    main()
