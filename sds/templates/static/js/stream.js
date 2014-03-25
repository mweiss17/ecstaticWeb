var mAudioPlayer = document.getElementsByTagName("audio")[0];
this.loadMix = function(){
	try{
		this.mAudioPlayer.play();
		setTimeout("mAudioPlayer.pause()", 10)
	}
	catch(err){
		console.log( err );
	}
}

this.playMix = function(){
	try{
		this.mAudioPlayer.currentTime = playtime;
		this.mAudioPlayer.play();
	}
	catch(err){
		console.log( err );
	}
}

var loadbutton = document.getElementById('load')
var playButton = document.getElementById('play')
var count = 0;
var count2 = 0;
var playtime = {{eta}};
setInterval(showRemaining, 1000);
loadbutton.addEventListener('click',hideshow,false);


function showRemaining() {
	document.getElementById('countdown').innerHTML = playtime;
	playtime = playtime + 1;
	if(playtime > -300){
		makeLoadButtonVisible();
	}
	if(playtime >= 0){
		makePlayButtonVisible();
	}

}

function makeLoadButtonVisible(){
	if(count == 1){
		return;
	}
	count++;
	document.getElementById('load').style.display = 'block';
}

function makePlayButtonVisible(){
	if(count2 == 1){
		return;
	}
	count2++;
	document.getElementById('play').style.display = 'block';
}
// hides the load button after you click it (if you reclick the load button, you move the mix forward by 10 millis)
function hideshow() {
    document.getElementById('load').style.display = 'none'; 
    //document.getElementById('load').style.backgroundColor = '#B0B0B0'; 
}  
