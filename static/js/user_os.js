$(function(){

    var os, ua = navigator.userAgent;
    if (ua.match(/Win(dows )?NT 10\.0/)) {
        os = "Windows 10";				// Windows 10 の処理 (Windows Server 2016, Windows Server 2019)
    }
    else if (ua.match(/Win(dows )?NT 6\.3/)) {
        os = "Windows 8.1";				// Windows 8.1 の処理 (Windows Server 2012 R2)
    }
    else if (ua.match(/Win(dows )?NT 6\.2/)) {
        os = "Windows 8";				// Windows 8 の処理 (Windows Server 2012)
    }
    else if (ua.match(/Win(dows )?NT 6\.1/)) {
        os = "Windows 7";				// Windows 7 の処理 (Windows Server 2008 R2, Windows Home Server 2011)
    }
    else if (ua.match(/Win(dows )?NT 6\.0/)) {
        os = "Windows Vista";				// Windows Vista の処理 (Windows Server 2008)
    }
    else if (ua.match(/Win(dows )?NT 5\.2/)) {
        os = "Windows Server 2003";			// Windows Server 2003 の処理 (Windows XP x64, Windows Server 2003 R2, Windows Home Server)
    }
    else if (ua.match(/Win(dows )?(NT 5\.1|XP)/)) {
        os = "Windows XP";				// Windows XP の処理
    }
    else if (ua.match(/Win(dows)? (9x 4\.90|ME)/)) {
        os = "Windows ME";				// Windows ME の処理
    }
    else if (ua.match(/Win(dows )?(NT 5\.0|2000)/)) {
        os = "Windows 2000";				// Windows 2000 の処理
    }
    else if (ua.match(/Win(dows )?98/)) {
        os = "Windows 98";				// Windows 98 の処理
    }
    else if (ua.match(/Win(dows )?NT( 4\.0)?/)) {
        os = "Windows NT";				// Windows NT の処理
    }
    else if (ua.match(/Win(dows )?95/)) {
        os = "Windows 95";				// Windows 95 の処理
    }
    else if (ua.match(/Windows Phone/)) {
        os = "Windows Phone";				// Windows Phone (Windows 10 Mobile) の処理
    
        /*
        if (ua.match(/Windows Phone( OS)? ([\.\d]+)/)) {
            os = "Windows Phone "  + RegExp.$2;
        }
        else {
            os = "Windows Phone";
        }
        */
    }
    else if (ua.match(/iPhone|iPad/)) {
        os = "iOS";					// iOS (iPhone, iPod touch, iPad) の処理
    
        /*
        if (ua.match(/(iPhone|CPU) OS ([\d_]+)/)) {
            os = "iOS " + RegExp.$2;
            os = os.replace(/_/g, ".");
        }
        else {
            os = "iOS";
        }
        */
    }
    else if (ua.match(/Mac|PPC/)) {
        os = "Mac OS";					// Macintosh の処理
    
        /*
        if (ua.match(/OS X|MSIE 5\.2/)) {
            if (ua.match(/Mac OS X ([\.\d_]+)/)) {
                os = "macOS " + RegExp.$1;
                os = os.replace(/_/g, ".");
            }
            else {
                os = "macOS";
            }
        }
        else {
            os = "Classic Mac OS";
        }
        */
    }
    else if (ua.match(/Android ([\.\d]+)/)) {
        os = "Android " + RegExp.$1;			// Android の処理
    }
    else if (ua.match(/Linux/)) {
        os = "Linux";					// Linux の処理
    }
    else if (ua.match(/^.*\s([A-Za-z]+BSD)/)) {
        os = RegExp.$1;					// BSD 系の処理
    }
    else if (ua.match(/SunOS/)) {
        os = "Solaris";					// Solaris の処理
    }
    else {
        os = "N/A";					// 上記以外 OS の処理
    }

    console.log(os);
    $(".os").val(os);
    $(".test").text(os);
});