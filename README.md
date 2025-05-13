# Log Monitoring Application

This is a Python application for monitoring and analyzing log files. It parses a log file, calculates the duration of each job, and generates warnings or errors if the processing time exceeds certain thresholds.

## Features

- Parses a CSV log file.
- Tracks the start and end times of jobs.
- Calculates the duration of each job.
- Logs a **warning** if a job takes longer than 5 minutes.
- Logs an **error** if a job takes longer than 10 minutes.

## Github Actions
- the project contains automatic triggered when pushing to the master branch - unit testing for the functions created and linting using the black formater

## Requirements

- Python 3.10 or higher
- `pip` for managing dependencies

   
