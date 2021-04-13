<template>
  <BaseComponent
    title="Ajout d'un membre"
    :breadcrumb="breadcrumb"
  >
    <MemberForm
      v-model="form"
      :postes="postes"
      :loadingopenaccount="loading"
      :loading="loading"
      @save="registerMember"
    />
  </BaseComponent>
</template>

<script>
import MemberForm from "../components/MemberForm"

const axios = require("axios")

export default {
  name: "EtudeCreer",
  components: {MemberForm},
  data () {
    return {
      form: {
        firstname: "",
        lastname: "",
        gender: "M.",
        promotion: "2021",
        email: "@insa-rennes.fr",
        email_junior: "@ouest-insa.fr",
        poste: 0,
        mobile: "",
        address: "",
        postcode: "",
        town: "Rennes",
        country: "France",
        nationality: "Française",
        birth_date: "",
        birth_place: ""
      },
      postes: [],
      loading: false,
      breadcrumb: [
        {
          name: "Liste des membres",
          link: "/membres"
        },
        {
          name: "Ajouter un membre",
          link: "/membres/ajouter"
        }
      ]
    }
  },
  beforeCreate () {
    axios.get(
      "/api/administration/postes/",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.postes = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le membre : "+ err, type: "error"})
    })
  },
  methods: {
    registerMember () {
      this.loading = true
      axios.post(
        "/api/membres/",
        this.form,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le membre a bien été ajouté.", type: "success"})
        this.$router.push("/membres")
      }).catch((err) => {
        this.$message({message: "Impossible de créer un membre : "+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    }
  }
}
</script>
