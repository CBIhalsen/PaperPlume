
function isAccessTokenValid() {
  const tokenString = localStorage.getItem('access_token');
  if (!tokenString) {
    // 如果没有access_token，视为过期
    return false;
  }

  const tokenObject = JSON.parse(tokenString);
  const currentTime = new Date().getTime();

  return currentTime < tokenObject.expiresAt;
}



    function startLoading() {
            var button = document.getElementById('sendButton');
            var button2 = document.getElementById('submit-button');
            var buttonText = document.getElementById('buttonText');
            var loader = document.getElementById('loader');
            // sloader

            // 获取标题输入框的值
            var titleInput = document.getElementById("title");
            var title = titleInput.value;
            const accessToken =  getAccessToken();

            if (!accessToken || accessToken == undefined || accessToken == null || !isAccessTokenValid() ) {
             // 如果access_token不存在，则设置其值为Null
                // 使用示例
                showContainer(10,'tologin');


                return;
            }


            const savedLanguage = localStorage.getItem("language");
            const savedWritingStyle = localStorage.getItem("writingStyle");
            const savedTextareaValue = localStorage.getItem("textareaValue");
             const savedModelValue = localStorage.getItem("modelValue");
            // 发送 POST 请求
            const formData = new FormData();
            formData.append("title",title);
            formData.append("reference", savedTextareaValue);
            formData.append("language",savedLanguage);
            formData.append("style",savedWritingStyle);
            formData.append("model",savedModelValue)

            fetch("https://transform.verseeding.com/generate_outline", {
                method: "POST",
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                },
                    body: formData
            })
            .then(response => response.text())
            .then(data => {
                if (data=='refuse'){
                   showContainer(10,'nagw');
                   data='Your balance is negative. Please recharge to use the features.';


                }
                // 将返回的 First_reply 设置为文本框的内容
                firstReplyTextBox.value = data;
                button.disabled = false; // 启用按钮点击
                button2.disabled = false;
                buttonText.style.display = 'inline'; // 恢复按钮文字
                loader.style.display = 'none'; // 隐藏加载圈
            })
            .catch(error => console.log(error));


     button.disabled = true; // 禁用按钮点击
        console.log("按钮1禁用");
button2.disabled = true;
if (button2.disabled) {
  console.log("按钮二禁用");
}

  // 隐藏按钮文字，显示加载圈
  buttonText.style.display = 'none';
  loader.style.display = 'inline-block';


}


