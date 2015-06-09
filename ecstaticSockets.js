var exports = module.exports = {};

// Declare variables used
var client, express, io, port, rtg, room_counter,request, async, proximity, publisher, util;

// Define values
util = require('util');
request = require('request');
port = process.env.PORT || 8080;
async = require('async');
client = require('redis').createClient();
publisher = require('redis').createClient();
proximity = require('geo-proximity').initialize(client);

exports.setupEcstaticSockets = function(app){
    // Listen
    io = require('socket.io')({
    }).listen(app.listen(port));
    console.log("Listening on port " + port);

    // Handle new messages
    io.sockets.on('connection', function (socket) {
        var subscriber = require('redis').createClient();
        subscriber.on("message", function(channel, message){
            var parsed_message = JSON.parse(message);
            switch(parsed_message.msg_type) {
                case 'join':
                    console.log("join room hit");
                    socket.emit("join", parsed_message.msg);
                    break;
                case 'leave_room':
                    socket.emit("leave_room", parsed_message.msg);
                    break;
                case 'add_song':
                    socket.emit("add_song", parsed_message.msg.song);
                    break;
                case 'remove_song':
                    socket.emit("remove_song", parsed_message.msg);
                    break;
                case 'move_song':
                    socket.emit("move_song", parsed_message.msg);
                    break;
                case 'create_room':
                    socket.emit("create_room", parsed_message.msg);
                    break;
                case 'send_text':
                    console.log("sendtext="+message+", channel="+channel);
                    socket.emit("send_text", parsed_message.msg);
                    break;
                case 'play':
                    socket.emit("realtime_player", {"msg_type":"play", "username":parsed_message.username});
                    break;
                case 'skip':
                    socket.emit("realtime_player", {"msg_type":"skip", "username":parsed_message.username});
                    break;
                case 'back':
                    socket.emit("realtime_player", {"msg_type":"back", "username":parsed_message.username});
                    break;
                default:
                    console.log("problem in subscriber switch");
            }
        });

        //Joins an existing room
        socket.on('join_room', function (data) {
            var params = JSON.parse(data);
            client.lrange('list_of_users:'+params.room_number, 0, -1, function(err, users){
                //join event (this is broken too)
                if(users.length === 0){
                    client.hmset(':1:room:'+params.room_number, "host_username", params.host_username, "room_name", params.room_name, "room_number", params.room_number, function (err, val){

                    });    
                    client.set(":1:"+params.username+":room", params.room_number); 

                    client.hgetall(':1:room:'+params.room_number+':chat', function(err, chatlog){
                        socket.emit('return_join_room', chatlog);
                    });

                    client.lpush('list_of_users:'+params.room_number, params.username);
                    subscriber.subscribe(params.room_number);
                    console.log("if subscribed room="+params.room_number);
                    //holy shit this is broken
    //                client.set('player:'+room_counter, params.player_state);
                }
                //join room
                else{
                    client.lpush('list_of_users:'+params.room_number, params.username);
                    publisher.publish(params.room_number, JSON.stringify({"msg":params.username, "msg_type":"join"}));
                    subscriber.subscribe(params.room_number);
                    console.log("else subscribed room="+params.room_number);
                    client.lrange(':1:room:'+params.room_number+':chat', 0, -1, function(err, chatlog){
                        socket.emit("return_join_room", chatlog);
                    });
                }
            });
        });

        //leaves an existing room
        socket.on('leave_room', function (data) {
            var params = JSON.parse(data);
            client.lrem('list_of_users:'+params.room_number, 1, params.username);
            publisher.publish(params.room_number, JSON.stringify({"msg":params.username, "msg_type":"leave_room"}));
            subscriber.unsubscribe(params.room_number);
        });

        socket.on('subscribe_to_ecstatic', function (data) {
            subscriber.subscribe('ecstatic');
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
                client.hmset(':1:room:'+room_counter, "host_username", params.username, "room_name", params.room_name, "room_number", room_counter, function (err, val){

                });    
                //create a new hashmap with the room number
                //create a key-value for the username (mweiss17) to the room_id
                client.set(":1:"+params.username+":room", room_counter); 
                //increment the number of rooms      
                client.incr('room_counter');          

                // emit room_info 
                client.hgetall(':1:room:'+room_counter, function(err, room_info){
                    socket.emit('return_create_room', {"room_info":room_info});
                    publisher.publish("ecstatic", JSON.stringify({"msg":room_info, "msg_type":"create_room"}));
                });

                client.lpush('list_of_users:'+room_counter, params.username);
                subscriber.subscribe(room_counter);
                console.log("create subscribed room="+room_counter);

                //Form of data params.player_state = {'is_playing': false, 'playing_song_index':3, 'elapsed': 44}
                //set player
                params.player_state.timestamp = new Date().getTime();
                var player_state = JSON.stringify(params.player_state);
                client.set('player:'+room_counter, player_state);
            });
        });
        

        //Joins an existing room
        socket.on('get_rooms_around_me', function (data) {
            var params = JSON.parse(data);
            console.log("get rooms around me="+data);
            proximity.location(params.username, function(err, location){
                proximity.nearby(location.latitude, location.longitude, 10000000000, function(err, people){
                    async.map(people, get_room_for_user, function(err, result){
                        if(!err){
                            console.log("people="+people);
                            async.map(result, get_room_info, function(err, result){
                                console.log({"rooms":result});
                                socket.emit("return_get_rooms_around_me", {"rooms":result});
                            });
                        }
                    });
                });
            });
        });

        //CHAT
        socket.on('send_text', function (data) {
            var params = JSON.parse(data);
            console.log("send_text");
            publisher.publish(params.room_number, JSON.stringify({"msg":params, "msg_type":"send_text"}));
            client.lpush(':1:room:'+params.room_number+':chat', data);
        });

        //PLAYLIST
        socket.on('add_song', function (data) {
            var params = JSON.parse(data);
            publisher.publish(params.room_number, JSON.stringify({"msg":{"song":params}, "msg_type":"add_song"}));
            client.rpush(':1:room:'+params.room_number+':playlist', data);
        });

        socket.on('remove_song', function (data) {
            var params = JSON.parse(data);
            publisher.publish(params.room_number, JSON.stringify({"msg":params, "msg_type":"remove_song"}));
            client.lrem(':1:room:'+params.room_number+':playlist', 1, data);
        });

        socket.on('move_song', function (data) {
            var params = JSON.parse(data);
            if(params.new_index !== 0){
                params.new_index--;
            }
            client.lindex(':1:room:'+params.room_number+':playlist', params.new_index, function(err, song_before){
                client.lrem(':1:room:'+params.room_number+':playlist', 1, params.to_insert);
                client.linsert(':1:room:'+params.room_number+':playlist', "BEFORE", song_before, params.to_insert, function(err, val) {});
                publisher.publish(params.room_number, JSON.stringify({"msg":params, "msg_type":"move_song"}));
            });
        });

        socket.on('get_playlist', function (data) {
            var params = JSON.parse(data);
            client.lrange(':1:room:'+params.room_number+':playlist', 0, -1, function(err, data) {
                socket.emit("return_get_playlist", {"playlist":data});
            });
        });

        //PLAYER
        socket.on('get_player_status', function (data) {
            var params = JSON.parse(data);
            client.get('player:'+params.room_number, function(err, data){
                console.log( {"player_state":JSON.parse(data), "current_time": new Date().getTime()});
                socket.emit("return_get_player_status", {"player_state":JSON.parse(data), "current_time": new Date().getTime()});
            });
        });

        socket.on('update_player_state', function (data) {
            var params = JSON.parse(data);
            params.player_state.timestamp = new Date().getTime();
            var player_state = JSON.stringify(params.player_state);
            client.set('player:'+params.room_number, player_state);
        });



        socket.on('player', function (data) {
            var params = JSON.parse(data);
            params.player_state.timestamp = new Date().getTime();
            client.set('player:'+params.room_number, params.player_state);
            switch(params.msg_type) {
                case "play":
                    publisher.publish(params.room_number, JSON.stringify({"msg_type":"play", "username":params.username}));
                    break;
                case "skip":
                    publisher.publish(params.room_number, JSON.stringify({"msg_type":"skip", "username":params.username}));
                    break;
                case "back":
                    publisher.publish(params.room_number, JSON.stringify({"msg_type":"back", "username":params.username}));
                    break;
                default:
                    console.log("something bad happened to player");
            }   
        });
    });
}
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
        client.lrange('list_of_users:'+room_number, 0, -1, function(err, users){
            callback(null, {"room_info":room_info, "users":users});
        });
    });
}    


