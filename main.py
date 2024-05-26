import json
import os
import time
from pathlib import Path
import datetime


import requests

import

while True:

    try:
        print('in try')
        baseurl = "https://www.nseindia.com/"
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) '
                                 'Chrome/80.0.3987.149 Safari/537.36',
                   'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
        session = requests.Session()
        request = session.get(baseurl, headers=headers)
        cookies = dict(request.cookies)
        response = session.get(url, headers=headers, cookies=cookies)
        FileName = str(response.json()["records"]["timestamp"]).replace(" ", "").replace(":", "")
        FolderName = str(response.json()["records"]["timestamp"])[0:11]
        FolderPath = Path('C:\\Users\\sushi\\Desktop\\BankNifty\\', FolderName)
        FolderPath.mkdir(parents=True, exist_ok=True)
        file = os.path.join(FolderPath, FileName)

        with open(file, 'a', newline='') as f:
            json.dump(response.json(), f, ensure_ascii=False)

        # Replace the placeholder with your Atlas connection string
        uri = "mongodb://localhost:27017"

        # Set the Stable API version when creating a new client
        client = MongoClient(uri)

        BankNiftyOI = client.BankNifty.BankNiftyOI
        NewOIMessage = {
            "_id": str(response.json()["records"]["timestamp"]),
            "MessageDump": response.json()
        }

        now = datetime.datetime.now().time()
        if now.hour >= 15 and now.minute >= 30:
            exit(0)

        BankNiftyOI.update_one({'_id': NewOIMessage['_id']}, {"$set": NewOIMessage}, upsert=True)
        time.sleep(300)
    except Exception as e:
        print(e.__repr__())
