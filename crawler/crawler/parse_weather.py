# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
from io import open
import DAN

def get_element(soup, tag, class_name):
    data = []
    table = soup.find(tag, attrs={'class':class_name})
    rows = table.find_all('tr')
    del rows[0]
    
    for row in rows:
        first_col = row.find_all('th')
        cols = row.find_all('td')
        cols.insert(0, first_col[0])
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) 
    return data

region ='BaoShan'
   
file_name = region+".html"

f = open (file_name,'r', encoding='utf-8')
s = f.readlines()
s = ''.join(s)

soup = BeautifulSoup(s, "lxml")

df_tmp = get_element(soup, 'table','BoxTable')

print(df_tmp[0])
#上面爬蟲完
#####################################################
#下面push 到IoTTalk

ServerURL = 'https://5.IoTtalk.tw' #with SSL connection
Reg_addr = None #if None, Reg_addr = MAC address

DAN.profile['dm_name']='0858812_1120'
DAN.profile['df_list']=['Humidity', 'Temperature', 'Total_volume_of_rain', 'temp_wind' ,'windPower', 'wind_dir']
DAN.device_registration_with_retry(ServerURL, Reg_addr)
print('try to push')
while True:
    
    try:
        #print(df_tmp[0])
        DAN.push ('Humidity', df_tmp[0][8])
        DAN.push ('Temperature', df_tmp[0][1])
        DAN.push ('Total_volume_of_rain', df_tmp[0][10])
        DAN.push ('temp_wind', df_tmp[0][6])
        DAN.push ('windPower', df_tmp[0][5])
        DAN.push ('wind_dir', df_tmp[0][4])
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(1)

#########################################################################################
"""
import pandas as pd
print ('Region :', region,'Building table ...')
col_list = ['觀測時間', '溫度(°C)', '溫度(°F)', '天氣', '風向', '風力 (m/s)|(級)', '陣風 (m/s)|(級)', '能見度(公里)', '相對溼度(%)', '海平面氣壓(百帕)', '當日累積雨量(毫米)', '日照時數(小時)']
df = pd.DataFrame(columns = col_list)
df_tmp = pd.DataFrame(df_tmp)
df_tmp.columns = col_list
df = pd.concat([df, df_tmp], axis=0)   
df = df.reset_index(drop=True)    
df.to_csv(( region + '.csv'), encoding = 'utf-8')
"""


