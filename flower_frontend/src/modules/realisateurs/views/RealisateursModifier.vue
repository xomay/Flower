<template>
  <BaseComponent
    title="Modifier le réalisateur"
    :breadcrumb="breadcrumb"
  >
    Réa : {{ realisateur.firstname+" "+realisateur.lastname }} :)
  </BaseComponent>
</template>

<script>
const axios = require("axios")

export default {
  name: "RealisateurModifier",
  data () {
    return {
      realisateur: {},
      loading: true,
      breadcrumb: [
        {
          name: "Liste des réalisateurs",
          link: "/realisateurs"
        },
        {
          name: "<loading>",
          link: `/realisateurs/${this.$route.params.id}/voir`
        },
        {
          name: "Modifier",
          link: `/realisateurs/${this.$route.params.id}/modifier`
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/realisateurs/${this.$route.params.id}`,
      {withCredentials: true}
    ).then((res) => {
      this.realisateur = res.data
      this.breadcrumb[1].name = `${this.realisateur.firstname} ${this.realisateur.lastname}`
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le réalisateur pour le moment : " + err,
        type: "error",
        offset: 40})
    }).finally(() => {
      this.loading = false
    })
  }
}
</script>
