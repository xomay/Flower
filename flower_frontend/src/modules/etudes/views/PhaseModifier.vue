<template>
  <BaseComponent
    title="Modifier les Phases"
    :breadcrumb="breadcrumb"
  >

      <template #title>
        <b><u>Note :</u> Il ne s'agit pas des phases originales de l'étude, mais celles d'un avenant.</b>
      </template>
    <PhasesForm
      v-model="phases"
      :small="false"
      @add-us="addUS"
      @add-phase="addPhase"
      @delete-phase="deletePhase"
      @delete-us="deleteUS"
    />
    <el-button
      type="primary"
      @click="submitPhases"
    >
      Enregistrer
    </el-button>
  </BaseComponent>
</template>

<script>
import PhasesForm from "../components/forms/PhasesForm"
import phases from "@/modules/etudes/components/Phases.vue";
const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

export default {
  name: "PhasesModifier",
  components: {PhasesForm},
  data () {
    return {
      loading: true,
      phases: [],
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
      //res.data.phases = res.data.phases.sort((a, b) => a.index - b.index)
      this.etude = res.data
      this.phases = res.data.phases
      this.phases.map(phase => {
        phase.priceJEH = Number(phase.priceJEH)
        return phase
      })
      this.breadcrumb[1].name = res.data.name
    }).catch(() => {
      this.$message({message: "Impossible de récupérer les groupes pour le moment", type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    addPhase () {
      this.loading = true
      const newIndex = (Math.max.apply(
          Math,
          this.phases.map((phase) => phase.index)
        ) | 0) + 1,
        newPhase = {
          index: newIndex,
          uss: [],
          etude: this.etude.id,
        }
      axios.post(
        "/api/etudes/phases/",
        [newPhase],
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "La phase a bien été ajoutée.", type: "success"})
        const phase = {
          ...res.data[0],
          etude: this.etude.id,
          uss: []
        }
        this.phases.push(phase)
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
          name: "US",
          phase: phase.id
        }
        phase.uss.push(newUS)
    },
    deletePhase ({phase}) {
      this.loading = true
      if (phase.id){

        axios.delete(
          `/api/etudes/phases/${phase.id}/`,
          {withCredentials: true}
        ).then(() => {
          const index = this.phases.indexOf(phase)
          if (index > -1) {
            this.phases.splice(
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
      } else {
        const index = this.phases.indexOf(phase)
        if (index > -1) {
          this.phases.splice(
            index,
            1
          )
        }
        this.loading = false
      }
    },
    deleteUS ({us, phase}) {
      this.loading = true
      if (!us.id) {
        const index = phase.uss.indexOf(us)
        if (index > -1) {
          phase.uss.splice(
            index,
            1
          )
        }
        this.loading = false
        return
      }
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
    submitPhases () {
      this.loading = true
      this.phases.map(phase => phase.period = phase.weeks * 7)
      axios.put(
        "/api/etudes/phases/",
        this.phases,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Les Phases ont bien été enregistrés", type: "success"})
        this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Phases`)
      }).catch((err) => {
        //this.$message({message: "Erreur lors de l'enregistrement : " + err, type: "error"})
        if (err.response && err.response.status === 400) {
          this.$message({message: "Le formulaire comporte des erreurs. Vérifiez les descriptions et les objectifs des phases (menu déroulant)",
            type: "error",
            offset: 40})
        } else {
          this.$message({message: "Impossible d'enregistrer les Phases pour le moment",
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
