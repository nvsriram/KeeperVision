import json
import timeit
from datetime import datetime, timedelta

import requests

# url = 'http://10.10.131.14:5000/api/predict'

# start = timeit.default_timer()

# # GET register
# url = "http://10.6.4.220:5000/api/register"
# data = {"username": "testuser@test.com"}
# r = requests.get(url, json=data)
# print(r.json())

# data = {"usernamed": "example_username"}
# r = requests.get(url, json=data)
# print(r.json())

# # POST register
# data = {"username": "example_username", "email": "example@email.com"}
# r = requests.post(url, json=data)
# print(r.json())

# data = {"username": "testuser2@test.com", "email": "testuser2@test.com"}
# r = requests.post(url, json=data)
# print(r.json())

# GET session
url = "http://10.6.4.220:5000/api/session"
# data = {"username": "testuser@test.com"}
# r = requests.get(url, json=data)
# print(r.json())

# data = {"username": "example_username"}
# r = requests.get(url, json=data)
# print(r.json())

# POST session
session_stats = {
    "session_start": (datetime.now() - timedelta(minutes=75)).strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
    "session_end": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
    "f": 0,
    "b": 1,
    "l": 2,
    "r": 1,
    "fl": 0,
    "fr": 1,
    "bl": 2,
    "br": 3,
    "s": 5,
}
data = {"username": "example_username", "session_stats": json.dumps(session_stats)}
inital = open("runs/detect/predict/image0.jpg", "rb")
files = {
    "initial_image": inital,
    # "final_image": open("runs/detect/predict2/image0.jpg", "rb"),
}
r = requests.post(url, data=data, files=files)
print(r.json())

# data = {"username": "testuser@test.com", "session_stats": json.dumps(session_stats)}
# r = requests.post(url, json=data)
# print(r.json())

# end = timeit.default_timer()
# print("Request time: ", end - start)
