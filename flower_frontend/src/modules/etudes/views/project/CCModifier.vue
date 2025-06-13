<template>
  <BaseComponent
    title="Modifier une Convention Cadre"
    :breadcrumb="breadcrumb"
  >
    <ConventionCadreForm
      v-model="form"
      :loading="loading"
      :members="members"
      :prospects="prospects"
      :taken-ids="takenIds"
      @save="submitChanges"
    />
  </BaseComponent>
</template>

<script>
import ConventionCadreForm from "../../components/projectConvention/ConventionCadreForm";

const axios = require("axios")

// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

export default {
  name: "CCModifier",
  components: { ConventionCadreForm },
  data () {
    return {
      loading: false,
      breadcrumb: [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: "Modifier une Convention Cadre",
          link: `/cc/${this.$route.params.id}/modifier`
        }
      ],
      form: {
        prospect: "",
        name: "",
        description: "",
        mandat: new Date().getFullYear(),
        number: 0,
        confidential: false,
        period: 2,
        signer1: "",
        signer2: "",
        signDate: "",
      },
      members: [],
      prospects: [],
      takenIds: []
    }
  },
  beforeCreate () {
    axios.get(
      "/api/etudes/",
      {withCredentials: true}
    ).then((res) => {
      const year = new Date().getFullYear()
      const baseInt = parseInt(year.toString().slice(-2) + "000", 10)
      this.takenIds = res.data.filter(etu => etu.mandat === year).map(etu => etu.number)
      const amount = this.takenIds.length
      const result = amount + baseInt
      axios.get(
        `/api/etudes/${this.$route.params.id}/cc/`,
        {withCredentials: true}
      ).then((res) => {
        this.form = res.data
        this.form.signer1 = res.data.signer1 ? res.data.signer1.id : ""
        this.form.signer2 = res.data.signer2 ? res.data.signer2.id : ""
        this.form.prospect = res.data.prospect.id
        this.breadcrumb[1].name = res.data.name
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer la Convention Cadre : " + err, type: "error", offset: 40})
      })
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la liste des études : " + err, type: "error", offset: 40})
    })
  },
  created () {
    axios.get(
      "/api/prospects",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.prospects = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la liste des prospects : " + err, type: "error", offset: 40})
    })
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
    submitChanges () {
      console.log("Submitting CC changes:", this.form)
      this.loading = true
      axios.put(
        `/api/etudes/${this.$route.params.id}/cc/`,
        this.form,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "La Convention Cadre a bien été modifiée.",
          type: "success",
          offset: 40})
        this.$router.push("/etudes")
      }).catch((err) => {
        this.$message({message: "Erreur lors de l'enregistrement : " + err, type: "error"})
        if (err.response && err.response.status === 400) {
          this.$message({message: "Le formulaire comporte des erreurs.",
            type: "error",
            offset: 40})
        } else {
          this.$message({message: "Impossible de modifier la convention pour le moment.",
            type: "error",
            offset: 40})
        }
      }).finally(() => {
        this.loading = false
      })
    }
  }
}
</script>
