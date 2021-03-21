<template>
  <BaseComponent
    title="Votre profil"
    :breadcrumb="breadcrumb"
  >
    Votre signature :<br>
    <i><font color="gray">
      Faites un clic droit puis "enregistrer l'image" pour sauvegarder votre signature.
    </font></i>
    <div
      v-show="displaysSignature"
      v-loading="!signatureJPG"
      class="flex-1"
      style="margin-top: 25px;"
    >
      <img
        :src="`data:image/jpeg;base64,${signatureJPG}`"
        width="95%"
      >
    </div>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
export default {
  name: "ProfileView",
  data () {
    return {
      breadcrumb: [
        {
          name: "Votre profil",
          link: "/profil"
        }
      ],
      signatureJPG: "",
      displaysSignature: true
    }
  },
  created () {
    axios.get(
      "/api/signature/",
      {
        withCredentials: true,
        responseType: "arraybuffer"
      }
    ).then((res) => {
      this.signatureJPG = Buffer.from(
        res.data,
        "binary"
      ).toString("base64")
    }).catch((err) => {
      if(err.message == "Request failed with status code 401")
        this.$message({message: "Votre compte n'est pas relié à un utilisateur (compte admin ?)", type: "error"})
      else if(err.message == "Request failed with status code 503")
        this.$message({message: "Pensez à instancier les paramètres de la JE !", type: "error"})
      else
        this.$message({message: "Impossible de récupérer la signature : "+err, type: "error"})
      this.displaysGantt = false
    })
  }
}
</script>