 $(function(){
        csmapi.set_endpoint ('https://5.iottalk.tw');
        var profile = {
		    'dm_name': 'blub_0858812',          
			'odf_list':[Lum_0858812,colcor_0858812],
		        'd_name': undefined,
        };
        var r = 255 ;
        var g = 255;
        var b = 0;
        var lum = 100;

        function draw () {
            var rr = Math.floor((r * lum) / 100);
            var gg = Math.floor((g * lum) / 100);
            var bb = Math.floor((b * lum) / 100);
            $('.bulb-top, .bulb-middle-1, .bulb-middle-2, .bulb-middle-3, .bulb-bottom, .night').css(
                {'background': 'rgb('+ rr +', '+ gg +', '+ bb +')'}
            );
        }
        lum = 255;
    
        
        r = 255;
        g = 0;
        b = 0;
        draw();
        
        function Lum_0858812(data){
            lum = data[0]
            draw();
         }		


        function colcor_0858812(data){
            r = (data[0])/360*255;
            g = (data[1]+90)/180*255;
            b = (data[2]+90)/180*255;
            draw();;
        }
      
/*******************************************************************/                
        function ida_init(){
	    console.log(profile.d_name);
	}
        var ida = {
            'ida_init': ida_init,
        }; 
        dai(profile,ida);     
});
