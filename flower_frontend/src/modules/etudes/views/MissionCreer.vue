<template>
  <BaseComponent
    title="Modifier les missions"
    :breadcrumb="breadcrumb"
  >
    <template v-slot:action>
      <el-button
        type="text"
        icon="el-icon-plus"
        @click="addMission"
      >
        Ajouter
      </el-button>
    </template>
    <MissionForm
      v-model="missions"
      :phases="phases"
      :loading="loading"
      @save="saveMissions"
    />
  </BaseComponent>
</template>

<script>
import MissionForm from "../components/forms/MissionForm"

const axios = require("axios")

export default {
  name: "MissionCreer",
  components: {MissionForm},
  data () {
    return {
      breadcrumb: [],
      missions: [],
      phases: [],
      loading: false
    }
  },
  beforeCreate () {
    axios.get(
      `${this.$server_url}/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.phases = res.data.groupes.map((groupe) => groupe.phases).flat()
      res.data.missions.forEach((mission) => {
        mission.consultant = mission.consultant.id
      })
      this.missions = res.data.missions
    }).
      catch((err) => {
        console.error(err)
      })
  },
  methods: {
    addMission () {
      axios.post(
        `${this.$server_url}/etudes/${this.$route.params.id}/missions/`,
        {project: this.$route.params.id},
        {withCredentials: true}
      ).then((res) => {
        this.missions.push(res.data)
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error",
            offset: 40})
        })
    },
    saveMissions () {
      this.loading = true
      axios.put(
        `${this.$server_url}/etudes/${this.$route.params.id}/missions/`,
        this.missions,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Les missions ont bien été enregistrées",
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
