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
    subscriber.on("message", function(channel, message){
        var parsed_message = JSON.parse(message);
        if (parsed_message.msg_type === 'join'){ 
            socket.emit("realtime_join_room", message);
        }
        if (parsed_message.msg_type === 'leave'){ 
            socket.emit("realtime_leave_room", message);
        }
        if (parsed_message.msg_type === 'add_song'){ 
            socket.emit("realtime_add_song", message);
        }
        if (parsed_message.msg_type === 'remove_song'){ 
            socket.emit("realtime_remove_song", message);
        }
        if (parsed_message.msg_type === 'create_room'){ 
            socket.emit("realtime_create_room", message);
        }
        if (parsed_message.msg_type === 'send_text'){ 
            socket.emit("realtime_send_text", message);
        }
    });

    //Joins an existing room
    socket.on('join_room', function (data) {
        var params = JSON.parse(data);
        client.lpush('list_of_users:'+params.room_number, params.username);
        publisher.publish(params.room_number, JSON.stringify({"msg":params.username, "msg_type":"join"}));
        subscriber.subscribe(params.room_number);
        client.lrange(':1:room:'+params.room_number+':chat', 0, -1, function(err, chatlog){
            socket.emit("return_join_room", chatlog);
        });
    });

    //leaves an existing room
    socket.on('leave_room', function (data) {
        var params = JSON.parse(data);
        client.lrem('list_of_users:'+params.room_number, 1, params.username);
        publisher.publish(params.room_number, JSON.stringify({"msg":params.username, "msg_type":"leave"}));
        subscriber.unsubscribe(params.room_number);
    });

    socket.on('get_user_list', function (data) {
        var params = JSON.parse(data);
        client.lrange('list_of_users:'+params.room_number, 0, -1, function(err, users){
            socket.emit("return_get_user_list", users);
        });
    });

    socket.on('post_location', function (data) {
        var params = JSON.parse(data);
        proximity.addLocation(params.latitude, params.longitude, params.username,  function(err, reply){
            if(err) {
                console.error("post_location_err="+err);
            }
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
            client.hmset(':1:room:'+room_counter, "host_username", params.username, "room_name", params.room_name, "room_number", room_counter, "number_of_users", 1, function (err, val){

            });    //create a new hashmap with the room number
            //create a key-value for the username (mweiss17) to the room_id
            client.set(":1:"+params.username+":room", room_counter);       
            client.incr('room_counter');         //increment the number of rooms 

            // emit room_info 
            client.hgetall(':1:room:'+room_counter, function(err, room_info){
                socket.emit('return_create_room', {"room_info":room_info});
                publisher.publish("ecstatic", JSON.stringify({"msg":room_info, "msg_type":"create_room"}));
            });
            //post location
            //post_location(data.params("username"), data.params("lat"), data.params("lon"));

            client.lpush('list_of_users:'+room_counter, params.username);
            subscriber.subscribe(room_counter);
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
            proximity.nearby(location.latitude, params.longitude, 10000000000, function(err, people){
                if(err) console.error(err);
                else {
                    async.map(people, get_room_for_user, function(err, result){
                        if(!err){
                            async.map(result, get_room_info, function(err, result){
                                socket.emit("return_get_rooms_around_me", {"rooms":result});
                                subscriber.subscribe("ecstatic");
                            });
                        }
                    });
                }
            });
        });
    });

    //PLAYER / PLAYLIST
    socket.on('add_song', function (data) {
        var params = JSON.parse(data);
        publisher.publish(params.room_number, JSON.stringify({"msg":{"song":params}, "msg_type":"add_song"}));
        client.lpush(':1:room:'+params.room_number+':playlist', data);
    });

    socket.on('remove_song', function (data) {
        var params = JSON.parse(data);
        publisher.publish(params.room_number, JSON.stringify({"msg":params, "msg_type":"remove_song"}));
        client.lrem(':1:room:'+params.room_number+':playlist', 1, data);
    });

    socket.on('send_text', function (data) {
        var params = JSON.parse(data);
        publisher.publish(params.room_number, JSON.stringify({"msg":params, "msg_type":"send_text"}));
        client.lpush(':1:room:'+params.room_number+':chat', data);
    });

//not done
    socket.on('move_song', function (data) {
        client.get(data.username, function(err, room_number) {
            client.linsert(':1:room:'+room_number+':playlist', "BEFORE", data.before, data.to_insert, function(err, val) {
                client.lrem(':1:room:'+room_number+':playlist', "1", data);
            });
        });
    });

//not done
    socket.on('get_playlist', function (data) {
        var params = JSON.parse(data);
        client.lrange(':1:room:'+params.room_number+':playlist', 0, -1, function(err, data) {
            socket.emit("return_get_playlist", {"playlist":data});
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
            console.log("err="+err);
        }
    });
}    



