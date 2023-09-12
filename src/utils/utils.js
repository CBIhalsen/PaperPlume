  // Google 登录
// Import the functions you need from the SDKs you need

import { initializeApp } from "firebase/app";
import { getAuth, signInWithPopup, GoogleAuthProvider, GithubAuthProvider ,  signOut} from "firebase/auth";



export function thirdLogout() {
    document.cookie = "img=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    // document.cookie = "password=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    localStorage.removeItem('access_token');

     location.reload();

const firebaseConfig = {
  apiKey: "AIzaSyCR0iILgK7aiU-jToDyDThPJ-rZRq5H2TI",
  authDomain: "verseeding.firebaseapp.com",
  projectId: "verseeding",
  storageBucket: "verseeding.appspot.com",
  messagingSenderId: "324985975074",
  appId: "1:324985975074:web:53ee9085289490a058757b",
  measurementId: "G-FJSQSRBPS6"
};
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
 app;
  const auth = getAuth();


  signOut(auth).then(() => {
    // Sign-out successful.
    console.log('用户已登出');
  }).catch((error) => {
    // An error happened.
    console.log('登出出错：', error);
  });
   showContainer(4,'showalertlo');
    // location.reload();
}



export function googleLogin() {

const firebaseConfig = {
  apiKey: "AIzaSyCR0iILgK7aiU-jToDyDThPJ-rZRq5H2TI",
  authDomain: "verseeding.firebaseapp.com",
  projectId: "verseeding",
  storageBucket: "verseeding.appspot.com",
  messagingSenderId: "324985975074",
  appId: "1:324985975074:web:53ee9085289490a058757b",
  measurementId: "G-FJSQSRBPS6"
};
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const provider = new GoogleAuthProvider();
   provider.setCustomParameters({
    prompt: 'select_account'
  });
  const auth = getAuth();
  signInWithPopup(auth, provider)
    .then((result) => {
      // This gives you a Google Access Token. You can use it to access the Google API.
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const token = credential.accessToken;
      //
      //       const emailValueElement = document.getElementById("Email-value");
      // const usernameValueElement = document.getElementById("username-value");
      // const TokenValueElement = document.getElementById("Token-value");
      // const numberValueElement = document.getElementById("number-value");
      // The signed-in user info.
        app;
      const user = result.user;
      console.log('已登录的用户信息：',user)
          // 构造要发送的用户信息
         console.log('pu',user.photoURL)
    setCookie(user.photoURL);
    // name: user.displayName,
    const userInfo = {
    type: "google",

    email: user.email,
    imageUrl: user.photoURL,
    token: token,
    uid: user.uid,
    };

        // 保存 username 到 Cookie

        // 填充值到容器元素中
        // emailValueElement.style.fontSize = "14px";
        //
        // emailValueElement.textContent = user.email.substring(0, 22);
        // usernameValueElement.textContent =  user.displayName;
        // 填充值到容器元素中
        // TokenValueElement.textContent = result.Token;
        // numberValueElement.textContent = result.number;

// 发送 POST 请求到后端接口
        console.log("下一步发送")
    fetch('https://transform.verseeding.com/auth/callback', {
     method: 'POST',
     headers: {
    'Content-Type': 'application/json'
     },
  body: JSON.stringify(userInfo)
    })
.then(response => response.json()) // Parse the response as JSON
  .then(data => {
    // Handle the response data
      console.log('已发送')
    console.log('Response from backend:', data);

    // Check if the login was successful
    if (data.status === 'success') {
      // Update frontend elements with returned data

       const accessToken = data.access_token;
        // 将令牌存储在本地（例如使用localStorage）
       // setCookie(user.email, 'google',);
         showContainer(4,'showalertls');
        setAccessToken(accessToken);

       // localStorage.setItem('access_token', accessToken);


      // Handle other data if needed

      // Show or hide elements based on the login status
     document.getElementById('None-button').style.display = 'block';
       document.getElementById('Login-button').style.display = 'None';
       document.getElementById('loginPopup').style.display = 'none';
      document.getElementById('signup-button').style.display = 'None';
      var img = document.getElementById('user-img');
      img.src =user.photoURL;
    } else {
      // Handle unsuccessful login (optional)
      console.error('Login failed:', data.message);
    }
  })
    .catch(error => {
  console.error('Error:', error);
    });
      // ...
    }).catch((error) => {
      // 此处处理错误。
      const errorCode = error.code;
      const errorMessage = error.message;
      // 使用的用户帐户的电子邮件。
      // const email = error.customData.email;
      // 使用的AuthCredential类型。
      const credential = GoogleAuthProvider.credentialFromError(error);
      errorMessage;errorCode;credential;
      // ...
    });



}



