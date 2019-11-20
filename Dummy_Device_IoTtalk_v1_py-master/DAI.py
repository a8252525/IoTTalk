import time, random, requests
import DAN

#ServerURL = 'http://IP:9999'      #with non-secure connection
ServerURL = 'https://5.IoTtalk.tw' #with SSL connection
Reg_addr = None #if None, Reg_addr = MAC address

DAN.profile['dm_name']='T0858812'
DAN.profile['df_list']=['T0858812-I', 'T0858812-O',]
#DAN.profile['d_name']= 'Assign a Device Name' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line
curr=0
last=1
while True:
    try:
        #IDF_data = random.uniform(1, 10)
        #DAN.push ('T0858812-I', IDF_data) #Push data to an input device feature "Dummy_Sensor"

        #==================================
        ODF_data = DAN.pull('T0858812-O')#Pull data from an output device feature "Dummy_Control"
        if ODF_data != None:
            if ODF_data[0]>0:
                curr=1
            else:
                curr=0
            if last != curr:
                print(curr)
            last=curr

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)

