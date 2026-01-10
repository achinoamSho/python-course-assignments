"""
Assignment Submission Analysis Tool
Analyzes submission data from subjects.txt and generates reports and visualizations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import re
import json
from pathlib import Path
from collections import defaultdict

# Try to import seaborn (optional)
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# Configure matplotlib for better plots
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    try:
        plt.style.use('seaborn-darkgrid')
    except:
        try:
            plt.style.use('ggplot')
        except:
            plt.style.use('default')
if HAS_SEABORN:
    sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 100

# Deadlines
DEADLINES = {
    'day01': datetime(2025, 11, 1, 22, 0),
    'day02': datetime(2025, 11, 9, 22, 0),
    'day03': datetime(2025, 11, 16, 22, 0),
    'day04': datetime(2025, 11, 23, 22, 0),
    'day05': datetime(2025, 11, 29, 22, 0),
    'day06': datetime(2025, 12, 6, 22, 0),
    'day08': datetime(2025, 12, 30, 22, 0),
    'final_project': datetime(2026, 1, 11, 22, 0),
}


def parse_submission_line(line):
    """Parse a single line from subjects.txt"""
    parts = line.strip().split('\t')
    
    # Format is: ID, STATUS, TITLE, (optional empty), TIMESTAMP
    # Handle cases where there might be empty parts between title and timestamp
    if len(parts) < 4:
        return None
    
    sub_id = parts[0]
    status = parts[1]
    title = parts[2]
    # Timestamp is the last non-empty part
    timestamp_str = None
    for part in reversed(parts):
        if part.strip():  # Find last non-empty part
            timestamp_str = part
            break
    
    if not timestamp_str:
        return None
    
    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        # Convert to naive datetime for easier comparison (assuming UTC)
        timestamp = timestamp.replace(tzinfo=None)
    except:
        return None
    
    return {
        'id': sub_id,
        'status': status,
        'title': title,
        'timestamp': timestamp
    }


def extract_assignment_days(title):
    """Extract assignment day(s) from title. Returns list of day keys."""
    title_lower = title.lower()
    days_found = []
    
    # Check for combined days (e.g., "Day03 and Day04")
    day_pattern = r'day\s*0?(\d+)'
    matches = re.findall(day_pattern, title_lower)
    
    for match in matches:
        day_num = int(match)
        if day_num == 1:
            days_found.append('day01')
        elif day_num == 2:
            days_found.append('day02')
        elif day_num == 3:
            days_found.append('day03')
        elif day_num == 4:
            days_found.append('day04')
        elif day_num == 5:
            days_found.append('day05')
        elif day_num == 6:
            days_found.append('day06')
        elif day_num == 8:
            days_found.append('day08')
    
    # Check for final project
    if 'final' in title_lower and 'project' in title_lower:
        days_found.append('final_project')
    
    return days_found if days_found else None


def extract_student_name(title):
    """Extract student name from title."""
    # Common patterns: "DayXX by Name", "Day XX by Name", etc.
    # Split by "by" or "By"
    parts = re.split(r'\s+by\s+', title, flags=re.IGNORECASE)
    if len(parts) > 1:
        name = parts[-1].strip()
        # Remove any trailing punctuation
        name = re.sub(r'[^\w\s-]+$', '', name)
        return name
    return None


def normalize_student_name(name):
    """Normalize student name for consistent matching."""
    if not name:
        return None
    # Convert to lowercase and strip
    normalized = name.lower().strip()
    # Capitalize first letter of each word
    normalized = ' '.join(word.capitalize() for word in normalized.split())
    return normalized


def parse_data(filepath):
    """Parse subjects.txt and create structured DataFrame."""
    records = []
    name_mapping = {}  # Map variations to normalized names
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parsed = parse_submission_line(line)
            if not parsed:
                continue
            
            title = parsed['title']
            assignment_days = extract_assignment_days(title)
            student_name_raw = extract_student_name(title)
            
            if not assignment_days or not student_name_raw:
                continue
            
            # Normalize student name
            student_name_normalized = normalize_student_name(student_name_raw)
            name_mapping[student_name_raw] = student_name_normalized
            
            # Create a record for each assignment day (for combined submissions)
            for day in assignment_days:
                deadline = DEADLINES.get(day)
                if deadline:
                    hours_after_deadline = (parsed['timestamp'] - deadline).total_seconds() / 3600
                    is_late = hours_after_deadline > 0
                    
                    records.append({
                        'id': parsed['id'],
                        'status': parsed['status'],
                        'assignment_day': day,
                        'student_name': student_name_normalized,
                        'submission_time': parsed['timestamp'],
                        'deadline': deadline,
                        'hours_after_deadline': hours_after_deadline,
                        'days_after_deadline': hours_after_deadline / 24,
                        'is_late': is_late,
                        'title_format': title,
                        'hours_before_deadline': -hours_after_deadline if hours_after_deadline < 0 else 0
                    })
    
    df = pd.DataFrame(records)
    
    # Store original title formats for analysis
    if len(df) > 0:
        df['title_format_pattern'] = df['title_format'].str.extract(r'^([Dd]ay\s*\d+|Final\s+[Pp]roject)', expand=False)
    
    return df


def generate_missing_submissions_report(df):
    """Generate report of students who haven't submitted each assignment."""
    if df.empty:
        return pd.DataFrame()
    
    all_students = sorted(df['student_name'].unique())
    all_assignments = sorted(DEADLINES.keys())
    
    missing_data = []
    for assignment in all_assignments:
        submitted_students = set(df[df['assignment_day'] == assignment]['student_name'].unique())
        missing_students = [s for s in all_students if s not in submitted_students]
        
        for student in all_students:
            missing_data.append({
                'assignment_day': assignment,
                'student_name': student,
                'submitted': student not in missing_students,
                'missing': student in missing_students
            })
    
    missing_df = pd.DataFrame(missing_data)
    return missing_df


