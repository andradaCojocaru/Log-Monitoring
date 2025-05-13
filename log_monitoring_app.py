import os
import csv
from datetime import datetime, timedelta

# Constants for thresholds
WARNING_THRESHOLD = timedelta(minutes=5)
ERROR_THRESHOLD = timedelta(minutes=10)

file_log_path = './data/logs.log'

# Check if the log file exists
if not os.path.exists(file_log_path):
    raise FileNotFoundError(f"Log file not found: {file_log_path}")

# Function to parse the log file
def parse_log_file(file_path):
    logs = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            timestamp, job_name, status, job_id = row
            if job_id not in logs:
                logs[job_id] = {}
                logs[job_id]['job_name'] = job_name.strip()
            if status.strip() == 'START':
                logs[job_id]['start_time'] = datetime.strptime(timestamp, '%H:%M:%S')
            elif status.strip() == 'END':
                logs[job_id]['end_time'] = datetime.strptime(timestamp, '%H:%M:%S')
                if 'start_time' in logs[job_id]:
                    logs[job_id]['duration'] = logs[job_id]['end_time'] - logs[job_id]['start_time']
    return logs

def calculate_durations(logs):
    """Calculates the duration of each job and generates warnings/errors."""
    for i in logs:
        if 'duration' in logs[i]:
            duration = logs[i]['duration']
            if duration > ERROR_THRESHOLD:
                print(f"ERROR: Job {logs[i]['job_name']} with PID {i} took {duration} (exceeds 10 minutes).")
            elif duration > WARNING_THRESHOLD:
                print(f"WARNING: Job {logs[i]['job_name']} with PID {i} took {duration} (exceeds 5 minutes).")
    
def main():
    logs =  parse_log_file(file_log_path)
    calculate_durations(logs)
    

if __name__ == '__main__':
    main()