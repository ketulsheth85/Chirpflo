function initializeChatWidget(company, testName, heading, sub_heading, avtarImg, icon, bg_color, popup_status, timer_count, styleString, client_bubble_color) {
  // HTML structure

  document.body.innerHTML += `
    <button id="chat-circle" class="btn btn-raised" style="background-color:${bg_color}">
    <img id="chat-image" src="${icon}" alt='chatbox-logo'/>
    <div class="close-icon" id='close-box' style="display: none;">
      &#10005;
    </div>
    </button>
    <div class='chatbot-popup-msg'>
          <div class='chatbot-popup-closeIcon'>
          &#10005;
          </div>
          <div class='chatbot-popup-inner'>
            <div class='flex-shrink-0 chatbot-popup-logo'>
              <img src=${avtarImg} alt='chatbox-logo' />
            </div>
            <div class='chatbot-popup-text'>
              <p class='' id='chatbot-popup-wlmsg'></p>
            </div>
          </div>
        </div>
  <div id="chat-widget">
  <div class="background-svg">
  <svg width="432" height="149" viewBox="0 0 296 98" fill="${bg_color}" xmlns="http://www.w3.org/2000/svg">
  <g filter="url(#filter0_d_74_92)">
    <path d="M135 84.5C62.5 90 0 61.5 0 61.5V-2H296.5V65.5C217.5 65.5 216 78.3552 135 84.5Z" fill="${bg_color}"/>
  </g>
  <defs>
    <filter id="filter0_d_74_92" x="-8" y="-6" width="312.5" height="103.205" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feFlood flood-opacity="0" result="BackgroundImageFix"/>
      <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
      <feOffset dy="4"/>
      <feGaussianBlur stdDeviation="4"/>
      <feComposite in2="hardAlpha" operator="out"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.0216493 0 0 0 0 0.0335989 0 0 0 0 0.179167 0 0 0 0.25 0"/>
      <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_74_92"/>
      <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_74_92" result="shape"/>
    </filter>
  </defs>
</svg>

  </div>
    <div class='chatbox-header' >  
      <div class='chabox-header-iconbox'>
        <div class='chatbox-header-text'>
          <h3 class=''>${testName}</h3>
          <p class=''>${heading}</p>
          <p class=''>${sub_heading}</p>          
        </div>
        <div class='chatbox-logo'>
          <img src="${avtarImg}" alt='chatbox-logo' />
        </div>
      </div>
    </div>
    <div class="chatbot-body">
      <div id="chat-messages" style="height:${window.innerHeight - 360}px"></div>
      
    </div>
    <hr/>
    <div class='chatbox-group'>
        <input type="text" id="chat-input" value="" placeholder="Type message...">
        <div class=' chatbox-input-group'>
          <button id="chat-send"><span>&#10148;</span></button>
        </div>
      </div>
  </div>
`;

  // CSS styles for the chat widget

  var styles = `
  .chatbox-header {
   display: flex;
   align-items: center;
   justify-content: space-between;
   padding: 10px 20px;
   border-radius: 12px 12px 0px 0px;
   height: 100px;
 }
 #chat-circle img {
   width:50px;
   height:50px;
   border-radius:50%;
 }

 .chabox-header-iconbox {
   display: flex;
   align-items: center;
   justify-content: space-between;
   width: 100%;
 }

  .chatbox-header .chatbox-logo img {
   width: 100%;
   height: 100%;
   border-radius:50%;
   display: flex;
   object-fit: cover;
   align-items: center;
   justify-content: center;
 }

  .chatbox-header .chatbox-header-text{
    margin: -25px 0px 0px 0px;
 }

  .chatbox-header .chatbox-header-text h3 {
   color:#ffffff;
   margin: 0;
   font-size: 25px;
 }
  .chatbox-header .chatbox-header-text h6 {
   color:#ffffff;
   margin:0;
   font-size: 18px;
 }

 .chatbox-header .chatbox-header-text p {
   color:#ffffff;
   margin:0;
   font-size: 17px;
 }

 .close-icon {
   color:#ffffff;
   font-size: 35px;
   cursor: pointer;
 }

 .chatbox-group {
   position: relative;
   display: flex;
   align-items: center;
   justify-content: space-between;
   height: 50px;
   margin:1.2rem;
 }
 .chatbox-group input::placeholder {
   font-size: 17.6px;
   padding-left: 0px;
   color: #000;
   letter-spacing: 0.8px;
 }

  #chat-input:focus-visible {
    border: 1px solid ${client_bubble_color};
   background-color: #white;
   color: #000;
   box-shadow: none;
   outline: 0;
 }

 .chatbox-input-group {
   position: absolute;
   right: 2%;
 } 

 .chatbox-input-group button {
   width: 100% !important;
   height: 100% !important;
   background: ${client_bubble_color} !important;
   border: none !important;
 }
 .chatbot-body {
  padding: 1rem 1rem 0rem 1rem;
}
#chat-messages {
  -ms-overflow-style: none; /* Internet Explorer 10+ */
  scrollbar-width: none; /* Firefox */
}
#chat-messages::-webkit-scrollbar {
  display: none; /* Safari and Chrome */
}
 #chat-widget {
  position: fixed;
  bottom: 10%;
  right: 3%;
  width: 400px;
  border: 1px solid #ccc;
  box-shadow: 4px 4px 32px rgba(0, 0, 0, 0.3);
  font-family: Arial, sans-serif;
  font-size: 14px;
  border-radius: 12px;
  overflow:hidden;
  background:${styleString};
  background-repeat: no-repeat;
  background-size: 100% 100%;
  z-index:9999;
}

 #chat-messages {
   max-height: 400px;
   overflow-y: auto;
 } 

 #chat-input {
   width: 100%;
   padding: 5px 20px;
   border-radius: 34px;
   height:100%;
  border: none;
  font-size: 17.6px;
  color: #000;
  background-color: #ffffff;
  border: 1px solid ${client_bubble_color};
 }

  #chat-send {
   padding: 5px 10px;
   background-color: #4CAF50;
   border: none;
   color: white;
   border-radius: 34px;
   cursor: pointer;
   height:100%;
 }

 #chat-send span {
   font-size:25px;
 }

 #chat-widget {
   display: none;
 }

 #chat-widget.open {
   display: block;
 }

 #chat-circle {
  position: fixed;
    right: 3%;
    bottom: 2%;
    cursor: pointer;
    width: 65px;
    height: 65px;
    min-width: 65px;
    border-radius: 50%;
    display: flex;
    border:none;  
    justify-content: center;
    align-items: center;
   box-shadow: 0px 3px 16px 0px rgba(0, 0, 0, 0.6), 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 1px 5px 0 rgba(0, 0, 0, 0.12);
   z-index: 99999;
 }

 .question-text-box {
   display: flex;
   justify-content: end;
   align-items: center;
   margin-top: 15px;
 }

 .question-text-box .chatbox-user-quetext {
   background: ${client_bubble_color};
   border-radius: 15px;
   padding: 15px;
   font-size: 17px;
   color: #ffffff;
   word-break: break-all;
 }
 .question-text-box .chatbox-user-quetext p{
  margin:0;
  font-size: 17px;
 }

 .answer-text-box {
   margin-top: 15px;
   width:95%;
 }
 .background-svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
}

.chatbox-logo {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  position: relative;
  bottom: -40px;
}

 .answer-text-box .chatbox-user-anstext {
  background: lightgray;
  border-radius: 15px;
  padding: 15px;
  margin-top:10px;
 } 
 .answer-text-box .chatbox-user-anstext p{
  margin:0;
  font-size: 17px;
  color: #ffffff;
}
.threedot-loader {
  padding: 22px 30px;
}

.snippet {
  display: flex;
  justify-content: flex-start;
  width: 100%;
  align-items: flex-end;
}

.dot-flashing {
  position: relative;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: ${bg_color};
  color: #04bcff;
  animation: dot-flashing 1s infinite linear alternate;
  animation-delay: 0.5s;
}

.dot-flashing::before,
.dot-flashing::after {
  content: '';
  display: inline-block;
  position: absolute;
  top: 0;
}

.dot-flashing::before {
  left: -15px;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: ${bg_color};
  color: #04bcff;
  animation: dot-flashing 1s infinite alternate;
  animation-delay: 0s;
}

.dot-flashing::after {
  left: 15px;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: ${bg_color};
  color: #04bcff;
  animation: dot-flashing 1s infinite alternate;
  animation-delay: 1s;
}
@keyframes dot-flashing {
  0% {
    background-color: ${bg_color};
  }

  50%,
  100% {
    background-color: ${client_bubble_color};
  }
}

.chatbot-popup-msg {
  position: fixed;
  right: 30px;
  bottom: 7%;
  transform: translate3d(0, -50%, 0);
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
  background: #ffffff;
  border-radius: 10px;
  max-width: 400px;
  width: 400px;
  display:none;
}
}

.chatbot-popup-msg::after {
  content: '';
  width: 20px;
  height: 20px;
  transform: rotate(-45deg);
  background: #fff;
  position: absolute;
  box-shadow: 1px 4px 8px rgba(0, 0, 0, 0.5);
  z-index: -1;
  bottom: -7px;
  left: calc(50% - -118px);
}

.chatbot-popup-closeIcon {
  position: absolute;
  right: 3px;
  top: -3px;
  cursor: pointer;
}

.chatbot-popup-inner {
  padding: 15px 10px;
  background: #fff;
  border-radius: 10px;
  display: flex;
  align-items: center;
}
.chatbot-popup-inner .chatbot-popup-logo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
.chatbot-popup-inner .chatbot-popup-logo img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
.chatbot-popup-text {
  margin-left: 1rem;
}
.chatbot-popup-text p {
  word-break: break-all;
  margin: 0;
}
 `;

  var styleSheet = document.createElement('style');
  styleSheet.type = 'text/css';
  styleSheet.innerText = styles;
  document.head.appendChild(styleSheet);

  var chatToggle = document.getElementById('chat-circle');
  var chatWidget = document.getElementById('chat-widget');
  var chatMessages = document.getElementById('chat-messages');
  var chatInput = document.getElementById('chat-input');
  var chatSend = document.getElementById('chat-send');
  var welcomeMessageShown = false;

  function createLinkifyComponent(reply) {
    const linkifyComponent = document.createElement('div');

    if (reply) {
      const linkifiedText = reply.replace(/(https?:\/\/[^\s]+)/g, function (url) {
        const link = document.createElement('a');
        link.href = url;
        link.target = '_blank';
        link.textContent = url;
        return link.outerHTML;
      });

      linkifyComponent.innerHTML = linkifiedText;
    }

    return linkifyComponent;
  }

  function sendMessage() {
    var message = chatInput.value;
    var messageElement = document.createElement('div');
    messageElement.classList.add('message');

    if (message != '') {
      messageElement.innerHTML = `<div class="question-text-box"><div class="chatbox-user-quetext "><p>${message}</p></div></div>`;
      chatMessages.appendChild(messageElement);
      showLoader();
    }

    getReplyFromAPI(message)
      .then(function (modifiedData) {
        // Hide the loader
        hideLoader();

        var replyElement = document.createElement('div');
        replyElement.classList.add('message');

        var replyTextContainer = document.createElement('div');
        replyTextContainer.classList.add('answer-text-box');

        for (var i = 0; i < modifiedData.length; i++) {
          var replyContent = document.createElement('div');
          replyContent.classList.add('chatbox-user-anstext');
          replyContent.style.backgroundColor = bg_color;

          var replyMessage = document.createElement('p');
          replyMessage.classList.add('message-text');

          var linkifyComponent = createLinkifyComponent(modifiedData[i].text);
          replyMessage.appendChild(linkifyComponent);

          replyContent.appendChild(replyMessage);
          replyTextContainer.appendChild(replyContent);
        }

        replyElement.appendChild(replyTextContainer);
        chatMessages.appendChild(replyElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
      })
      .catch(function (error) {
        console.log('Error:', error);
      });

    chatInput.value = '';
  }

  function showLoader() {
    var loaderElement = document.createElement('div');
    loaderElement.classList.add('loader');
    loaderElement.innerHTML = `
      <div class='threedot-loader'>
        <div class='snippet' data-title='dot-flashing'>
          <div class='stage'>
            <div class='dot-flashing'></div>
          </div>
        </div>
      </div>
    `;

    chatMessages.appendChild(loaderElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function hideLoader() {
    var loaderElement = document.querySelector('.loader');

    if (loaderElement) {
      loaderElement.remove();
    }
  }

  function getReplyFromAPI(message) {
    if (message != '') {
      var apiUrl = 'https://webapi.chirpflo.com/v1/LoginChatGPTAPI?company=' + company;

      return fetch(apiUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ prompt: message }) })
        .then(function (response) {
          if (!response.ok) {
            throw new Error('Failed to fetch API');
          }
          return response.json();
        })
        .then(function (data) {
          var modifiedData = data.data.map(function (item) {
            var modifiedItem = { id: item.id, prompt: item.prmt, text: item.text };
            return modifiedItem;
          });

          return modifiedData;
        });
    }
  }

  function getWelcomeMsg() {
    var apiUrl = 'https://webapi.chirpflo.com/v1/welcomesms_linkAPI/?company=' + company;

    return fetch(apiUrl, { method: 'GET', headers: { 'Content-Type': 'application/json' } })
      .then(function (response) {
        if (!response.ok) {
          throw new Error('Failed to fetch API');
        }
        return response.json();
      })

      .then(function (data) {
        let WelMsg = data?.data?.welcome_msg;
        return WelMsg;
      });
  }

  chatSend.addEventListener('click', sendMessage);
  chatInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
      sendMessage();
    }
  });

  var chatImage = document.getElementById('chat-image');
  var closeIcon = document.getElementById('close-box');
  var chatWidget = document.getElementById('chat-widget');
  var chatMessages = document.getElementById('chat-messages');
  var chatbotPopup = document.querySelector('.chatbot-popup-msg');
  var closePopupIcon = document.querySelector('.chatbot-popup-closeIcon');
  var welcomeMessageShown = false;

  chatWidget.style.display = 'none';
  closeIcon.style.display = 'none';
  chatImage.style.display = 'block';

  function showChatWidget() {
    chatWidget.style.display = 'block';
    closeIcon.style.display = 'block';
    chatImage.style.display = 'none';

    if (!welcomeMessageShown) {
      getWelcomeMsg()
        .then(function (WelMsg) {
          var welElement = document.createElement('div');
          welElement.classList.add('message');
          welElement.innerHTML = `<div class="answer-text-box"><div class="chatbox-user-anstext" style="background-color:${bg_color}"><p>${WelMsg}</p></div></div>`;
          chatMessages.appendChild(welElement);
          chatMessages.scrollTop = chatMessages.scrollHeight;
          welcomeMessageShown = true;
        })
        .catch(function (error) {
          console.log('Error:', error);
        });
    }
  }

  getWelcomeMsg()
    .then(function (WelMsg) {
      document.getElementById('chatbot-popup-wlmsg').innerHTML = WelMsg;
    })
    .catch(function (error) {
      console.log('Error:', error);
    });

  function hideChatWidget() {
    chatWidget.style.display = 'none';
    chatImage.style.display = 'block';
    closeIcon.style.display = 'none';
  }

  console.log('popup_status: ', popup_status);
  if (popup_status === true) {
    setTimeout(function () {
      chatbotPopup.style.display = 'block';
      closePopupIcon.addEventListener('click', function () {
        chatbotPopup.style.display = 'none';
      });
    }, timer_count * 1000);
  }

  chatToggle.addEventListener('click', function () {
    if (chatWidget.style.display === 'none') {
      showChatWidget();
      chatbotPopup.style.display = 'none';
    } else {
      hideChatWidget();
    }
  });
}

fetch(`https://webapi.chirpflo.com/v1/WidgetGetAPI/${id}`)
  .then((response) => response.json())
  .then((data) => {
    console.log('response: ', data);
    const company = data.data.company;
    const testName = data.data.name;
    const heading = data.data.heading;
    const sub_heading = data.data.sub_heading;
    const avtarImg = data.data.chatbot_avtar;
    const icon = data.data.launcher_icon;
    const bg_color = data.data.color;
    const popup_status = data.data.popup_status;
    const timer_count = data.data.timer_count;
    const background_color = data.data.background_color;
    const client_bubble_color = data.data.client_bubble_color;

    let styleString = '';

    if (background_color.startsWith('http') || background_color.startsWith('https')) {
      // Background is a URL
      styleString = `url(${background_color});`;
    } else {
      // Background is a hexadecimal code
      styleString = `${background_color};`;
    }

    if (data.data.status == true) {
      initializeChatWidget(company, testName, heading, sub_heading, avtarImg, icon, bg_color, popup_status, timer_count, styleString, client_bubble_color);
    }
  })
  .catch((error) => {
    console.error('Error:', error);
  });