def generate_late_submissions_report(df):
    """Generate report of late submissions."""
    late_df = df[df['is_late'] == True].copy()
    late_df = late_df.sort_values(['assignment_day', 'hours_after_deadline'], ascending=[True, False])
    return late_df


def generate_format_popularity_report(df):
    """Analyze title format popularity."""
    if df.empty:
        return pd.DataFrame()
    
    format_counts = df['title_format_pattern'].value_counts().reset_index()
    format_counts.columns = ['format_pattern', 'count']
    format_counts['percentage'] = (format_counts['count'] / len(df) * 100).round(2)
    return format_counts


def create_visualizations(df, output_dir):
    """Create all visualizations and save them."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    fig_count = 1
    
    # 1. Bar plot: Total submissions per day (colorful)
    plt.figure(fig_count, figsize=(12, 6))
    fig_count += 1
    submissions_per_day = df.groupby('assignment_day').size().reset_index(name='count')
    submissions_per_day = submissions_per_day.sort_values('assignment_day')
    
    x = range(len(submissions_per_day))
    # Use colorful colormap
    colors = plt.cm.viridis(np.linspace(0, 1, len(submissions_per_day)))
    bars = plt.bar(x, submissions_per_day['count'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    plt.xlabel('Assignment Day', fontsize=11)
    plt.ylabel('Number of Submissions', fontsize=11)
    plt.title('Total Submissions per Assignment', fontsize=13, fontweight='bold')
    plt.xticks(x, [day.replace('_', ' ').title() for day in submissions_per_day['assignment_day']], rotation=45, ha='right')
    
    # Add value labels on bars
    for i, (idx, row) in enumerate(submissions_per_day.iterrows()):
        plt.text(i, row['count'] + 0.5, str(int(row['count'])), ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_dir / '1_submissions_per_day.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Bar plot: On-time vs Late submissions per day
    plt.figure(fig_count, figsize=(12, 6))
    fig_count += 1
    late_by_assignment = df.groupby('assignment_day').agg({
        'is_late': ['sum', 'count']
    }).reset_index()
    late_by_assignment.columns = ['assignment_day', 'late_count', 'total_count']
    late_by_assignment['on_time_count'] = late_by_assignment['total_count'] - late_by_assignment['late_count']
    late_by_assignment = late_by_assignment.sort_values('assignment_day')
    
    x = range(len(late_by_assignment))
    width = 0.6
    bars1 = plt.bar(x, late_by_assignment['on_time_count'], width, label='On Time', color='#2ecc71', alpha=0.8, edgecolor='black')
    bars2 = plt.bar(x, late_by_assignment['late_count'], width, bottom=late_by_assignment['on_time_count'], 
            label='Late', color='#e74c3c', alpha=0.8, edgecolor='black')
    
    # Add value labels
    for i, (idx, row) in enumerate(late_by_assignment.iterrows()):
        if row['on_time_count'] > 0:
            plt.text(i, row['on_time_count']/2, str(int(row['on_time_count'])), ha='center', va='center', 
                    fontweight='bold', color='white', fontsize=9)
        if row['late_count'] > 0:
            plt.text(i, row['on_time_count'] + row['late_count']/2, str(int(row['late_count'])), 
                    ha='center', va='center', fontweight='bold', color='white', fontsize=9)
    
    plt.xlabel('Assignment Day', fontsize=11)
    plt.ylabel('Number of Submissions', fontsize=11)
    plt.title('On-Time vs Late Submissions per Day', fontsize=13, fontweight='bold')
    plt.xticks(x, [day.replace('_', ' ').title() for day in late_by_assignment['assignment_day']], rotation=45, ha='right')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Move legend to the right
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_dir / '2_ontime_vs_late_per_day.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. Day vs Night Owl: Submission hour analysis
    plt.figure(fig_count, figsize=(12, 6))
    fig_count += 1
    # Extract hour from submission time
    df['submission_hour'] = df['submission_time'].dt.hour
    
    # Categorize as Day (6-18) or Night (19-5)
    def categorize_time(hour):
        if 6 <= hour < 19:
            return 'Day (6 AM - 6 PM)'
        else:
            return 'Night (7 PM - 5 AM)'
    
    df['time_category'] = df['submission_hour'].apply(categorize_time)
    
    # Group by assignment day and time category
    time_analysis = df.groupby(['assignment_day', 'time_category']).size().unstack(fill_value=0)
    time_analysis = time_analysis.reindex(sorted(time_analysis.index))
    
    x = range(len(time_analysis))
    width = 0.6
    
    if 'Day (6 AM - 6 PM)' in time_analysis.columns:
        day_counts = time_analysis['Day (6 AM - 6 PM)'].values
    else:
        day_counts = [0] * len(time_analysis)
    
    if 'Night (7 PM - 5 AM)' in time_analysis.columns:
        night_counts = time_analysis['Night (7 PM - 5 AM)'].values
    else:
        night_counts = [0] * len(time_analysis)
    
    bars1 = plt.bar(x, day_counts, width, label='Day (6 AM - 6 PM)', color='#f39c12', alpha=0.8, edgecolor='black')
    bars2 = plt.bar(x, night_counts, width, bottom=day_counts, label='Night (7 PM - 5 AM)', 
            color='#3498db', alpha=0.8, edgecolor='black')
    
    # Add value labels
    for i in range(len(time_analysis)):
        if day_counts[i] > 0:
            plt.text(i, day_counts[i]/2, str(int(day_counts[i])), ha='center', va='center', 
                    fontweight='bold', color='black', fontsize=9)
        if night_counts[i] > 0:
            plt.text(i, day_counts[i] + night_counts[i]/2, str(int(night_counts[i])), 
                    ha='center', va='center', fontweight='bold', color='white', fontsize=9)
    
    plt.xlabel('Assignment Day', fontsize=11)
    plt.ylabel('Number of Submissions', fontsize=11)
    plt.title('Submission Time Patterns: Daytime vs Nighttime by Assignment', 
             fontsize=12, fontweight='bold', pad=15)
    plt.xticks(x, [day.replace('_', ' ').title() for day in time_analysis.index], rotation=45, ha='right')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Move legend to the right
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_dir / '3_day_vs_night_owl.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 4. Distribution of submission time relative to deadline (Density only, filled with color)
    plt.figure(fig_count, figsize=(12, 6))
    fig_count += 1
    
    # Debug: Check if calculation is correct
    # Negative values = before deadline, positive = after deadline
    before_count = (df['hours_after_deadline'] < 0).sum()
    after_count = (df['hours_after_deadline'] > 0).sum()
    on_time_count = (df['hours_after_deadline'] == 0).sum()
    print(f"\nDebug Figure 4: Before deadline: {before_count}, After deadline: {after_count}, Exactly on time: {on_time_count}")
    
    # Calculate KDE
    try:
        from scipy import stats
        x_kde = np.linspace(df['hours_after_deadline'].min(), df['hours_after_deadline'].max(), 300)
        kde = stats.gaussian_kde(df['hours_after_deadline'].dropna())
        y_kde = kde(x_kde)
        
        # Plot filled density curve
        plt.fill_between(x_kde, y_kde, alpha=0.6, color='#3498db', label='Density')
        plt.plot(x_kde, y_kde, 'b-', linewidth=2.5, color='#2980b9')
    except ImportError:
        # If scipy not available, use seaborn or fallback to simple histogram density
        if HAS_SEABORN:
            sns.histplot(df['hours_after_deadline'], bins=50, kde=True, alpha=0.6, 
                        stat='density', color='#3498db', edgecolor=None, fill=True)
        else:
            # Fallback: use histogram with density
            n, bins, patches = plt.hist(df['hours_after_deadline'], bins=50, density=True, 
                                      alpha=0.6, color='#3498db', edgecolor=None)
            # Fill the histogram
            plt.fill_between((bins[:-1] + bins[1:]) / 2, n, alpha=0.6, color='#3498db')
    
    plt.axvline(x=0, color='red', linestyle='--', linewidth=2.5, label='Deadline', alpha=0.9)
    plt.xlabel('Hours After Deadline (negative = before deadline)', fontsize=11)
    plt.ylabel('Density', fontsize=11)
    plt.title('Distribution of Submission Time Relative to Deadline', fontsize=13, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(output_dir / '4_submission_time_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 5. Title format patterns (Treemap-style or horizontal bar chart)
    format_df = generate_format_popularity_report(df)
    if not format_df.empty:
        plt.figure(fig_count, figsize=(10, 6))
        fig_count += 1
        
        # Sort by count for better visualization
        format_df = format_df.sort_values('count', ascending=True)
        
        # Create horizontal bar chart with gradient colors
        y_pos = range(len(format_df))
        colors_bar = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(format_df)))
        bars = plt.barh(y_pos, format_df['count'], color=colors_bar, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Add value labels
        for i, (idx, row) in enumerate(format_df.iterrows()):
            plt.text(row['count'] + 0.5, i, f"{int(row['count'])} ({row['percentage']}%)", 
                    va='center', fontweight='bold', fontsize=10)
        
        plt.yticks(y_pos, format_df['format_pattern'], fontsize=10)
        plt.xlabel('Number of Submissions', fontsize=11)
        plt.ylabel('Title Format Pattern', fontsize=11)
        plt.title('Title Format Patterns: Distribution of Submission Title Formats', 
                 fontsize=13, fontweight='bold', pad=15)
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        plt.savefig(output_dir / '5_title_format_patterns.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # 6. OPEN vs CLOSED assignments (total across all assignments)
    plt.figure(fig_count, figsize=(8, 6))
    fig_count += 1
    
    # Count total OPEN vs CLOSED across all assignments
    status_counts = df['status'].value_counts()
    
    open_count = status_counts.get('OPEN', 0)
    closed_count = status_counts.get('CLOSED', 0)
    total_count = open_count + closed_count
    
    # Create bar plot
    categories = ['OPEN', 'CLOSED']
    counts = [open_count, closed_count]
    colors_bar = ['#e74c3c', '#2ecc71']
    
    bars = plt.bar(categories, counts, color=colors_bar, alpha=0.8, edgecolor='black', linewidth=2, width=0.6)
    
    # Add value labels on bars
    for i, (cat, count) in enumerate(zip(categories, counts)):
        plt.text(i, count + total_count * 0.01, f'{int(count)}\n({count/total_count*100:.1f}%)', 
                ha='center', va='bottom', fontweight='bold', fontsize=12, color='black')
    
    plt.ylabel('Number of Submissions', fontsize=12, fontweight='bold')
    plt.title(f'OPEN vs CLOSED Submissions (Total)\nTotal: {int(total_count)} submissions', 
             fontsize=13, fontweight='bold', pad=15)
    plt.grid(True, alpha=0.3, axis='y', linestyle='--')
    plt.tight_layout()
    plt.savefig(output_dir / '6_open_vs_closed.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n✓ All visualizations saved to: {output_dir}")
    print(f"✓ {fig_count - 1} plots generated and displayed")


def generate_text_reports(df, output_dir):
    """Generate text-based reports."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    reports = []
    
    # Summary Statistics
    reports.append("=" * 80)
    reports.append("ASSIGNMENT SUBMISSION ANALYSIS - SUMMARY STATISTICS")
    reports.append("=" * 80)
    reports.append(f"\nTotal Submissions: {len(df)}")
    reports.append(f"Unique Students: {df['student_name'].nunique()}")
    reports.append(f"Unique Assignments: {df['assignment_day'].nunique()}")
    reports.append(f"Late Submissions: {df['is_late'].sum()} ({df['is_late'].mean()*100:.1f}%)")
    reports.append(f"On-Time Submissions: {(~df['is_late']).sum()} ({(~df['is_late']).mean()*100:.1f}%)")
    
    # By Assignment
    reports.append("\n" + "=" * 80)
    reports.append("STATISTICS BY ASSIGNMENT")
    reports.append("=" * 80)
    for assignment in sorted(df['assignment_day'].unique()):
        assignment_df = df[df['assignment_day'] == assignment]
        late_count = assignment_df['is_late'].sum()
        total_count = len(assignment_df)
        reports.append(f"\n{assignment.replace('_', ' ').title()}:")
        reports.append(f"  Total Submissions: {total_count}")
        reports.append(f"  Late: {late_count} ({late_count/total_count*100:.1f}%)")
        reports.append(f"  On-Time: {total_count - late_count} ({(total_count-late_count)/total_count*100:.1f}%)")
        if late_count > 0:
            avg_late = assignment_df[assignment_df['is_late']]['days_after_deadline'].mean()
            max_late = assignment_df[assignment_df['is_late']]['days_after_deadline'].max()
            reports.append(f"  Average Days Late: {avg_late:.1f}")
            reports.append(f"  Maximum Days Late: {max_late:.1f}")
    
    # Missing Submissions
    missing_df = generate_missing_submissions_report(df)
    if not missing_df.empty:
        reports.append("\n" + "=" * 80)
        reports.append("MISSING SUBMISSIONS")
        reports.append("=" * 80)
        for assignment in sorted(DEADLINES.keys()):
            missing = missing_df[(missing_df['assignment_day'] == assignment) & (missing_df['missing'] == True)]
            if len(missing) > 0:
                reports.append(f"\n{assignment.replace('_', ' ').title()} - Missing ({len(missing)} students):")
                for _, row in missing.iterrows():
                    reports.append(f"  - {row['student_name']}")
    
    # Late Submissions Details
    late_df = generate_late_submissions_report(df)
    if not late_df.empty:
        reports.append("\n" + "=" * 80)
        reports.append("LATE SUBMISSIONS DETAILS")
        reports.append("=" * 80)
        for assignment in sorted(late_df['assignment_day'].unique()):
            assignment_late = late_df[late_df['assignment_day'] == assignment]
            reports.append(f"\n{assignment.replace('_', ' ').title()} - Late Submissions ({len(assignment_late)}):")
            for _, row in assignment_late.iterrows():
                reports.append(f"  - {row['student_name']}: {row['days_after_deadline']:.1f} days late")
    
    # Format Popularity
    format_df = generate_format_popularity_report(df)
    if not format_df.empty:
        reports.append("\n" + "=" * 80)
        reports.append("TITLE FORMAT POPULARITY")
        reports.append("=" * 80)
        for _, row in format_df.iterrows():
            reports.append(f"{row['format_pattern']}: {int(row['count'])} ({row['percentage']}%)")
    
    report_text = "\n".join(reports)
    
    # Save to file (should be in analysis/ root, not reports/)
    # output_dir here is passed as analysis/reports, but we need to go up one level
    if output_dir.name == 'reports':
        parent_dir = output_dir.parent
    else:
        parent_dir = output_dir
    report_file = parent_dir / 'summary_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    # Print to console
    print(report_text)
    
    return report_text


