<template>
  <BaseComponent
    title="Edition d'un PVR"
    :breadcrumb="breadcrumb"
  >
    <PVRForm
      v-model="pvr"
      :etude="etude"
      :loading="loading"
      @save="updatePVR"
    />
  </BaseComponent>
</template>

<script>
import PVRForm from "../components/forms/PVRForm"

const axios = require("axios")

export default {
  name: "PVREditor",
  components: {PVRForm},
  data () {
    return {
      etude: {},
      pvr: {},
      breadcrumb: [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: "<loading>",
          link: `/etudes/${this.$route.params.id}/voir?active=Rédaction`
        },
        {
          name: "PVR",
          link: `/etudes/${this.$route.params.id}/pvr/ajouter`
        }
      ],
      loading: false
    }
  },
  created () {
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.etude = res.data
      this.breadcrumb[1].name = this.etude.name
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer l'étude : " + err, type: "error"})
    })
    axios.get(
      `/api/pvr/${this.$route.params.pvr_id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.pvr = res.data
    }).catch((err) => {
      this.$message({message: err, type: "error", offset: 40})
    })
  },
  methods: {
    updatePVR () {
      this.loading = true
      axios.put(
        `/api/pvr/${this.$route.params.pvr_id}/`,
        this.pvr,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le PVR a bien été modifié.", type: "success", offset: 40})
        this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Rédaction`)
      }).catch((err) => {
        this.$message({message: err, type: "error", offset: 40})
      }).finally(() => {
        this.loading = false
      })
    }
  }
}
</script>

<style>

</style>
