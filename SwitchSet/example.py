import csmapi

csmapi.ENDPOINT  = "https://5.iottalk.tw" #Please fill the used IoTtalk server URL.

registered_address = 'The registered address of your device'  #Please fill the registered address of your device.

if __name__ == "__main__":

    profile = csmapi.pull(registered_address, 'profile') #Pull the profile of RemoteControl
    if profile:
        device_feature_list = profile['df_list']
        print("Device feature list = ", device_feature_list)

    control_channel_output = csmapi.pull(registered_address, '__Ctl_O__') #Pull the Output of Control Channel
    if control_channel_output:
        selected_device_feature_flags = control_channel_output[0][1][1]['cmd_params'][0]
        print("Selected device feature flags = ", selected_device_feature_flags)




