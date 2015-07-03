var exports = module.exports = {};

// Declare variables used
var client, express, io, port, rtg, room_counter,request, async, proximity, publisher, subscriber, util, mongoose, socket;

// Define values
util = require('util');
request = require('request');
port = process.env.PORT || 8080;
async = require('async');
client = require('redis').createClient();
publisher = require('redis').createClient();
proximity = require('geo-proximity').initialize(client);
socket_number = 0;

//make client avilable in index.js
exports.client = client;
//MONGO STUFF
/*mongoose = require('mongoose');
mongoose.connect('mongodb://ecstatic:dancefloor04@ds045252.mongolab.com:45252/ecstatic');

var Event = mongoose.model('Event', { host_username: String, title: String, start_time: Date, playlist: Array, userlist: Array });
var startupFest = new Event({ host_username: "Internet Wizards", title: "International Startup Fest", start_time: 1434261600000, playlist: [{title:"test1", link:"http://soundcloud.com/asdf"}, {title:"test2", link:"http://soundcloud.com/fdas"}], userlist: ["anonymous squid", "anonymous monkey"]});

startupFest.save(function (err) {
  if (err) // ...
  console.log('meow');
});*/


exports.setupEcstaticSockets = function(app){
    // Listen
    io = require('socket.io')({
    }).listen(app.listen(port));
    console.log("Listening on port " + port);

    // Handle new messages
    io.sockets.on('connection', function (socket) {


        //need to create a new subscriber for each socket connection.
        //subscriber = require('redis').createClient();
/*
        subscriber.on("message", function(channel, message){
            console.log("channel="+channel+", message="+message);
            var parsed_message = JSON.parse(message);
            switch(parsed_message.msg_type) {
                case 'join':
                    socket.emit("join", parsed_message.msg);
                    break;
                case 'leave_room':
                    socket.emit("leave_room", parsed_message.msg);
                    break;
                case 'new_owner':
                    socket.emit("new_owner", {"msg_type":"new_owner", "msg":parsed_message.msg});
                    break;
                case 'add_song':
                    console.log("add_song, channel="+channel);
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
                    socket.emit("send_text", parsed_message.msg);
                    break;
                case 'play':
                    socket.emit("realtime_player", {"msg_type":"play", "username":parsed_message.username});
                    break;
                case 'pause':
                    socket.emit("realtime_player", {"msg_type":"pause", "username":parsed_message.username});
                    break;
                case 'skip':
                    socket.emit("realtime_player", {"msg_type":"skip", "username":parsed_message.username});
                    break;
                case 'back':
                    socket.emit("realtime_player", {"msg_type":"back", "username":parsed_message.username});
                    break;
                case 'lock':
                    socket.emit("realtime_player", {"msg_type":"lock", "username":parsed_message.username});
                    break;
                case 'lock':
                    socket.emit("realtime_player", {"msg_type":"unlock", "username":parsed_message.username});
                    break;
                default:
                    console.log("parsed_message.msg_type="+parsed_message.msg_type);
                    console.log("problem in subscriber switch, parsed_message="+parsed_message);
            }
        });
*/
        //creates a new room
        socket.on('create_room', function (data) {
            client.get('room_counter', function(err, room_counter) {
                //if there is no room counter, set it to 1.
                if(!room_counter){
                    client.set('room_counter', 1, function(err, room_counter) {
                        if(err) console.log(err);
                    });
                    room_counter = 1;
                }
                //increment the number of rooms      
                client.incr('room_counter');          
                //Parse the create room message
                var is_event = false;
                create_room(data, room_counter, socket, is_event);
            });
        });
        


        //Joins an existing room
        socket.on('join_room', function (data) {
            console.log("Join_room");
            var params = JSON.parse(data);
            client.get(':1:room:' + params.room_number, function (err, room_info){
                client.lrange('list_of_users:'+params.room_number, 0, -1, function(err, users){
                    console.log("join room, room_info = "+room_info);
                    console.log("join room, is_event = "+params.is_event);
                    //if the room doesn't exist, then create it
                    if(room_info == null){
                       console.log("join_room, create event room => calling create_room on params.room_number="+params.room_number+", media_item="+params.media_item);
                       create_room(data, params.room_number, socket, params.is_event, params.media_item);
                    }

                    //else join the room: tell people you joined the room, add yourself to the list of users, and subscribe to updates.
                    else{
                        console.log("join_room, room_number="+params.room_number);
                        client.lpush('list_of_users:'+params.room_number, params.username);
                        //subscriber.subscribe(params.room_number);
                        socket.join(params.room_number);
                        //publisher.publish(params.room_number, JSON.stringify({"msg":params.username, "msg_type":"join"}));
                        socket.broadcast.to(params.room_number).emit("join", params.username);
                    }
                    client.set(":1:" + params.username+":room", params.room_number); 
                });
            });
        });

        //leaves an existing room
        socket.on('leave_room', function (data) {
            var params = JSON.parse(data);

            //logging
            console.log("leave_room, username="+params.username);
            console.log("leave_room, params.is_owner="+params.is_owner);
            console.log("leave_room, room_number="+params.room_number);

            //remove yourself from the list_of_users, get the count of users
            client.lrem('list_of_users:' + params.room_number, 1, params.username);
            client.llen('list_of_users:' + params.room_number, function (err, user_count) {
                console.log("leave_room, params.username="+params.username+", room_number_set_to="+0);
                client.set(":1:" + params.username+":room", 0); 

                //if you're the host of the room, and there's no one left in the room
                if(user_count == 0 && params.is_owner == "true") {
                    //destroy the room
                    console.log("leave room, destroy room");
                    client.del(':1:room:' + params.room_number);    
                    client.del('player:' + params.room_number);
                    //subscriber.unsubscribe(params.room_number);
                    socket.leave(params.room_number);
                }
                //if you're the host of the room, and there's someone left
                else if(user_count != 0 && params.is_owner == "true") {
                    console.log("leave room, transfer ownership");
                    client.lindex('list_of_users:' + params.room_number, 0, function (err, first_user){
                        console.log("leave_room, new_owner="+first_user);
                        client.get(':1:room:' + params.room_number, function (err, room_info_obj){
                            room_info_obj = JSON.parse(room_info_obj);
                            room_info_obj.host_username = first_user;
                            room_info_obj.room_name = first_user;
                            client.set(':1:room:'+params.room_number, JSON.stringify(room_info_obj));
                        });
                        //publisher.publish(params.room_number, JSON.stringify({"msg_type":"new_owner", "msg":first_user}));
                        socket.broadcast.to(params.room_number).emit("new_owner", {"msg":first_user});
                        
                        //Need to do this AFTER assigning a new owner
                        //publisher.publish(params.room_number, JSON.stringify({"msg_type":"leave_room", "msg":params.username}));
                        socket.broadcast.to(params.room_number).emit("leave_room", params.username);

                        console.log("leave_room, room_number="+params.room_number);
                        //subscriber.unsubscribe(params.room_number);
                        socket.leave(params.room_number);
                    });
                }
                //if there are people in the room, and you're not the owner
                else{
                    console.log("leave room, leave room");
                    //publisher.publish(params.room_number, JSON.stringify({"msg_type":"leave_room", "msg":params.username}));
                    socket.broadcast.to(params.room_number).emit("leave_room", params.username);
                    //subscriber.unsubscribe(params.room_number);
                    socket.leave(params.room_number);
                }
            });
        });

        socket.on('get_user_list', function (data) {
            var params = JSON.parse(data);
            client.lrange('list_of_users:'+params.room_number, 0, -1, function(err, users){
                socket.emit("return_get_user_list", users);
            });
        });

        socket.on('post_location', function (data) {
            try{
                var params = JSON.parse(data);
                proximity.addLocation(params.latitude, params.longitude, params.username,  function(err, reply){
                    if(err) {
                        console.error("post_location_err="+err);
                    }
                    else {
                        console.log("post_location, params.username="+params.username);
                        socket.emit('return_post_location');
                    }
                });
            }
            catch(err){
                console.log("post_location, Error: missed a location, "+ err);
            }
        });

        //Joins an existing room
        socket.on('get_rooms_around_me', function (data) {
            var params = JSON.parse(data);
            console.log("get_rooms_around_me, data="+data);
            proximity.location(params.username, function(err, location){
                proximity.nearby(location.latitude, location.longitude, 10000000000, function(err, people){
                    async.map(people, get_room_for_user, function(err, result){
                        console.log("get_rooms_around_me, people="+people);
                        console.log("get_rooms_around_me, result="+result);
                        if(!err){
                            console.log("get_rooms_around_me, result.length"+result.length);
                                //filter out all zeroes (representing people not in rooms)
                                var active_rooms = [];
                                for(var x = 0; x< result.length; x++){
                                    console.log("get_rooms_around_me, x="+x);
                                    console.log("get_rooms_around_me, result[x]="+result[x]);
                                    if(result[x] != 0){
                                        active_rooms.push(result[x]);
                                    }
                                }
                                //remove duplicate rooms
                                for(var y = 0; y < active_rooms.length; y++){
                                    for(var z = 0; z < active_rooms.length; z++){
                                        //don't remove a room if it is the same as itself
                                        if(y==z){
                                            continue;
                                        }
                                        //if the two rooms are the same, remove one
                                        if(active_rooms[y] == active_rooms[z]){
                                            active_rooms.splice(y, 1);
                                        }
                                    }
                                }

                            //The clean array without a bunch of zeroes representing people not in rooms
                            console.log("get_rooms_around_me, active_rooms="+active_rooms);
                            async.map(active_rooms, get_room_info, function(err, result){
                                console.log("get_rooms_around_me, result="+JSON.stringify(result));
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
            console.log("room_number="+params.room_number);
            //TESTED
            //publisher.publish(params.room_number, JSON.stringify({"msg":params, "msg_type":"send_text"}));
            socket.broadcast.to(params.room_number).emit("send_text", params);
            client.lpush(':1:room:'+params.room_number+':chat', data);
        });

        socket.on('get_chat_backlog', function (data){
            var params = JSON.parse(data);
            console.log("room_number="+params.room_number);
            client.lrange(':1:room:'+params.room_number+':chat', 0, -1, function(err, chatlog){
                console.log("chat="+chatlog);
                socket.emit("return_chat_backlog", {"chatlog":chatlog});
            });
        });

        //PLAYLIST
        socket.on('add_song', function (data) {
            var params = JSON.parse(data);
            console.log("add_song, params.room_number="+params.room_number);
            //TESTED
            //publisher.publish(params.room_number, JSON.stringify({"msg":{"song":params}, "msg_type":"add_song"}));
            socket.broadcast.to(params.room_number).emit("add_song", params);
            client.rpush(':1:room:'+params.room_number+':playlist', data);
        });

        socket.on('remove_song', function (data) {
            var params = JSON.parse(data);
            //TESTED
            //publisher.publish(params.room_number, JSON.stringify({"msg":params, "msg_type":"remove_song"}));
            socket.broadcast.to(params.room_number).emit("remove_song", params);
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
                
                //publisher.publish(params.room_number, JSON.stringify({"msg":params, "msg_type":"move_song"}));
                socket.broadcast.to(params.room_number).emit("move_song", params);
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
            client.get('player:'+params.room_number, function(err, player_state){
                
                //Variable Logging
                console.log("get_player_status, data="+data);
                console.log("get_player_status, params.room_number="+params.room_number);
                console.log("get_player_status, player_state="+player_state+", err="+err+", room_number="+params.room_number);
                socket.emit("get_player_status", {"player_state":player_state, "current_time": new Date().getTime()});
            });
        });

        socket.on('update_player_state', function (data) {
            console.log("update_player_state");
            //parse JSON
            var params = JSON.parse(data);
            update_player_state(params, client);
        });

        socket.on('player', function (data) {
            console.log("player");
            //parse JSON
            var params = JSON.parse(data);
            update_player_state(params, client);
            switch(params.msg_type) {
                case "play":
                    console.log("played");
                    //publisher.publish(params.room_number, JSON.stringify({"msg_type":"play", "username":params.username}));
                    socket.broadcast.to(params.room_number).emit("realtime_player", {"msg_type":"play"});
                    break;
                case "pause":
                    console.log("paused");
                    //publisher.publish(params.room_number, JSON.stringify({"msg_type":"pause", "username":params.username}));
                    socket.broadcast.to(params.room_number).emit("realtime_player", {"msg_type":"pause"});
                    break;
                case "skip":
                    console.log("skipped");
                    //publisher.publish(params.room_number, JSON.stringify({"msg_type":"skip", "username":params.username}));
                    socket.broadcast.to(params.room_number).emit("realtime_player", {"msg_type":"skip"});                    
                    break;
                case "back":
                    console.log("back");
                    //publisher.publish(params.room_number, JSON.stringify({"msg_type":"back", "username":params.username}));
                    socket.broadcast.to(params.room_number).emit("realtime_player", {"msg_type":"back"});
                    break;
                case "lock":
                    //publisher.publish(params.room_number, JSON.stringify({"msg_type":"lock", "username":params.username}));
                    socket.broadcast.to(params.room_number).emit("realtime_player", {"msg_type":"lock"});
                    break;
                case "unlock":
                    //publisher.publish(params.room_number, JSON.stringify({"msg_type":"unlock", "username":params.username}));
                    socket.broadcast.to(params.room_number).emit("realtime_player", {"msg_type":"unlock"});
                    break;
                default:
                    console.log("something bad happened to player");
            }   
        });
    });
}
//stores the playerstate, with a timestamp of when it was stored 
function update_player_state(params, client){
    console.log("update_player_state, params.room_number="+params.room_number);
    console.log("update_player_state, params.player_state="+JSON.stringify(params.player_state));
    params.player_state.timestamp = new Date().getTime();
    client.set('player:'+params.room_number, JSON.stringify(params.player_state));
}

function create_room(data_obj, room_number, socket, is_event, media_item){
    var params = JSON.parse(data_obj);
    //create the room info JSON
    var room_info_obj = {"host_username": params.username, "room_name": params.room_name, "room_number": room_number};
    
    //logging
    console.log("create_room, params.username="+params.username);
    console.log("create_room, params.room_name="+params.room_name);
    console.log("create_room, room_number="+room_number);
    console.log("create_room, room_info_obj="+JSON.stringify(room_info_obj));

    //room_info is stored with key: ":1:room:+room_number"
    client.set(':1:room:'+room_number, JSON.stringify(room_info_obj));    

    //can get room_number for user
    client.set(":1:"+params.username+":room", room_number); 
    
    //add yourself to the user list
    client.lpush('list_of_users:'+room_number, params.username, function(err) {});

    //join the room
    socket.join(room_number);

    //notify client of the new room 
    socket.emit('return_create_room', {"room_info":room_info_obj});
    console.log("create_room, is_event="+is_event);
    
    //initialize the player_state
    if(is_event){
        console.log("create_room, is_event="+is_event);
        client.rpush(':1:room:'+params.room_number+':playlist', media_item);
        socket.broadcast.to(params.room_number).emit("add_song", media_item);
        var player_state = {'is_playing': 0, 'is_locked': 1, 'playing_song_index':0, 'elapsed': 0, 'timestamp': new Date().getTime()};
    }
    else{
        var player_state = {'is_playing': 1, 'is_locked': 0, 'playing_song_index':0, 'elapsed': 0, 'timestamp': new Date().getTime()};
    }
    client.set('player:'+room_number, JSON.stringify(player_state));
}

function get_room_for_user(username, callback){
    client.get(":1:"+username+":room", function(err, room_number) {
        console.log("get_room_for_user, room_number="+room_number);
        console.log("get_room_for_user, username="+username);
        if(room_number == null){
            console.log("get_room_for_user, PATH room_number=null");
            callback(null, 0);
        }
        else{
            callback(null, room_number);
        }
    });
}

function get_room_info(room_number, callback){
    client.get(':1:room:'+room_number, function (err, room_info) {
        var room_info_obj = JSON.parse(room_info);
        //logging room info
        console.log("get_room_info, room_number="+room_number);
        console.log("get_room_info, room_info_obj.host_username="+room_info_obj.host_username);
        
        if(room_info_obj == null){
            console.log("room doesn't exist");
            return;
        }

        client.lrange('list_of_users:'+room_number, 0, -1, function(err, users){
            proximity.location(room_info_obj.host_username, function(err, host_location){
                console.log("get_room_info, host_location="+JSON.stringify(host_location));
                callback(null, {"room_info":room_info_obj, "users":users,"host_location":host_location});
            });
        });
    });
}    


