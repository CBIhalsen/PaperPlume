//这是你的测试可发布API密钥。
const stripe = Stripe("pk_live_51NTks7EmFokDEaGkzZkhyBj0yLkFlLaYbfHK3a7WxOzayZViD0ZVfct3QY1KIdkkFYvmJGB9lxnKPA4A0cLwQE1r00zUkfm4mL");

// The items the customer wants to buy
const items = [{ id: "xl-tshirt" }];

let elements;

initialize();
checkStatus();

document
  .querySelector("#payment-form")
  .addEventListener("submit", handleSubmit);

let emailAddress = '';
//获取支付意图并捕获客户端秘密
const accessToken =  getAccessToken();
console.log(accessToken)
async function initialize() {
  const response = await fetch("http://127.0.0.1:5000/create_payment", {
    method: "POST",
    headers: { "Content-Type": "application/json",

    },
    body: JSON.stringify({ items , type: "stripe",amount: 200}),
  });
const data = await response.json();

const { clientSecret, amount } = data;

console.log('Client Secret:', clientSecret);
console.log('Amount:', amount);
  const appearance = {
    theme: 'stripe',
  };
  elements = stripe.elements({ appearance, clientSecret });

  const linkAuthenticationElement = elements.create("linkAuthentication");
  linkAuthenticationElement.mount("#link-authentication-element");

  linkAuthenticationElement.on('change', (event) => {
    emailAddress = event.value.email;
  });

  const paymentElementOptions = {
    layout: "tabs",
  };

  const paymentElement = elements.create("payment", paymentElementOptions);
  paymentElement.mount("#payment-element");
}

async function handleSubmit(e) {
  e.preventDefault();
  setLoading(true);

  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
//确保将此更改为付款完成页面
      return_url: "http://localhost:8080/checkout.html",
      receipt_email: emailAddress,
    },
  });

//只有在执行命令时发生立即错误时才会到达此点
//确认付款。否则，您的客户将被重定向到
//你的' return_url '。对于某些付款方式，如iDEAL，您的客户会
//被重定向到一个中间站点，然后授权支付
//重定向到' return_url '。
  if (error.type === "card_error" || error.type === "validation_error") {
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occurred.");
  }

  setLoading(false);
}

//在支付提交后获取支付意图状态
async function checkStatus() {
  const clientSecret = new URLSearchParams(window.location.search).get(
    "payment_intent_client_secret"
  );

  if (!clientSecret) {
    return;
  }

  const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

  switch (paymentIntent.status) {
    case "succeeded":
      showMessage("Payment succeeded!");
      break;
    case "processing":
      showMessage("Your payment is processing.");
      break;
    case "requires_payment_method":
      showMessage("Your payment was not successful, please try again.");
      break;
    default:
      showMessage("Something went wrong.");
      break;
  }
}

// ------- UI helpers -------

function showMessage(messageText) {
  const messageContainer = document.querySelector("#payment-message");

  messageContainer.classList.remove("hidden");
  messageContainer.textContent = messageText;

  setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageContainer.textContent = "";1
  }, 1000);
}

//在付款提交时显示转轮
function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}

// eslint-disable-next-line no-unused-vars
function getAccessToken() {
  const tokenString = localStorage.getItem('access_token');
  if (!tokenString) {
    return null; // 如果没有access_token，则返回null
  }

  const tokenObject = JSON.parse(tokenString);
  return tokenObject.token;
}
