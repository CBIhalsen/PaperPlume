<template>

  <!-- Top Up 模态窗口 -->
<div class="login-popup " style="backdrop-filter: blur(10px);" id="topUpModal" data-bs-backdrop="false" tabindex="-1">
  <div class="modal-dialog  custom-width border-topup"  >
    <div class="modal-content custom-width border-topup" >
      <div class="modal-header">
        <h5 class="modal-title" data-lang-key="touup">付费使用</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body" style="font-size: 1rem;">
        <p data-lang-key="touup1"><i class="fa fa-check check-icon"></i>亲爱的用户，感谢您选择我们的论文写作服务。为了持续提供优质的服务并帮助您实现学术目标，我们需要您的支持。</p>
<p data-lang-key="touup2"><i class="fa fa-check check-icon"></i>我们致力于为您提供最高效、最便捷的论文写作工具，让您在学术之路上更加游刃有余。</p>
        <p data-lang-key="touup3"><i class="fa fa-check check-icon"></i>您可以选择充值以继续使用我们的服务。我们提供实惠的价格，每次充值金额不低于0.5美元。您可以使用支付宝进行支付。</p>
        <p data-lang-key="touup4"><i class="fa fa-check check-icon"></i> 再次感谢您对我们的支持和理解。继续您的学术旅程吧！</p>
        <p data-lang-key="touup5">🐣祝写作愉快！</p>
<div class="input-usd">
  <span>$</span>
      <input type="number" ref="amount" class="form-control" @input="InputValue" id = 'amount' min="0.50" max="1000" step="1.00" placeholder="Enter recharge amount in USD" @change="checkInputValue">
</div>
      </div>
      <div class="modal-footer">

           <button type="button" class="alipay-button btn" style="outline: none;"  @click="alipay" >
               <img class="alipay" src="https://i.postimg.cc/pLHnjRQ5/bigalipay.jpg" alt="Alipay"></button>
        <button type="button" class="btn stripe"  @click="stripe">Pay now</button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
    data() {
    return {
      amount: '',
        tempAmount: ''
    };
  },
    methods: {
  InputValue(event) {
    let value = event.target.value;
    let decimal = value.split('.')[1];

    if(decimal && decimal.length > 2) {
      event.target.value = value.slice(0, -(decimal.length-2));
    }
  },


           checkInputValue() {
  var input = document.getElementById("amount");
  var value = parseFloat(input.value);

  if (value < 0.50) {
    input.value = "0.50";

  }
  if (value >1000.00){
      input.value = "1000.00"
  }



},
    stripe() {
      console.log("use stripe")
      // console.log('stripe222')
      // window.open('https://en.wikipedia.org/wiki/URL_encoding');
      const accessToken = this.getAccessToken();

       if ( !accessToken) {
         console.log('stripe no')
             return ;
}


        fetch("http://127.0.0.1:5000/create_payment", {
    method: "POST",
     body: JSON.stringify({

    type: 'stripe'
  }),
    headers: {
      "Content-Type": "application/json",
         'Authorization': `Bearer ${accessToken}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {

      if (data.type === "stripe") {
            window.open(data.url);
          }

    });
    },



     getAccessToken() {
  const tokenString = localStorage.getItem('access_token');
  if (!tokenString) {
    return null; // 如果没有access_token，则返回null
  }

  const tokenObject = JSON.parse(tokenString);
  return tokenObject.token;
},

          alipay() {
       const inputValue = this.$refs.amount.value;
         const accessToken = this.getAccessToken();
       if (!inputValue || !accessToken) {
             return ;
}


        fetch("http://127.0.0.1:5000/create_payment", {
    method: "POST",
     body: JSON.stringify({

    type: 'alipay',
    amount: inputValue,
  }),
    headers: {
      "Content-Type": "application/json",
         'Authorization': `Bearer ${accessToken}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {

      if (data.type === "alipay") {
            window.open(data.url);
          }

    });
    },







  }
}

</script>

<style>

        .alipay-button:hover {
  background-color: #f2f2f2;
}

      .alipay {
    width:auto;
    height: 45.5px;
  }

.border-topup{
  background-color: whitesmoke;
    border-radius: 5%;
}
/* your styles here */


  .input-usd {
    position: relative;
    /*display: inline-block;*/
  }

  .input-usd span {
    position: absolute;
    top: 50%;
    left: 10px;
    transform: translateY(-50%);
    color: #555555;
  }

  .input-usd input {
    padding-left: 25px;
  }
    .check-icon {
    color: #007bff;
    font-size: 20px;
    margin-right: 5px;
  }
    .stripe {
          background: #5469d4;
  font-family: Arial, sans-serif;
  color: #ffffff;
  border-radius: 4px;
  border: 0;
  padding: 12px 16px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display:  inline-block; ;
  transition: all 0.2s ease;
  box-shadow: 0px 4px 5.5px 0px rgba(0, 0, 0, 0.07);
  width: auto;
    }
        .alipay-button {
          background: transparent!important;
  font-family: Arial, sans-serif;
  color: #ffffff;
  border-radius: 4px;
  border: 0px;
  padding: 2px ;
  font-size: 16px;
            margin-right: 20px;
  font-weight: 600;
  cursor: pointer;
  display:  inline-block; ;
  transition: all 0.2s ease;
box-shadow: 0 0 0.2rem rgba(16, 15, 15, 0.1);
  width: auto;
    }

</style>
