
var xmlhttp = new XMLHttpRequest();
function record(){
	//Hit the server's view that checks whether this account has already "attended" this event
	try{
		xmlhttp.open("GET","/recordEventAttendees.html/?eventID="+eventID,true);
		xmlhttp.send();
	}
	catch(err){
		console.log( err );
	}
}

function recordStream() {
	record();
	window.location.href = "/stream.html?id="+eventID;
}

function recordDownload() {
	record();
	window.location.href = "https://s3.amazonaws.com/silentdiscosquad/"+eventMix;
}
