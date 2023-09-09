

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>


<template>
  <div id="thirdpartylogin">
    <view-component></view-component>
    <top-up></top-up>
    <chat-window></chat-window>

  </div>
  <div>
    <footerComponent></footerComponent>
  </div>

</template>

<script>
import ViewComponent from './components/google-view.vue'
import Topup from './components/top-up.vue'
import chatwindow from './components/chat-with-service.vue'
import footerComponent from './components/footerComponent.vue'
export default {
  components: {
     'view-component': ViewComponent,
    'top-up': Topup,
    'chat-window':chatwindow,
    'footerComponent': footerComponent,

  }
}
</script>

