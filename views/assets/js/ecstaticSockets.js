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
subscriber = require('redis').createClient();
proximity = require('geo-proximity').initialize(client);

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
                default:
                    console.log("problem in subscriber switch");
            }
        });

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
                console.log("create_room, room_counter="+room_counter);
                //Parse the create room message
                console.log("create_room, data = "+data);
                console.log("create_room, data.username="+data.username);
                console.log("create_room, data.room_name="+data.room_name);
                create_room(data, room_counter, socket);
            });
        });
        


        //Joins an existing room
        socket.on('join_room', function (data) {
            var params = JSON.parse(data);
            client.get(':1:room:' + params.room_number, function (err, room_info){
                client.lrange('list_of_users:'+params.room_number, 0, -1, function(err, users){
                    console.log("join room, room_info = "+room_info);
                    //if the room doesn't exist, then create it
                     if(typeof room_info === 'undefined'){
                        console.log("room doesn't exist");
                        create_room(params, params.room_number, socket);
                     }

                     //else join the room
                     else{
                        client.lpush('list_of_users:'+params.room_number, params.username);
                        publisher.publish(params.room_number, JSON.stringify({"msg":params.username, "msg_type":"join"}));
                        subscriber.subscribe(params.room_number);
                     }
                });
            });
        });

        //leaves an existing room
        socket.on('leave_room', function (data) {
            var params = JSON.parse(data);
            console.log("leave_room, username="+params.username+", room_number="+params.room_number);
            client.llen('list_of_users:' + params.room_number, function (count) {
                console.log("listofusersCountBEFORE="+count);
            });

            client.lrem('list_of_users:'+params.room_number, 1, params.username);

            client.llen('list_of_users:' + params.room_number, function (count) {
                //if you're the host of the room, and there's no one left in the room, and you leave
                if(count == 0 && params.is_owner) {
                    //destroy the room
                    console.log("count == 0 && params.is_owner");
                        client.del(':1:room:'+params.room_number);    
                        client.del('player:'+params.room_number);
                }

                //if you're the host of the room, and there's someone left
                else if(count != 0 && params.is_owner) {
                    //pick someone from the list to become host
                    console.log("count != 0 && params.is_owner");
                }

                //if there are people in the room, and you're not the owner
                else{
                    //remove yourself from the user list 
                    console.log("count != 0 && !params.is_owner");
                }


            });
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
            try{
                var params = JSON.parse(data);
                proximity.addLocation(params.latitude, params.longitude, params.username,  function(err, reply){
                    if(err) {
                        console.error("post_location_err="+err);
                    }
                    else {
                        socket.emit('return_post_location');
                    }
                });
            }
            catch(err){
                console.log("error in post_location", err);
            }
        });

        //Joins an existing room
        socket.on('get_rooms_around_me', function (data) {
            var params = JSON.parse(data);
            console.log("get_rooms_around_me, data="+data);
            proximity.location(params.username, function(err, location){
                proximity.nearby(location.latitude, location.longitude, 10000000000, function(err, people){
                    async.map(people, get_room_for_user, function(err, result){
                        if(!err){
                            async.map(result, get_room_info, function(err, result){
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
            publisher.publish(params.room_number, JSON.stringify({"msg":params, "msg_type":"send_text"}));
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
            console.log("return_get_player_status, params.room_number="+params.room_number);
            client.get('player:'+params.room_number, function(err, player_state){
                console.log("return_get_player_status, player_state="+player_state+", err="+err+", room_number="+params.room_number);
                socket.emit("return_get_player_status", {"player_state":player_state, "current_time": new Date().getTime()});
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
            client.set('player:'+params.room_number, JSON.stringify(params.player_state));
            switch(params.msg_type) {
                case "play":
                    console.log("played");
                    publisher.publish(params.room_number, JSON.stringify({"msg_type":"play", "username":params.username}));
                    break;
                case "pause":
                    console.log("paused");
                    publisher.publish(params.room_number, JSON.stringify({"msg_type":"pause", "username":params.username}));
                    break;
                case "skip":
                    console.log("skipped");
                    publisher.publish(params.room_number, JSON.stringify({"msg_type":"skip", "username":params.username}));
                    break;
                case "back":
                    console.log("back");
                    publisher.publish(params.room_number, JSON.stringify({"msg_type":"back", "username":params.username}));
                    break;
                case "lock":
                    publisher.publish(params.room_number, JSON.stringify({"msg_type":"lock", "username":params.username}));
                    break;
                default:
                    console.log("something bad happened to player");
            }   
        });
    });
}

function create_room(data_obj, room_number, socket){
    var params = JSON.parse(data_obj);
    console.log("create_room, params.username="+params.username);
    console.log("create_room, params.room_name="+params.room_name);
    //create the room info JSON
    var room_info_obj = {"host_username": params.username, "room_name": params.room_name, "room_number": room_number};
    console.log("create_room, room_info_obj="+room_info_obj);
    //room_info is stored with key: ":1:room:+room_number"
    client.set(':1:room:'+room_number, JSON.stringify(room_info_obj));    

    //can get room_number for user
    client.set(":1:"+data_obj.username+":room", room_number); 
    
    //add yourself to the user list
    client.lpush('list_of_users:'+room_number, data_obj.username, function(err) {
        console.log("create_room, list_of_users_err="+err);
    });

    //subscribe to the room
    subscriber.subscribe(room_number);

    //notify client and other users of the new room 
    socket.emit('return_create_room', {"room_info":room_info_obj});
    publisher.publish("ecstatic", JSON.stringify({"msg":room_info_obj, "msg_type":"create_room"}));

    //initialize the player_state
    var player_state = {'is_playing': 0, 'is_locked': 0, 'playing_song_index':0, 'elapsed': 0, 'timestamp': new Date().getTime()};
    console.log("create_room, player_state="+JSON.stringify(player_state)+", room_number="+room_number);
    client.set('player:'+room_number, JSON.stringify(player_state));
}

function get_room_for_user(username, callback){
    client.get(":1:"+username+":room", function(err, room_number) {
        try{
            console.log("get_room_for_user, err="+err+", room_number="+room_number);
            callback(null, room_number);
        }
        catch(err){
            console.log("caught error, room_number="+room_number);
        }
    });
}

function get_room_info(room_number, callback){
    client.get(':1:room:'+room_number, function (err, room_info) {
        console.log("get_room_info, room_info="+room_info+", err="+err);
        if(room_info === null){
            console.log("room doesn't exist");
            return;
        }

        client.lrange('list_of_users:'+room_number, 0, -1, function(err, users){
            try{
                proximity.location(room_info.host_username, function(err, host_location){
                    callback(null, {"room_info":JSON.parse(room_info), "users":users,"host_location":host_location});
                });
            }
            catch(err){
                callback(null, "get_room_info error. Someting to do with host location maybe?");
                console.log("get_room_info=", err);
            }
        });
    });
}    


