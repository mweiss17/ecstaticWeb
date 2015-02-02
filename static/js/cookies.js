
function record_stream() {
	record();
	delete_cookie("method");
	delete_cookie("eventID");
	window.location.href = "/stream.html?id="+eventID;
}

function record_download() {
	record();
	delete_cookie("method");
	delete_cookie("eventID");
	window.location.href = "https://s3.amazonaws.com/silentdiscosquad/"+eventMix;
}

function set_stream_cookie() {
	set_cookie("method", "stream", 300);
	set_cookie("eventID", eventID, 300);
	window.location.href = "#login";
}

function set_download_cookie() {
	set_cookie("method", "download", 300);
	set_cookie("eventID", eventID, 300);
	window.location.href = "#login";
}

function delete_cookie(c_name) {
	set_cookie(c_name, "deleted", 0);
}

function set_cookie(cname, cvalue, maxage) {
    document.cookie = cname + "=" + cvalue + "; " + 'max-age='+ maxage + "; " + "path=/";
}

function get_cookie(cname) {
	var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}