// 获取元素的引用
        const firstReplyTextBox = document.getElementById("first-reply");
        const reloadButton = document.getElementById("reload-button");
        const submitButton = document.getElementById("submit-button");

        // 处理表单提交的函数
        function handleFormSubmit(event) {
            event.preventDefault();  // 阻止表单默认提交行为

            // 获取标题输入框的值
            var titleInput = document.getElementById("title");
            var title = titleInput.value;

            // alert(accessToken)
            // 发送 POST 请求
            // alert("多余")

        }

        // 处理 reload 按钮的点击事件
        function handleReloadButtonClick() {
            // 调用表单提交的函数
            handleFormSubmit(new Event("submit"));
        }
        function getAccessToken() {
  const tokenString = localStorage.getItem('access_token');
  if (!tokenString) {
    return null; // 如果没有access_token，则返回null
  }

  const tokenObject = JSON.parse(tokenString);
  return tokenObject.token;
}


        // 处理 submit 按钮的点击事件
        function handleSubmitButtonClick() {
            var firstReply = firstReplyTextBox.value;
             var textareaField = document.createElement("textarea");
            // textareaField.name = "first_reply";
            textareaField.value = firstReply; // 设置为HTML内容


            var titleInput = document.getElementById("title");
            var title = titleInput.value;
            var titleField = document.createElement("input");
            titleField.type = "text";
            titleField.name = "title";
            titleField.value = title;
            const savedLanguage = localStorage.getItem("language");
            const savedWritingStyle = localStorage.getItem("writingStyle");
            const savedModelValue = localStorage.getItem("modelValue");
            const formData = new FormData();
            formData.append("first_reply",textareaField.value);
            formData.append("title", title);
             formData.append("language",savedLanguage)
            formData.append("style",savedWritingStyle)
            formData.append("model",savedModelValue)

             const accessToken =  getAccessToken();



            alert("请等候10分钟左右,会自动弹出下载链接");
            fetch("https://transform.verseeding.com/write_docx", {
                method: "POST",
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                },
                body: formData
            })
             .then(response => response.text())
            .then(data => {
                if (data =='refuse3'){
                     showContainer(10,'nagw3');
                     return;
                } else if(data =='refuse4'){
                     colorshowContainer(10,'nagw4');
                      return;
                }
                // const content = '<a href="' + data + '" target="_blank">' + data + '</a>';
                window.open(data, '_blank');
                alert("Url:",data);
                localStorage.setItem('previousUrl', data);

                // 显示带有超链接的弹窗
                // alert(content);
                // 将返回的 First_reply 设置为文本框的内容
                // firstReplyTextBox.value = data;
                // button.disabled = false; // 启用按钮点击
                // buttonText.style.display = 'inline'; // 恢复按钮文字
                // loader.style.display = 'none'; // 隐藏加载圈
            })
            .catch(error => console.log(error));

}



        // 监听表单的提交事件
        var generateForm = document.getElementById("generate-form");
        generateForm.addEventListener("submit", handleFormSubmit);

        // 监听 reload 按钮的点击事件


        // 监听 submit 按钮的点击事件

        function showConfirmationDialog() {
            const firstReply = firstReplyTextBox.value;
            const accessToken =  getAccessToken();

             if (!accessToken || accessToken == undefined || accessToken == null ) {
             // 如果access_token不存在，则设置其值为Null
                // 使用示例
                    showContainer(6,'tologin');


                return;
            }

            if (!firstReply || firstReply.length < 30) {

                 showContainer(7,'getstart');
               // ("Please edit the outline correctly.");
                return ;
            }


            var confirmation = confirm("你是否要生成论文？生成论文的费用为基础的token费用和每篇0.3usd，一篇费用大概在0.5usd左右。");

            if (confirmation) {
                handleSubmitButtonClick();
            }
        }
        function selectButton() {
            const url = localStorage.getItem('previousUrl');
            if (url) {
                alert(url);
                window.open(url, '_blank');
            } else {
                alert('Sorry, you don\'t have an order')
            }

        }

        function openLoginPopup() {
        document.getElementById('loginPopup').style.display = 'flex';
                 document.getElementById('cpc').style.display='none';
         document.getElementById('ecc').style.display='none';
         document.getElementById('register').style.display='none';
         document.getElementById('login').style.display='block';
         document.getElementById('allogin').style.display='none';
         document.getElementById('fp').style.display='block';
         document.getElementById('nosignup').style.display='block';


        }

          function closeLoginPopup() {
            document.getElementById('loginPopup').style.display = 'none';
          }
         function openNonePopup() {
                document.getElementById('NonePopup').style.display = 'flex';
                   const accessToken = getAccessToken();
            if (accessToken && isAccessTokenValid() ) {

            fetch("https://transform.verseeding.com/user_information", {
                method: "POST",
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                },
            })
    .then(function(response) {
      return response.json();
    })
    .then(function(result) {
         const balanceValueElement = document.getElementById("balance-value");
      const emailValueElement = document.getElementById("Email-value");
      const useridValueElement = document.getElementById("userid-value");
      const TokenValueElement = document.getElementById("Token-value");
      const numberValueElement = document.getElementById("number-value");
      if (result.message === 'success') {
        // 登录成功，显示成功消息
        // popupMessage.innerHTML = '登录成功';

        // 保存 username 到 Cookie

        // 填充值到容器元素中


        emailValueElement.textContent = result.Email;
         balanceValueElement.textContent = result.balance + ' $';
        useridValueElement.textContent = 1971628+result.userid;
        // 填充值到容器元素中
        TokenValueElement.textContent = result.Token;
        numberValueElement.textContent = result.number;

      } else {
            alert("unknown error")
      }
    })
    .catch(function(error) {
      console.error('发生错误:', error);
    });
  }



        }

          function closeNonePopup() {
            document.getElementById('NonePopup').style.display = 'none';
          }
          function openNonebutton(){
            document.getElementById('None-button').style.display = 'block';
          }
          function closeloginbutton(){
            document.getElementById('Login-button').style.display = 'None';
          }
           function closeregisterbutton(){
            document.getElementById('signup-button').style.display = 'None';
          }

          function login() {
            // 在这里执行登录的逻辑
            console.log('登录');
          }

          // function loginWithGoogle() {
          //   // 在这里执行使用Google登录的逻辑
          //   console.log('使用Google登录');
          // }

          // function loginWithGithub() {
          //   // 在这里执行使用Github登录的逻辑
          //   console.log('使用Github登录');
          // }
         // function logout() {
         //    document.cookie = "img=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
         //    // document.cookie = "password=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
         //    localStorage.removeItem('access_token');
         //    alert("Logout success");
         //    location.reload();
         //    }




    //  function showAlert(message) {
    //   var modal = document.getElementById("myModal");
    //   var modalMessage = document.getElementById("modalMessage");
    //   modal.style.display = "block";
    //   modalMessage.textContent = message;
    // }
    function openTermsAndPrivacy() {
  window.open("TermsServiceandPrivacyPolicy.html", "_blank");
}

