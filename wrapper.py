
import os
import subprocess
import json
import pymongo
import random
import time
from pymongo import MongoClient

os.chdir("/action")
log = open("log.txt", 'w')
error = open('error.txt', 'w')
process = subprocess.Popen("/usr/bin/Rscript code.R", shell=True, stdout=log, stderr=error)
process.wait()
client = MongoClient(
        db_ip, 
        db_port,
        username=db_username,
        password=db_password,
        authSource=db_source)
db = client.EcoForecastTest
results = db.results
log.close()
error.close()
log = open('log.txt', 'r')
error = open('error.txt', 'r')
if os.path.isfile("/action/out.json"):
    with open('/action/out.json') as f:
        data = json.load(f)
        io = {"stdout": log.read(), "stderr": error.read()}
        result = {"data": data, "logs": io}
        print(json.dumps(result))
else:
    result = {"stdout": log.read(), "stderr": error.read()}
    print(json.dumps(result))

log.close()
error.close()

result_data = {
    'user_id': user_id,
    'transaction_id': transaction_id,
    'time': time.asctime(),
    'result': result,
    'model_name': model_name,
    'interval' : interval,
    'stop_date': stop_date
}
results.insert_one(result_data)