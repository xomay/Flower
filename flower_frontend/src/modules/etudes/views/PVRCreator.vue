<template>
  <BaseComponent
    title="Ajout d'un PVR"
    :breadcrumb="breadcrumb"
  >
    <PVRForm
      v-model="pvr"
      :etude="etude"
      :loading="loading"
      @save="submitPVR"
    />
  </BaseComponent>
</template>

<script>
import PVRForm from "../components/forms/PVRForm"

const axios = require("axios")

export default {
  name: "PVRCreator",
  components: {PVRForm},
  data () {
    return {
      etude: {},
      pvr: {},
      breadcrumb: [],
      loading: false
    }
  },
  created () {
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
          name: "PVR",
          link: `/etudes/${this.etude.id}/pvr/ajouter`
        }
      ]
    }).catch(() => {
      this.$message({message: "Impossible de récupérer l'études pour le moment", type: "error"})
    })
  },
  methods: {
    submitPVR () {
      this.loading = true
      this.pvr.project = this.$route.params.id
      axios.post(
        "/api/pvr/",
        this.pvr,
        {withCredentials: true}
      ).then(() => {
        this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Rédaction`)
        this.$message({message: "Le PVR a bien été ajouté.", type: "success"})
      }).catch((err) => {
        this.$message({message: err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    }
  }
}
</script>

<style>

</style>
