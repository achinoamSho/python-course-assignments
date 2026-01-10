# Assignment Submission Analyzer

This program analyzes assignment submission data from `subjects.txt` and generates comprehensive reports and visualizations.

## Features

- **Missing Submissions Report**: Identifies students who haven't submitted each assignment
- **Late Submissions Report**: Lists all late submissions with days/hours overdue
- **Submission Time Distribution**: Analyzes when students submit relative to deadlines
- **Format Popularity Analysis**: Analyzes title format variations used by students
- **Comprehensive Visualizations**: 6 different plots showing various aspects of submission behavior

## Requirements

Install the required Python packages:

```bash
pip install pandas matplotlib seaborn numpy
```

## Usage

Simply run the script:

```bash
python assignment_analyzer.py
```

The program will:
1. Parse data from `subjects.txt`
2. Generate text reports (displayed in console and saved to files)
3. Create visualizations (displayed in windows and saved as PNG files)
4. Save all outputs to the `analysis/` directory

## Output Structure

```
Day09/
  analysis/
    reports/
      missing_submissions.csv
      late_submissions.csv
      submission_statistics.json
      format_popularity.csv
      statistics_by_assignment.csv
    plots/
      1_submissions_per_day.png
      2_ontime_vs_late_per_day.png
      3_day_vs_night_owl.png
      4_submission_time_distribution.png
      5_title_format_patterns.png
      6_open_vs_closed.png
    summary_report.txt
```

## Visualizations

1. **Total Submissions per Assignment**: Colorful bar plot showing the total number of submissions for each assignment day (day01, day02, day03, etc.)

2. **On-Time vs Late Submissions per Day**: Stacked bar chart comparing on-time (green) and late (red) submissions for each assignment. Shows both counts and percentages with legend positioned on the right.

3. **Submission Time Patterns: Daytime vs Nighttime by Assignment**: Stacked bar chart showing when students submit - during daytime hours (6 AM - 6 PM) vs nighttime hours (7 PM - 5 AM) for each assignment. Helps identify "day owls" vs "night owls" among students.

4. **Distribution of Submission Time Relative to Deadline**: Density plot (filled with color) showing the distribution of when students submit relative to assignment deadlines. Negative values indicate submissions before the deadline, positive values indicate late submissions. Includes a red vertical line marking the deadline.

5. **Title Format Patterns**: Horizontal bar chart showing the popularity of different title format patterns students use when submitting assignments (e.g., "Day08", "Day 08", "day08", "Final Project", etc.). Displays both counts and percentages.

6. **OPEN vs CLOSED Submissions (Total)**: Simple bar chart showing the total number of OPEN vs CLOSED submissions across all assignments. Includes total counts, percentages, and overall submission count in the title.

## Data Format

The `subjects.txt` file should be tab-separated with the format:
```
ID<TAB>STATUS<TAB>TITLE<TAB>TIMESTAMP
```

Where:
- `ID`: Submission identifier
- `STATUS`: OPEN or CLOSED
- `TITLE`: Assignment title (e.g., "Day08 by Student Name")
- `TIMESTAMP`: ISO 8601 format timestamp (UTC)


