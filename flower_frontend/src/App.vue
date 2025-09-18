<template>
  <div id="app" v-loading="loading" :class="{ 'h-screen': loading }">
    <router-view v-if="!loading" />
  </div>
</template>

<script>
import axios from "axios";  // Utilisation de l'importation ES6

// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

export default {
  name: "App",
  data() {
    return {
      loading: true,
    };
  },
  created() {  // Utiliser 'created' au lieu de 'beforeCreate'
    axios
      .post("/api/accounts/login", {
        withCredentials: true
      })
      .then((res) => {
        this.$store.currentUser = res.data;
        this.loading = false;
      })
      .catch((error) => {
        // Permet aux utilisateurs non connectés d'accéder aux pages de réinitialisation de mot de passe
        if (this.$route.path.includes("passwordreset")) {
          this.loading = false;
          return;
        }
        this.$router.push("/login");
        this.loading = false; // Déplacer cela ici pour s'assurer que loading est mis à false
      });
  },
};
</script>

<style lang="scss">
@import "tailwindcss/base";
@import "tailwindcss/components";
@import "tailwindcss/utilities";
@import 'element-plus/theme-chalk/index.css';

:root {
  --main-bg-color: #545c64;
  --el-color-primary: #1351aa;
  --el-color-success: #67c23a;
  --el-color-warning: #e6a23c;
  --el-color-danger:  #f56c6c;
  --el-color-info:    #909399;
}

.el-loading-spinner>.circular {
  margin: auto !important;
}

.el-card,
.el-button {
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
