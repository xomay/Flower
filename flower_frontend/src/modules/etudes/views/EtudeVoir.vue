<template>
  <BaseComponent
    title="Suivi d'études"
    :breadcrumb="breadcrumb"
  >
    <el-tabs
      v-model="currentTab"
      type="card"
      @tab-click="updateEtudes"
    >
      <el-tab-pane
        label="Études en cours"
        name="current"
      />
      <el-tab-pane
        label="Études terminées"
        name="finished"
        :lazy="true"
      />
      <el-tab-pane
        label="Études avortées"
        name="aborted"
        :lazy="true"
      />
      <el-tab-pane
        label="Tout voir"
        name="all"
        :lazy="true"
      />
    </el-tabs>
    <!-- filters will modify this.etudes directly -->
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
      currentTab: "current",
      originalEtudes: [],
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
      this.originalEtudes = res.data
      this.updateEtudes()
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les études pour le moment: "+err, type: "error"})
      this.loading = false
    })
  },
  methods: {
    goToEtude (id) {
      this.$router.push(`/etudes/${id}/voir`)
    },
    updateEtudes () {
      this.loading = true
      if(this.currentTab == "current")
        this.etudes = this.originalEtudes.filter(e => !(e.isAborted || e.isFinished))
      else if(this.currentTab == "aborted")
        this.etudes = this.originalEtudes.filter(e => e.isAborted)
      else if(this.currentTab == "finished")
        this.etudes = this.originalEtudes.filter(e => e.isFinished)
      else
        this.etudes = this.originalEtudes
      this.loading = false
    }
  }
}
</script>

<style>
</style>
