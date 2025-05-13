import unittest
from datetime import datetime, timedelta
from log_monitoring_app import parse_log_file, calculate_durations, WARNING_THRESHOLD, ERROR_THRESHOLD
import os

class TestLogMonitoringApp(unittest.TestCase):

    def setUp(self):
        """Set up sample log data for testing."""
        self.sample_logs = [
            ['11:35:23', 'scheduled task 032', 'START', '37980'],
            ['11:35:56', 'scheduled task 032', 'END', '37980'],
            ['11:36:11', 'scheduled task 796', 'START', '57672'],
            ['11:36:58', 'background job wmy', 'START', '81258'],
            ['11:44:44', 'background job wmy', 'END', '81258'],  # Exceeds 5 minutes
            ['11:37:14', 'scheduled task 515', 'START', '45135'],
            ['11:49:37', 'scheduled task 515', 'END', '45135'],  # Exceeds 10 minutes
        ]

    def test_parse_log_file(self):
        """Test parsing of log file and handling of missing data."""
        # Simulate writing the sample logs to a temporary file
        test_file_path = 'test_logs.csv'
        with open(test_file_path, 'w') as f:
            for log in self.sample_logs:
                f.write(','.join(log) + '\n')

        logs = parse_log_file(test_file_path)

        # Check if logs are parsed correctly
        self.assertIn('37980', logs)
        self.assertEqual(logs['37980']['job_name'], 'scheduled task 032')
        self.assertEqual(logs['37980']['start_time'], datetime.strptime('11:35:23', '%H:%M:%S'))
        self.assertEqual(logs['37980']['end_time'], datetime.strptime('11:35:56', '%H:%M:%S'))
        self.assertEqual(logs['37980']['duration'], timedelta(seconds=33))

        # Check for missing END entry
        self.assertIn('57672', logs)
        self.assertEqual(logs['57672']['job_name'], 'scheduled task 796')
        self.assertNotIn('end_time', logs['57672'])

        # Check for missing START entry
        self.assertIn('81258', logs)
        self.assertEqual(logs['81258']['job_name'], 'background job wmy')
        self.assertIn('start_time', logs['81258'])
        self.assertIn('end_time', logs['81258'])

        # Clean up the temporary file
        os.remove(test_file_path)

    def test_calculate_durations(self):
        """Test calculation of durations and warnings/errors."""
        logs = {
            '37980': {
                'job_name': 'scheduled task 032',
                'start_time': datetime.strptime('11:35:23', '%H:%M:%S'),
                'end_time': datetime.strptime('11:35:56', '%H:%M:%S'),
                'duration': timedelta(seconds=33),
            },
            '81258': {
                'job_name': 'background job wmy',
                'start_time': datetime.strptime('11:36:58', '%H:%M:%S'),
                'end_time': datetime.strptime('11:44:44', '%H:%M:%S'),
                'duration': timedelta(minutes=7, seconds=46),
            },
            '45135': {
                'job_name': 'scheduled task 515',
                'start_time': datetime.strptime('11:37:14', '%H:%M:%S'),
                'end_time': datetime.strptime('11:49:37', '%H:%M:%S'),
                'duration': timedelta(minutes=12, seconds=23),
            },
        }

        # Capture printed output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        calculate_durations(logs)

        # Restore stdout
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        # Check for warnings and errors in the output
        self.assertIn("WARNING: Job background job wmy with PID 81258 took 0:07:46 (exceeds 5 minutes).", output)
        self.assertIn("ERROR: Job scheduled task 515 with PID 45135 took 0:12:23 (exceeds 10 minutes).", output)
        self.assertNotIn("WARNING: Job scheduled task 032", output)

if __name__ == '__main__':
    unittest.main()