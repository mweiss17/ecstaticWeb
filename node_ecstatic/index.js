/*jslint node: true */
'use strict';

// Declare variables used
var app, base_url, client, express, hbs, io, port, rtg, room_counter,request, async, proximity, subscriber, publisher;

// Define values
request = require('request');
express = require('express');
app = express();
port = process.env.PORT || 8888;
base_url = process.env.BASE_URL || 'http://localhost:8888';
hbs = require('hbs');
async = require('async');
client = require('redis').createClient();
subscriber = require('redis').createClient();
publisher = require('redis').createClient();
proximity = require('geo-proximity').initialize(client);


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
    subscriber.subscribe('rooms');
    subscriber.on("message", function(channel, message){
        var parsed_message = JSON.parse(message);
        if ((channel === 'rooms') && (parsed_message.msg_type === 'join')){ 
            socket.emit("realtime_join_room", message);
        }
        if ((channel === 'rooms') && (parsed_message.msg_type === 'leave')){ 
            socket.emit("realtime_leave_room", message);
        }
    });

    //Joins an existing room
    socket.on('join_room', function (data) {
        var params = JSON.parse(data);
        client.lpush('list_of_users:'+params.room_number, params.username);
        publisher.publish("rooms", JSON.stringify({"msg":params.username, "msg_type":"join"}));
    });

    //leaves an existing room
    socket.on('leave_room', function (data) {
        var params = JSON.parse(data);
        client.lrem('list_of_users:'+params.room_number, 1, params.username);
        publisher.publish("rooms", JSON.stringify({"msg":params.username, "msg_type":"leave"}));
    });

    socket.on('get_user_list', function (data) {
        var params = JSON.parse(data);
        client.lrange('list_of_users:'+params.room_number, 0, -1, function(err, users){
            console.log(users);
            socket.emit("return_get_user_list", users);
        });
    });

    socket.on('post_location', function (data) {
        var params = JSON.parse(data);
        proximity.addLocation(params.lat, params.lon, params.username,  function(err, reply){
            if(err) console.error(err);
            else {
                socket.emit('return_post_location');
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

            client.lpush('list_of_users:'+room_counter, params.username);
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
            console.log(JSON.stringify(location));
            proximity.nearby(location.latitude, params.longitude, 10000000000, function(err, people){
                console.log("people="+JSON.stringify(people));
                if(err) console.error(err);
                else {
                    async.map(people, get_room_for_user, function(err, result){
                        if(!err){
                            async.map(result, get_room_info, function(err, result){
                                console.log("get_rooms_around_me_returns="+JSON.stringify(result));
                                socket.emit("return_get_rooms_around_me", JSON.stringify(result));
                            });
                        }
                    });
                }
            });
        });
    });
});

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



