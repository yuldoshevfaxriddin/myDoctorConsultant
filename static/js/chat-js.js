// alert("salom");
const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const configButton = get(".msger-header-options");
const searchButton = get(".msger-header-options-2");
const activeUserChat = get(".user-chat-info");
const mainUser = get(".user-info");
const usersList = get(".users-list");

var searchInput = document.getElementById("search-button");
const userId = document.getElementById("user_id");;

var nextConfigButton = true;
var nextSearchButton = true;

var active_user = -1;
var active_chat_id = document.getElementById("chat_id");

const BOT_MSGS = [
"Salom, Sizga qanda yordam bera olaman ?",
"Uzr tushunmadim ?!",
"Ushbu dastur beta versiyada taqdim etilmoqda. ",
"Ushbu chat dasturidan foydalanganingiz uchun minnddormiz !",
"Rahmat ! :))",
"Uzr vaqtim yo'q :("];


// Icons made by Freepik from www.flaticon.com
var BOT_IMG = "https://static.vecteezy.com/system/resources/thumbnails/007/225/199/small/robot-chat-bot-concept-illustration-vector.jpg";
var BOT_IMG = activeUserChat.children[0].children[0].getAttribute('src');
var PERSON_IMG = mainUser.children[0].children[0].getAttribute('src');

var BOT_NAME = "BOT";
var BOT_NAME = activeUserChat.children[1].children[0].textContent;
var PERSON_NAME = mainUser.children[1].children[0].textContent;

msgerForm.addEventListener("submit", event => {
  // serverga malumot yuborilsin
    event.preventDefault();
    const msgText = msgerInput.value;
    if (!msgText) return;

    var user_id_1 = active_chat_id.value; // client 
    var user_id_2 = userId.value; // current user
    var text = msgText;
    sendMessage(user_id_1,user_id_2,text);
  var time = new Date();
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText, time);
  msgerInput.value = "";
  // botResponse();
});
/*
get("html").addEventListener("click",()=>{
  if(next==true){
    get(".config-button").style.display= "none";
  }
});
*/
configButton.addEventListener("click",() =>{
  // alert('click');
  if(nextConfigButton === true){
    configButton.classList.add("active-button");
    get(".config-button").style.display= "block";
  }
  else{
    configButton.classList.remove("active-button");
    get(".config-button").style.display= "none";
  }
  nextConfigButton = ! nextConfigButton;

});

searchButton.addEventListener("click",() =>{
  if(nextSearchButton === true){
    searchButton.classList.add("active-button");
    get(".search-button").style.display= "block";
    searchInput.focus();
  }
  else{
    searchButton.classList.remove("active-button");
    get(".search-button").style.display= "none";
  }
  nextSearchButton = ! nextSearchButton;
});

function appendMessage(name, img, side, text, time) {
  // var date = formatDate(new Date());
  var date = formatDate(time);
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${date}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function botResponse() {
  const r = random(0, BOT_MSGS.length - 1);
  const msgText = BOT_MSGS[r];
  const delay = msgText.split(" ").length * 100;

  setTimeout(() => {
    appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
  }, delay);
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

function selectUser(id){
  // var id = this.event.srcElement.id;
  console.log(id);
  if(id==active_chat_id.value){
    return 
  }
  deleteMsgerChat();
  setUserChat(id);
  var user_1 = active_chat_id.value;
  var user_2 = userId.value;
  var data = '';
  var request = "/get-messages?user_1="+user_1+"&user_2="+user_2;
  console.log(request);
  // var request = "/get-messages?user_1=4&user_2=3";
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
      var respons = JSON.parse(this.responseText);
      data = respons;
  }
  };
  xhttp.open("GET", request,false);
  xhttp.send();

  console.log(data);
  setMessageChat(data);
}

function setUserChat(user_id){
  /* new user */
  let user_chat = document.getElementById(user_id);
  let user_chat_img = user_chat.children[0];
  let user_chat_info = user_chat.children[1];
  let user_chat_img_src = user_chat_img.children[0].getAttribute('src');
  let user_chat_name = user_chat_info.children[0].textContent;
  let user_chat_bio = user_chat_info.children[1].textContent;

  /* old user */
  // let old_user_chat = document.getElementById(active_user);
  if(active_user != user_id){
    let old_user = activeUserChat.children;
    let old_user_img = old_user[0].children[0];
    let old_user_info = old_user[1];
    let old_user_name = old_user_info.children[0];
    let old_user_bio = old_user_info.children[1];
    
    old_user_img.setAttribute("src",user_chat_img_src)  ;
    old_user_name.textContent = user_chat_name;
    old_user_bio.textContent = user_chat_bio;

    active_chat_id.value = user_id ;

    BOT_IMG = user_chat_img_src;
    BOT_NAME = user_chat_name;

    // console.log(old_user_img);
    // console.log(old_user_info);
    // console.log(old_user_name);
    // console.log(old_user_bio);    
  }
  active_user = user_id;  
}

function deleteMsgerChat(){
  while (msgerChat.firstChild) {
    msgerChat.removeChild(msgerChat.lastChild);
  }
}
function setMessageChat(data){
  // habarlarni joylashtirish
  console.log(data.length);
//  globaldata = data;
  for(let i=0;data.length;i++){
    
    // var chat_id = data[i][1]; //chat id
    var user_id = data[i][2]; //user id
    var username ;
    var image ;
    var time = new Date(1000 * data[i][4]);
    var msgText = data[i][3];
    if (user_id==userId.value){
      username = document.getElementById('user_id').parentElement.children[0].textContent;
      image = document.getElementById('user_id').parentElement.parentElement.children[0].children[0].src;
      appendMessage(username, image, "right", msgText,time);
    }
    else{
      var username = document.getElementById(user_id).children[1].children[0].textContent;
      var image = document.getElementById(user_id).children[0].children[0].src;
      appendMessage(username, image, "left", msgText,time);
    }
  }

}

function appendUsersList(data){
  let new_user_name = data['user_name_2']; // client 
  let new_user_bio = data['user_bio_2'];
  let new_user_img = data['user_img_2'];
  let new_user_id = data['user_id_2'];
  let new_message =  data['text'];
  let time = new Date(1000 * data['time'])
  setTestUser(new_user_id,new_user_name,new_user_bio,new_user_img);
}

function setTestUser(id,name,bio,img){
  const userHTML = `
    <div class="user-chat"  id="${id}" onclick="selectUser('${id}')">
            <div class="user-img">
              <img src="${'static/'+img}"alt="">
            </div>
            <div class="user-name">
              <h3>${name} </h3>
              <p>${bio}</p>
            </div>
          </div>
  `;
  usersList.insertAdjacentHTML("beforeend", userHTML);
  // usersList.scrollTop += 500;
}

function getMessages(user_1,user_2){
}

