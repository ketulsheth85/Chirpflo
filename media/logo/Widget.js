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
      <div class='chatbox-header'>
          <div class='chatbox-logo'>
            <img src="${avtarImg}" alt='chatbox-logo' />
          </div>
          <div class='chatbox-header-text'>
            <h3 class=''>${testName}</h3>
            <p class=''>${heading}</p>
            <p class=''>${sub_heading}</p>
          </div>
      </div>
      <div class="chatbot-body">

      <div class="chatbotbody" id="chat-IinnerScroll" style="height:${window.innerHeight - 420}px; max-height:350px">
      <div id="chat-messages" ></div>
      <div class="user-box-wrapper style="display: none;">
            <div class="user-box">
            <form id="form">
              <div class="">
                <input
                  type="text"
                  name="name"
                  id="name"
                  required
                  autoComplete="off"
                  placeholder=" "
                />
                <label>Name</label>
              </div>
              <div class="">
                <input
                  type="email"
                  name="email"
                  required
                  autoComplete="off"
                  placeholder=" "
                />
                <label>Email</label>
              </div>
              <div class="">
                <input
                  type="tel"
                  name="phone_number"
                  required
                  autoComplete="off"
                  placeholder=" "
                  maxLength="10"
                />
                <label>Phone Number</label>
              </div>
              <input
                id="submit"
                type="submit"
                style="background-color:${client_bubble_color}"
              />
            </form>
          </div>
        </div>
      </div>

      <div id="chatbox-form-group">

      <div id="lead-button">
      <button class='btn-custom-border' id="btn_lead" style="background-color:${client_bubble_color}">
        
      </button>
    </div>
        <div class='chatbox-group' >
          <input type="text" id="chat-input" value="" placeholder="Type message...">
          <div class=' chatbox-input-group'>
            <button id="chat-send"><span>&#10148;</span></button>
          </div>
        </div>
      </div>
      </div>
        
      <div class='custom-chat-footer'>
        <p class=''>Powered By</p>
        <img src='https://chatgpts.s3.us-west-2.amazonaws.com/chatlogo/chirpflo.png' alt='chirpflo-logo' />
      </div>
    </div>
  `;

  // CSS styles for the chat widget

  var styles = `
  .chatbox-header {
   display: flex;
   align-items: center;
   padding: 15px;
 }
  .chatbotbody{
  height: 450px;
  overflow-y: auto;
  padding: 20px 0px;
  }

