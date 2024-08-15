import io
import sys
import requests
import datetime
import pandas as pd
#from twilio.rest import Client
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf8')


def lineNotifyMessage(msg):
    token = 'KOjU7cFm8lMz3aZxbnmkHh4w5laDFbLkyDKy7ZXyqqO' # 替換Line Notify Token
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    
    # Post 封包出去給 Line Notify
    r = requests.post(
        "https://notify-api.line.me/api/notify",
        headers = headers, 
        params = payload)
    return r.status_code


# def sendSms(smsText):
#     account_sid = "AC261e9fc43b45b15f156d94ff806b7002"
#     auth_token = "9b2ad81e1070ee909e6878391526c9aa"
#     client = Client(account_sid, auth_token)
#     # 傳送簡訊
#     message = client.messages.create( 
#     body = smsText,
#     from_ = "+16592224701",
#     to = "+886910017739")



def dist1_computerRoom():
    loc_dt = datetime.datetime.today()  #系統現在時間
    dt_file = loc_dt.strftime("%Y%m%d") #讀取csv檔名用變數
    read_file = pd.read_csv(fr'\\172.23.160.46\62181d2b\62181D2B_{dt_file}.csv', encoding = 'utf-8-sig')# 讀取路徑中的CSV檔案
    newist_data = read_file.iloc[-1].tolist() # 讀取CSV檔案中最後一筆資料
    limit = {"temp_upper":27, "temp_lower":15, "humid_upper":70, "humid_lower":30} # 溫濕度上下限
    overtemp = f"\n 時間紀錄:{newist_data[0]}\n 目前溫度:{newist_data[1]}°C已超過閥值，請注意!"
    lowertemp = f"\n 時間紀錄:{newist_data[0]}\n 目前溫度:{newist_data[1]}°C已低於閥值，請注意!"
    overhumid = f"\n 時間紀錄:{newist_data[0]}\n 目前濕度:{newist_data[2]}%已超過閥值，請注意!"
    lowerhumid = f"\n 時間紀錄:{newist_data[0]}\n 目前濕度:{newist_data[2]}%已低於閥值，請注意!"

    compareTemp = lambda x, y, z: overtemp if x > y else (lowertemp if x < z else None)
    compareHumid = lambda a, b, c: overhumid if a > b else (lowerhumid if a < c else None)

    #測試輸出
    #print(compareTemp(newist_data[1], limit["temp_upper"], limit["temp_lower"]))
    
    #Line通知
    lineNotifyMessage(compareTemp(newist_data[1], limit["temp_upper"], limit["temp_lower"]))
    lineNotifyMessage(compareHumid(newist_data[2], limit["humid_upper"], limit["humid_lower"]))

    # Line及手機簡訊通知
    # if newist_data[1] > limit["temp_upper"]:
    #     lineNotifyMessage(overtemp)
    #     #sendSms(overtemp)
    # if newist_data[1] < limit["temp_lower"]:
    #     lineNotifyMessage(lowertemp)
    #     #sendSms(lowertemp)
    # if newist_data[2] > limit["humid_upper"]:
    #     lineNotifyMessage(overhumid)
    #     #sendSms(overhumid)
    # if newist_data[2] < limit["humid_lower"]:
    #     lineNotifyMessage(lowerhumid)
    #     #sendSms(lowerhumid)


if __name__ == '__main__':
    dist1_computerRoom()
