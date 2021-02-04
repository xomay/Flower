<template>
  <BaseComponent
    title="Ajouter un réalisateur"
    :breadcrumb="breadcrumb"
    :loading="loading"
  >
    <RealisateurForm
      :value="realisateur"
      :loading="loading"
      @edited="createRea"
    />
  </BaseComponent>
</template>

<script>
import RealisateurForm from "../components/RealisateurForm.vue"
const axios = require("axios")

export default {
  name: "RealisateurCreer",
  components: { RealisateurForm },
  data () {
    return {
      realisateur: {
        lastname: "",
        firstname: "",
        gender: "",
        promotion: "2021",
        mobile: "",
        email: "",
        email_insa: "",
        address: "",
        postcode: "",
        town: "",
        country: "France",
        nationality: "FR",
        birth_date: "",
        birth_place: "",
        filiere: "INFO",
        security_social_number: ""
      },
      loading: false,
      breadcrumb: [
        {
          name: "Liste des réalisateurs",
          link: "/realisateurs"
        },
        {
          name: "Ajouter un réalisateur",
          link: "/realisateurs/ajouter"
        }
      ]
    }
  },
  methods: {
    createRea () {
      this.loading = true
      axios.post(
        "/api/realisateurs/",
        this.realisateur,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le réalisateur a bien été ajouté.", type: "success"})
        this.$router.push("/realisateurs")
      }).catch((err) => {
        this.$message({message: "Impossible d'ajouter le réalisateur : "+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    }
  }
}
</script>
