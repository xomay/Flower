<template>
  <BaseComponent
    title="Suivi d'études"
    :breadcrumb="breadcrumb"
  >
    <el-tabs
      v-model="currentTab"
      type="card"
    >
      <el-tab-pane
        label="Études en cours"
        name="current"
      />
      <el-tab-pane
        label="Études du mandat"
        name="mandat"
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
        label="Voir les CC"
        name="ccs"
        :lazy="true"
      />
      <el-tab-pane
        label="Tout voir"
        name="all"
        :lazy="true"
      />
    </el-tabs>
    <el-switch
      v-model="viewType"
      class="mb-2"
      style="--el-switch-off-color: #13ce66; --el-switch-on-color: #ff4949"
      active-text="Dashboard"
      inactive-text="Liste"
      v-show="currentTab === 'current'"
    />
    <!-- filters will modify this.etudes directly -->
    <EtudesList
      :etudes="etudes"
      :loading="loading"
      @select="goToEtude"
      v-show="currentTab !== 'ccs' && currentTab !== 'dashboard' && viewType !== true"
    />
      <EtudesDahsboard
      :etudes="originalEtudes"
      :loading="loading"
      @select="goToEtude"
      v-show="viewType === true"
      />
    <CCList
      :ccs="ccs"
      :loading="loading"
      @select="goToEtude"
      v-show="currentTab === 'ccs'"
    />
  </BaseComponent>
</template>

<script>
import EtudesList from "../components/EtudesList.vue"
import CCList from "../components/CCList.vue"
import EtudesDahsboard from "../components/EtudesDahsboard.vue"
const axios = require("axios")

export default {
  name: "EtudeVoir",
  components: { EtudesList, CCList, EtudesDahsboard },
  data () {
    return {
      currentTab: "current",
      viewType: false,
      originalEtudes: [],
      etudes: [],
      ccs: [],
      loading: true,
      breadcrumb: [
        {
          name: "Suivi d'étude",
          link: "/etudes"
        }
      ]
    }
  },
  created () {
    this.loading = true
    axios.get(
      "/api/etudes/",
      {withCredentials: true}
    ).then((res) => {
      this.originalEtudes = res.data
      axios.get(
        "/api/etudes/cc/",
        {withCredentials: true}
      ).then((res) => {
        this.ccs = res.data
      }).catch((err) => {
        this.$message({message: err,
          type: "error",
          offset: 40})
      })
      this.updateEtudes()
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les études pour le moment: "+err, type: "error"})
      this.loading = false
    })
  },
  watch: {
    currentTab () {
      this.updateEtudes()
    }
  },
  methods: {
    goToEtude (id) {
      this.$router.push(`/etudes/${id}/voir`)
    },
    updateEtudes () {
      const currentYear = new Date().getFullYear();
      this.loading = true
      if(this.currentTab == "current")
        this.etudes = this.originalEtudes.filter(e => !(e.isAborted || e.isFinished))
      else if(this.currentTab == "aborted")
        this.etudes = this.originalEtudes.filter(e => e.isAborted)
      else if(this.currentTab == "finished")
        this.etudes = this.originalEtudes.filter(e => e.isFinished)
      else if(this.currentTab == "mandat")
        this.etudes = this.originalEtudes.filter(e => e.mandat == currentYear )
      else
        this.etudes = this.originalEtudes
      this.loading = false
    }
  }
}
</script>

<style>
</style>
