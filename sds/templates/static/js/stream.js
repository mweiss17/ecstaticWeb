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

var playtime = {{eta}};
function showRemaining() {
	document.getElementById('countdown').innerHTML = playtime;
	playtime = playtime + 1;
}
setInterval(showRemaining, 1000);
// hides the load button after you click it (if you reclick the load button, you move the mix forward by 10 millis)
var loadbutton = document.getElementById('load')
loadbutton.addEventListener('click',hideshow,false);
function hideshow() {
    document.getElementById('load').style.display = 'block'; 
    this.style.display = 'none'
}   