<template>
  <BaseComponent
    title="Suivi d'études"
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
import EtudesList from "../components/EtudesList.vue"
const axios = require("axios")

export default {
  name: "EtudeVoir",
  components: { EtudesList },
  data () {
    return {
      etudes: [],
      loading: true,
      breadcrumb: [
        {
          name: "Suivi d'étude",
          link: "/etudes"
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
      this.$router.push(`/etudes/${id}/voir`)
    }
  }
}
</script>

<style>
  .confiStyle {
    color: rgb(165, 27, 27);
    font-weight: bold;
  }
</style>
