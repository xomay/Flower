<template>
  <BaseComponent
    :title="etude.name"
    :breadcrumb="breadcrumb"
  >
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
    </el-tabs>
    <Summary
      v-show="currentTab === 'Récapitulatif'"
      :etude="etude"
    />
    <Phases
      v-show="currentTab === 'Phases'"
      :groupes="etude.groupes"
      :etude="etude"
      :editable="false"
      :loading="loading"
      @us-change="usChanged"
    />
  </BaseComponent>
</template>

<script>
import Summary from "../../components/Summary"
import Phases from "../../components/Phases"

const axios = require("axios")

export default {
  name: "ReaEtudeDetail",
  components: {Summary, Phases},
  data () {
    return {
      currentTab: this.$route.query.active || "Récapitulatif",
      loading: false,
      etude: {
        name: "", // valeurs par défault afin d'éviter des warnings inutiles.
        groupes: []
      },
      breadcrumb: [
        {
          name: "Mes études",
          link: "/etudes/acces-rea"
        },
        {
          name: "<loading>",
          link: `/etudes/acces-rea/${this.$route.params.id}/voir`
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/etudes/getReaEtudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.etude = res.data
      this.breadcrumb[1].name = this.etude.name
    }).catch(() => {
      this.$message({ message: "Impossible de récupérer l'études pour le moment", type: "error" })
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    handleTabChange (tab) {
      this.$router.push({query: {active: tab.label}})
    },
    usChanged (us, newState) {
      this.loading = true
      axios.put(
        `/api/etudes/uss/${us.id}/`,
        {
          ...us,
          state: newState
        },
        { withCredentials: true }
      ).then(() => {
        this.$message({message: "US mis à jour", type: "success"})
        us.state = newState
      }).catch((err) => {
        this.$message({message: "Impossible de mettre à jour l'US : " + err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    }
  }
}
</script>
