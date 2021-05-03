import requests
import datetime
import json
import pytz
import random 
from collections import OrderedDict

#INSTALL pytz,requests module before running this script (Commands Given Below)
#pip install requests
#pip install pytz

headers_list = [
    # Chrome 90 Windows
    {
        'authority': 'cdn-api.co-vin.in',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '^\\^',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-IN,en;q=0.9',
        'if-none-match': 'W/^\\^891-mfzfdA0Hj6vMmtX5I878Me/px+4^\\^',
    },
    # Chrome 90 Mac
    {
        'authority': 'cdn-api.co-vin.in',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'accept': 'application/json, text/plain, /',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'origin': 'https://www.cowin.gov.in',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.cowin.gov.in/',
        'accept-language': 'en-US,en;q=0.9',
        'if-none-match': 'W/"d29-7GrD1F7qDTsS2AtKr5e7BH1FPrY"',
    },
    # Firefox Windows
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'If-None-Match': 'W/891-mfzfdA0Hj6vMmtX5I878Me/px+4',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers',
    },
    # Safari Chrome
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
        'Accept-Language': 'en-us',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'br, gzip, deflate',
        'Host': 'cdn-api.co-vin.in',
    }
]

ordered_headers_list = []
for headers in headers_list:
    h = OrderedDict()
    for header,value in headers.items():
        h[header]=value
    ordered_headers_list.append(h)

    
IST = pytz.timezone('Asia/Kolkata')
a_date = datetime.datetime.now(IST)
print("========= SEARCHING STARTED AT : ",a_date.strftime("%m/%d/%Y, %H:%M:%S"),"=========\n")
date_1 = a_date.strftime('%d-%m-%Y')

date_2 = a_date + datetime.timedelta(7)
date_2 = date_2.strftime('%d-%m-%Y')
date_3 = a_date + datetime.timedelta(14)
date_3 = date_3.strftime('%d-%m-%Y')
dates = []
for i in range(0,7):
    new_date = a_date + datetime.timedelta(i)
    new_date = new_date.strftime('%d-%m-%Y')
    dates.append(new_date)

dist_id = [294,265,276] #Fill your district id (You can find the id's in 'District-ID' folder),
urls = []
for did in dist_id:
    for date in dates:   
        urls.append(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={did}&date={date}")

fetched_all_data = []
for u in urls:
    try:
        headers = random.choice(headers_list)
        r = requests.Session()
        r.headers = headers
        response = r.get(u)
        data = {}
        data=response.json()
        for session in data['sessions']:
            if session['min_age_limit']==18 and session['available_capacity']>0:
                new_dict = {}
                new_dict['CENTRE_NAME'] = session['name']
                new_dict['CENTRE_ID'] = session['center_id']
                new_dict['DISTRICT'] = session['district_name']
                new_dict['PINCODE'] = session['pincode']
                new_dict['AVAILABLE_DOSES'] = session['available_capacity']
                new_dict['DATE'] = session['date']
                new_dict['VACCINE'] = session['vaccine']
                fetched_all_data.append(new_dict)
    except:
        print("ERROR IN URL : ",u)
        continue
        

for fetched_data in fetched_all_data:
    print("Vaccine available at center: ",fetched_data['CENTRE_NAME'],"on",fetched_data['DATE'])
    print("Total doses avaiable: ",fetched_data['AVAILABLE_DOSES'])
    print("Centre pincode: ",fetched_data['PINCODE'],"\n")

if not fetched_all_data:
    print("NO VACCINE AVAILABLE")

