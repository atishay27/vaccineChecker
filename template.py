import requests
import datetime
import json
import pytz
import random
import sys
from collections import OrderedDict
from time import sleep
#logFile = open("cron.log", "at")
# {chat-id:[{},{}]}
#python template.py 4 1 141 4,4,4,4,4
def writeLog(*txts):
    #with open("/home/ubuntu/vacify/script/cron.log", "at") as logFile:
    with open("cron.log", "at") as logFile:
        for txt in txts:
            logFile.write(str(txt))
            logFile.write(" ")
        logFile.write("\n")

def checkMessage(counter,teleGroup):
    if teleGroup in [0,1,2,3,4] and commFrequency[teleGroup]!=0 and counter%commFrequency[teleGroup]==0:
        return True
    else:
        return False

def increment_bot_counter():
    global bot_counter
    global total_bots
    if bot_counter==total_bots-1:
      bot_counter = 0
    else:
      bot_counter += 1
    
def genMessage(session,telURL,avalDoses,ageGroup,dose,counter,teleGroup,chat_id,fetched_all_data):
    if not checkMessage(counter,teleGroup):
        return
    #writeLog("INSIDE SEND MESSAGE",session)
    new_dict = {}
    telegram = ""
    new_dict['CENTRE_NAME'] = session['name']
    new_dict['CENTRE_ID'] = session['center_id']
    new_dict['DISTRICT'] = session['district_name']
    new_dict['PINCODE'] = session['pincode']
    new_dict['AVAILABLE_DOSES'] = avalDoses
    new_dict['DATE'] = session['date']
    new_dict['VACCINE'] = session['vaccine']
    new_dict['AGE_GROUP'] = str(ageGroup)
    new_dict['DOSE'] = str(dose)
    #writeLog("NEW_DICT: ",new_dict)
    if chat_id in fetched_all_data:
        fetched_all_data[chat_id].append(new_dict)
    else:
        fetched_all_data[chat_id] = []
        fetched_all_data[chat_id].append(new_dict)

    # telegram += str(new_dict['PINCODE']) + "\n"
    # telegram += str(new_dict['AVAILABLE_DOSES']) + " slots available on "
    # telegram += str(new_dict['DATE']) + "\n\n"
    # telegram += str(new_dict['CENTRE_NAME']) + "\n"
    # telegram += str(new_dict['DISTRICT']) + "\n"
    # telegram += "Age: " + str(ageGroup) + "\n"
    # telegram += "Vaccine: " + str(new_dict['VACCINE']) + "\n"
    # telegram += "Dose: " + str(dose) + "\n\n"
    # telegram += "Register Now at: https://selfregistration.cowin.gov.in/"
    # r = requests.Session()
    # telURL = telURL + telegram
    # telResp = r.get(telURL)


def sendMessage(fetched_all_data):
    global bot_counter
    for chat_id in fetched_all_data:
        writeLog("FOR CHAT_ID: ",chat_id)
        # if len(fetched_all_data[chat_id]) > 25:
        #     writeLog("MORE THEN 25 CENTRES FOUND\n")
        #     continue
        message = ""
        writeLog("TOTAL CENTRES FOUND: ",len(fetched_all_data[chat_id]))
        for each_centre in fetched_all_data[chat_id]:
            message += str(each_centre['PINCODE']) + " ("
            message += str(each_centre['AVAILABLE_DOSES']) + " Slot"
            if each_centre['DOSE'] == "1":
                message += " - " + each_centre['VACCINE']
            message += ")\n"
            message += "Available on " + str(each_centre['DATE']) + "\n"
            message += str(each_centre['DISTRICT']) + "\n"
            message += str(each_centre['CENTRE_NAME']) + "\n"
            message += "===================\n\n"
        for additional_info in chat_id_info[chat_id]:
            message += additional_info + "\n"
        message += "Register Now at: https://selfregistration.cowin.gov.in/"
        writeLog(f"=== MESSAGE FOR CHAT-ID: {chat_id} ===\n")
        writeLog("\n==== MESSAGE STARTING ====\n")
        writeLog(message)
        writeLog("\n==== MESSAGE ENDING ======\n\n")
        bot_url = telUrls[bot_counter] + str(chat_id) + "&text="
        writeLog(f"MESSAGE WILL BE SEND VIA BOT URL: {bot_url}")
        # r = requests.Session()
        # bot_url = bot_url + message
        # telResp = r.get(bot_url)
        increment_bot_counter()
        #writeLog(each_centre,"\n")
        #writeLog("value: ",type(fetched_all_data[chat_id]))

    
