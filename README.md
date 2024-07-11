# Check Power

This script fetches information about scheduled power outages for a specific account number
from an API endpoint. It checks if there's a scheduled or possible power outage expected
within the next 15 minutes and alerts the user via macOS speech synthesis.

## Usage

Manual run

```bash
python check_power.py <accountNumber>
```

Cron

```bash
*/15 * * * * /path/to/check_power.py <accountNumber>
```

## Requirements:
    - Python 3.x requests library (install via `pip install requests`)

## Description

The script performs the following steps:

1. Validates command line arguments to ensure correct usage.
2. Sends a POST request to an API endpoint with the account number to retrieve outage data.
3. Parses the JSON response to extract outage schedule information.
4. Defines a function to check if a scheduled or possible outage is expected soon.
5. Alerts the user using macOS `say` command if an outage is expected within 15 minutes.

## Notes

- The script requires a valid 8-digit account number as a command line argument.
- It uses macOS specific commands (`say`) for audio alerts.
- It handles JSON decoding errors and HTTP 404 errors from the API gracefully.
- Be attentive hoursList start from 1 and go to 24 (python's datetime expected 0..23)
- Electricity statuses: 0 - Power, 1 - Scheduled Power Outage, 2 - Possible Power Outage
- You can also use graphs -> tomorrow if it available

## Example of API response:

```json
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
```
