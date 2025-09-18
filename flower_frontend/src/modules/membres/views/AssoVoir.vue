<template>
    <el-tabs
      v-model="currentTab"
      type="card"
      style="margin: 20px 0 0 10px;"
    >
      <el-tab-pane
        label="Lister les membres"
        name="membre"
      />
      <el-tab-pane
        label="Lister les réalisateurs"
        name="inter"
      />
    </el-tabs>
    <MembresVoir
      v-show="currentTab === 'membre'"
    />
    <RealisateursVoir
      v-show="currentTab === 'inter'"
    />
</template>

<script>
import MembresVoir from "../views/MembresVoir.vue"
import RealisateursVoir from "../../realisateurs/views/RealisateursVoir.vue"

export default {
  name: "AssoVoir",
  components: { MembresVoir, RealisateursVoir },
  data () {
    return {
      currentTab: "membre",
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