def getVaccine(urls,IST,headers_list,counter):
    fetched_all_data = {}
    s_date = datetime.datetime.now(IST)
    writeLog("===============  START:",s_date.strftime("%d/%m/%Y %H:%M:%S"),"==================\n")
    for u in urls:
        try:
            headers = random.choice(headers_list)
            r = requests.Session()
            r.headers = headers
            response = r.get(u)
            print("REACHING HERE: ",response)
            data = {}
            data=response.json()
            #writeLog("\n",data,"\n\n")
            for session in data['sessions']:
                #18+
                #writeLog("\n",session,"\n")
                avalDose = 0
                avalDoses_1 = max(session['available_capacity']-session['available_capacity_dose2'],session['available_capacity_dose1'])
                avalDoses_2 = max(session['available_capacity']-session['available_capacity_dose1'],session['available_capacity_dose2'])
                #writeLog("=====================")
                #writeLog("SESSION: ",session,"\n")
                if session['min_age_limit']==18:
                    if avalDoses_1>0:
                        chat_id=-1001330575353
                        teleGroup = 0
                        doseType = 1
                        writeLog("FOUND A VACCINE FOR 18+ DOSE-1","\n")
                        telURL = "https://api.telegram.org/bot1780713361:AAHBh6Pum5EDcu7m5LZsLdmSgOHbKK0LAhg/sendMessage?chat_id=-1001330575353&text="
                        avalDose = avalDoses_1
                        genMessage(session,telURL,avalDose,"18 to 44",doseType,counter,teleGroup,chat_id,fetched_all_data)
                    if avalDoses_2>0:
                        doseType = 2
                        if session['vaccine']=="COVAXIN":
                            teleGroup = 1
                            chat_id=-1001378155509
                            writeLog("FOUND A VACCINE FOR 18+ DOSE-2 COVAXIN","\n")
                            avalDose = avalDoses_2
                            telURL = "https://api.telegram.org/bot1780713361:AAHBh6Pum5EDcu7m5LZsLdmSgOHbKK0LAhg/sendMessage?chat_id=-1001378155509&text="
                        elif session['vaccine']=="COVISHIELD":
                            writeLog("FOUND A VACCINE FOR 18+ DOSE-2 COVISHIELD","\n")
                            continue
                            #teleGroup = 0
                            #telURL = "https://api.telegram.org/bot1780713361:AAHBh6Pum5EDcu7m5LZsLdmSgOHbKK0LAhg/sendMessage?chat_id=-1001330575353&text="
                        else:
                            #teleGroup = 2
                            writeLog("FOUND A VACCINE FOR 18+ DOSE-2 UNDEFINED DOSE","\n")
                            continue
                        genMessage(session,telURL,avalDose,"18 to 44",doseType,counter,teleGroup,chat_id,fetched_all_data)
                #45+
                elif session['min_age_limit']==45:
                    if avalDoses_1>0:
                        teleGroup = 2
                        doseType = 1
                        chat_id=-1001305707080
                        writeLog("FOUND A VACCINE FOR 45+ DOSE-1","\n")
                        telURL = "https://api.telegram.org/bot1778212262:AAHPxXzkj28DJo4XbmEJ4MsVuDSBT2h08tw/sendMessage?chat_id=-1001305707080&text="
                        avalDose = avalDoses_1
                        genMessage(session,telURL,avalDose,"45",doseType,counter,teleGroup,chat_id,fetched_all_data)
                    if avalDoses_2>0:
                        doseType = 2
                        avalDose = avalDoses_2
                        if session['vaccine']=="COVAXIN":
                            teleGroup = 3
                            chat_id=-1001414478856
                            writeLog("FOUND A VACCINE FOR 45+ DOSE-2 COVAXIN DOSE","\n")
                            telURL = "https://api.telegram.org/bot1778212262:AAHPxXzkj28DJo4XbmEJ4MsVuDSBT2h08tw/sendMessage?chat_id=-1001414478856&text="
                        elif session['vaccine']=="COVISHIELD":
                            teleGroup = 4
                            chat_id=-1001329655614
                            writeLog("FOUND A VACCINE FOR 45+ DOSE-2 COVISHIELD DOSE","\n")
                            telURL = "https://api.telegram.org/bot1778212262:AAHPxXzkj28DJo4XbmEJ4MsVuDSBT2h08tw/sendMessage?chat_id=-1001329655614&text="
                        else:
                            writeLog("FOUND A VACCINE FOR 45+ DOSE-2 UNDEFINED DOSE","\n")
                            continue
                        genMessage(session,telURL,avalDose,"45",doseType,counter,teleGroup,chat_id,fetched_all_data)
        except Exception as e:
            writeLog("ERROR IN URL : ",u)
            writeLog(e)
            continue
    #writeLog(fetched_all_data)
    writeLog("GOING TO SEND MESSAGE\n")
    sendMessage(fetched_all_data)
    e_date = datetime.datetime.now(IST)       
    writeLog("\n===============    END:",e_date.strftime("%d/%m/%Y %H:%M:%S"),"==================\n\n\n\n")
    return (e_date-s_date)

