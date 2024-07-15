#!/usr/bin/env python3

"""
This script fetches information about scheduled power outages for a specific account number
from an API endpoint. It checks if there's a scheduled or possible power outage expected
within the next 15 minutes and alerts the user via macOS speech synthesis.

Usage:
    python script_name.py <accountNumber>

Requirements:
    - Python 3.x requests library (install via `pip install requests`)

The script performs the following steps:
1. Validates command line arguments to ensure correct usage.
2. Sends a POST request to an API endpoint with the account number to retrieve outage data.
3. Parses the JSON response to extract outage schedule information.
4. Defines a function to check if a scheduled or possible outage is expected soon.
5. Alerts the user using macOS `say` command if an outage is expected within 15 minutes.

Notes:
- The script requires a valid 8-digit account number as a command line argument.
- It uses macOS specific commands (`say`) for audio alerts.
- It handles JSON decoding errors and HTTP 404 errors from the API gracefully.
- Be attentive hoursList start from 1 and go to 24 (python's datetime expected 0..23)
- Electricity statuses: 0 - Power, 1 - Scheduled Power Outage, 2 - Possible Power Outage but if we have 1 after 0 it be with no power too ;)

Example of response:
{
  "current": {
    "note": "За вказаним особовим рахунком '00000000' споживач підпадає під чергу '5.2' Графіку погодинних вимкнень(ГПВ)",
    "hasQueue": "yes",
    "subqueue": 2,
    "queue": 5
  },
  "graphs": {
    "today": {
      "scheduleApprovedSince": "10-07-2024 19:18",
      "hoursList": [
        {
          "hour": "1",
          "electricity": 0
        },
        {
          "hour": "2",
          "electricity": 0
        },
        {
          "hour": "3",
          "electricity": 1
        },
        {
          "hour": "4",
          "electricity": 1
        },
        {
          "hour": "5",
          "electricity": 1
        },
        {
          "hour": "6",
          "electricity": 1
        },
        {
          "hour": "7",
          "electricity": 0
        },
        {
          "hour": "8",
          "electricity": 0
        },
        {
          "hour": "9",
          "electricity": 0
        },
        {
          "hour": "10",
          "electricity": 0
        },
        {
          "hour": "11",
          "electricity": 1
        },
        {
          "hour": "12",
          "electricity": 1
        },
        {
          "hour": "13",
          "electricity": 1
        },
        {
          "hour": "14",
          "electricity": 1
        },
        {
          "hour": "15",
          "electricity": 1
        },
        {
          "hour": "16",
          "electricity": 0
        },
        {
          "hour": "17",
          "electricity": 0
        },
        {
          "hour": "18",
          "electricity": 0
        },
        {
          "hour": "19",
          "electricity": 1
        },
        {
          "hour": "20",
          "electricity": 1
        },
        {
          "hour": "21",
          "electricity": 1
        },
        {
          "hour": "22",
          "electricity": 1
        },
        {
          "hour": "23",
          "electricity": 0
        },
        {
          "hour": "24",
          "electricity": 0
        }
      ],
      "eventDate": "2024-07-11"
    }
  },
  "showFutureDateUntil": "01.05.2023"
}
"""

import requests
import json
import sys
import re
import subprocess
from datetime import datetime, timedelta

def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <accountNumber>")

    account_number = sys.argv[1]
    valid_account_number = re.compile(r'^\d{8}$')

    if not valid_account_number.match(account_number):
        sys.exit("Invalid account number. It must be exactly 8 digits.")

    url = "https://svitlo.oe.if.ua/GAVTurnOff/GavGroupByAccountNumber"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Accept-Language": "en-GB,en;q=0.9",
        "Cache-Control": "no-cache",
        "Sec-Fetch-Mode": "cors",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://svitlo.oe.if.ua",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Referer": "https://svitlo.oe.if.ua/",
        "Connection": "keep-alive",
        "Host": "svitlo.oe.if.ua",
        "Sec-Fetch-Dest": "empty",
        "X-Requested-With": "XMLHttpRequest"
    }
    payload = f"accountNumber={account_number}&userSearchChoice=pob&address="

    response = requests.post(url, headers=headers, data=payload)

    # Check for 404 response
    if response.status_code == 404:
        sys.exit(f"Error: The account number {account_number} is incorrect.")

    # Parse the JSON response
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError as e:
        sys.exit(f"Error parsing JSON response: {e}")

    def macos_say(message):
        # You can use any other voice model. The clearest voice I found in "Samantha"
        subprocess.call(["/usr/bin/say", "-v", "Bahh", "--quality", "127", "-i", message])

    def check_outage(schedule):
        current_time = datetime.now()
        current_hour = (current_time.hour + 1) % 24
        warning_hour = (current_hour + 1) % 24

        current_status = schedule["today"]["hoursList"][current_hour]["electricity"]
        warning_status = schedule["today"]["hoursList"][warning_hour]["electricity"]

        print(f"Current status: {current_status}")
        print(f"Warning status: {current_status}")

        if current_status == 0:
            if warning_status == 1:
                return "A scheduled power outage is expected in 15 minutes"
            elif warning_status == 2:
                return "A possible power outage is expected in 15 minutes"

        return None

    outage_message = check_outage(data['graphs'])

    if outage_message:
        macos_say(outage_message)
        sys.exit()

if __name__ == "__main__":
    main()

