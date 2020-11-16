<template>
  <BaseComponent
    title="Modifier les Phases"
    :breadcrumb="breadcrumb"
  >
    <PhasesForm
      v-model="groupes"
      @add-groupe="addGroupe"
      @add-phase="addPhase"
      @delete-groupe="deleteGroupe"
      @delete-phase="deletePhase"
    />
    <el-button
      type="primary"
      @click="submitGroupesAndPhases"
    >
      Enregister
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
      breadcrumb: []
    }
  },
  created () {
    this.loading = true
    axios.get(
      `${this.$server_url}/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      res.data.groupes = res.data.groupes.sort((a, b) => a.index - b.index)
      res.data.groupes.forEach((groupe) => {
        groupe.phases = groupe.phases.sort((a, b) => a.index - b.index)
      })
      this.groupes = res.data.groupes
      this.breadcrumb = [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: res.data.name,
          link: `/etudes/${this.$route.params.id}/voir`
        },
        {
          name: "Phases",
          link: `/etudes/${this.$route.params.id}/phases`
        }
      ]
    }).
      catch(() => {
        this.$message({message: "Impossible de récupérer les groupes pour le moment",
          type: "error"})
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
        `${this.$server_url}/etudes/groupes/`,
        newGroup,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "Le groupe a bien été créé",
          type: "success"})
        this.groupes.push(res.data)
      }).
        catch(() => {
          this.$message({message: "Impossible de créer un groupe pour le moment",
            type: "error"})
        }).
        finally(() => {
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
        `${this.$server_url}/etudes/phases/`,
        newPhase,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "La phase a bien été créé",
          type: "success"})
        groupe.phases.push(res.data)
      }).
        catch(() => {
          this.$message({message: "Impossible de créer une phase pour le moment",
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    },
    deleteGroupe ({groupeId, groupeIndex}) {
      axios.delete(
        `${this.$server_url}/etudes/groupes/${groupeId}/`,
        {withCredentials: true}
      ).then(() => {
        this.groupes.splice(
          groupeIndex,
          1
        )
        this.$message({message: "Le groupe a bien été supprimé",
          type: "success"})
      }).
        catch(() => {
          this.$message({message: "Impossible de supprimer ce groupe pour le moment",
            type: "error"})
        })
    },
    deletePhase ({phase, groupe}) {
      axios.delete(
        `${this.$server_url}/etudes/phases/${phase.id}/`,
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
      }).
        catch(() => {
          this.$message({message: "Impossible de supprimer cette phase pour le moment",
            type: "error"})
        })
    },
    submitGroupesAndPhases () {
      // Let phases = this.groupes.map(groupe => groupe.phases).flat()
      axios.put(
        `${this.$server_url}/etudes/groupes/`,
        this.groupes,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Les Groupes et Phases ont bien été enregistrés",
          type: "success"})
      }).
        catch(() => {
          this.$message({message: "Impossible d'enregistrer les groupes pour le moment",
            type: "error"})
        }).
        finally(() => {
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
