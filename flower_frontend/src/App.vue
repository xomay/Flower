<template>
  <div
    id="app"
    v-loading="loading"
    :class="{'h-screen': loading}"
  >
    <router-view v-if="!loading" />
  </div>
</template>

<script>
const axios = require("axios")
axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

export default {
  name: "App",
  data () {
    return {
      loading: true
    }
  },
  beforeCreate () {
    axios.get(
      "/api/accounts/login",
      {withCredentials: true}
    ).then((res) => {
      console.log(res)
      this.loading = false
    }).
      catch(() => {
        // Allows unsigned users to go to password reset pages
        if (this.$router.currentRoute.path.includes("passwordreset")) {
          this.loading = false
          return
        }
        this.$router.push(
          "/login",
          () => {
            this.loading = false
          },
          () => {
            this.loading = false
          }
        )
      })
  }
}
</script>

<style lang="scss">
@import "tailwindcss/base";
@import "tailwindcss/components";
@import "tailwindcss/utilities";

:root {
  --main-bg-color: #545c64;
}

.el-loading-spinner > .circular {
  margin: auto !important;
}

.el-card, .el-button {
  border-radius: 0.5rem !important;
}
.el-button--text {
  padding: 1rem !important;
}
.el-button--text:hover {
  background-color: #eee !important;
}
body {
  overflow-y: scroll;
}
button.dark {
  background-color: transparent !important;
  border: none;
  color: #eee;
}
button.dark:hover {
  background-color: #0004 !important;
  color: white;
}
button.dark:focus {
  color: white;
}

</style>
