<template>
  <el-card class="w-64 mx-auto my-8">
    <img src="@/assets/Logo_fond_blanc.jpg" :style="logoStyle" alt="Logo" />
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
    <el-button type="danger" @click="redirectToGoogleAuthSimple">
      Connexion avec Google
    </el-button>
        <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon />
  </el-card>
</template>

<script>
export default {
  name: "LoginComponent",
  data() {
    return {
      authForm: {
        username: "",
        password: ""
      },
      logoStyle: {
        width: '100%',
      },
      connectionLoading: false,
      errorMessage: "",
    };
  },

  methods: {
    async redirectToGoogleAuthSimple(){
    try {
      window.location.href = 'http://127.0.0.1:8000/accounts/google/login/';
    } catch (error) {
      console.error('Erreur de connexion Google', error);
    }
  },
  validateForm() {},
  },
};
</script>