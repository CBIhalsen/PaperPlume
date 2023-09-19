
     function openregisterpopup(type) {
      // document.getElementById('registerModal').style.display = 'flex';
         openLoginPopup();
         if (type=='forget'){
             console.log();
             // fregister
         document.getElementById('ypas').style.display='none';
         document.getElementById('npss').style.display='block';
         document.getElementById('fcpc').style.display='block';
         document.getElementById('ecc').style.display='block';
         document.getElementById('fregister').style.display='block';
         document.getElementById('login').style.display='none';
         document.getElementById('allogin').style.display='block';
         document.getElementById('fp').style.display='none';
         document.getElementById('nosignup').style.display='none';
         document.getElementById('fsendCodeBtn').style.display='block';
         document.getElementById('sendCodeBtn').style.display='none';


         }
         else {
                      document.getElementById('cpc').style.display='block';
         document.getElementById('ecc').style.display='block';
         document.getElementById('register').style.display='block';
         document.getElementById('login').style.display='none';
         document.getElementById('allogin').style.display='block';
         document.getElementById('fp').style.display='none';
         document.getElementById('nosignup').style.display='none';
                           document.getElementById('sendCodeBtn').style.display='block';
         document.getElementById('fsendCodeBtn').style.display='none';


         }





         const elements = document.querySelectorAll('.input-container');
        elements.forEach(element => {
             element.style.marginBottom = '0.5rem';

                  // 获取所有具有 class="input-filed" 的元素

        });
        const elements2 = document.querySelectorAll('.input-field');

        // 遍历每个元素并修改 margin-bottom 属性
        elements2.forEach(element => {
               element.style.height = '2rem';
        });

    }

    // 关闭注册弹窗
    function closeregisterpopup() {
      document.getElementById('registerModal').style.display = 'none';
    }

            function openLoginPopup() {
    // fcpc fsyp
    //             npss ypas fregister
        document.getElementById('fregister').style.display='none';
        document.getElementById('ypas').style.display='block';
        document.getElementById('npss').style.display='none';
        document.getElementById('fcpc').style.display='none';
        document.getElementById('loginPopup').style.display = 'flex';
                 document.getElementById('cpc').style.display='none';
         document.getElementById('ecc').style.display='none';
         document.getElementById('register').style.display='none';
         document.getElementById('login').style.display='block';
         document.getElementById('allogin').style.display='none';
         document.getElementById('fp').style.display='block';
         document.getElementById('nosignup').style.display='block';
                  const elements = document.querySelectorAll('.input-container');
        elements.forEach(element => {
             element.style.marginBottom = '1.08rem';

                  // 获取所有具有 class="input-filed" 的元素

        });
        const elements2 = document.querySelectorAll('.input-field');

        // 遍历每个元素并修改 margin-bottom 属性
        elements2.forEach(element => {
               element.style.height = '2.7rem';
        });


        }


        function check_email(type) {
          const input = document.getElementById('emailInput');
          input.reportValidity();
          console.log(type)
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // 正则表达式用于验证邮箱格式

  if (!emailRegex.test(input.value)) {
    return; // 如果输入值不是有效的邮箱格式，直接返回
  }

      // 向后端发送GET请求
        fetch(`https://transform.verseeding.com/check?email=${input.value}&type=${type}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.text())
        .then(data => {
            console.log(data)
          // alert(data.message)
     if (data == "True") {
            // alert("true")
        // 后端返回的是 True
        // 执行相应的操作
        //
        // input.setCustomValidity('');
        sendVerificationCode(type);

    } else if (data == "False") {
        // 后端返回的是 False
        // 执行相应的操作
        // alert("false")
        input.setCustomValidity('Email account already exists');
         input.reportValidity();
        // input.reportValidity();
    } else if(data == "none"){
         input.setCustomValidity('Email account does not exist.');
           input.reportValidity();
        // input.reportValidity();

          }
     else {
        // 处理其他情况
        console.log("未知的返回值: " + data);
    }
        })
        .catch(error => {
            // 处理错误
            console.error('Error:', error);
        });
}
    function check(input,type) {
    if (type=='register'){
      if (input.value != document.getElementById('passwordInput').value) {
        input.setCustomValidity('Passwords do not match. Please try again.');
    } else {
        // 输入正确，重置错误消息
        input.setCustomValidity('');
    }

    } else{
              if (input.value != document.getElementById('fpasswordInput').value) {
        input.setCustomValidity('Passwords do not match. Please try again.');
    } else {
        // 输入正确，重置错误消息
        input.setCustomValidity('');
    }

    }
     input.reportValidity();

}
    var countdownInterval; // 用于存储倒计时的定时器
    // document.getElementById("open-modal-button").addEventListener("click", openModal);

    // 打开注册弹窗
    // function openModal() {
    //   document.getElementById('registerModal').style.display = 'block';
    // }
    //
    // // 关闭注册弹窗
    // function closeModal() {
    //   document.getElementById('registerModal').style.display = 'none';
    // }

    // 发送验证码
    function sendVerificationCode(type) {
      var email = document.getElementById('emailInput').value;
          showContainer(6,'showalertsc');
      if (type=='register'){
      var sendCodeBtn = document.getElementById('sendCodeBtn');
      var loader = document.getElementById('sloader');
      var buttonText = document.getElementById('sendcodeText');
      var countdown = document.getElementById('sendcountdown');
      } else{
      var sendCodeBtn = document.getElementById('fsendCodeBtn');
      var loader = document.getElementById('fsloader');
      var buttonText = document.getElementById('fsendcodeText');
      var countdown = document.getElementById('fsendcountdown');
      }


      var verifyCode = generateRandomNumber();
     const input = document.getElementById('emailInput');
     input.reportValidity();
      // alert(verifyCode)

      document.getElementById("codenumber").value = verifyCode;

      // 检查邮箱是否有效，这里可以使用正则表达式进行更详细的验证

      if (!validateEmail(email)) {
        input.reportValidity();
        return;
      }
      fetch('https://transform.verseeding.com/send_code', {
      method: 'POST',
      headers: {
      'Content-Type': 'application/json',

    },
     body: JSON.stringify({ temp_id: verifyCode, email: email })
  })
  .then(response => {
    // 处理响应
    if (response.ok) {
      console.log('验证码已成功发送！');
    } else {
      console.error('发送验证码时发生错误。');
    }
  })
  .catch(error => {
    console.error('发送请求时发生网络错误:', error);
  });


      // 禁用发送验证码按钮并显示倒计时
      sendCodeBtn.disabled = true;
      countdown.innerText = '60s';
      var timeLeft = 60;
      buttonText.style.display = 'none';
      countdownInterval = setInterval(function() {
        timeLeft--;
        countdown.innerText = timeLeft + 's' ;

        if (timeLeft <= 0) {
          clearInterval(countdownInterval);
          loader.style.display = 'none'; // 隐藏加载圈
           buttonText.style.display = 'flex';
          // loader.style.display = 'inline-block';
          sendCodeBtn.disabled = false;
          countdown.innerText = '';
        }
      }, 1000);



    }

 function register(type){

          const emailInput = document.getElementById('emailInput');
          const fconfirmPassword = document.getElementById('fconfirmPassword');
          const confirmPassword = document.getElementById('confirmPassword');
           const passwordInput = document.getElementById('passwordInput');
           const fpasswordInput = document.getElementById('fpasswordInput');
  const verificationCode = document.getElementById('verificationCode');

        emailInput.reportValidity();
    fconfirmPassword.reportValidity();
    verificationCode.reportValidity();
    fpasswordInput.reportValidity();
    fconfirmPassword.reportValidity();
       passwordInput.reportValidity();

  // if (!passwordInput.checkValidity()||!fpasswordInput.checkValidity()){
  //      showContainer(6,'prequir');
  // }

  if(type=='register'){
      if (!passwordInput.checkValidity()){
          showContainer(30,'prequir');
      }

      else if (!confirmPassword.checkValidity() || !verificationCode.checkValidity() ||!emailInput.checkValidity() ) {
            return;
        }

      else {
    registerfetch(type);
  }
  }

  if(type=='forget'){
      if (!fpasswordInput.checkValidity()){
          showContainer(30,'prequir');
      }

      else if (!fconfirmPassword.checkValidity() || !verificationCode.checkValidity() ||!emailInput.checkValidity() ||!fpasswordInput.checkValidity()) {
            return;
        }

   else {
    registerfetch(type);
  }
  }


  // event.preventDefault(); // 首先阻止表单提交
  // if (!event.target.checkValidity()) {
  //   // 如果表单没有通过验证，显示出验证消息
  //   // 注意，这个消息是浏览器默认的，可能在不同浏览器上显示效果不同
  //   event.target.reportValidity();
  // } else {
  //
  //   registerfetch(type);
  //
  // }
}



    // 注册
    function registerfetch(type) {
      //
      // var username = document.getElementById('username').value;
      var email = document.getElementById('emailInput').value;

      // var confirmPassword = document.getElementById('confirmPassword').value;
      var verificationCode = document.getElementById('verificationCode').value;
      // var passwordHelpBlock = document.getElementById('passwordHelpBlock');
      // event.preventDefault();
      // checkValidity()
      const randomNum = document.getElementById("codenumber").value;
      const input = document.getElementById('emailInput');
      input.setCustomValidity('');
      if (type=='forget'){
          const password = document.getElementById('fpasswordInput').value;
           const formData = new FormData();
      formData.append("type", 'forget');
      formData.append("password", password);
      formData.append("email", email);
      formData.append("code", verificationCode);
      formData.append("temp_id", randomNum);

        fetch("https://transform.verseeding.com/register_account", {
        method: "POST",
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        // alert(data.message);

        if (data.status === 'success') {
          // alert('注册成功');
            closeLoginPopup();
             showContainer(4,'showalertrs');
          closeModal();
        } else  {
             showContainer(10,'sce');
          // event.preventDefault();

        }
      })
      .catch(error => console.log(error));
      }  else {
          const password = document.getElementById('passwordInput').value;
           const formData = new FormData();
      formData.append("type", 'register');
      formData.append("password", password);
      formData.append("email", email);
      formData.append("code", verificationCode);
      formData.append("temp_id", randomNum);

        fetch("https://transform.verseeding.com/register_account", {
        method: "POST",
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        // alert(data.message);

        if (data.status === 'success') {
          // alert('注册成功');
            const email_str =data.email;
            const password_str=data.password;
            Tologin(email_str,password_str);
           showContainer(4,'showalertss');
          // closeModal();
        } else  {
            showContainer(10,'sce');
          // event.preventDefault();

        }
      })
      .catch(error => console.log(error));
      }





    }




    // 生成六位数字的随机数
    function generateRandomNumber() {
      return Math.floor(100000 + Math.random() * 900000);
    }
    // 验证邮箱格式
    function validateEmail(email) {
      var emailRegex = /^\S+@\S+\.\S+$/;
      return emailRegex.test(email);
    }
    function closeLoginPopup() {
            document.getElementById('loginPopup').style.display = 'none';
          }