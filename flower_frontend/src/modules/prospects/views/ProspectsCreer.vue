<template>
  <BaseComponent
    title="Ajout d'un prospect"
    :breadcrumb="breadcrumb"
  >
    <ProspectsForm
      v-model="prospect"
      :loading="loading"
      :members="members"
      :employes="employes"
      @save="registerProspect"
    />
  </BaseComponent>
</template>

<script>
import ProspectsForm from "../components/ProspectsForm"
const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.withCredentials = true

export default {
  name: "ProspectsCreer",
  components: {ProspectsForm},
  data () {
    return {
      prospect: {
        contactWay: [""]
      },
      employes: [],
      members: [],
      loading: false,
      breadcrumb: [
        {
          name: "Liste des prospects",
          link: "/prospects"
        },
        {
          name: "Ajouter un prospect",
          link: "/prospects/ajouter"
        }
      ]
    }
  },
  created () {
    this.getMembers()
  },
  methods: {
    registerProspect (employes) {
      this.loading = true
      axios.post(
        "/api/prospects/",
        this.prospect,
        {withCredentials: true}
      ).then((res) => {
        const prospectId = res.data.id
        // Crée un tableau de promesses pour chaque employé
        const requests = employes.map(emp =>
          axios.post(
            `/api/prospects/${prospectId}/employes/`,
            emp,
            {withCredentials: true}
          )
        )
        // Attend que tous les POST soient terminés
        Promise.all(requests)
        .then(() => {
          this.$message({message: "Le prospect a bien été ajouté", type: "success"})
          this.$router.push("/prospects/"+prospectId+"/voir")
        }).
          catch((err) => {
            this.$message({message: err,
              type: "error"})
          }).
          finally(() => {
            this.loading = false
          })
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer le prospect : "+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    getMembers () {
      axios.get(
        "/api/membres/",
        {withCredentials: true}
      ).then((res) => {
        res.data.forEach((mem) => mem.value = `${mem.firstname} ${mem.lastname}`)
        this.members = res.data
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer les membres : "+err, type: "error"})
      })
    }
  }
}
</script>