def save_data_reports(df, output_dir):
    """Save data reports as CSV files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Missing submissions
    missing_df = generate_missing_submissions_report(df)
    if not missing_df.empty:
        missing_df.to_csv(output_dir / 'missing_submissions.csv', index=False)
        print(f"✓ Saved: {output_dir / 'missing_submissions.csv'}")
    
    # Late submissions
    late_df = generate_late_submissions_report(df)
    if not late_df.empty:
        late_df.to_csv(output_dir / 'late_submissions.csv', index=False)
        print(f"✓ Saved: {output_dir / 'late_submissions.csv'}")
    
    # Format popularity
    format_df = generate_format_popularity_report(df)
    if not format_df.empty:
        format_df.to_csv(output_dir / 'format_popularity.csv', index=False)
        print(f"✓ Saved: {output_dir / 'format_popularity.csv'}")
    
    # Statistics by assignment
    stats = df.groupby('assignment_day').agg({
        'id': 'count',
        'is_late': 'sum',
        'hours_after_deadline': ['mean', 'median', 'min', 'max']
    }).reset_index()
    stats.columns = ['assignment_day', 'total_submissions', 'late_count', 
                     'avg_hours_after_deadline', 'median_hours_after_deadline',
                     'min_hours_after_deadline', 'max_hours_after_deadline']
    stats['on_time_count'] = stats['total_submissions'] - stats['late_count']
    stats['late_percentage'] = (stats['late_count'] / stats['total_submissions'] * 100).round(2)
    stats.to_csv(output_dir / 'statistics_by_assignment.csv', index=False)
    print(f"✓ Saved: {output_dir / 'statistics_by_assignment.csv'}")
    
    # Save statistics as JSON (as per plan)
    stats_dict = stats.to_dict('records')
    # Convert numpy types to native Python types for JSON serialization
    for record in stats_dict:
        for key, value in record.items():
            if isinstance(value, (np.integer, np.floating)):
                record[key] = float(value) if isinstance(value, np.floating) else int(value)
            elif pd.isna(value):
                record[key] = None
    
    # Also add overall statistics
    overall_stats = {
        'total_submissions': int(len(df)),
        'unique_students': int(df['student_name'].nunique()),
        'unique_assignments': int(df['assignment_day'].nunique()),
        'total_late': int(df['is_late'].sum()),
        'late_percentage': float(df['is_late'].mean() * 100),
        'on_time_percentage': float((~df['is_late']).mean() * 100)
    }
    
    json_data = {
        'overall_statistics': overall_stats,
        'statistics_by_assignment': stats_dict
    }
    
    with open(output_dir / 'submission_statistics.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved: {output_dir / 'submission_statistics.json'}")


def main():
    """Main function to run the analysis."""
    # File paths
    data_file = Path(__file__).parent / 'subjects.txt'
    output_dir = Path(__file__).parent / 'analysis'
    
    print("=" * 80)
    print("ASSIGNMENT SUBMISSION ANALYZER")
    print("=" * 80)
    print(f"\nReading data from: {data_file}")
    
    # Parse data
    df = parse_data(data_file)
    
    if df.empty:
        print("ERROR: No data parsed. Please check the file format.")
        return
    
    print(f"✓ Parsed {len(df)} submission records")
    print(f"✓ Found {df['student_name'].nunique()} unique students")
    print(f"✓ Found {df['assignment_day'].nunique()} unique assignments")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'reports').mkdir(parents=True, exist_ok=True)
    (output_dir / 'plots').mkdir(parents=True, exist_ok=True)
    
    print(f"\nGenerating reports...")
    # summary_report.txt should be in analysis/ root, not in reports/
    generate_text_reports(df, output_dir / 'reports')
    
    print(f"\nSaving data reports...")
    save_data_reports(df, output_dir / 'reports')
    
    print(f"\nGenerating visualizations...")
    print("Note: Plots will be displayed in separate windows and saved to disk.")
    create_visualizations(df, output_dir / 'plots')
    
    print(f"\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nAll outputs saved to: {output_dir}")
    print(f"  - Reports: {output_dir / 'reports'}")
    print(f"  - Plots: {output_dir / 'plots'}")


if __name__ == '__main__':
    main()

