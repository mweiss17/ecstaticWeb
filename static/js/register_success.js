window.onload = function() {
	if (get_cookie("eventID")) {
		if(get_cookie("method") == "stream"){
			window.location.href = "/stream.html?id="+get_cookie("eventID");
			delete_cookie("eventID");
			delete_cookie("method");
		}
		if(get_cookie("method") == "download"){
			window.location.href = "/future.html?id="+get_cookie("eventID");
			delete_cookie("eventID");
		}
	}
	else {
		window.location.href = "/";
	}
}
