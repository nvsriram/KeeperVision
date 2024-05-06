import json
import timeit
from datetime import datetime, timedelta

import requests

# url = 'https://sumanth0.pythonanywhere.com/api/predict'

# start = timeit.default_timer()

# # GET register
# url = "http://10.10.108.238:5000/api/register/example_username"
# data = {"username": "testuser@test.com"}
# r = requests.get(url)
# print(r.json())

# data = {"username": "example_username"}
# r = requests.get(url, json=data)
# print(r.json())

# # POST register
# data = {"email": "degea@gmail.com"}
# r = requests.post(url, json=data)
# print(r.json())

# data = {"username": "testuser2@test.com", "email": "testuser2@test.com"}
# r = requests.post(url, json=data)
# print(r.json())

# GET session
url = "https://sumanth0.pythonanywhere.com/api/session/buffon"
# data = {"username": "testuser@test.com"}
# r = requests.get(url)
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
data = {"session_stats": json.dumps(session_stats)}
inital = open("images/frame_1.jpg", "rb")
files = {
    "image": inital,
}
r = requests.post(url, files=files)
print(r.content)

# data = {"username": "testuser@test.com", "session_stats": json.dumps(session_stats)}
# r = requests.post(url, json=data)
# print(r.json())

# end = timeit.default_timer()
# print("Request time: ", end - start)