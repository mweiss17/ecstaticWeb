var lastSync = 0;
var mAudioPlayer = document.getElementsByTagName("audio")[0];
var tryToJumpInterval;
var updateProgressInterval;
setInterval(incrementClock, 1000); //Increment the countdown clock 
setInterval(checkIfPhoneSlept, 5000); //check every 5 seconds whether a minute has passed since last sync

function checkIfPhoneSlept() {
  var now = new Date().getTime();
  if ((now - lastSync) > 30000 ) {
	  lastSync = new Date().getTime(); //record the time when we synced 
	  sync();
  }
}

function incrementClock(){
	eta = eta + 1;
	showClock();
	if(eta > 0){
		updateProgress(); //update the progress bar's UI if the mix is playing
	}
}

function sync(){
	try{
		var xmlhttp = new XMLHttpRequest();
		xmlhttp.onreadystatechange=function(){
			if (xmlhttp.readyState==4 && xmlhttp.status==200){
				console.log(xmlhttp);
				eta = Number(xmlhttp.responseText);
				console.log(eta);
			}
		}
		xmlhttp.open("GET","/stream.html/?id="+eventID+"&async=2",true);
		xmlhttp.send();
	}
	catch(err){
		console.log( err );
	}
}

function playMix() {
	//the first time we click the play button, the player is stopped, so we want to toggle the player and sync it REALLY quick
	if(mAudioPlayer.paused){
		this.mAudioPlayer.play();
		this.mAudioPlayer.pause();
		tryToJumpInterval = setInterval(tryToJump, 200);
	}
	//if we're trying to 'resync' 
	else{
		tryToJumpInterval = setInterval(tryToJump, 1000);
	}
}

function tryToJump() {
	//Try to jump if the current time is more than 5 seconds off playtime
	if(Math.abs(mAudioPlayer.currentTime - eta) > 1){
		mAudioPlayer.currentTime = eta;
		this.mAudioPlayer.play();
	}
	//Clear the interval if the it's within 5 seconds, and the player is playing
	else if(!mAudioPlayer.paused){
		clearInterval(tryToJumpInterval);
	}
}



//Update the countdown clock, handle making the play button appear.
function showClock() {
	if(eta >= 0){
		makePlayButtonVisible();
	}
	if(eta >= 0){
		var hours = Math.floor(( eta / 3600) % 24);
		var minutes = Math.floor(( eta / 60) % 60);
		var seconds = Math.floor( eta % 60);
		document.getElementById("countdown").innerHTML = hours + 'h ';
		document.getElementById("countdown").innerHTML += minutes + 'm ';
		document.getElementById("countdown").innerHTML += seconds + 's';
	}
	if(eta <= 0){
		var days = Math.floor( -eta / 86400);
		var hours = Math.floor(( -eta / 3600) % 24);
		var minutes = Math.floor(( -eta / 60) % 60);
		var seconds = Math.floor( -eta % 60);
		document.getElementById("countdown").innerHTML = days + 'd ';
		document.getElementById("countdown").innerHTML += hours + 'h ';
		document.getElementById("countdown").innerHTML += minutes + 'm ';
		document.getElementById("countdown").innerHTML += seconds + 's';
	}
}


//Makes the html for the play button visible at 0 seconds
function makePlayButtonVisible(){
	document.getElementById('play').disabled = false;
}

//Progress through Mix
function updateProgress() { 
	document.getElementById('progDiv').style.display = 'block';
	document.getElementById('smile').style.display = 'none';
	var progress = document.getElementById("prog");
	var value = 0; 
	if (mAudioPlayer.currentTime > 0) { 
		value = Math.floor((100 / mAudioPlayer.duration) * mAudioPlayer.currentTime);
	} 
	progress.value = value; 
}

