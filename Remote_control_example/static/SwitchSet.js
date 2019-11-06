let device_id = null;
var _ENDPOINT =  "https://5.iottalk.tw"; 
var password = null;
var numberOfSwitches = 0;
var profile = {
    'dm_name': 'Remote_control',
    'df_list':[],
    'd_name': '',
    'is_sim':false,
};    

function set_device_id(d_id, count){
    device_id = d_id;
    numberOfSwitches = count;
    profile['d_name'] = d_id;
    //for (var index=1; index<=count; index++) profile['df_list'].push('Switch'+String(index));
    profile['df_list']=['Keypad1','Keypad2','Keypad3','Keypad4','Keypad5','Keypad6','Keypad7','Keypad8', 'Keypad9','Color-I1','Color-I2','Color-I3','Color-I4','Color-I5','Color-I6','Color-I7','Color-I8','Color-I9', 'Button1','Button2','Button3','Button4','Button5','Button6','Button7','Button8','Button9','Switch1', 'Switch2', 'Switch3', 'Switch4', 'Switch5', 'Switch6', 'Switch7', 'Switch8', 'Switch9','Knob1','Knob2','Knob3','Knob4','Knob5','Knob6','Knob7','Knob8','Knob9']
    //profile['df_list']=['Button1', 'Button2', 'Color-I1', 'Color-I2', 'Keypad1', 'Keypad2', 'Knob1', 'Knob2','Switch1', 'Switch2']
    csmapi.set_endpoint(_ENDPOINT);   
}

function regisration_state(state, d_name, passwd){
    if (state){ 
        console.log('Register successfully.');
        password = passwd;
        load_alias_and_switchState(device_id, numberOfSwitches);	    
    }
    else console.log('Register failed.');
}

function state_check(data, exception=null){
    if (exception){
        if (String(exception.responseText).indexOf('mac_addr not found') != -1){
            console.log('Device is not existed. Try to register.');
            console.log('device_id =', device_id);
            csmapi.register(device_id, profile, regisration_state);
        }
        else if(String(exception.responseText).indexOf('password-key error') != -1){
	    console.log('Password is expired. Re-register.');
            console.log('Because device_auth is enabled, the Switch state cannot be loaded.');
	    csmapi.register(device_id, profile, regisration_state);
        }
        else{
            console.log('Error occurred!');
            console.log('Response:', exception.responseText);
            console.log('Status:', exception.statusText);
            console.log('Endpoint =', _ENDPOINT);
        }
    }
    else{
        console.log('Device is existed. Continue.');
        if (profile['df_list'].length > data['df_list'].length){
            console.log('Required number of Switches larger than that in the server. Re-register.');
            csmapi.register(device_id, profile, regisration_state);
        }
	else load_alias_and_switchState(device_id, numberOfSwitches);
           
    }
}

function check_registerion_state(mac_addr){
    csmapi.pull(mac_addr, password, 'profile', state_check);
}

$(function () {
    $(document).on('click', '.toggle', function() {
	var self_id = $(this)[0].childNodes[0].id;
	console.log (self_id);
	var clicked = $(this).hasClass('btn-primary');
        csmapi.push(device_id, password, self_id, [clicked ? 1 : 0]);
    });
});

function get_alias(mac_addr, df_name, callback){
    var alias;
    var ajax_obj = $.ajax({
        url: _ENDPOINT +'/get_alias/' + mac_addr+ '/' + df_name,
        type: 'GET',
        data: {alias},
    }).done(function(alias){
        if(typeof callback === 'function') callback(df_name, alias['alias_name'][0]);
    });
}

function update_alias(df_name, alias){
    if (alias!=undefined) $('.'+df_name)[0].innerText = alias;
}

function load_alias_and_switchState(mac_addr, count){
    for(var index=1; index<=count; index++){
	    get_alias(mac_addr, 'Switch'+index.toString(), update_alias);
	    csmapi.pull(mac_addr, password, 'Switch'+String(index), update_switch_state);
    }
}

function update_switch_state(data, exception, df_name){
    if (data.length != 0)
        if (data[0][1][0] == 1) $('#'+df_name).bootstrapToggle('on');
}

function close_page(){
    document.location.href=window.location.origin;
}

function dereg(mac_addr) {
    var decision = confirm("警告: Delete this Controller.\nAre you sure?");
    if (decision){ 
        console.log('Deregister this reomte control and close the page now.');
	csmapi.deregister(mac_addr, close_page);
    }
    else{
        console.log('Won\'t deregister.');
    }
}

function output_df(data){
    console.log(data['df_list']);
}

function output_dfs(mac_addr){
        csmapi.pull(mac_addr, 'passwd', 'profile', output_df);
}

function output_selected_df(data){
    console.log(data[0][1][1]['cmd_params'])
    
}

function output_selected_dfs(mac_addr){
        csmapi.pull(mac_addr, 'passwd', '__Ctl_O__', output_selected_df);
}

$(function () {
    console.log('SwitchSet JS has been successfully loaded.');
    
});


