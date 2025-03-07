

function chat_handlers(socket) {

    socket.on("fire", () => {
        socket.emit("ice");
    });

    socket.on("chat_channel_get_typers", function (channel) {
        socket.has_permission("Chat Channel", channel).then(() => {
            // Show who's typing in the channel - only send this to the user who requested it
            // User emits this event when they open the channel
            notify_typing({ socket, channel, toUser: true });

        });
    });

    socket.on("chat_channel_typing", function (channel) {

        // Join the typing room and notify users in the channel room that the user is typing
        socket.join(channel_typing_room(channel));

        notify_typing({ socket, channel, toUser: false });

    })

    socket.on("chat_channel_typing_stopped", function (channel) {


        // Leave the typing room and notify users in the channel room that the user has stopped typing

        socket.leave(channel_typing_room(channel));

        notify_typing({ socket, channel, toUser: false });

    })

}

function notify_typing(args) {
    if (!(args && args.socket && args.channel)) return;

    const socket = args.socket;
    const channel = args.channel;

    const typers_room = channel_typing_room(channel);

    const clients = Array.from(socket.nsp.adapter.rooms.get(typers_room) || []);

    let users = [];

    socket.nsp.sockets.forEach((sock) => {
        if (clients.includes(sock.id)) {
            users.push(sock.user);
        }
    });

    const channel_room = args.toUser ? user_room(args.socket.user) : open_doc_room("Chat Channel", channel);

    // notify
    socket.nsp.to(channel_room).emit("chat_channel_typers", {
        channel,
        users: Array.from(new Set(users)),
    });
}

const channel_typing_room = (channel) => "chat_channel_typing:" + channel;
const open_doc_room = (doctype, docname) => "open_doc:" + doctype + "/" + docname;
const user_room = (user) => "user:" + user;

module.exports = chat_handlers