export function githubLogin() {
  const firebaseConfig = {
  apiKey: "AIzaSyCR0iILgK7aiU-jToDyDThPJ-rZRq5H2TI",
  authDomain: "verseeding.firebaseapp.com",
  projectId: "verseeding",
  storageBucket: "verseeding.appspot.com",
  messagingSenderId: "324985975074",
  appId: "1:324985975074:web:53ee9085289490a058757b",
  measurementId: "G-FJSQSRBPS6"
};
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const provider = new GithubAuthProvider();
  // provider.addScope('user:email');
   provider.setCustomParameters({
    prompt: 'select_account'
  });
  const auth = getAuth();
  let primaryEmail;
  signInWithPopup(auth, provider)
    .then((result) => {
      // This gives you a Google Access Token. You can use it to access the Google API.
      const credential = GithubAuthProvider.credentialFromResult(result);
      const token = credential.accessToken;
      // The signed-in user info.
       app;
      const user = result.user;
      console.log('已登录的用户信息：',user)
      // ...
          fetch('https://api.github.com/user/emails', {
        headers: {
          Authorization: `token ${token}`,
        },
      })
      .then(response => response.json())
      .then(emails => {
        // `emails` is an array of objects with `email`, `primary`, and `verified` properties
        primaryEmail = emails.find(email => email.primary).email;
        console.log('用户的主要电邮是：', primaryEmail);
        // now you have the user's primary email, you can save it to your database
        // name: user.displayName,
        setCookie(user.photoURL);
        console.log('pu',user.photoURL)
        const userInfo = {
            type: "github",
            email: primaryEmail,
            imageUrl: user.photoURL,
            token: token,
            uid: user.uid,
    };

      fetch('https://transform.verseeding.com/auth/callback', {
     method: 'POST',
     headers: {
    'Content-Type': 'application/json'
     },
  body: JSON.stringify(userInfo)
    })
.then(response => response.json()) // Parse the response as JSON
  .then(data => {
    // Handle the response data
    console.log('Response from backend:', data);

    // Check if the login was successful
    if (data.status === 'success') {
      // Update frontend elements with returned data

       const accessToken = data.access_token;
        // 将令牌存储在本地（例如使用localStorage）
       // setCookie(primaryEmail, 'github',);
        setAccessToken(accessToken);
         showContainer(4,'showalertls');

      // Handle other data if needed


      // Show or hide elements based on the login status
     document.getElementById('None-button').style.display = 'block';
       document.getElementById('Login-button').style.display = 'None';
       document.getElementById('loginPopup').style.display = 'none';
      document.getElementById('signup-button').style.display = 'None';
        var img = document.getElementById('user-img');
      img.src =user.photoURL;
    } else {
      // Handle unsuccessful login (optional)
      console.error('Login failed:', data.message);
    }
  })
    .catch(error => {
  console.error('Error:', error);
    });
      // ...
      })
      .catch(error => {
        console.error("获取电邮时发生错误:", error);
      });


    }).catch((error) => {
      // 此处处理错误。
      const errorCode = error.code;
      const errorMessage = error.message;
      // 使用的用户帐户的电子邮件。
      const email = error.customData.email;
      // 使用的AuthCredential类型。

      const credential = GithubAuthProvider.credentialFromError(error);
      errorMessage;errorCode;email;credential;
      // ...
    });


}


function setCookie(img) {
  const expirationDate = new Date();
  expirationDate.setDate(expirationDate.getDate() + 7);

  // 对Email和type进行编码，以处理特殊字符
  // const encodedEmail = encodeURIComponent(Email);
  const encodedType = encodeURIComponent(img);

  // 创建包含编码值的Cookie字符串
  // const cookieEmail = `Email=${encodedEmail}; expires=${expirationDate.toUTCString()}; path=/`;
  const cookieType = `img=${encodedType}; expires=${expirationDate.toUTCString()}; path=/`;

  // 设置Cookie
  // document.cookie = cookieEmail;
  document.cookie = cookieType;
}

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

        function showContainer(time,type) {
      const container = document.getElementById('showalert');
      // showalert-text
      const textDiv = document.getElementById('showalert-text');

      const line = document.getElementById('blueline');
      // .querySelector('.blueline');
        const div = document.getElementById(type);
      const divText = div.innerHTML;

      textDiv.innerHTML = divText;
      // textDiv.innerHTML = str;
      container.style.display = 'flex';

      line.style.animationDuration = `${time}s`;

      setTimeout(() => {
        container.style.display = 'none';
      }, time * 1000);
    }
