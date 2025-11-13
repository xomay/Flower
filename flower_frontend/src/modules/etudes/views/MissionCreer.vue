<template>
  <BaseComponent
    title="Modifier les missions"
    :breadcrumb="breadcrumb"
  >
    <template v-slot:action>
      <el-button
        type="text"
        icon="Plus"
        @click="addMission"
      >
        Ajouter
      </el-button>
    </template>
    <el-alert
      v-if="unpicked_phases.length > 0"
      title="Attention, des phases n'ont pas été sélectionnées"
      type="warning"
      :description="printUselected()"
      :closable="false"
      center
      effect="dark"
      show-icon
    />
    <MissionForm
      v-model="missions"
      :requirements="requirements"
      :phases="phases"
      :loading="loading"
      :consultants="consultants"
      @save="saveMissions"
      @phases-selection="pickedPhasesUpdated"
    />
  </BaseComponent>
</template>

<script>
import MissionForm from "../components/forms/MissionForm"

const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

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
      requirements: [],
      consultants: [],
      loading: false
    }
  },
  computed: {
    // Phases non sélectionnées par les RDM
    unpicked_phases () {
      return this.phases.filter(ph => ph.nbJEH > 0 && !ph.hasRDM)
    }
  },
  beforeCreate () {
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.phases = res.data.phases
      res.data.missions.forEach((mission) => {
        mission.consultant = mission.consultant.id
      })
      this.requirements = res.data.requirements
      //this.missions = res.data.missions.filter(mission => mission.isCurrent).slice()
      this.missions = res.data.missions
      this.originalIDs = this.missions.map(m => m.id)
      // Collecter toutes les phases assignées à tous les RMs
      const allAssignedPhases = new Set()
      
      this.missions.forEach((mission) => {
        mission.originalPMs = mission.phasesMission.slice()
        mission.phases = this.phases.filter(phase => mission.originalPMs.some(pm => pm.phaseEtude === phase.id))
        mission.phases = mission.phases.map(phase => phase.id)
        
        // Ajouter les phases de cette mission au set global
        mission.phases.forEach(phaseId => allAssignedPhases.add(phaseId))
      })
      
      // Mettre à jour hasRDM basé sur toutes les assignations
      this.phases = this.phases.map(ph => {
        return {
          ...ph,
          hasRDM: allAssignedPhases.has(ph.id)
        }
      })
      this.breadcrumb[1].name = res.data.name
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer l'étude : "+err, type: "error", offset: 40})
    })
    axios.get(
      "/api/realisateurs",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((realisateur) => realisateur.value = `${realisateur.firstname} ${realisateur.lastname}`)
      this.consultants = res.data.filter(r => r.security_social_number && r.birth_date && r.address && r.postcode && r.town && r.country)
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les réalisateurs : "+err, type: "error", offset: 40})
    })
  },
  methods: {
    updateAllPhasesStatus() {
      // Collecter toutes les phases assignées à tous les RMs
      const allAssignedPhases = new Set()
      this.missions.forEach(mission => {
        if (mission.phases && Array.isArray(mission.phases)) {
          mission.phases.forEach(phaseId => allAssignedPhases.add(phaseId))
        }
      })
      
      // Mettre à jour le status hasRDM basé sur toutes les assignations
      this.phases = this.phases.map(ph => {
        return {
          ...ph,
          hasRDM: allAssignedPhases.has(ph.id)
        }
      })
    },
    pickedPhasesUpdated (rdms_ids) {
      // Recalculer le statut de toutes les phases
      this.updateAllPhasesStatus()
    },
    addMission () {
      this.missions.push({
        consultant: "",
        missionBegin: "",
        missionEnd: "",
        percentageJunior: "0.51",
        JEHNumber: 1,
        phasesMission: [],
        originalPMs: [],
        phases: [],
      })
      // Recalculer le statut des phases après ajout
      this.updateAllPhasesStatus()
    },
    saveMissions (deletedIDS, deletedPhases) {
      this.loading = true
      var promesses = [] // promesses à réaliser sur les objets de missions avant de changer l'étude
      var newMissions = []
      for(const mission of this.missions) {
        if(mission.id == undefined) {
          // Nouvelle mission : il faut la créer
          promesses.push(this.saveMissionObject(mission))
        } else {
          // La mission est normale : on la met à jour
          const phasesASupprimer = mission.originalPMs.filter(
            originalPhase => !mission.phasesMission.some(
              currentPhase => currentPhase.id === originalPhase.id
            )
          )
          phasesASupprimer.forEach(phase => {
            // On supprime les phases de mission qui ne sont plus dans la mission
            promesses.push(this.deletePhaseID(phase.id))
          })
          newMissions.push(mission)
        }
      }
      // On émet un DELETE sur les missions à supprimer.
      deletedIDS.forEach(id => {
        promesses.push(this.deleteMissionID(id))
      })
      // Attendre l'éxécution des promesses précédentes, et ensuite exécuter la mise à jour.
      Promise.all(promesses).then((result) => {
        result.forEach(r => {
          if(r != null)
            newMissions.push(r)
        })
        newMissions.map(m => m.doc_mission = m.doc_mission.id)
        axios.put(
          `/api/etudes/missions/`,
          newMissions,
          {withCredentials: true}
        ).then(() => {
          //crée les phasesMissions par requetes
          promesses = []
          this.missions.forEach((mission) => {
            for (const phaseMission of mission.phasesMission) {
              if (phaseMission.id === undefined) {
                // Nouvelle phase de mission, on la crée
                //phaseMission.uss = phaseMission.uss.map(us => us.id)
                phaseMission.uss = []
                const {id ,...newPhase} = phaseMission;
                const phase = {
                  ...newPhase,
                  mission: mission.id
                }
                axios.post(
                  `/api/etudes/phases/missions/`,
                  [phase],
                  {withCredentials: true}
                ).then((res) => {
                }).catch((err) => {
                  this.$message({message: "Impossible de créer la phase de mission : "+err, type: "error", offset: 40})
                })
              } else {
                // Phase de mission existante, on la met à jour
                promesses.push(axios.put(
                  `/api/etudes/phases/missions/${phaseMission.id}/`,
                  phaseMission,
                  {withCredentials: true}
                ))
              }
            }
          })
          Promise.all(promesses).then(() => {
            this.$message({message: "Les missions ont bien été enregistrées", type: "success", offset: 40})
            this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Rédaction`)
          }).catch((err) => {
            this.$message({message: "Impossible de mettre à jour les phases de mission : "+err, type: "error", offset: 40})
          })
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
      // Modifier pour split mission et doc_mission
      return new Promise((resolve, fail) => {
        axios.post(
          `/api/etudes/${this.$route.params.id}/missions/`,
          mission_obj,
          {withCredentials: true}
        ).then((res) => {
          mission_obj.id = res.data.id
          resolve(res.data)
        }).catch((err) => {
          this.$message({message: "Impossible d'enregistrer' une nouvelle mission : "+err,
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
    },
    deletePhaseID (phase_id) {
      return new Promise((resolve, fail) => {
        axios.delete(
          `/api/etudes/phases/missions/${phase_id}/`,
          {withCredentials: true}
        ).then(() => {
          resolve()
        }).catch((err) => {
          this.$message({message: "Impossible de supprimer la phase : "+err,
            type: "error",
            offset: 40})
          fail(err)
        })
      })
    },
    printUselected () {
      return "Phases non sélectionnées : [" + this.unpicked_phases.map(ph => ph.title).join(", ") + "]."
    }
  }
}
</script>

