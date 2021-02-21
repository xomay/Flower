<template>
  <BaseComponent
    title="Facture - Choix de l'étude"
    :breadcrumb="breadcrumb"
  >
    <EtudesList
      :etudes="etudes"
      :loading="loading"
      @select="goToEtude"
    />
  </BaseComponent>
</template>

<script>
import EtudesList from "@/modules/etudes/components/EtudesList.vue"
const axios = require("axios")

export default {
  name: "FactureSelectEtude",
  components: { EtudesList },
  data () {
    return {
      etudes: [],
      loading: true,
      breadcrumb: [
        {
          name: "Factures",
          link: "tresorerie/factures"
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/etudes/",
      {withCredentials: true}
    ).then((res) => {
      this.etudes = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les études pour le moment: "+err, type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    goToEtude (id) {
      this.$router.push(`/tresorerie/factures/${id}/`)
    }
  }
}
</script>