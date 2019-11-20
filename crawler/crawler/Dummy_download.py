import time, random, requests
import DAN

#ServerURL = 'http://IP:9999'      #with non-secure connection
ServerURL = 'https://5.IoTtalk.tw' #with SSL connection
Reg_addr = None #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Dummy_Device'
DAN.profile['df_list']=['Dummy_Control']
#DAN.profile['d_name']= 'Assign a Device Name' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line

while True:
    try:
        #IDF_data = random.uniform(1, 10)
        #DAN.push ('T0858812-I', IDF_data) #Push data to an input device feature "Dummy_Sensor"

        #==================================
        ODF_data = DAN.pull('Dummy_Control')#Pull data from an output device feature "Dummy_Control"
        print("ODF_data:" ,ODF_data)
        f_name = ['Humidity', 'Temperature', 'Total_volume_of_rain', 'temp_wind' ,'windPower', 'wind_dir']
        for i,ele in enumerate(f_name):
            print(ele,':',ODF_data[i])

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)
