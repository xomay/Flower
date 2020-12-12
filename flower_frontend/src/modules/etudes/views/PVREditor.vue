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
      etude: null,
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
    }).
      catch(() => {
        this.$message({message: "Impossible de récupérer l'études pour le moment",
          type: "error"})
      })
    this.getPVR()
  },
  methods: {
    getPVR () {
      axios.get(
        `/api/pvr/${this.$route.params.pvr_id}/`,
        {withCredentials: true}
      ).then((res) => {
        this.pvr = res.data
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error",
            offset: 40})
        })
    },
    updatePVR () {
      this.loading = true
      axios.put(
        `/api/pvr/${this.$route.params.pvr_id}/`,
        this.pvr,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le PVR a bien été modifié.",
          type: "success",
          offset: 40})
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error",
            offset: 40})
        }).
        finally(() => {
          this.loading = false
        })
    }
  }
}
</script>

<style>

</style>
