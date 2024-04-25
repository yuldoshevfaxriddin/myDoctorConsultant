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
    console.log(data);
    var name = document.getElementById(user_id_1).children[1].children[0].textContent; //chatni egasi
    var image = document.getElementById(user_id_1).children[0].children[0].src; // chatni egasi
    appendMessage(name, image, "left", text,time); 
    console.log("ok ");  

})
