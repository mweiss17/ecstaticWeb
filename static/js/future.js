var xmlhttp = new XMLHttpRequest();

function startCountdown() {
	var str = new Date(Number(music_start_time));
	var adj = new Date((str.getTime())*1000);
	new Countdown({
	  selector: '.countdown',
	  msgPattern: "{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds till Disco!",
	  dateStart: new Date(), //milliseconds since epoch,
	  //dateEnd: new Date(Number(str.concat('000'))) /*seconds since epoch*/
	  dateEnd: adj
	});
}

window.onload = function() {
	startCountdown();
	if (get_cookie("method") == "stream"){
		document.getElementById("stream").click(); 
	}
	else if (get_cookie("method") == "download"){
		document.getElementById("download").click(); 
	}
}


