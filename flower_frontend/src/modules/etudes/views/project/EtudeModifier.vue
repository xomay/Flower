<template>
  <BaseComponent
    title="Modifier une étude"
    :breadcrumb="breadcrumb"
  >
    <ProjectForm
      v-model="etude"
      :loading="loading"
      :members="membres"
      :prospects="prospects"
      :taken-ids="takenIds"
      @save="saveProject"
    />
  </BaseComponent>
</template>

<script>
import ProjectForm from "../../components/forms/ProjectForm"

const axios = require("axios")

export default {
  name: "EtudeCreer",
  components: {ProjectForm},
  data () {
    return {
      loading: false,
      breadcrumb: [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: "<loading>",
          link: `/etudes/${this.$route.params.id}/voir`
        },
        {
          name: "Modifier une étude",
          link: `/etudes/${this.$route.params.id}/modifier`
        }
      ],
      etude: {
        prospect: 0,
        clientContact: 0,
        name: "",
        description: "",
        mandat: "",
        number: "",
        confidential: false,
        projectManager: 0,
        qualityManager: 0
      },
      membres: [],
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
      this.takenIds = res.data.filter(etu => etu.id != this.$route.params.id).filter(etu => etu.mandat == year).map(etu => etu.number)
      const amount = this.takenIds.length
      const result = amount + baseInt
      this.etude.number = result
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la liste des études : " + err, type: "error", offset: 40})
    })
  },
  created () {
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.etude = res.data
      this.etude.projectManager = this.etude.projectManager.id
      this.etude.qualityManager = this.etude.qualityManager.id
      this.etude.clientContact = this.etude.clientContact.id
      this.etude.prospect = this.etude.prospect.id
      this.breadcrumb[1].name = this.etude.name
      axios.get(
        "/api/membres/",
        {withCredentials: true}
      ).then((res) => {
        this.membres = res.data.map(obj => ({...obj, value: obj.firstname+" "+obj.lastname}))
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer les membres pour le moment : "+err, type: "error"})
      })
      axios.get(
        "/api/prospects/",
        {withCredentials: true}
      ).then((res) => {
        this.prospects = res.data.map(obj => ({...obj, value: obj.name}))
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer les prospects pour le moment : "+err, type: "error"})
      })
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer l'étude :" + err, type: "error"})
    })
  },
  methods: {
    saveProject () {
      this.loading = true
      axios.put(
        `/api/etudes/${this.etude.id}/`,
        this.etude,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'étude a bien été modifié.", type: "success", offset: 40})
        this.$router.push("/etudes/"+this.etude.id+"/voir")
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
