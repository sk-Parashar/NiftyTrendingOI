# Libraries
import requests
import json
import math
import pandas as pd


# Method to get nearest strikes
def round_nearest(x, num=50): return int(math.ceil(float(x) / num) * num)


def nearest_strike_bnf(x): return round_nearest(x, 100)


def nearest_strike_nf(x): return round_nearest(x, 50)


# Urls for fetching Data
url_oc = "https://www.nseindia.com/option-chain"
url_bnf = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_nf = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
url_indices = "https://www.nseindia.com/api/allIndices"

# Headers
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'accept-language': 'en,gu;q=0.9,hi;q=0.8',
    'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()


# Local methods
def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)


def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if (response.status_code == 401):
        set_cookie()
        response = sess.get(url_nf, headers=headers, timeout=5, cookies=cookies)
    if (response.status_code == 200):
        return response.text
    return ""


def set_header():
    global bnf_ul
    global nf_ul
    global bnf_nearest
    global nf_nearest
    response_text = get_data(url_indices)
    data = json.loads(response_text)
    for index in data["data"]:
        if index["index"] == "NIFTY 50":
            nf_ul = index["last"]
            print("nifty")
        if index["index"] == "NIFTY BANK":
            bnf_ul = index["last"]
            print("banknifty")
    bnf_nearest = nearest_strike_bnf(bnf_ul)
    nf_nearest = nearest_strike_nf(nf_ul)


# Showing Header in structured format with Last Price and Nearest Strike


# Fetching CE and PE data based on Nearest Expiry Date
def request_oi(url):
    global df
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            new_row = {'Time': str(data["records"]["timestamp"])[0:17],
                       'StrikePrice':item["strikePrice"],
                       'CECOi':item["CE"]["changeinOpenInterest"],
                       'PECOI':item["PE"]["changeinOpenInterest"]
                       }

            df.loc[len(df)] = new_row
            # print(new_row)
            # OIList.append(
            #     [str(data["records"]["timestamp"])[0:17], item["strikePrice"], item["CE"]["changeinOpenInterest"],
            #      item["PE"]["changeinOpenInterest"]])

            # print(OIList)
            # OIDF = pd.DataFrame(OIDict)
            # print(data["records"]["timestamp"], item["strikePrice"], item["c"]["changeinOpenInterest"],
            #       item["PE"]["changeinOpenInterest"])


OIDict = {
    'Time': [],
    'StrikePrice': [],
    'CECOi': [],
    'PECOI': []
}

df = pd.DataFrame(OIDict)

while True:
    try:
        request_oi(url_nf)
        print(df)
    except Exception as e:
        print(e.__repr__())
