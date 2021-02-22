<template>
  <BaseComponent
    title="Ajouter une étude"
    :breadcrumb="breadcrumb"
  >
    <ProjectForm
      v-model="form"
      :loading="loading"
      :members="members"
      :prospects="prospects"
      :taken-ids="takenIds"
      @save="submitProject"
    />
  </BaseComponent>
</template>

<script>
import ProjectForm from "../../components/forms/ProjectForm"

const axios = require("axios")

export default {
  name: "EtudeCreer",
  components: { ProjectForm },
  data () {
    return {
      loading: false,
      breadcrumb: [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: "Ajouter une étude",
          link: "/etudes/ajouter"
        }
      ],
      form: {
        prospect: "",
        clientContact: "",
        name: "",
        description: "",
        mandat: 2021,
        number: "",
        confidential: false,
        qualiValidatePeda: false,
        projectManager: "",
        qualityManager: ""
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
      this.takenIds = res.data.filter(etu => etu.mandat == year).map(etu => etu.number)
      const amount = this.takenIds.length
      const result = amount + baseInt
      this.form.number = result
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
    submitProject () {
      this.loading = true
      this.form.prospect = this.form.prospect.toString()
      axios.post(
        "/api/etudes/",
        this.form,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'étude a bien été créée.",
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
          this.$message({message: "Impossible de créer l'étude pour le moment.",
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

<style>

</style>
