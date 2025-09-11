module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: process.env.VUE_APP_SITE_URL,
        changeOrigin: true
      },
    }
  }
}