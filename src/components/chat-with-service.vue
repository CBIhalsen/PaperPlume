<template>
<div id="chat-window" class="chat-window">
        <div class="chat-header" id="chat-header" style="font-size:1rem;">Chat with Vee
<!--            <i class="fa-solid fa-angles-down"></i> fa-solid fa-angles-up-->
            <i class="fa-solid fa-angles-down" @click="windowdown" id="fa-angles-down" style="color: #9bb6e4; margin-left: 100%;cursor: pointer;"></i>
            <i class="fa-solid fa-angles-up" @click="windowup" id="fa-angles-up" style="color: #9bb6e4; margin-left: 100%;display: none;cursor: pointer"></i>
        </div>

        <div class="chat-body" id ="chat-body">
            <div class="existed-message-container" style="margin-top: 15px;margin-bottom: 0px;">
                <span class="icon-service"><i class="fa-solid fa-headset" style="color: #768bad;"></i></span> <div class="chat-message-existed" data-lang-key="chats"  >Are you looking for help in creating a paper title?</div>`


            </div>
            <!-- Message content here -->
        </div>

        <div class="chat-footer" id="chat-footer">
 <button class=" magic" id ="new-topic" @click="deleteMessage()" data-bs-toggle="tooltip" data-bs-placement="top" title="New topic" ><i class="fa-solid fa-wand-magic-sparkles " style="color:#f5f5f5; font-size: 15px;"></i></button>
            <div class="icon-container" @mouseover="imouseover" @mouseout="imouseout" id = "magic-container">

        <textarea class="chat-input" id="chat-textarea"  @input="textareainput" placeholder="Type a message..." @keydown.enter.prevent="sendMessage" v-model="inputText"></textarea>

           <button style="padding: 0px; background: transparent; border: none; cursor: pointer; outline: none !important;"><i class="fa-solid fa-arrow-right  chat-send" id="chat-send" @click=sendMessage ></i></button>
  <div id="chat-char-counter" class="chat-char" v-show="inputText.length !== 0">{{ inputText.length }} / 1000</div>
<!--                <div id="chat-char-counter"  > </div>-->
            </div>

        </div>
    </div>

</template>

<script>




// 获取聊天窗口和输入框元素
const chatBody = document.getElementById("chat-body");
const chatInput = document.getElementById("chat-textarea");
chatBody,chatInput




// 监听发送按钮的点击事件




        function getAccessToken() {
  const tokenString = localStorage.getItem('access_token');
  if (!tokenString) {
    return null; // 如果没有access_token，则返回null
  }

  const tokenObject = JSON.parse(tokenString);
  return tokenObject.token;
}

export default {
    data() {
    return {
      inputText: ''
    };
  },
          mounted() {
          },
  methods:{
deleteMessage(){
    const elements = document.querySelectorAll(".chat-message-container");
elements.forEach(element => {
  element.remove();
});

},



  windowdown() {
document.getElementById('chat-body').style.display = 'none';
document.getElementById('chat-footer').style.display = 'none';
document.getElementById('chat-window').style.height = '40px';
document.getElementById('fa-angles-down').style.display = 'none';


document.getElementById('fa-angles-up').style.display = 'inline-block';
    },


    // 监听点击事件
     windowup() {
document.getElementById('chat-body').style.display = '';
document.getElementById('chat-footer').style.display = 'flex';
document.getElementById('chat-window').style.height = '400px';
document.getElementById('fa-angles-up').style.display = 'none';
document.getElementById('fa-angles-down').style.display = 'inline-block';
    },
// 发送消息的函数
 sendMessage() {
    const chatBody = document.getElementById("chat-body");
const chatInput = document.getElementById("chat-textarea");


if (chatInput.value.length == 0) {
    return ;
}
// const textarea = document.getElementById('chat-textarea');
// textarea.scrollTop = textarea.scrollHeight - textarea.clientHeight;


    // var chat_body = document.getElementById("chat-body");
    // chat_body.scrollTop = chat_body.scrollHeight;

     const accessToken =  getAccessToken();
     const chatMessages = Array.from(document.querySelectorAll('.chat-message')).map(element => element.innerText);
     const userMessages = Array.from(document.querySelectorAll('.chat-message-user')).map(element => element.innerText);

  const message = chatInput.value; // 获取输入框中的文本内容

     const messageContainer = document.createElement("div");
   messageContainer.classList.add("chat-message-container");
   messageContainer.innerHTML = `<span class="icon-service-user"><i class="fa-regular fa-face-kiss-wink-heart" style="color: #e3ee4f;"></i></span> <div class="chat-message-user">${message}</div>`;

    chatBody.appendChild(messageContainer);

   const chatservice = document.getElementById("chat-body");

  // 向后端发送消息
  fetch("https://akkca.verseeding.com/api/proxy/send-message", {
    method: "POST",
     body: JSON.stringify({
    chatMessages: chatMessages,
    userMessages: userMessages,
    prompt: message
  }),
    headers: {
      "Content-Type": "application/json",
         'Authorization': `Bearer ${accessToken}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {
           const messageContainer2 = document.createElement("div");
      if (data.sender === "service") {

   messageContainer2.classList.add("chat-message-container");
   messageContainer2.innerHTML = `<span class="icon-service"><i class="fa-solid fa-headset" style="color: #768bad;"></i></span> <div class="chat-message"> ${data.message}</div>`;
    //
    chatservice.appendChild(messageContainer2);
    var chat_body = document.getElementById("chat-body");
    chat_body.scrollTop = chat_body.scrollHeight;

          }

    });

  // 清空输入框
  chatInput.value = "";
},

      imouseover() {
    // this.style.width = "calc(100% - 80px)";
        document.getElementById('magic-container').style.marginLeft = '0px';
      document.getElementById('new-topic').style.display = 'None';
       document.getElementById('new-topic').style.opacity = '1';

},

imouseout() {
        let textarea = document.getElementById("chat-textarea");
        if (textarea && textarea.value.trim() == ""){
           document.getElementById('chat-char-counter').style.display = 'none'
           document.getElementById('new-topic').style.opacity = '1';
            document.getElementById('new-topic').style.display = 'inline';
                 document.getElementById('chat-textarea').style.height = '40px';
                         document.getElementById('magic-container').style.marginLeft = '2.9rem';
                      document.getElementById('magic-container').style.height = '45px';



        }


        if (textarea && textarea.value.trim() !== ""){
                 document.getElementById('new-topic').style.opacity = '0';
               document.getElementById('new-topic').style.display = 'none';
                          document.getElementById('chat-char-counter').style.display = 'none';
           document.getElementById('chat-char-counter').style.display = 'inline-block';
            document.getElementById('chat-textarea').style.height = '65px';

              document.getElementById('magic-container').style.height = '90px';


        }

    },

        textareainput() {
        let textarea = document.getElementById("chat-textarea");
                if (textarea && textarea.value.trim() !== ""){
                document.getElementById('new-topic').style.opacity = '0';
               document.getElementById('new-topic').style.display = 'none';
                          document.getElementById('chat-char-counter').style.display = 'none';
           document.getElementById('chat-char-counter').style.display = 'inline-block';
            document.getElementById('chat-textarea').style.height = '65px';
               document.getElementById('magic-container').style.marginLeft = '0px';
              document.getElementById('magic-container').style.height = '90px';


        }

        },



},

}

</script>

<style>

</style>
