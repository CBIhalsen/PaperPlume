  // Google 登录
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";

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
  const auth = getAuth();
  signInWithPopup(auth, provider)
    .then((result) => {
      // This gives you a Google Access Token. You can use it to access the Google API.
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const token = credential.accessToken;
      // The signed-in user info.
      const user = result.user;
      console.log('已登录的用户信息：',user)
      // ...
    }).catch((error) => {
      // 此处处理错误。
      const errorCode = error.code;
      const errorMessage = error.message;
      // 使用的用户帐户的电子邮件。
      const email = error.customData.email;
      // 使用的AuthCredential类型。
      const credential = GoogleAuthProvider.credentialFromError(error);
      // ...
    });
}
