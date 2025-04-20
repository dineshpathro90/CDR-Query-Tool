#!/usr/bin/env python3

import subprocess
import sys
from datetime import datetime
from tabulate import tabulate
from colorama import init, Fore, Style

# Initialize colorama
init()

class AndroidCDR:
    def __init__(self):
        self.adb_path = "adb"
        self.device_connected = False
        self.check_adb()

    def check_adb(self):
        """Check if ADB is available and device is connected."""
        try:
            result = subprocess.run([self.adb_path, "devices"], 
                                  capture_output=True, 
                                  text=True)
            if "device" in result.stdout:
                self.device_connected = True
                print(f"{Fore.GREEN}✓ Device connected{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ No device connected{Style.RESET_ALL}")
                sys.exit(1)
        except FileNotFoundError:
            print(f"{Fore.RED}✗ ADB not found. Please ensure Android SDK is installed and ADB is in your PATH{Style.RESET_ALL}")
            sys.exit(1)

    def query_call_logs(self):
        """Query call logs from the Android device."""
        # Base content query
        content_query = "content query --uri content://call_log/calls"
        
        # Add projection for specific columns
        projection = " --projection _id,number,date,duration,type,name"
        
        # Build the query
        query = f"{self.adb_path} shell {content_query}{projection}"
        
        try:
            result = subprocess.run(query.split(), 
                                  capture_output=True, 
                                  text=True)
            
            if result.returncode != 0:
                print(f"{Fore.RED}Error querying call logs: {result.stderr}{Style.RESET_ALL}")
                return []
            
            return self.parse_call_logs(result.stdout)
            
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
            return []

    def parse_call_logs(self, raw_logs):
        """Parse call logs."""
        logs = []
        current_record = {}
        
        for line in raw_logs.split('\n'):
            if 'Row:' in line:
                if current_record:
                    logs.append(current_record)
                current_record = {}
            elif '=' in line:
                key, value = line.strip().split('=', 1)
                current_record[key.strip()] = value.strip()
        
        # Add the last record if it exists
        if current_record:
            logs.append(current_record)
            
        return logs

    def format_call_type(self, call_type):
        """Format call type for display."""
        call_types = {
            '1': f"{Fore.GREEN}Outgoing{Style.RESET_ALL}",
            '2': f"{Fore.BLUE}Incoming{Style.RESET_ALL}",
            '3': f"{Fore.RED}Missed{Style.RESET_ALL}",
            '4': f"{Fore.YELLOW}Voicemail{Style.RESET_ALL}",
            '5': f"{Fore.CYAN}Rejected{Style.RESET_ALL}",
            '6': f"{Fore.MAGENTA}Blocked{Style.RESET_ALL}"
        }
        return call_types.get(call_type, call_type)

    def format_duration(self, duration):
        """Format duration in seconds to HH:MM:SS."""
        try:
            seconds = int(duration)
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except (ValueError, TypeError):
            return "00:00:00"

    def display_results(self, logs):
        """Display results in a formatted table."""
        if not logs:
            print(f"{Fore.YELLOW}No call logs found{Style.RESET_ALL}")
            return

        # Prepare data for tabulate
        table_data = []
        headers = ["Date", "Number", "Type", "Duration", "Name"]
        
        for log in logs:
            call_date = datetime.fromtimestamp(int(log.get('date', 0)) / 1000)
            row = [
                call_date.strftime("%Y-%m-%d %H:%M:%S"),
                log.get('number', 'Unknown'),
                self.format_call_type(log.get('type', 'Unknown')),
                self.format_duration(log.get('duration', 0)),
                log.get('name', 'Unknown')
            ]
            table_data.append(row)

        # Display table
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

def main():
    cdr = AndroidCDR()
    logs = cdr.query_call_logs()
    cdr.display_results(logs)

if __name__ == "__main__":
    main() 