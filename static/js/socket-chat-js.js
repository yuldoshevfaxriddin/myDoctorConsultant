const socket = io();

socket.on("connect", () => {
    console.log("You're connected");
})

function sendMessage(chat_id,data){
    var message = JSON.stringify({'chat_id':chat_id,'message':data});
    // message = JSON.stringify({'username':'test','message':messageInput.value});
    socket.emit("message", message);
}

socket.on('message', (message) => {
    message = JSON.parse(message);
    if(chat_id==active_chat_id){
        var chat_id = message['chat_id'];
        var name = message['username'];
        var image = message['image'];
        var msgText = message['text'];
        appendMessage(name, image, "left", msgText);    
    }
    alert('ok !');
})

function getMessages(chat_id){
    var request = "/get-data/"+chat_id;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var respons = JSON.parse(this.responseText);
        return respons;
    }
    };
    xhttp.open("GET", request,false);
    xhttp.send();
}