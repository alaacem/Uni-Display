import requests

# Define the URL
URL = 'http://127.0.0.1:7296/API/DEVICES/'

# Define the headers
HEADERS = {
    'Content-Type': 'text/plain;charset=UTF-8',
    'Accept': '*/*'
}

# Define the payload
DATA = {
    "cmd": "api_code",
    "session": 1,
    "method": "write",
    "cmd_code": 16,
    "data": [
        {
            "code": 0,
            "number": 0,  # Key number 1
            "values": [0, 0, 0, 255, 0, 0, 0, 0]  # Color values for key number 1
        },
        {
            "code": 0,
            "number": 2,  # Key number 2
            "values": [255, 0, 0, 255, 0, 0, 0, 0]  # Color values for key number 2
        }
    ]
}

# Make the POST request
response = requests.post(URL, json=DATA, headers=HEADERS)

# Check the response
if response.status_code == 200:
    print("RGB color set successfully!")
else:
    print("Failed to set RGB color:", response.text)
