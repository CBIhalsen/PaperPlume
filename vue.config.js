const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    allowedHosts: [
      'host.com',
      '.host.com',
      'huge-model-javelin.ngrok-free.app'
    ]
  }
})
