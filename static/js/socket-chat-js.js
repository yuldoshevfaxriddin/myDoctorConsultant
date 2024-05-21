const socket = io();

socket.on("connect", () => {
    console.log("You're connected");
})

function sendMessage(user_id_1,user_id_2,text){
    var data = {user_id_1:user_id_1, user_id_2:user_id_2, text:text};
    var message = JSON.stringify(data);
    // message = JSON.stringify({'username':'test','message':messageInput.value});
    socket.emit("sendMessage", message);
    // alert("bahar ketdi");
}

socket.on('sendMessage', (message) => {
    // alert("habar keldi qara"); 
       var data = JSON.parse(message);
       var user_id_1 = data['user_id_2']; // client 
    var user_id_2 = data['user_id_1']; // current user
    var text = data['text'];
    var time = new Date(1000 * data['time'])
    if(userId.value==user_id_1){
        return ;
    }
    if(document.getElementById(user_id_1) == null){
        appendUsersList(data);
    }else{
        if(active_user == user_id_1){
            var name = document.getElementById(user_id_1).children[1].children[0].textContent; //chatni egasi
            var image = document.getElementById(user_id_1).children[0].children[0].src; // chatni egasi
            appendMessage(name, image, "left", text,time); 
        }
    }
    if(user_id_1 != active_user){
        let a = document.getElementById(user_id_1);
        a.children[0].children[1].style.display = 'block';
        playNotification();
        console.log('play sound');
    }
    console.log("ok ");  

})
