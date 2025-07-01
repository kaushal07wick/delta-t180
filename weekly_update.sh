#!/bin/bash

set -e

readme="progress_overview.md"
temp_readme="progress_overview_temp.md"

# Run the Python analyzer and capture output
declare -A skills_status
while IFS='=' read -r key value; do
    if [[ "$key" == "PROJECT_WEEK" ]]; then
        project_week=$value
    else
        skills_status["$key"]=$value
    fi
done < <(python3 /home/kaushal/delta-t180/scripts/analyze.py)

# Get this week's Sunday date
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sunday_date=$(date -d "last sunday +7 days" '+%Y-%m-%d')
else
    sunday_date=$(date -v +Sun '+%Y-%m-%d')
fi

# Add weekly header with date at the end of the file
echo -e "\n### Week ${project_week} - ${sunday_date}\n" >> "$readme"

# Update Weekly Execution Tracker: add ✅ emoji directly
awk -F '|' -v week_num="$project_week" \
    -v cf="${skills_status[CF]}" \
    -v math="${skills_status[Math]}" \
    -v workout="${skills_status[Workout]}" \
    -v euler="${skills_status[Euler]}" \
    -v ctf="${skills_status[CTF]}" \
    -v kaggle="${skills_status[Kaggle]}" \
    -v project="${skills_status[Project]}" \
'
BEGIN { OFS = "|" }
{
    gsub(/^ +| +$/, "", $2)

    if ($2 == "Week " week_num) {
        if (cf == 1 && $3 ~ /^ *$/)       $3 = " ✅ "
        if (math == 1 && $4 ~ /^ *$/)     $4 = " ✅ "
        if (workout == 1 && $5 ~ /^ *$/)  $5 = " ✅ "
        if (euler == 1 && $6 ~ /^ *$/)    $6 = " ✅ "
        if (ctf == 1 && $7 ~ /^ *$/)      $7 = " ✅ "
        if (kaggle == 1 && $8 ~ /^ *$/)   $8 = " ✅ "
        if (project == 1 && $9 ~ /^ *$/)  $9 = " ✅ "
    }
    print
}' "$readme" > "$temp_readme"

mv "$temp_readme" "$readme"

echo "✅ Weekly progress updated for Week ${project_week} (${sunday_date})."
