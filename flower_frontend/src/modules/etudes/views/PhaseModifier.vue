<template>
  <BaseComponent
    title="Modifier les Phases"
    :breadcrumb="breadcrumb"
  >
    <PhasesForm
      v-model="groupes"
      :small="false"
      @add-groupe="addGroupe"
      @add-phase="addPhase"
      @delete-groupe="deleteGroupe"
      @delete-phase="deletePhase"
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
      res.data.groupes = res.data.groupes.sort((a, b) => a.index - b.index)
      res.data.groupes.forEach((groupe) => {
        groupe.phases = groupe.phases.sort((a, b) => a.index - b.index)
      })
      this.groupes = res.data.groupes
      this.breadcrumb[1].name = res.data.name
    }).catch(() => {
      this.$message({message: "Impossible de récupérer les groupes pour le moment", type: "error"})
    })
  },
  methods: {
    addGroupe () {
      const newGroup = {
        title: "Titre",
        description: "Description",
        project: this.$route.params.id,
        index: this.groupes.length + 1,
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
      const newIndex = (Math.max.apply(
          Math,
          groupe.phases.map((phase) => phase.index)
        ) | 0) + 1,
        newPhase = {
          index: newIndex,
          groupe: groupe.id
        }
      axios.post(
        "/api/etudes/phases/",
        newPhase,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "La phase a bien été créée", type: "success"})
        groupe.phases.push(res.data)
      }).catch(() => {
        this.$message({message: "Impossible de créer une phase pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deleteGroupe ({groupeId, groupeIndex}) {
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
      })
    },
    deletePhase ({phase, groupe}) {
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
        this.$message({message: "La phase a bien été supprimé",
          type: "success"})
      }).catch(() => {
        this.$message({message: "Impossible de supprimer cette phase pour le moment", type: "error"})
      })
    },
    submitGroupesAndPhases () {
      axios.put(
        "/api/etudes/groupes/",
        this.groupes,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Les Groupes et Phases ont bien été enregistrés", type: "success"})
        this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Phases`)
      }).catch((err) => {
        console.log(err)
        if (err.response && err.response.status === 400) {
          this.$message({message: "Le formulaire comporte des erreurs. Vérifiez les descriptions et les objectifs des phases (menu déroulant)",
            type: "error",
            offset: 40})
        } else {
          this.$message({message: "Impossible d'enregistrer les Groupes et Phases pour le moment",
            type: "error",
            offset: 40})
        }
      }).finally(() => {
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
