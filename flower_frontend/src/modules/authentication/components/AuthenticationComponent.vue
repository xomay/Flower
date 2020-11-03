<template>
  <el-card class="w-64">
    <img src="@/assets/Logo_fond_blanc.jpg">
    <h1 class="text-center font-semibold m-2">
      Connexion
    </h1>
    <el-form :model="authForm">
      <el-form-item>
        <el-input
          v-model="authForm.username"
          placeholder="Nom d'utilisateur"
          @keydown.enter.native="submitAuthForm"
        />
      </el-form-item>
      <el-form-item>
        <el-input
          v-model="authForm.password"
          placeholder="Mot de passe"
          show-password
          @keydown.enter.native="submitAuthForm"
        />
      </el-form-item>
      <el-form-item>
        <el-button
          class="w-full"
          type="primary"
          :loading="connectionLoading"
          @click="submitAuthForm"
        >
          Connexion
        </el-button>
      </el-form-item>
    </el-form>
    <el-alert
      v-if="errorMessage"
      :title="errorMessage"
      type="error"
      show-icon
    />
  </el-card>
</template>

<script>
const axios = require("axios")

export default {
  name: "LoginComponent",
  data () {
    return {
      authForm: {
        username: "",
        password: ""
      },
      connectionLoading: false,
      errorMessage: ""
    }
  },
  methods: {
    submitAuthForm () {
      this.connectionLoading = true
      this.errorMessage = ""
      axios.post(
        `${this.$server_url}/accounts/login`,
        this.authForm,
        {withCredentials: true}
      ).then(() => {
        this.$router.push("/")
      }).
        catch((err) => {
          this.errorMessage = err
        }).
        finally(() => {
          this.connectionLoading = false
        })
    }
  }
}
</script>

<style>

</style>
