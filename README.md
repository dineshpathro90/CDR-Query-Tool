# Android CDR Query Tool

A command-line tool to query and filter Android call logs using ADB.

## Prerequisites

- Python 3.6 or higher
- Android SDK with ADB installed and in your PATH
- An Android device connected via USB with USB debugging enabled

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Basic usage:
```bash
python android_cdr.py
```

Filter by phone number:
```bash
python android_cdr.py -n "+1234567890"
```

Filter by date range:
```bash
python android_cdr.py -s "2024-01-01" -e "2024-12-31"
```

Filter by both phone number and date range:
```bash
python android_cdr.py -n "+1234567890" -s "2024-01-01" -e "2024-12-31"
```

Save results to CSV:
```bash
python android_cdr.py -n "+1234567890" -o "call_logs.csv"
```

## Command Line Arguments

- `-n, --number`: Phone number to filter (e.g., +1234567890)
- `-s, --start-date`: Start date in YYYY-MM-DD format
- `-e, --end-date`: End date in YYYY-MM-DD format
- `-o, --output`: Output file name for CSV export

## Output Format

The tool displays call logs in a table format with the following columns:
- Date: Call date and time
- Number: Phone number
- Type: Call type (color-coded)
  - Green: Outgoing
  - Blue: Incoming
  - Red: Missed
  - Yellow: Voicemail
  - Cyan: Rejected
  - Magenta: Blocked
- Duration: Call duration in HH:MM:SS format
- Name: Contact name (if available)

## Notes

- Make sure your Android device is connected and USB debugging is enabled
- The tool requires ADB to be installed and accessible from the command line
- Date filtering is inclusive of both start and end dates
- If no phone number is specified, all call logs will be displayed 