# Finding_Website_Pages-Cpanel
Educational Python tool to help website owners identify exposed admin panels for ethical security testing.

# Admin Panel Finder

An educational Python tool designed to help website owners identify exposed admin panels on their own websites for security testing purposes.

**WARNING**: This tool is for **ETHICAL TESTING ONLY**. Use it **ONLY** on websites you own or have explicit written permission to test. Unauthorized scanning is illegal under laws like the Computer Fraud and Abuse Act (CFAA). The author is not responsible for any misuse or damage caused by this tool.

## Features
- Scans for common admin panel URLs (e.g., `/admin`, `/login.php`).
- Uses multithreading for efficient scanning.
- Detects potential login pages based on keywords.
- Saves results to a text file for analysis.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Lovincebrave/Finding_Website_Pages-Cpanel.git
   cd Admin_list_finder

## Install dependencies
pip install requests colorama

## Run the script
python Admin_list_finder.py http://example.com -t 10
- Change it to any website you want to check 

## Usage
python Admin_list_finder.py <website_url> [-t <threads>]
- <website_url>: The URL of the website to scan (e.g., http://example.com).
- t <threads>: Number of threads for scanning (default: 10).
- Results are saved to admin_scan_results.txt.

## For any kind of help, support, suggetion and request ask in Telegram and Whatsapp
+2348108603409
LovinceBrave   







