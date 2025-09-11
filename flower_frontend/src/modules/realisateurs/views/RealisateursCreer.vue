<template>
  <BaseComponent
    title="Ajouter un réalisateur"
    :breadcrumb="breadcrumb"
    :loading="loading"
  >
    <RealisateurForm
      v-model="realisateur"
      :members="members"
      :loading="loading"
      :ecole-suffix="mailSuffix"
      @edited="createRea"
    />
  </BaseComponent>
</template>

<script>
import RealisateurForm from "../components/RealisateurForm.vue"
import GlobalData from "@/mixins/GlobalData"
const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

export default {
  name: "RealisateurCreer",
  components: { RealisateurForm },
  mixins: [GlobalData],
  data () {
    return {
      mailSuffix: "",
      realisateur: {
        lastname: "",
        firstname: "",
        gender: "M.",
        promotion: 2025,
        mobile: "",
        email: "",
        email_insa: "@insa-rennes.fr",
        address: "",
        postcode: "",
        town: "Rennes",
        country: "France",
        nationality: "Française",
        birth_date: "",
        birth_place: "",
        filiere: "INFO",
        security_social_number: "",
        isMember: false,
        member: "",
        ba: null,
        ba_id: null,
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
      ],
      members: []
    }
  },
  created () {
    this.queryData(axios, "mail_suffix")
      .then((res) => this.mailSuffix = "@" + res.data[0])
      .catch((err) => this.$message({message: "Erreur: " + err, type: "error"}))
    axios.get(
      "/api/membres",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.firstname + " " + elt.lastname)
      this.members = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la liste des prospects : " + err, type: "error", offset: 40})
    })
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
