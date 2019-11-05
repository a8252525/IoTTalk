from flask import Flask, request, abort
from flask import render_template
from flask import make_response
import csmapi


csmapi.ENDPOINT  = "https://5.iottalk.tw"
registered_address = '4655444565454465cscss'
app = Flask(__name__)

@app.route('/<mac_addr>/<count>/', methods=['GET', 'POST'])
def SwitchSetCount(mac_addr, count):
    registered_address=mac_addr
    try:
        s_count=0
        print('mac_addr:',mac_addr)
        profile = csmapi.pull(registered_address, 'profile') #Pull the profile of RemoteControl
        print('Profile:',profile)
        print(789)
        if profile:
            device_feature_list = profile['df_list']
            print("Device feature list = ", device_feature_list)

        control_channel_output = csmapi.pull(registered_address, '__Ctl_O__') #Pull the Output of Control Channel
        if control_channel_output:
            selected_device_feature_flags = control_channel_output[0][1][1]['cmd_params'][0]
            print("Selected device feature flags = ", selected_device_feature_flags)
        print(type(selected_device_feature_flags))
        print('before_for')
        for i in selected_device_feature_flags:
            if i == '1':
                s_count+=1
        print(s_count)
        return make_response(render_template('index.html', mac_addr=registered_address, count=int(s_count)))

    except Exception as e:
        print(e)
    return make_response(render_template('index.html', mac_addr=registered_address, count=int(count)))

    

if __name__ == "__main__":
    app.run('127.0.0.1', port=9453, threaded=True, use_reloader=False, debug=True)
