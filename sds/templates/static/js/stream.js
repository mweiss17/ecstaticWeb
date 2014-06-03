var firstClick = true;
var playButton = document.getElementById('play');
var count = 0;
var playtime = {{eta}};
var xmlhttp;
xmlhttp=new XMLHttpRequest();
setInterval(incrementPlaytime, 1000);
setInterval(showRemaining, 1000);

var lastSyncSleepRecovery = 0;
var syncIntervalSleepRecovery = 30000; 
var mAudioPlayer = document.getElementsByTagName("audio")[0];
mAudioPlayer.addEventListener('play', setPlayerTime, false);

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
	console.log("playtime="+playtime);
	console.log("currentTime="+mAudioPlayer.currentTime);
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
	try{
		console.log("playPressed");
		this.mAudioPlayer.play();
	}
	catch(err){
		console.log( err );
	}
}

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

function makePlayButtonVisible(){
	if(count == 1){
		return;
	}
	count++;
	document.getElementById('play').style.display = 'block';
}

/* prog bar
function updateProgress() { 
	var progress = document.getElementById("prog");
	var value = 0; 
	console.log("currentTime="+mAudioPlayer.currentTime);
	if (mAudioPlayer.currentTime > 0) { 
		console.log("duration="+mAudioPlayer.duration);

		value = Math.floor((100 / mAudioPlayer.duration) * mAudioPlayer.currentTime);
		console.log("value="+mAudioPlayer.currentTime);
	} 
	progress.style.width = value + "%"; 
}*/

function setPlayerTime(){
	console.log("setPlayerTime");
	mAudioPlayer.currentTime = playtime;
  	mAudioPlayer.removeEventListener('progress', setPlayerTime, false);
}