.chatbotbody {
  -ms-overflow-style: none; /* Internet Explorer 10+ */
  scrollbar-width: none; /* Firefox */
}
.chatbotbody::-webkit-scrollbar {
  display: none; /* Safari and Chrome */
}
 .user-box-wrapper {
  display: none;
  padding-top: 3rem;
}
 #chat-circle img {
   width:40px;
   height:40px;
   border-radius:50%;
 }

 .chabox-header-iconbox {
   display: flex;
   align-items: center;
   justify-content: space-between;
   width: 100%;
 }

  .chatbox-header .chatbox-logo img {
   width: 75%;
   height: 75%;
   display: flex;
   object-fit: cover;
   align-items: center;
   justify-content: center;
 }


  .chatbox-header .chatbox-header-text h3 {
    font-size: 18px;
    margin-bottom: 5px;
    margin-top: 0px;
    color: #ffffff;
 }

 .chatbox-header .chatbox-header-text p {
  font-size: 13px;
  margin: 0;
  color: #d6d9ff;
  line-height: 18px;
 }

 .close-icon {
   color:#ffffff;
   font-size: 25px;
   cursor: pointer;
 }

 .chatbox-group {
   position: relative;
   display: flex;
   align-items: center;
   justify-content: space-between;
   height: 40px;
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
  width: 35px;
  height: 35px;
 } 

 .chatbox-input-group button {
   width: 100% !important;
   height: 100% !important;
   background: ${client_bubble_color} !important;
   border: none !important;
 }
 .chatbot-body {
  padding: 1rem 1rem 1rem 1rem;
  border-radius: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  background: ${styleString} !important;
  background-repeat: no-repeat;
  background-size: 100% 100%;
}

 #chat-widget {
  position: fixed;
  bottom: 10%;
  right: 2%;
  width: 350px;
  border: 1px solid #ccc;
  box-shadow: 4px 4px 32px rgba(0, 0, 0, 0.3);
  font-family: Arial, sans-serif;
  font-size: 14px;
  border-radius: 1.5rem;
  overflow:hidden;
  background:${bg_color};
  background-repeat: no-repeat;
  background-size: 100% 100%;
  z-index:9999;
}
#chatbox-form-group
{
  margin-top:auto;
}

 #chat-input {
  border-radius: 34px;
    width: 100%;
    height: 100%;
    max-width: 100%;
    border: none;
    font-size: 17.6px;
    padding: 0px 65px 0px 20px;
    color: #000000;
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
  font-size: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
 }

 #chat-widget {
   display: none;
 }

 #chat-widget.open {
   display: block;
 }

 #chat-circle {
  position: fixed;
  right: 2%;
  bottom: 2%;
    cursor: pointer;
    width: 50px;
    height: 50px;
    min-width: 50px;
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
   margin-bottom: 15px;
 }

 .question-text-box .chatbox-user-quetext {
   background: ${client_bubble_color};
   padding: 0.625rem 1rem;
   font-size: max(0.8rem, 12px) !important;
   color: #ffffff;
   word-break: break-word;
   border-radius: 12px 12px 0px 12px;
   word-break: break-all;
   display: flex;
  align-items: center;
  justify-content: center;
 }
 .question-text-box .chatbox-user-quetext p{
  margin:0;
  font-family: sans-serif !important;
  font-size: max(0.8rem, 12px) !important;
 }

 .answer-text-box {
   margin-bottom:15px;
 }
 .content-container {
  display: flex;
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
  width: 50px;
  height: 50px;
  min-width: 50px;
  min-height: 50px;
  border-radius: 50%;
  margin-right: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

 .answer-text-box .chatbox-user-anstext {
  padding: 0.625rem 1rem;
  font-size: max(0.8rem, 12px) !important;
  color: #ffffff;
  word-break: break-word;
  border-radius: 12px 12px 12px 0px;
  display: flex;
  align-items: center;
  justify-content: center;
 } 
 .answer-text-box .chatbox-user-anstext p{
  margin:0;
  font-family: sans-serif !important;
  font-size: max(0.8rem, 12px) !important;
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
  display:none;
  position: fixed;
  right: 3%;
  bottom: 6%;
  transform: translate3d(0, -50%, 0);
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
  background: #ffffff;
  border-radius: 10px;
  max-width: 300px;
}

.chatbot-popup-closeIcon {
  position: absolute;
  right: 3px;
  top: -6px;
  cursor: pointer;
  background: transparent;
  border: 0;
  color: gray;
  margin-right: -5px;
  padding: 5px;
  z-index: 1;
  font-size: 20px;
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
#leadChoiceContainer
{
  display: flex;
  align-items: center;
  flex-direction: column;
}
#leadChoiceContainer span
{
  font-size: 13px;
  color: #ffffff;
  opacity: 0.7;
  margin:1rem 0;
}
.lead-choice-container
{
  display: flex;
  align-items: center;
  margin-top:15px;
}
.btn-submit-login {
  background: #04bcff;
  border-radius:12px;
  color: #ffffff;
  width: 100%;
  max-width: fit-content;
  font-family: sans-serif !important;
  font-size: max(0.8rem, 12px) !important;
  height: 45px;
  margin-right:10px;
  padding:10px 25px;
  border: 1px solid #04bcff;
  cursor:pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}
.custom-chat-footer
{
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px;
}
.custom-chat-footer p {
  margin:0px 10px 0px 0px;
  font-size: 0.875rem;
  line-height: 1.25rem;
  color: #ffffff;
  opacity:0.75;
}
.custom-chat-footer img {
  width: 70px;
  aspect-ratio: auto 70 / 22;
  height: 22px;
}
.image-content {
  width: 45px;
  height: 45px;
  min-width: 45px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.image-content img{
  width: 80%;
  height: 80%;
}

.user-box-wrapper {
  width: 100%;
}
.user-box {
  max-width: 75%;
  margin: auto;
  box-sizing: border-box;
}



.user-box input {
  padding: 10px 0;
  background-color: transparent;
  color: #ffffff;
}

.user-box textarea {
  height: 80px;
  padding: 10px 0;
  margin-bottom: 40px;
}

.user-box input,
.user-box textarea {
  width: 100%;
  box-sizing: border-box;
  box-shadow: none;
  outline: none;
  border: none;
  border-bottom: 2px solid #999;
}
.user-box textarea {
  margin-bottom: 20px;
}

.user-box input[type='submit'] {
  font-size: 1.1em;
  border-bottom: none;
  cursor: pointer;
  background: #433e70;
  border-radius:0.375rem;
  color: #ffffff;
  margin-bottom: 0;
  text-transform: uppercase;
}

.user-box form div {
  position: relative;
  margin-bottom: 1.5rem;
}

.user-box form div label {
  position: absolute;
  top: 10px;
  left: 0;
  color: #9ba9d6;
  pointer-events: none;
  transition: 0.5s;
}

.user-box input:focus ~ label,
.user-box textarea:focus ~ label,
.user-box input:valid ~ label,
.user-box textarea:valid ~ label {
  top: -16px;
  left: 0;
  color: #9ba9d6;
  font-size: 1em;
  font-weight: bold;
}
#lead-button{
  display:none;
  margin-bottom: 0.5rem;
  justify-content: flex-end;
  align-items: center;
}
.btn-custom-border {
  position: relative;
  color: #ffffff;
  padding: 5px 10px;
  font-size: 15px;
  width: 81px;
  background: transparent;
  border-radius:0.375rem;
  cursor: pointer;
  border: none;
  height:35px;
}
.wel-msg-color{
  color:#ffffff;
  margin:0 0 1.5rem!important;
  font-family: sans-serif !important;
  font-size: max(0.8rem, 12px) !important;
  text-align:center;
  background-color: transparent !important;
  display: flex;
  align-items: center;
  justify-content: center;
}
.wel-message
{
  display: flex;
  flex margin-right: 0.5rem;
  flex-direction: column;
  justify-content: center;
}
#welcome-image
{
  display:none;
}
 `;

  // Create a stylesheet dynamically and append it to the head of the document
  var styleSheet = document.createElement('style');
  styleSheet.type = 'text/css';
  styleSheet.innerText = styles;
  document.head.appendChild(styleSheet);

  // Get references to various elements in the HTML
  var chatToggle = document.getElementById('chat-circle');
  var chatWidget = document.getElementById('chat-widget');
  var chatMessages = document.getElementById('chat-messages');
  var chatInnerScroll = document.getElementById('chat-IinnerScroll');
  var chatInput = document.getElementById('chat-input');
  var chatSend = document.getElementById('chat-send');
  var chatboxFormGroup = document.getElementById('chatbox-form-group');
  var chatImage = document.getElementById('chat-image');
  var closeIcon = document.getElementById('close-box');
  var LeadButton = document.getElementById('lead-button');
  var userBoxWrapper = document.querySelector('.user-box-wrapper');
  var btn_Lead = document.getElementById('btn_lead');
  var chatbotPopup = document.querySelector('.chatbot-popup-msg');
  var closePopupIcon = document.querySelector('.chatbot-popup-closeIcon');
  var welcomeMessageShown = false;

  // Function to create a linkify component for URLs in the chat messages
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

  chatInput.addEventListener('input', function () {
    // Enable the send button if the chat input value is not empty
    chatSend.disabled = chatInput.value === '';
  });
  // Function to send a user message and retrieve a reply from the API
  function sendMessage() {
    var message = chatInput.value;
    console.log('message: ', message);
    var messageElement = document.createElement('div');
    messageElement.classList.add('message');

    if (message != '') {
      messageElement.innerHTML = `<div class="question-text-box"><div class="chatbox-user-quetext "><p>${message}</p></div></div>`;
      chatMessages.appendChild(messageElement);
      showLoader();
    }

    getReplyFromAPI(message)
      .then(function (modifiedData) {
        hideLoader();

        for (const closingLead of modifiedData) {
          const closingLeadChoices = closingLead.choice?.closing_lead_choice;

          const replyElement = document.createElement('div');
          replyElement.classList.add('message');

          const contentDiv = document.createElement('div');
          contentDiv.classList.add('content-container');

          const replyTextContainer = document.createElement('div');
          replyTextContainer.classList.add('answer-text-box');

          if (closingLead.text !== undefined) {
            const imageElement = document.createElement('img');
            imageElement.src = avtarImg; // Make sure avtarImg is defined
            imageElement.alt = 'Image description';

            const imageDiv = document.createElement('div');
            imageDiv.classList.add('image-content');
            imageDiv.appendChild(imageElement);
            contentDiv.appendChild(imageDiv);

            const replyContent = document.createElement('div');
            replyContent.classList.add('chatbox-user-anstext');
            replyContent.style.backgroundColor = bg_color;

            const replyMessage = document.createElement('p');
            replyMessage.classList.add('message-text');
            replyMessage.appendChild(createLinkifyComponent(closingLead.text));
            replyContent.appendChild(replyMessage);

            contentDiv.appendChild(replyContent);
            replyTextContainer.appendChild(contentDiv);
            replyElement.appendChild(replyTextContainer);
            chatMessages.appendChild(replyElement);
          }

          if (closingLeadChoices) {
            const leadChoiceContainer = document.createElement('div');
            leadChoiceContainer.classList.add('lead-choice-container');
            chatboxFormGroup.style.display = 'none';

            closingLeadChoices.forEach(function (choice) {
              const button = document.createElement('button');
              button.className = 'btn-submit-login';
              button.style.background = client_bubble_color;
              button.style.borderColor = client_bubble_color;
              button.textContent = choice;

              button.addEventListener('click', function (e) {
                leadChoiceContainer.style.display = 'none';
                if (choice === closingLeadChoices[0]) {
                  openForm();
                } else {
                  handleChoice(e, choice);
                }
              });

              leadChoiceContainer.appendChild(button);
            });

            replyTextContainer.appendChild(leadChoiceContainer);
            replyElement.appendChild(replyTextContainer);
            chatMessages.appendChild(replyElement);
          }

          chatInnerScroll.scrollTo({
            top: chatInnerScroll.scrollHeight,
            behavior: 'smooth',
          });
        }
      })
      .catch(function (error) {
        console.log('Error:', error);
      });

    chatInput.value = '';
  }

  // Function to show a loader while waiting for a response from the API
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
    chatInnerScroll.scrollTo({
      top: chatInnerScroll.scrollHeight,
      behavior: 'smooth',
    });
  }

  // Function to hide the loader
  function hideLoader() {
    var loaderElement = document.querySelector('.loader');

    if (loaderElement) {
      loaderElement.remove();
    }
  }

  // Function to generate a random ID
  function generateRandomId(length) {
    const numbers = '0123456789';
    let randomId = '';
    for (let i = 0; i < length; i++) {
      const randomIndex = Math.floor(Math.random() * numbers.length);
      randomId += numbers.charAt(randomIndex);
    }
    return randomId;
  }

  // Function to get a reply from the API based on the user's message
  function getReplyFromAPI(message) {
    chatSend.disabled = true;
    if (message !== '') {
      const length = 8;
      let randomId = localStorage.getItem('sessionId');
      if (!randomId) {
        randomId = generateRandomId(length);
        localStorage.setItem('sessionId', randomId);
      }
      const apiUrl = 'https://webapi.chirpflo.com/v1/LoginChatGPTAPI?company=' + company;
      // const apiUrl = 'https://webapi.chirpflo.com/v1/LoginChatGPTAPI?company=30';
      // const apiUrl = 'http://192.168.1.183:7000/v1/LoginChatGPTAPI?company=47';

      return fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: message, session_id: randomId }),
      })
        .then(function (response) {
          if (!response.ok) {
            throw new Error('Failed to fetch API');
          }
          chatSend.disabled = false;
          return response.json();
        })
        .then(function (data) {
          if (data?.data[1]?.closing_chatbot == true) {
            setTimeout(() => {
              hideLoader();
              chatWidget.style.display = 'none';
              closeIcon.style.display = 'none';
              chatImage.style.display = 'block';
              localStorage.clear();
              DaleteChatFromAPI();
              clearChatMessages();
            }, 2000);
          }
          chatSend.disabled = false;
          var modifiedData = data.data.map(function (item) {
            var modifiedItem = { id: item.id, prompt: item.prmt, text: item.text, choice: item };
            return modifiedItem;
          });

          return modifiedData;
        });
    }
  }

  // Function to retrieve the welcome message from the API
  function getWelcomeMsg() {
    var apiUrl = 'https://webapi.chirpflo.com/v1/welcomesms_linkAPI/?company=' + company;
    // var apiUrl = 'https://webapi.chirpflo.com/v1/welcomesms_linkAPI/?company=30';
    // var apiUrl = 'http://192.168.1.183:7000/v1/welcomesms_linkAPI/?company=47';

    return fetch(apiUrl, { method: 'GET', headers: { 'Content-Type': 'application/json' } })
      .then(function (response) {
        if (!response.ok) {
          throw new Error('Failed to fetch API');
        }
        return response.json();
      })
      .then(function (data) {
        let WelMsgDetails = data?.data;
        btn_Lead.innerText = WelMsgDetails?.generate_lead_choice;
        return WelMsgDetails;
      });
  }

  chatSend.disabled = false;

  // Add an event listener to the chatSend button for click event
  chatSend.addEventListener('click', sendMessage);

  // Add an event listener to the chatInput element for keydown event
  chatInput.addEventListener('keydown', function (event) {
    if (!chatSend.disabled && event.key === 'Enter') {
      sendMessage();
    }
  });

  // Hide the chat widget and show the chat image initially
  chatWidget.style.display = 'none';
  closeIcon.style.display = 'none';
  chatImage.style.display = 'block';

  // Function to show the chat widget and load the welcome message
  function showChatWidget() {
    chatWidget.style.display = 'block';
    closeIcon.style.display = 'block';
    chatImage.style.display = 'none';

    getWelcomeMsg()
      .then(function (WelMsgDetails) {
        var welElement = document.createElement('div');
        welElement.classList.add('wel-message');
        welElement.innerHTML = `<div class="answer-text-box" id="add-conatiner">
        <div class="image-content" id="welcome-image"><img src=${avtarImg} alt="Image description"></div>
       <div class=${WelMsgDetails?.lead_choice ? 'wel-msg-color' : 'chatbox-user-anstext'} id="welcomeCOLOR" style="background-color:${bg_color}">
        <p>${WelMsgDetails?.welcome_msg}</p></div></div><div class="lead-container" id="leadChoiceContainer"></div>`;
        chatMessages.appendChild(welElement);
        chatInnerScroll.scrollTo({
          top: chatInnerScroll.scrollHeight,
          behavior: 'smooth',
        });
        welcomeMessageShown = true;
        if (WelMsgDetails?.lead_choice.length) {
          chatboxFormGroup.style.display = 'none';
        }
        var leadChoiceContainer = document.getElementById('leadChoiceContainer');
        WelMsgDetails?.lead_choice.forEach(function (choice, index) {
          var button = document.createElement('button');
          button.className = 'btn-submit-login';
          button.style.background = index == 0 ? bg_color : '#ffffff';
          button.style.borderColor = index == 0 ? bg_color : bg_color;
          button.style.color = index == 0 ? '' : bg_color;
          button.style.margin = index == 0 ? 0 : 0;
          button.textContent = choice;
          button.addEventListener('click', function (e) {
            document.getElementById('welcome-image').style.display = 'block';
            document.getElementById('welcomeCOLOR').classList.remove('wel-msg-color');
            document.getElementById('welcomeCOLOR').classList.add('chatbox-user-anstext');
            document.getElementById('add-conatiner').classList.add('content-container');
            if (choice === WelMsgDetails.lead_choice[0]) {
              // openForm();
              handleChoice(e, choice);
            } else {
              handleChoice(e, choice);
              showLeadButton();
            }
          });

          leadChoiceContainer.appendChild(button);

          if (index < WelMsgDetails.lead_choice.length - 1) {
            var orSpan = document.createElement('span');
            orSpan.textContent = 'Or';
            leadChoiceContainer.appendChild(orSpan);
          }
        });
      })
      .catch(function (error) {
        console.log('Error:', error);
      });
  }

  function openForm() {
    document.querySelector('.user-box-wrapper').style.display = 'block';
    var leadChoiceContainer = document.getElementById('leadChoiceContainer');
    leadChoiceContainer.style.display = 'none';
  }
  function showLeadButton() {
    LeadButton.style.display = 'flex';
  }

  function clearChat() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = '';
    hideLoader();
  }
  btn_Lead.addEventListener('click', function (e) {
    var innerText = btn_Lead.innerText;
    handleChoice(e, innerText);
  });

  function preSubmit(event) {
    event.preventDefault();

    const length = 8;
    let randomId = localStorage.getItem('sessionId');
    if (!randomId) {
      randomId = generateRandomId(length);
      localStorage.setItem('sessionId', randomId);
    }
    getWelcomeMsg()
      .then(function () {
        var formData = {
          name: document.getElementById('name').value,
          email: document.getElementsByName('email')[0].value,
          phone_number: document.querySelector('input[name="phone_number"]').value,
          session_id: randomId,
        };

        // const apiUrl = 'http://192.168.1.183:7000/v1/Create_LeadInformationAPI?company=47';
        var apiUrl = 'https://webapi.chirpflo.com/v1/Create_LeadInformationAPI?company=' + company;

        fetch(apiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
        })
          .then(function (response) {
            if (response.ok) {
              return response.json();
            } else {
              throw new Error('Network response was not ok');
            }
          })
          .then(function (data) {
            handleChoice(event, `${formData.name} ${formData.email} ${formData.phone_number}`);
            document.querySelector('.user-box-wrapper').style.display = 'none';

            // Clear form inputs after successful API request
            document.getElementById('name').value = '';
            document.getElementsByName('email')[0].value = '';
            document.querySelector('input[name="phone_number"]').value = '';
          })
          .catch(function (error) {
            console.error('Error:', error);
          });
      })
      .catch(function (error) {
        console.log('Error:', error);
      });
  }

  // Get the form element
  const form = document.getElementById('form');

  // Attach the onsubmit event listener
  form.addEventListener('submit', preSubmit);

  function handleChoice(event, choice) {
    var leadChoiceContainer = document.getElementById('leadChoiceContainer');
    if (leadChoiceContainer && chatboxFormGroup) {
      leadChoiceContainer.style.display = 'none';
      chatboxFormGroup.style.display = 'block';
    }
    // leadChoiceContainer.style.display = 'none';
    // chatboxFormGroup.style.display = 'block';

    // Display the prompt message as a question in the chatbox
    var promptElement = document.createElement('div');
    promptElement.classList.add('message');

    var questionTextContainer = document.createElement('div');
    questionTextContainer.classList.add('question-text-box');

    var questionContent = document.createElement('div');
    questionContent.classList.add('chatbox-user-quetext');

    var questionMessage = document.createElement('p');
    questionMessage.textContent = choice;

    questionContent.appendChild(questionMessage);
    questionTextContainer.appendChild(questionContent);
    promptElement.appendChild(questionTextContainer);
    chatMessages.appendChild(promptElement);
    showLoader();
    getReplyFromAPI(choice)
      .then(function (data) {
        var modifiedData = data.map(function (item) {
          var modifiedItem = { id: item.id, prompt: item.prmt, text: item.text };
          return modifiedItem;
        });
        hideLoader();

        var replyElement = document.createElement('div');
        replyElement.classList.add('message');

        var replyTextContainer = document.createElement('div');
        replyTextContainer.classList.add('answer-text-box');

        for (var i = 0; i < modifiedData.length; i++) {
          var contentDiv = document.createElement('div');
          contentDiv.classList.add('content-container');

          var imageElement = document.createElement('img');
          imageElement.src = avtarImg;
          imageElement.alt = 'Image description';

          var imageDiv = document.createElement('div');
          imageDiv.classList.add('image-content');
          imageDiv.appendChild(imageElement);
          contentDiv.appendChild(imageDiv);

          var replyContent = document.createElement('div');
          replyContent.classList.add('chatbox-user-anstext');
          replyContent.style.backgroundColor = bg_color;

          if (modifiedData[i].text !== undefined) {
            var replyMessage = document.createElement('p');
            replyMessage.classList.add('message-text');
            replyMessage.textContent = modifiedData[i].text;
            replyContent.appendChild(replyMessage);
          }

          contentDiv.appendChild(replyContent);
          replyTextContainer.appendChild(contentDiv);
        }

        replyElement.appendChild(replyTextContainer);
        chatMessages.appendChild(replyElement);
        chatInnerScroll.scrollTo({
          top: chatInnerScroll.scrollHeight,
          behavior: 'smooth',
        });
      })
      .catch(function (error) {
        console.log('Error:', error);
      });
  }

  // Get the welcome message and display it in the chatbot popup
  getWelcomeMsg()
    .then(function (WelMsgDetails) {
      document.getElementById('chatbot-popup-wlmsg').innerHTML = WelMsgDetails?.welcome_msg;
    })
    .catch(function (error) {
      console.log('Error:', error);
    });

  // Function to hide the chat widget
  function hideChatWidget() {
    chatWidget.style.display = 'none';
    chatImage.style.display = 'block';
    closeIcon.style.display = 'none';
  }

  // Show the chatbot popup if enabled
  // if (popup_status === true) {
  //   setTimeout(function () {
  //     chatbotPopup.style.display = 'block';
  //     closePopupIcon.addEventListener('click', function () {
  //       chatbotPopup.style.display = 'none';
  //     });
  //   }, timer_count * 1000);
  // }
  function clearChatMessages() {
    chatMessages.innerHTML = ''; // Clear all chat messages
  }
  function DaleteChatFromAPI() {
    const apiUrl = 'https://webapi.chirpflo.com/v1/LoginChatGPTAPI?company=' + company;
    // const apiUrl = 'https://webapi.chirpflo.com/v1/LoginChatGPTAPI?company=30';
    // const apiUrl = 'http://192.168.1.183:7000/v1/LoginChatGPTAPI?company=47';

    return fetch(apiUrl, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        clearChatMessages();
      });
  }

  // Event listener for the chat toggle button
  chatToggle.addEventListener('click', function () {
    if (chatWidget.style.display === 'none') {
      showChatWidget();
      getWelcomeMsg();
      chatbotPopup.style.display = 'none';
      document.querySelector('.user-box-wrapper').style.display = 'none';
    } else {
      hideChatWidget();
      localStorage.clear();
      DaleteChatFromAPI();
    }
  });
}

// fetch(`http://192.168.1.128:7000/v1/WidgetGetAPI/${id}`)
fetch(`https://webapi.chirpflo.com/v1/WidgetGetAPI/${id}`)
// fetch(`http://192.168.1.183:7000/v1/WidgetGetAPI/28`)
  .then((response) => response.json())
  .then((data) => {
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