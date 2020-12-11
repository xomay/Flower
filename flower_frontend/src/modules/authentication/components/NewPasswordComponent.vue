<template>
  <el-card class="w-64">
    <img src="@/assets/Logo_fond_blanc.jpg">
    <h1 class="text-center font-semibold m-2">
      Réinitialisation du mot de passe
    </h1>
    <el-form :model="form">
      <el-form-item>
        <el-input
          v-model="form.password"
          placeholder="Mot de passe"
          show-password
          @keydown.enter.native="submitAuthForm"
        />
      </el-form-item>
      <el-form-item>
        <el-input
          v-model="passwordConfirmation"
          placeholder="Confirmation du mot de passe"
          show-password
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
          Enregistrer
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
  name: "NewPasswordComponent",
  data () {
    return {
      form: {
        password: "",
      },
      passwordConfirmation: "",
      loading: false,
      errorMessage: "",
      successMessage: "",
    }
  },
  methods: {
    submitForm () {
      if (this.form.password !== this.passwordConfirmation) {
        this.errorMessage = "Les mots de passe ne correspondent pas."
        return
      }
      this.form.token = this.$route.params.token
      this.loading = true
      this.errorMessage = ""
      this.successMessage = ""
      axios.post(
        `${this.$server_url}/password_reset/confirm/`,
        this.form,
        {withCredentials: true}
      ).then(() => {
        this.successMessage = "Votre mot de passe a bien été modifié, vous pouvez à présent vous connecter."
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
