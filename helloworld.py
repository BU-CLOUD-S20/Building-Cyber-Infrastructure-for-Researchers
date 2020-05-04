import requests
from urllib3.exceptions import InsecureRequestWarning
import json


def helloworld():
    url = "http://128.31.25.50/api/v1/namespaces/_/actions/helloPy?blocking=true&result=false"
    payload = "{\"name\":\"World\"}"
    headers = {
        'Authorization': 'Basic MjNiYzQ2YjEtNzFmNi00ZWQ1LThjNTQtODE2YWE0ZjhjNTAyOjEyM3pPM3haQ0xyTU42djJCS0sxZFhZRnBYbFBrY2NPRnFtMTJDZEFzTWdSVTRWck5aOWx5R1ZDR3VNREdJd1A=',
        'Content-Type': 'application/json'
    }
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(response.text.encode('utf8'))
    return response.json()
    # return response.text.encode('utf8')


def create(name,payload):
    url = "https://128.31.25.50/api/v1/namespaces/_/actions/"+name+"?overwrite=false"
    payload=format(name,payload)
    headers = {
        'Authorization': 'Basic MjNiYzQ2YjEtNzFmNi00ZWQ1LThjNTQtODE2YWE0ZjhjNTAyOjEyM3pPM3haQ0xyTU42djJCS0sxZFhZRnBYbFBrY2NPRnFtMTJDZEFzTWdSVTRWck5aOWx5R1ZDR3VNREdJd1A=',
        'Content-Type': 'application/json',
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
    print(response.text.encode('utf8'))
    return True


def invoke(name,payload):
    url = "http://128.31.25.50/api/v1/namespaces/_/actions/"+name+"?blocking=true&result=false"
    payload = "{\"name\":\"World\"}"
    headers = {
        'Authorization': 'Basic MjNiYzQ2YjEtNzFmNi00ZWQ1LThjNTQtODE2YWE0ZjhjNTAyOjEyM3pPM3haQ0xyTU42djJCS0sxZFhZRnBYbFBrY2NPRnFtMTJDZEFzTWdSVTRWck5aOWx5R1ZDR3VNREdJd1A=',
        'Content-Type': 'application/json'
    }
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(response.text.encode('utf8'))
    return response.json()


def update(name,payload):
    url = "https://128.31.25.50/api/v1/namespaces/_/actio0ns/"+name+"?overwrite=true"
    payload = format(name, payload)
    headers = {
        'Authorization': 'Basic MjNiYzQ2YjEtNzFmNi00ZWQ1LThjNTQtODE2YWE0ZjhjNTAyOjEyM3pPM3haQ0xyTU42djJCS0sxZFhZRnBYbFBrY2NPRnFtMTJDZEFzTWdSVTRWck5aOWx5R1ZDR3VNREdJd1A=',
        'Content-Type': 'application/json',
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
    print(response.text.encode('utf8'))
    return True


def format(name,code):
    new_entry = {
                "namespace": "_",
                "name": name,
                "exec": {
                    "kind": "python:default",
                    "code": code
                    }
                }
    return json.dumps(new_entry)


if __name__ == "__main__":
    helloworld()
