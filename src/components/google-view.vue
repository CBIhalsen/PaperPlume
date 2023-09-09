<template>
    <div class="ssocial-login">

    </div>


</template>

<script>
import {githubLogin, googleLogin,thirdLogout } from '../utils/utils.js'
export default {
  mounted() {
     const button = document.getElementById('google-login-button');
    button.addEventListener('click', this.onclick);
    const github = document.getElementById('github-login-button');
    github.addEventListener('click', this.github);
    const Logout = document.getElementById('logout');
    Logout.addEventListener('click', this.Logout);

  },
  methods: {
    onclick() {
      googleLogin()
    },
    github(){
      githubLogin()
    },
    Logout(){

      thirdLogout()
    },
  }
}
</script>

<style>
/* your styles here */
</style>
