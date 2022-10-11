<template>
  <BaseComponent
    title="Ajout d'un prospect"
    :breadcrumb="breadcrumb"
  >
    <ProspectsForm
      v-model="prospect"
      :loading="loading"
      :members="members"
      @save="registerProspect"
    />
  </BaseComponent>
</template>

<script>
import ProspectsForm from "../components/ProspectsForm"
const axios = require("axios")

export default {
  name: "ProspectsCreer",
  components: {ProspectsForm},
  data () {
    return {
      prospect: {
        contactWay: [""]
      },
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
    registerProspect () {
      this.loading = true
      axios.post(
        "/api/prospects/",
        this.prospect,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "Le prospect a bien été ajouté", type: "success"})
        this.$router.push("/prospects/"+res.data.id+"/voir")
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
        this.members.push({
          value: "Non assigné"
        })
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer les membres : "+err, type: "error"})
      })
    }
  }
}
</script>
