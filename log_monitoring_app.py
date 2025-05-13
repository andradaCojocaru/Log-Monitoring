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
    logs = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            timestamp, job_name, status, job_id = row
            logs.append({
                'timestamp': datetime.strptime(timestamp, '%H:%M:%S'),
                'job_name': job_name,
                'status': status,
                'job_id': job_id
            })
    return logs

def main():
    logs =  parse_log_file(file_log_path)
    print("Logs entries:")
    for log in logs:
        print(log)

if __name__ == '__main__':
    main()