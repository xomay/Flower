<template>
  <BaseComponent
    :title="etude.name"
    :breadcrumb="breadcrumb"
  >
    <!-- <el-divider content-position="left">
            <span class="text-lg"><i class="el-icon-collection"/> {{ etude.name }}</span>
        </el-divider> -->
    <template v-slot:action>
      <router-link :to="`/etudes/${$route.params.id}/modifier`">
        <el-button
          type="text"
          icon="el-icon-edit"
        >
          Modifier
        </el-button>
      </router-link>
    </template>
    <el-tabs
      v-model="currentTab"
      @tab-click="handleTabChange"
    >
      <el-tab-pane
        label="Récapitulatif"
        name="Récapitulatif"
      />
      <el-tab-pane
        label="Phases"
        name="Phases"
      />
      <el-tab-pane
        label="Rédaction"
        name="Rédaction"
      />
    </el-tabs>
    <Summary
      v-show="currentTab === 'Récapitulatif'"
      :etude="etude"
    />
    <Phases
      v-show="currentTab === 'Phases'"
      :groupes="etude.groupes"
    />
    <Generation
      v-show="currentTab === 'Rédaction'"
      :etude="etude"
    />
  </BaseComponent>
</template>

<script>
import Summary from "../../components/Summary"
import Phases from "../../components/Phases"
import Generation from "../../components/Generation"

const axios = require("axios")

export default {
  name: "EtudeDetail",
  components: {Summary, Phases, Generation},
  data () {
    return {
      currentTab: this.$route.query.active || "Récapitulatif",
      etude: {},
      // Groupes: [],
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
        }
      ]
    }).
      catch(() => {
        this.$message({
          message: "Impossible de récupérer l'études pour le moment", type: "error"})
      }).
      finally(() => {
        this.loading = false
      })

    /*
         * Axios.get("/api/etudes/" + this.$route.params.id + '/groupes', { withCredentials: true }).then(res => {
         *   this.groupes = res.data
         * }).catch(() => {
         *   this.$message({ message: 'Impossible de récupérer les groupes pour le moment', type: 'error'})
         * }).finally(() => {
         *   this.loading = false
         * })
         */
  },
  methods: {
    handleTabChange (tab) {
      this.$router.push({query: {active: tab.label}})
    }
  }
}
</script>

<style>

</style>
