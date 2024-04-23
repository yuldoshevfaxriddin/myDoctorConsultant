// alert("salom");
const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const configButton = get(".msger-header-options");
const activeUserChat = get(".user-chat-info");
const mainUser = get(".user-info");

const userId = document.getElementById("user_id");;

var nextConfigButton = true;

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
  sendMessage();
    // serverga malumot yuborilsin
    event.preventDefault();
  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";
  botResponse();
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
  // alert(get(".config-button").style.);
});

function appendMessage(name, img, side, text, time) {
  // var date = formatDate(new Date());
  var date = time;
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

function selectUser(){
  var id = this.event.srcElement.id;
  deleteMsgerChat();
  setUserChat(id);
  var data = getMessages(active_chat_id);
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
  for(var i=0;data.length;i++){
    
    var chat_id = data[i]['chat_id'];
    var name = data[i]['username'];
    var image = data[i]['image'];
    var time = data[i]['time'];
    var msgText = data[i]['text'];
    if (data[i]['user_id']==userId){
      appendMessage(BOT_NAME, BOT_IMG, "right", msgText,time);
    }
    else{
      appendMessage(BOT_NAME, BOT_IMG, "left", msgText,time);
    }
  }

}

