var playtime = {{eta}};
var xmlhttp = new XMLHttpRequest();
var lastSyncSleepRecovery = 0;
var syncIntervalSleepRecovery = 30000; 
var mAudioPlayer = document.getElementsByTagName("audio")[0];
var tryToJumpInterval;
var updateProgressInterval;
setInterval(incrementPlaytime, 1000);
setInterval(showRemaining, 1000);

/**** Recovers after phone is closed, makes 1 ajax request every 30 seconds.*****
***** Checks if phone was closed every 5 seconds. 							****/
function updateLastSyncSleepRecovery() {
  lastSyncSleepRecovery = new Date().getTime(); //set last sync to be now
  sync();
}

setInterval(function() {
  var now = new Date().getTime();
  if ((now - lastSyncSleepRecovery) > syncIntervalSleepRecovery ) {
    updateLastSyncSleepRecovery();
  }
}, 5000); //check every 5 seconds whether a minute has passed since last sync


function incrementPlaytime(){
	playtime = playtime + 1;
}

function sync(){
	try{
		xmlhttp.onreadystatechange=function(){
			if (xmlhttp.readyState==4 && xmlhttp.status==200){
				console.log(xmlhttp);
				playtime = Number(xmlhttp.responseText);
			}
		}
		xmlhttp.open("GET","/stream.html/?id=31&async=2",true);
		xmlhttp.send();
	}
	catch(err){
		console.log( err );
	}
}

function playMix() {
	this.mAudioPlayer.play();
	this.mAudioPlayer.pause();
	tryToJumpInterval = setInterval(tryToJump, 50);
	updateProgressInterval = setInterval(updateProgress, 1000);
}

function tryToJump() {
	//Try to jump if the current time is more than 5 seconds off playtime
	if(Math.abs(mAudioPlayer.currentTime - playtime) > 5){
		mAudioPlayer.currentTime = playtime;
		this.mAudioPlayer.play();
	}
	//Clear the interval if the it's within 5 seconds, and the player is playing
	else if(!mAudioPlayer.paused){
		clearInterval(tryToJumpInterval);
	}
}



//Update the countdown clock, handle making the play button appear.
function showRemaining() {
	if(playtime >= 0){
		makePlayButtonVisible();
	}
	if(playtime >= 0){
		var hours = Math.floor(( playtime/ 3600) % 24);
		var minutes = Math.floor(( playtime / 60) % 60);
		var seconds = Math.floor( playtime % 60);
		document.getElementById("countdown").innerHTML = hours + 'hrs ';
		document.getElementById("countdown").innerHTML += minutes + 'mins ';
		document.getElementById("countdown").innerHTML += seconds + 'secs';
	}
	if(playtime <= 0){
		var days = Math.floor( -playtime / 86400);
		var hours = Math.floor(( -playtime / 3600) % 24);
		var minutes = Math.floor(( -playtime / 60) % 60);
		var seconds = Math.floor( -playtime % 60);
		document.getElementById("countdown").innerHTML = days + 'days ';
		document.getElementById("countdown").innerHTML += hours + 'hrs ';
		document.getElementById("countdown").innerHTML += minutes + 'mins ';
		document.getElementById("countdown").innerHTML += seconds + 'secs';
	}
}


//Makes the html for the play button visible at 0 seconds
function makePlayButtonVisible(){
	document.getElementById('play').style.display = 'block';
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

