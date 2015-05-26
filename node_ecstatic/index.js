/*jslint node: true */
'use strict';

// Declare variables used
var app, base_url, client, express, hbs, io, port, rtg, subscribe, room_counter,request, async, Promise;

// Define values
request = require('request');
express = require('express');
app = express();
port = process.env.PORT || 8888;
base_url = process.env.BASE_URL || 'http://localhost:8888';
hbs = require('hbs');
async = require('async');
Promise = require('promise');
// Set up connection to Redis
/* istanbul ignore if */
if (process.env.REDISTOGO_URL) {
    rtg  = require("url").parse(process.env.REDISTOGO_URL);
    client = require("redis").createClient(rtg.port, rtg.hostname);
    subscribe = require("redis").createClient(rtg.port, rtg.hostname);
    client.auth(rtg.auth.split(":")[1]);
    subscribe.auth(rtg.auth.split(":")[1]);
} else {
    client = require('redis').createClient();
    subscribe = require('redis').createClient();
}
var proximity = require('geo-proximity').initialize(client);


// Set up templating
app.set('views', __dirname + '/views');
app.set('view engine', "hbs");
app.engine('hbs', require('hbs').__express);

// Register partials
hbs.registerPartials(__dirname + '/views/partials');

// Set URL
app.set('base_url', base_url);

// Define index route
app.get('/', function (req, res) {
    res.render('index');
});

// Serve static files
app.use(express.static(__dirname + '/static'));

// Listen
io = require('socket.io')({
}).listen(app.listen(port));
console.log("Listening on port " + port);

// Handle new messages
io.sockets.on('connection', function (socket) {

    //Joins an existing room
    socket.on('get_room_for_user', function (data) {
        client.get(data.username, function(err, room_number) {
            //add yourself to the users list
            client.hmset('list_of_users:'+room_number, 'username', data.username);
        });
    });

    //Joins an existing room
    socket.on('join_room', function (data) {
        client.get(data.user_id, function(err, room_number) {
            //add yourself to the users list
            client.hmset('list_of_users:'+room_number, 'username', data.username);
        });
    });

    socket.on('leave_room', function (data) {
        client.get(data.user_id, function(err, room_number) {
            //add yourself to the users list
            client.hmset('list_of_users:'+room_number, 'username', data.username);
        });
    });

    socket.on('post_location', function (data) {
        var params = JSON.parse(data);
        proximity.addLocation(params.lat, params.lon, params.username,  function(err, reply){
            if(err) console.error(err);
            else {
                socket.emit('return_post_location');
                console.log('added location:', reply);
            }
        });
    });

    //creates a new room
    socket.on('create_room', function (data) {
        client.get('room_counter', function(err, room_counter) {
            if(!room_counter){
                client.set('room_counter', 0, function(err, room_counter) {
                    if(err) console.log(err);
                });
                room_counter = 0;
            }
            var params = JSON.parse(data);
            client.hmset(':1:room:'+room_counter, "room_name", params.room_name, "room_number", room_counter, "number_of_users", 1, function (err, val){

            });    //create a new hashmap with the room number
            //create a key-value for the username (mweiss17) to the room_id
            client.set(":1:"+params.username+":room", room_counter);       
            client.incr('room_counter');         //increment the number of rooms 

            // emit room_info 
            client.hgetall(':1:room:'+room_counter, function(err, room_info){
                socket.emit('return_create_room', room_info);
            });
            //post location
            //post_location(data.params("username"), data.params("lat"), data.params("lon"));

            //set list_of_users
            //client.hmset('list_of_users:'+room_counter, "username", data.username);

            //set playlist
            //client.hmset(':1:room:'+room_counter+':playlist, "");

            //set player
            //client.hmset('player:'+room_counter, 'is_playing', false, 'playertime', 0);
        });
    });
    

    //Joins an existing room
    socket.on('get_rooms_around_me', function (data) {
        var params = JSON.parse(data);
        proximity.location(params.username, function(err, location){
            console.log(location);
            proximity.nearby(location.latitude, params.longitude, 100000000, function(err, people){
                if(err) console.error(err);
                else {
                    async.map(people, get_room_for_user, function(err, result){
                        if(!err){
                            async.map(result, get_room_info, function(err, result){
                                socket.emit("return_get_rooms_around_me", JSON.stringify(result));
                            });
                        }
                    });
                }
            });
        });
    });

    //Joins an existing room
    /*socket.on('get_rooms_around_me', function (data) {
        var params = JSON.parse(data);
        proximity.location(params.username, function(err, location){
            console.log(location);
            proximity.nearby(location.latitude, params.longitude, 100000000, function(err, people){
                if(err) console.error(err);
                else {
                    get_room_for_users(people).done(function(results){
                        async.map(results, get_room_info, function(err, result){
                            socket.emit("return_get_rooms_around_me", JSON.stringify(result));
                        });
                    }, function(err){
                        console.log("fuck");
                    });
                }
            });
        });
    });*/
});


/*function get_room_for_users(usernames){
    return Promise.all(usernames.map(get_room_for_user));
}

function get_room_for_user(username){
    client.get(":1:"+username+":room", function(err, room_number) {
        try{
            console.log("room_number="+room_number);
            return room_number;
        }
        catch(err){
            console.log("caught error, room_number="+room_number);
        }
    });
}*/


function get_room_for_user(username, callback){
    client.get(":1:"+username+":room", function(err, room_number) {
        try{
            callback(null, room_number);
        }
        catch(err){
            console.log("caught error, room_number="+room_number);
        }
    });
}

function get_room_info(room_number, callback){
    client.hgetall(':1:room:'+room_number, function (err, room_info) {
        try{
            callback(null, room_info);
        }
        catch(err){
            console.log("caught error, room_info="+room_info);
        }
    });
}    



