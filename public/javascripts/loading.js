
function Tologin() {
    // event.preventDefault(); // 阻止表单的默认提交行为
            const emailInput = document.getElementById('emailInput');

           const passwordInput = document.getElementById('passwordInput');
                emailInput.reportValidity();
            passwordInput.reportValidity();
  if (!passwordInput.checkValidity()||!emailInput.checkValidity()){
       // showContainer(6,'prequir');
       return;
  }


        var Email = document.getElementById('emailInput').value;
        var password = document.getElementById('passwordInput').value;




    fetch('https://transform.verseeding.com/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ Email: Email, password: password })
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(result) {

      // var popupMessage = document.getElementById('popup-message');
      const emailValueElement = document.getElementById("Email-value");
      const usernameValueElement = document.getElementById("username-value");
      const TokenValueElement = document.getElementById("Token-value");
      const numberValueElement = document.getElementById("number-value");
      const input = document.getElementById('emailInput');
      if (result.message === '登录成功') {
        // 登录成功，显示成功消息
        // 获取要填充值的容器元素
        const accessToken = result.access_token;
        // 将令牌存储在本地（例如使用localStorage）
      setAccessToken(accessToken);
       // localStorage.setItem('access_token', accessToken);

        closeLoginPopup();



        // 保存 username 到 Cookie
        openNonebutton();
        closeloginbutton();
        closeregisterbutton();
        showContainer(4,'showalertls');



        setCookie(result.Email, result.password,);

      // 填充值到容器元素中
        emailValueElement.style.fontSize = "15px";

        emailValueElement.textContent = result.Email.substring(0, 22);
        usernameValueElement.textContent = result.username;
        // 填充值到容器元素中
        TokenValueElement.textContent = result.Token;
        numberValueElement.textContent = result.number;
        // 修改按钮点击事件
      // 修改按钮点击事件


      } else if(result.message === 'not'){
        input.setCustomValidity('Dear user, our system has detected that you previously registered with a Google/GitHub account. To login with a password, please complete the registration process to set a login password. Thank you for your understanding and cooperation.');
        input.reportValidity();

      } else {
        // 登录失败，显示错误消息
        console.log(result.message);

        colorshowContainer(8,'showalertpe','#ea4545');
            // showContainer(8,'showalertpe');

        // popupMessage.innerHTML = result.message;
      }
    })
    .catch(function(error) {
      console.error('发生错误:', error);
    });
  };

function setCookie(type) {
  const expirationDate = new Date();
  expirationDate.setDate(expirationDate.getDate() + 7);

  // 对Email和type进行编码，以处理特殊字符
  // const encodedEmail = encodeURIComponent(Email);
  const encodedType = encodeURIComponent(type);

  // 创建包含编码值的Cookie字符串
  // const cookieEmail = `Email=${encodedEmail}; expires=${expirationDate.toUTCString()}; path=/`;
  const cookieType = `type=${encodedType}; expires=${expirationDate.toUTCString()}; path=/`;

  // 设置Cookie
  // document.cookie = cookieEmail;
  document.cookie = cookieType;
}

  // 保存 username 到 Cookie
  // function setCookie(Email,password) {
  //   const expirationDate = new Date();
  //   expirationDate.setDate(expirationDate.getDate() + 7);
  //   // 对用户名和密码进行编码，以处理特殊字符
  // const encodedEmail = encodeURIComponent(Email);
  // const encodedPassword = encodeURIComponent(password);
  //
  // // 创建包含编码值的 Cookie 字符串
  // const cookieEmail = `Email=${encodedEmail}; expires=${expirationDate.toUTCString()}; path=/`;
  // const cookiePassword = `password=${encodedPassword}; expires=${expirationDate.toUTCString()}; path=/`;
  // document.cookie = cookieEmail;
  // document.cookie = cookiePassword;
  // }
  // 从 Cookie 中获取用户名和密码
  function getCredentialsFromCookie() {
  const Email = getCookie("Email");
  const password = getCookie("password");
  return { Email, password };
}

  // 获取 Cookie 中的 值
  function getCookie(name) {
    const cookieName = name + "=";
    const cookieArray = document.cookie.split(';');
    for (let i = 0; i < cookieArray.length; i++) {
      let cookie = cookieArray[i];
      while (cookie.charAt(0) === ' ') {
        cookie = cookie.substring(1);
      }
      if (cookie.indexOf(cookieName) === 0) {
        return decodeURIComponent(cookie.substring(cookieName.length, cookie.length));
      }
    }
    return null;
  }

  // 设置按钮文本为 Cookie 中的 username
  // var loginButton = document.getElementById('Login-button');
  const imgurl = getCookie("img");
  const img = document.getElementById('user-img');
 if (imgurl) {
   console.log(imgurl)
      img.src =imgurl;
 }
  // var storedPassword = getCookie("password");
   const accessToken = getAccessToken();
  // var storedType = getCookie("type");
  //    const accessToken = getAccessToken();
  // if (accessToken && !isAccessTokenValid
 if (accessToken && !isAccessTokenValid()) {
   console.log("accesstoken 验证success");

 }

  if (accessToken && isAccessTokenValid() ) {
        openNonebutton();
        closeloginbutton();
        closeregisterbutton();

  }


  if (accessToken && !isAccessTokenValid()) {
    console.log("访问令牌已过期，已删除。");
    localStorage.removeItem('access_token');
  }





// 通过isAccessTokenValid函数验证access_token是否有效
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

// 设置access_token，并保存在LocalStorage中
function setAccessToken(token) {
  const expirationDate = new Date();
  expirationDate.setDate(expirationDate.getDate() + 7); // 设置过期时间为7天后

  const tokenObject = {
    token: token,
    expiresAt: expirationDate.getTime(), // 将过期时间转换为时间戳保存
  };

  // 将tokenObject转换为JSON字符串，并保存在LocalStorage中
  localStorage.setItem('access_token', JSON.stringify(tokenObject));
}

// 获取已存储的access_token
function getAccessToken() {
  const tokenString = localStorage.getItem('access_token');
  if (!tokenString) {
    return null; // 如果没有access_token，则返回null
  }

  const tokenObject = JSON.parse(tokenString);
  return tokenObject.token;
}


// 示例代码


