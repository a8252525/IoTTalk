import requests, time
import csmapi, DAN
from datetime import datetime as dt

ServerURL = 'https://5.iottalk.tw' #Change to your IoTtalk IP or None for autoSearching
Reg_addr='getAlias-Default' # if None, Reg_addr = MAC address
Reg_addr = None

DAN.profile['dm_name']='Timer0858812'
DAN.profile['df_list']=['Timer0858812']
#DAN.profile['d_name']= 'Assign a Device Name' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line
last=0
DAN.push('Timer0858812',0)
print(0)
while 1:
    try:
        alias = DAN.get_alias('Timer0858812')
        if alias != []:
            Timelist=alias[0].split('~')
            Start = dt.strptime(Timelist[0],'%H:%M:%S')
            End = dt.strptime(Timelist[1],'%H:%M:%S')
            Now = dt.now().strftime('%H:%M:%S')
            Now = dt.strptime(Now,'%H:%M:%S')

            if Start<=Now and Now<=End:
                if last==0:
                    DAN.push('Timer0858812',1)
                    print(1)
                    last=1
            else:
                if last==1:
                    DAN.push('Timer0858812',0)
                    print(0)
                    last=0





    except:
        alias = DAN.get_alias('Timer0858812')
        print(alias[0])

    time.sleep(1)