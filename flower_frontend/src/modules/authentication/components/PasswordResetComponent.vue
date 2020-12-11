<template>
  <el-card class="w-64">
    <img src="@/assets/Logo_fond_blanc.jpg">
    <h1 class="text-center font-semibold m-2">
      Réinitialisation du mot de passe
    </h1>
    <el-form :model="form">
      <el-form-item>
        <el-input
          v-model="form.email"
          placeholder="Adresse mail"
          @keydown.enter.native="submitForm"
        />
      </el-form-item>
      <el-form-item>
        <el-button
          class="w-full"
          type="primary"
          :loading="loading"
          @click="submitForm"
        >
          Envoyer
        </el-button>
      </el-form-item>
    </el-form>
    <el-alert
      v-if="successMessage"
      :title="successMessage"
      type="success"
      show-icon
    />
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
  name: "PasswordResetComponent",
  data () {
    return {
      form: {
        email: "",
      },
      loading: false,
      errorMessage: "",
      successMessage: "",
    }
  },
  methods: {
    submitForm () {
      this.loading = true
      this.errorMessage = ""
      this.successMessage = ""
      axios.post(
        `${this.$server_url}/password_reset/`,
        this.form,
        {withCredentials: true}
      ).then(() => {
        this.successMessage = "Un e-mail avec un lien de réinitialisation vous a été envoyé."
      }).
        catch((err) => {
          this.errorMessage = err
        }).
        finally(() => {
          this.loading = false
        })
    }
  }
}
</script>

<style>

</style>
