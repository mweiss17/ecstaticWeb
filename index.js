/*jslint node: true */
'use strict';

// Declare variables used
var ecstaticSockets, app, express, path, http, request, events, sc, cors;
sc = require("soundclouder");
express = require('express');
path = require('path');
app = express();
http = require('http');
request = require('request');
cors = require('cors');

//set up soundcloud
var sc_client_id="4cd54fa30dd13312d10dd24cc2bdcae4";
var sc_client_secret="2f845ee306729bf01254031ea1eb9803";
var sc_redirect_uri="http://ecstatic.fm/scRedirect";

//SHIT THAT SHOULD BE IN A DATABASE
var my_sc_api_url = "https://api.soundcloud.com/playlists/116100614.json?client_id=4cd54fa30dd13312d10dd24cc2bdcae4";

//set up sockets
ecstaticSockets = require("./views/assets/js/ecstaticSockets.js");
ecstaticSockets.setupEcstaticSockets(app);

// Set up templating
app.set('views', __dirname + '/views');
app.set('views', __dirname + '/squad/views');
app.set('view engine', "jade"); 
app.set('port', process.env.PORT || 3000); 
app.use(express.static('squad/views'));
app.use(express.static('views'));
app.use(cors());

//ROUTES
app.get('/', function (req, res) {
  	res.render('squad_index');
});
app.get('/api/upcomingEvents', function(req, res) {
	//actual event start time = 1434448800000
    res.json({ host_username: "Internet Wizards", title: "International Startup Fest", start_time: 1435184721000, playlist:"https://soundcloud.com/silentdiscosquad/sets/international-startup-fest"}); 
});

app.get('/api/sync', function(req, res) {
	console.log(my_sc_api_url);
	var returnedjson = calculatePlaylistSync(my_sc_api_url, 1435184721000 /*1434448800000 /*Start time @ June 16th in milli*/, function (returnedjson){
		res.json(JSON.stringify(returnedjson)); 
	});
});

app.get('/flush', function(req, res) {
	ecstaticSockets.client.flushdb();
	console.log("flushing redis database");
	res.json({"succesful":true});
});

app.listen(app.get('port'), function(req, res) {
 console.log('Server listening at ' + app.get('port'));
});


//Landing page
app.get('/api/upcomingEvents', function(req, res) {
	//actual event start time = 1434448800000
    res.json({ host_username: "Internet Wizards", title: "International Startup Fest", start_time: 1435184721000, playlist:"https://soundcloud.com/silentdiscosquad/sets/international-startup-fest"}); 
});

//SERVER STARTUP SHIT
//initialize event variable on server startup
request('http://54.173.157.204/appindex/', function (error, response, body) {
  if (!error && response.statusCode == 200) {
  	events = JSON.parse(body);
    for(var e in events) {
    	console.log(e);
    }
  }
});



//calculates the elapsed time since event start
function calculateElapsedTime(eventStartTime){
	//calculates the actual elapsed time
	var now = new Date().getTime();

	//used for testing
	//var now = 1434448810000;
	console.log("  " + now + "  (now)");
	console.log("- " + eventStartTime + "  (eventStartTime)");
	var elapsed = now - eventStartTime;
	console.log("_______________");
	console.log("  "+elapsed + "       (elapsed)");
	return elapsed;
}

//returns json {"index" : int, "elapsedTime" : (milli) int}
function setupSyncJson(elapsed, json){
	var needToSync = false;
	var trackIndex = 0;
	for(var i=0; i < json.tracks.length; i++) {
		console.log("elapsed="+elapsed);
		console.log("json.tracks[i].duration="+json.tracks[i].duration);
		if(json.tracks[i].duration > elapsed/* || json.tracks[i].duration > elapsed + 43200000 12 hours in milli*/){
			needToSync = true;
			break;
		}
		trackIndex++;
		elapsed -= json.tracks[i].duration;
	}

	//Playlist is over
	if(!needToSync){
		return -1;
	}
	//Or elapsed will sync the client in the song
	else{
		json = {"trackIndex" : trackIndex, "elapsedTime" : elapsed};
		console.log(json);
		return json;
	}
}

//returns json {"index" : int, "elapsedTime" : (milli) int}
function calculatePlaylistSync(my_sc_api_url, eventStartTime, callback){
	request(my_sc_api_url, function (error, response, body) {
		//need to determine which song we're in
		var elapsed = calculateElapsedTime(eventStartTime);
		var json = JSON.parse(body);
		if(elapsed < 0){
			console.log("event has not started");
			callback(-1);
		}
		else{
			var returnedJson = setupSyncJson(elapsed, json);
			console.log(returnedJson);
			callback(returnedJson);
		}
	});
}