chat_id_info = {
    -1001330575353:["AGE GROUP: 18 to 44","DOSE-1"],
    -1001378155509:["AGE GROUP: 18 to 44","DOSE-2","COVAXIN"],
    -1001305707080:["AGE GROUP: 45 and above","DOSE-1"],
    -1001414478856:["AGE GROUP: 45 and above","DOSE-2","COVAXIN"],
    -1001329655614:["AGE GROUP: 45 and above","DOSE-2","COVISHIELD"]
}
bot_counter = 0
total_bots = 2
telUrls = [
    "https://api.telegram.org/bot1780713361:AAHBh6Pum5EDcu7m5LZsLdmSgOHbKK0LAhg/sendMessage?chat_id=",
    "https://api.telegram.org/bot1778212262:AAHPxXzkj28DJo4XbmEJ4MsVuDSBT2h08tw/sendMessage?chat_id=",
]
# This data was created by using the curl method explained above
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
# Create ordered dict from Headers above
ordered_headers_list = []
for headers in headers_list:
    h = OrderedDict()
    for header,value in headers.items():
        h[header]=value
    ordered_headers_list.append(h)

count = 1    
IST = pytz.timezone('Asia/Kolkata')
a_date = datetime.datetime.now(IST)
dates = []
start_date = int(sys.argv[2])
end_date = start_date+1
today3pm = a_date.replace(hour=15, minute=0, second=0, microsecond=0)
if a_date > today3pm:
    start_date += 1
    end_date += 1
for i in range(start_date,end_date):
    new_date = a_date + datetime.timedelta(i)
    new_date = new_date.strftime('%d-%m-%Y')
    dates.append(new_date)

dist_id = [int(sys.argv[3])] #294,294,274,195
urls = []
for did in dist_id:
    for date in dates:
        urls.append(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={did}&date={date}")
#urls.append(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=294&date=15-05-2021")
#urls.append(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=294&date=15-05-2021")

writeLog(urls)
#print(urls)
sleepTime = int(sys.argv[1])
commFrequency = sys.argv[4].strip('}{').split(',')
commFrequency = [int(x) for x in commFrequency]
for x in commFrequency:
   if x%sleepTime!=0:
      writeLog("ARGUMENT ERROR")
      exit()
counter = 0
endLoop =   4//sleepTime
for i in range(0,endLoop):

    writeLog(f"COUNT: {i+1}")
    elapsedTime = getVaccine(urls,IST,headers_list,counter)
    getSleep = str(elapsedTime).split(":")
    getSleep = max(float(sleepTime)-float(getSleep[2]),0)
    print(getSleep,type(getSleep))
    sleep(getSleep)
    counter += sleepTime


#logFile.close()

