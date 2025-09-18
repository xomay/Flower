<template>
  <BaseComponent
    :title="'Proposition Commerciale de l\'étude ' + etude.name"
    :breadcrumb="breadcrumb"
  >
    <DevisForm :etude="etude" />
  </BaseComponent>
</template>

<script>
import DevisForm from "../../components/forms/DevisForm.vue"

const axios = require("axios")

export default {
  name: "EtudeDevis",
  components: {DevisForm},
  data () {
    return {
      currentTab: "Récapitulatif",
      etude: {},
      breadcrumb: [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.etude = res.data
      this.breadcrumb = [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: this.etude.name,
          link: `/etudes/${this.etude.id}/voir`
        },
        {
          name: "Convention Etude",
          link: `/etudes/${this.etude.id}/convention-etude`
        }
      ]
    }).catch(() => {
      this.$message({message: "Impossible de récupérer l'études pour le moment", type: "error"})
    }).finally(() => {
      this.loading = false
    })
  }
}
</script>

<style>

</style>
