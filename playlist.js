    socket.on('subscribe_to_playlist', function (data) {

    });

    socket.on('push_song', function (data) {
        console.log("data="+data);
        client.get(data.username, function(err, room_number) {
            client.lpush(':1:room:'+room_number+':playlist', data);
        });
    });

    socket.on('pop_song', function (data) {
        console.log("data="+data);
        console.log("pop");
        client.get(data.username, function(err, room_number) {
            client.rpop(':1:room:'+room_number+':playlist', function(err, track) {
                socket.emit("pop_song", track);
            });
        });
    });

    socket.on('remove_song', function (data) {
        console.log("data="+data);
        client.get(data.username, function(err, room_number) {
            client.lrem(':1:room:'+room_number+':playlist', "1", data);
        });
    });

    socket.on('move_song', function (data) {
        console.log("data="+data);
        client.get(data.username, function(err, room_number) {
            client.linsert(':1:room:'+room_number+':playlist', "BEFORE", data.before, data.to_insert, function(err, val) {
                client.lrem(':1:room:'+room_number+':playlist', "1", data);
            });
        });
    });
