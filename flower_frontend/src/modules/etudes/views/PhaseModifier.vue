<template>
  <BaseComponent
    title="Modifier les Phases"
    :breadcrumb="breadcrumb"
  >
    <el-alert
      v-if="!isOriginalGroupes"
      type="info"
      show-icon
      :closable="false"
      style="margin: 10px;"
    >
      <template slot="title">
        <b><u>Note :</u> Il ne s'agit pas des phases originales de l'étude, mais celles d'un avenant.</b>
      </template>
    </el-alert>
    <PhasesForm
      v-model="groupes"
      :small="false"
      @add-us="addUS"
      @add-groupe="addGroupe"
      @add-phase="addPhase"
      @delete-groupe="deleteGroupe"
      @delete-phase="deletePhase"
      @delete-us="deleteUS"
    />
    <el-button
      type="primary"
      @click="submitGroupesAndPhases"
    >
      Enregistrer
    </el-button>
  </BaseComponent>
</template>

<script>
import PhasesForm from "../components/forms/PhasesForm"
const axios = require("axios")

export default {
  name: "PhasesModifier",
  components: {PhasesForm},
  data () {
    return {
      loading: true,
      groupes: [],
      isOriginalGroupes: true,
      originalGroupOwner: -1,
      breadcrumb: [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: "<loading>",
          link: `/etudes/${this.$route.params.id}/voir`
        },
        {
          name: "Phases",
          link: `/etudes/${this.$route.params.id}/phases`
        }
      ]
    }
  },
  created () {
    this.loading = true
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.isOriginalGroupes = res.data.isOriginalGroupes
      this.originalGroupOwner = res.data.currentGroupes.id
      res.data.groupes = res.data.currentGroupes.groupes.sort((a, b) => a.index - b.index)
      res.data.groupes.forEach((groupe) => {
        groupe.phases = groupe.phases.sort((a, b) => a.index - b.index)
      })
      this.groupes = res.data.groupes
      this.breadcrumb[1].name = res.data.name
    }).catch(() => {
      this.$message({message: "Impossible de récupérer les groupes pour le moment", type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    addGroupe () {
      this.loading = true
      const newGroup = {
        title: "Titre",
        description: "Description",
        project: this.$route.params.id,
        index: this.groupes.length + 1,
        owner: this.originalGroupOwner,
        phases: []
      }
      axios.post(
        "/api/etudes/groupes/",
        newGroup,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "Le groupe a bien été créé", type: "success"})
        this.groupes.push(res.data)
      }).catch(() => {
        this.$message({message: "Impossible de créer un groupe pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    addPhase (groupe) {
      this.loading = true
      const newIndex = (Math.max.apply(
          Math,
          groupe.phases.map((phase) => phase.index)
        ) | 0) + 1,
        newPhase = {
          index: newIndex,
          uss: [],
          groupe: groupe.id
        }
      axios.post(
        "/api/etudes/phases/",
        newPhase,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "La phase a bien été ajoutée.", type: "success"})
        groupe.phases.push(res.data)
      }).catch(() => {
        this.$message({message: "Impossible de créer une phase pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    addUS (phase) {
      this.loading = true
      const newIndex = (Math.max.apply(
          Math,
          phase.uss.map((us) => us.index)
        ) | 0) + 1,
        newUS = {
          index: newIndex,
          uss: [],
          name: "US",
          phase: phase.id
        }
      axios.post(
        "/api/etudes/uss/",
        newUS,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "L'US a bien été ajouté.", type: "success"})
        phase.uss.push(res.data)
      }).catch(() => {
        this.$message({message: "Impossible de créer une US pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deleteGroupe ({groupeId, groupeIndex}) {
      this.loading = true
      axios.delete(
        `/api/etudes/groupes/${groupeId}/`,
        {withCredentials: true}
      ).then(() => {
        this.groupes.splice(
          groupeIndex,
          1
        )
        this.$message({message: "Le groupe a bien été supprimé",
          type: "success"})
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer ce groupe pour le moment :"+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deletePhase ({phase, groupe}) {
      this.loading = true
      axios.delete(
        `/api/etudes/phases/${phase.id}/`,
        {withCredentials: true}
      ).then(() => {
        const index = groupe.phases.indexOf(phase)
        if (index > -1) {
          groupe.phases.splice(
            index,
            1
          )
        }
        this.$message({message: "La phase a bien été supprimée.", type: "success"})
      }).catch(() => {
        this.$message({message: "Impossible de supprimer cette phase pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deleteUS ({us, phase}) {
      this.loading = true
      axios.delete(
        `/api/etudes/uss/${us.id}/`,
        {withCredentials: true}
      ).then(() => {
        const index = phase.uss.indexOf(us)
        if (index > -1) {
          phase.uss.splice(
            index,
            1
          )
        }
        this.$message({message: "L'US a bien été supprimée.", type: "success"})
      }).catch(() => {
        this.$message({message: "Impossible de supprimer cette US pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    submitGroupesAndPhases () {
      this.loading = true
      axios.put(
        "/api/etudes/groupes/",
        this.groupes,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Les Groupes et Phases ont bien été enregistrés", type: "success"})
        this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Phases`)
      }).catch((err) => {
        this.$message({message: "Erreur lors de l'enregistrement : " + err, type: "error"})
        if (err.response && err.response.status === 400) {
          this.$message({message: "Le formulaire comporte des erreurs. Vérifiez les descriptions et les objectifs des phases (menu déroulant)",
            type: "error",
            offset: 40})
        } else {
          this.$message({message: "Impossible d'enregistrer les Groupes et Phases pour le moment",
            type: "error",
            offset: 40})
        }
        this.loading = false
      })
    }
  }
}
</script>

<style>
.el-date-editor.el-input {
  width: 120px;
}
</style>
