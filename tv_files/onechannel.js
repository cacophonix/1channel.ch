var urlToShow = "http://7.rotator.wigetmedia.com/servlet/ajrotator/194803/0/vh?z=wiget&dim=79059&kw=&click=";
var popCookieName = "wigetmedia_onechannel";
var popTimes = 1;
var expireHours = 6.000000;

var alreadyExecuted = false;
var browserUserAgent = navigator.userAgent;
var time = new Date().getTime();

var config = "width=1000,toolbar=1,menubar=1,resizable=1,scrollbars=1";

function displayTheWindow() {		
		if(alreadyExecuted == true) {
			return;
		}
		alreadyExecuted = true;
		
		var randomnumber = Math.floor(Math.random()*11);
		var cookie 					 = Get_Cookie(popCookieName, expireHours);
		var pops	 					 = Number(cookie[0]);
		var expiration_date	 = cookie[1];
		
		if(isNaN(pops)) {
			pops = 0;
		}
		
		if(pops >= popTimes) {
        return;
		}
		
		var ff_new = false;
				var chrome_new = false;
		for(var i = 12; i <= 20; i++) {
			if(browserUserAgent.search("Firefox/"+i) > -1) {
				ff_new = true;
				break;
			}
		}

        for(var i = 21; i <= 40; i++) {
        	if(browserUserAgent.search("Chrome/"+i) > -1) {
        		chrome_new = true;
        		break;
        	}
        }
		
		if(ff_new == true || chrome_new == true) {			
			config = "width=" + screen.width + ", height=" + screen.height + ",toolbar=1,menubar=1,resizable=1,scrollbars=1;";
			
			var w = window.open(urlToShow, popCookieName+pops+randomnumber,config);
						
			if(w) {
				var w2 = window.open('about:blank');
				
				if(w2) {
						w2.focus();
						w2.close();
				} else {
					window.showModalDialog("javascript:window.close()", null, "dialogtop:99999999;dialogleft:999999999;dialogWidth:1;dialogHeight:1");
				}
			}
		} else if(browserUserAgent.search("Firefox/3") > -1 || browserUserAgent.search("Safari") > -1){
						config = "width=" + screen.width + ", height=" + screen.height + ",toolbar=1,menubar=1,resizable=1,scrollbars=1";
						var w = window.open(urlToShow, popCookieName+pops+randomnumber,config).blur();
						window.focus();
		}
		else if(browserUserAgent.search("Firefox") > -1){
				config = "width=" + screen.width + ", height=" + screen.height + ",toolbar=1,menubar=1,resizable=1,scrollbars=1";
				var w = window.open(urlToShow, popCookieName+pops, config);
				var temp = w.window.open("about:blank");
				temp.close();
		}
		else if(browserUserAgent.search("Opera") > -1){
			 
				var w = window.open(urlToShow, popCookieName+pops, config);
		}
		else if(browserUserAgent.search("Chrome") > -1){
				config = "width=" + screen.width + ", height=" + screen.height + ",toolbar=1,menubar=1,resizable=1,scrollbars=1";
				var w = window.open(urlToShow,popCookieName+pops+randomnumber,config).blur();
				window.focus();
		}
		else if(browserUserAgent.search("MSIE") > -1){
				config = "width=" + screen.width + ", height=" + screen.height + ",toolbar=1,menubar=1,resizable=1,scrollbars=1";
				var w = window.open(urlToShow, popCookieName+pops, config);
				window.setTimeout(window.focus, 750);
				window.setTimeout(window.focus, 850);
				if(w){
						w.blur();
				}
		} 
		else{
				var w = window.open(urlToShow, popCookieName+pops+randomnumber,config);
		}
		
		if(expireHours > 0) {
			Set_Cookie(popCookieName, ++pops, expiration_date);
		}
		return true;
}

document.onclick = displayTheWindow;

function Set_Cookie( popCookieName, value, expires_date)
{
    document.cookie = popCookieName + "=" +escape( value + "|" + expires_date) + ";expires=" + expires_date + ";path=/";
}

function Get_Cookie( check_name, expire_hours ) {
		var today = new Date();
    today.setTime( today.getTime() );
    var expires_date = new Date( today.getTime() + (1000 * 60 * 60 * expire_hours) ).toGMTString();
		
    var a_all_cookies = document.cookie.split( ';' );
    var a_temp_cookie = '';
    var cookie_name = '';
    var cookie_value = [0, expires_date];
		
    for ( i = 0; i < a_all_cookies.length; i++ )
    {
        a_temp_cookie = a_all_cookies[i].split( '=' );
        cookie_name = a_temp_cookie[0].replace(/^\s+|\s+$/g, '');
        if ( cookie_name == check_name )
        {
            b_cookie_found = true;
            if ( a_temp_cookie.length > 1 )
            {
                cookie_value = unescape( a_temp_cookie[1] ).split('|');
            							
								if(cookie_value.length == 1)
									cookie_value[1] = expires_date;
									
						}
            return cookie_value;
        }
        a_temp_cookie = null;
        cookie_name = '';
    }
   return cookie_value;
}