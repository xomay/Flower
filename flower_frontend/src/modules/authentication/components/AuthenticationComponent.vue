<template>
  <el-card class="w-64 mx-auto my-8"> <!-- Centrer la carte -->
    <img src="@/assets/Logo_fond_blanc.jpg" alt="Logo" />
    <h1 class="text-center font-semibold m-2">Connexion</h1>
    <el-form ref="authentFormRef" :model="authForm">
      <el-form-item
        prop="username"
        :rules="[{ required: true, message: 'Obligatoire', trigger: 'change' }]">
        <el-input
          v-model="authForm.username"
          placeholder="Nom d'utilisateur"
          @keydown.enter.native="validateForm()"
        />
      </el-form-item>
      <el-form-item
        prop="password"
        :rules="[{ required: true, message: 'Obligatoire', trigger: 'change' }]">
        <el-input
          v-model="authForm.password"
          placeholder="Mot de passe"
          show-password
          @keydown.enter.native="validateForm()"
        />
      </el-form-item>
    </el-form>
    <el-button
      class="w-full"
      type="primary"
      :loading="connectionLoading"
      @click="validateForm()">
      Connexion
    </el-button>
    <router-link :to="`/passwordreset`">Mot de passe oublié</router-link>
    <el-alert
      v-if="errorMessage"
      :title="errorMessage"
      type="error"
      show-icon
    />
  </el-card>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginComponent",
  data() {
    return {
      authForm: {
        username: "",
        password: ""
      },
      connectionLoading: false,
      errorMessage: ""
    };
  },
  methods: {
    validateForm() {
      this.errorMessage = "";
      this.$refs.authentFormRef.validate((r) => {
        if (r) {
          this.submitAuthForm();
        } else {
          this.$message({ message: "Certains champs ne sont pas remplis !", type: "error" });
          this.errorMessage = "Certains champs ne sont pas remplis.";
        }
      });
    },
    submitAuthForm() {
      this.connectionLoading = true;
      this.errorMessage = "";
      axios.post(
        "/api/accounts/login",
        this.authForm,
        { withCredentials: true }
      )
      .then((res) => {
        this.$store.currentUser = res.data;
        this.$router.push("/");
      })
      .catch((err) => {
        if (err.response && err.response.status === 401) {
          this.errorMessage = "Les identifiants ne correspondent à aucun compte.";
        } else {
          this.errorMessage = err.message;
        }
      })
      .finally(() => {
        this.connectionLoading = false;
      });
    }
  }
};
</script>
