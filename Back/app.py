#### Welcome Script ####
print('Google Health Retool is running now')

#### Modules ####
from tracemalloc import start

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import getCredentials
import time as timer
from datetime import datetime, time, timedelta, timezone, date
#### app ####
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
#### main ####
@app.get("/steps/week")
def weekSteps():
    steps_url = "https://health.googleapis.com/v4/users/me/dataTypes/steps/dataPoints"

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=7)

    start_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    week_filterStr = (
        'steps.interval.start_time >= "{}" AND steps.interval.start_time < "{}"'.format(start_str,end_str)
    )
    week = {
        "monday": {
            "steps": 0
        },
        "tuesday": {
            "steps": 0
        },
        "wednesday": {
            "steps": 0
        },
        "thursday": {
            "steps": 0
        },
        "friday": {
            "steps": 0
        },
        "saturday": {
            "steps": 0
        },
        "sunday": {
            "steps": 0
        }
    }
    params = {
        "page_size": 100,
        "filter": week_filterStr
    }
    token = ''
    start = timer.perf_counter()
    while True:
        stepsData = stepsResponse(pageToken=token,url=steps_url,filter=week_filterStr)
        stepsRecords = stepsData.get('dataPoints', [])
        sumSteps_4dayOfweek(stepsRecords,weekObj = week)
        token = stepsData.get('nextPageToken')
        if not token:
                break
    print(week)
    print("Time taken to fetch and process steps data:", timer.perf_counter() - start, "seconds")
    return week

def stepsResponse(pageToken,url,filter):
    #### creds ####
    credentials = getCredentials()
    headers = {
        "Authorization": f"Bearer {credentials.token}"
    }
    response = requests.get(
        url,
        headers=headers,
        params={
            "page_size": 100,
            'filter': filter,
            'pageToken':pageToken
        }
    )
    response.raise_for_status()
    # print("Steps status:", response.status_code)
    return response.json()

def sumSteps_4dayOfweek(records,weekObj):
    for record in records:
        if record['dataSource']['platform'] != 'FITBIT':
            continue
        steps = record['steps']['count']
        dateData = record['steps']['interval']['civilEndTime']['date']
        dayOfweek = date(
            dateData['year'],
            dateData['month'],
            dateData['day']
        ).strftime('%A').lower()
        weekObj[dayOfweek]['steps'] += int(steps)

# print(stepsData.keys()) # ['dataPoints','nextPageToken']
#### stepsData['dataPoints'] one instance ####
# {
#     "dataSource": {
#         "recordingMethod": "PASSIVELY_MEASURED",
#         "device": {
#             "displayName": "Charge 6"
#         },
#         "platform": "FITBIT"
#     },

#     "steps": {
#         "interval": {
#             "startTime": "2026-08-15T02:03:00Z",
#             "startUtcOffset": "-14400s",

#             "endTime": "2026-08-15T02:04:00Z",
#             "endUtcOffset": "-14400s",

#             "civilStartTime": {
#                 "date": {
#                     "year": 2026,
#                     "month": 8,
#                     "day": 14
#                 },
#                 "time": {
#                     "hours": 22,
#                     "minutes": 3
#                 }
#             },

#             "civilEndTime": {
#                 "date": {
#                     "year": 2026,
#                     "month": 8,
#                     "day": 14
#                 },
#                 "time": {
#                     "hours": 22,
#                     "minutes": 4
#                 }
#             }
#         },

#         "count": "6"
#     }
# }
# weekSteps() #-main call