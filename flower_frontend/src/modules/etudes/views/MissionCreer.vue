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
      :consultants="consultants"
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
      breadcrumb: [
        {
          name: "Suivi d'étude",
          link: "/etudes"
        },
        {
          name: "<loading>",
          link: `/etudes/${this.$route.params.id}/voir?active=Rédaction`
        },
        {
          name: "Gérer les missions",
          link: `/etudes/${this.$route.params.id}/missions`
        }
      ],
      // Tableau de missions, qui grossit ou non interactivement
      missions: [],
      // Tableau des missions originelles, qui sert à savoir lesquelles il faut supprimer.
      originalIDs: [],
      // Phases concernées par l'étude, read-only
      phases: [],
      consultants: [],
      loading: false
    }
  },
  beforeCreate () {
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.phases = res.data.currentGroupes .groupes.map((groupe) => groupe.phases).flat()
      res.data.missions.forEach((mission) => {
        mission.consultant = mission.consultant.id
      })
      this.missions = res.data.missions.slice()
      this.originalIDs = this.missions.map(m => m.id)
      this.breadcrumb[1].name = res.data.name
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer l'étude : "+err,
        type: "error",
        offset: 40})
    })
    axios.get(
      "/api/realisateurs",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((realisateur) => realisateur.value = `${realisateur.firstname} ${realisateur.lastname}`)
      this.consultants = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les membres : "+err,
        type: "error",
        offset: 40})
    })
  },
  methods: {
    addMission () {
      this.missions.push({
        consultant: "",
        missionBegin: "",
        missionEnd: "",
        percentageJunior: "0.55",
        JEHNumber: 1,
        JEHPrice: 400,
        phases: []
      })
    },
    saveMissions (deletedIDS) {
      this.loading = true
      var promesses = [] // promesses à réaliser sur les objets de missions avant de changer l'étude
      var newMissions = []
      for(const mission of this.missions) {
        if(mission.id == undefined) {
          // Nouvelle mission : il faut la créer
          promesses.push(this.saveMissionObject(mission))
        } else {
          // La mission est normale : on la met à jour
          newMissions.push(mission)
        }
      }
      // On émet un DELETE sur les étues à supprimer.
      deletedIDS.forEach(id => {
        promesses.push(this.deleteMissionID(id))
      })
      // Attendre l'éxécution des promesses précédentes, et ensuite exécuter la mise à jour.
      Promise.all(promesses).then((result) => {
        result.forEach(r => {
          if(r != null)
            newMissions.push(r)
        })
        axios.put(
          `/api/etudes/${this.$route.params.id}/missions/`,
          newMissions,
          {withCredentials: true}
        ).then(() => {
          this.$message({message: "Les missions ont bien été enregistrées",
            type: "success",
            offset: 40})
          this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Rédaction`)
        }).catch((err) => {
          this.$message({message: "Impossible de mettre à jour les missions : "+err, type: "error", offset: 40})
        }).finally(() => {
          this.loading = false
        })
      }).catch(() => {
        this.$message({message: "Annulation de la mise à jour de RM.", type: "error"})
        this.loading = false
      })
    },
    saveMissionObject (mission_obj) {
      mission_obj.project = this.$route.params.id
      return new Promise((resolve, fail) => {
        axios.post(
          `/api/etudes/${this.$route.params.id}/missions/`,
          mission_obj,
          {withCredentials: true}
        ).then((res) => {
          resolve(res.data)
        }).catch((err) => {
          this.$message({message: "Impossible de register une nouvelle mission : "+err,
            type: "error",
            offset: 40})
          fail(err)
        })
      })
    },
    deleteMissionID (mission_id) {
      return new Promise((resolve, fail) => {
        axios.delete(
          `/api/etudes/${this.$route.params.id}/missions/${mission_id}/`,
          {withCredentials: true}
        ).then(() => {
          resolve()
        }).catch((err) => {
          this.$message({message: "Impossible de supprimer la mission : "+err,
            type: "error",
            offset: 40})
          fail(err)
        })
      })
    }
  }
}
</script>

