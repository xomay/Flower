<template>
  <BaseComponent
    title="Modifier le Cahier des Charges"
    :breadcrumb="breadcrumb"
  >
    <CdCForm
      v-model="requirements"
      :phases="phases"
      :disabled="disabled"
      :loading="loading"
      @add-requirement="addRequirement"
      @delete-requirement="deleteRequirement"
    />
    <el-button
      type="primary"
      style="margin-top: 20px;"
      @click="submitCdC"
    >
      Enregistrer
    </el-button>
  </BaseComponent>
</template>

<script>
import CdCForm from "../components/forms/CdCForm.vue";
const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

export default {
  name: "CdCModifier",
  components: {CdCForm},
  data () {
    return {
      loading: true,
      requirements: [],
      phases: [],
      disabled: false,
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
          name: "Cahier des Charges",
          link: `/etudes/${this.$route.params.id}/cdc`
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
      this.requirements = res.data.requirements
      this.phases = res.data.phases
      this.breadcrumb[1].name = res.data.name
    }).catch(() => {
      this.$message({message: "Impossible de récupérer les groupes pour le moment", type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    addRequirement () {
      this.loading = true
      const requirement = {
        reference: "<REFERENCE>",
        description: "Description du point de cahier des charges.",
        etude: this.$route.params.id,
      }
      axios.post(
        "/api/requirements/",
        [requirement],
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "Le point de cahier des charges a bien été ajoutée.", type: "success"})
        const requirement = res.data[0];
        this.requirements.push(requirement)
      }).catch(() => {
        this.$message({message: "Impossible de créer un point de cahier des charges pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deleteRequirement (requirement) {
      this.loading = true
      axios.delete(
        `/api/requirements/${requirement.id}/`,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le point de cahier des charges a bien été supprimé.", type: "success"})
        this.requirements = this.requirements.filter(r => r.id !== requirement.id)
      }).catch(() => {
        this.$message({message: "Impossible de supprimer le point de cahier des charges pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    submitCdC () {
      this.loading = true
      axios.put(
        "/api/requirements/",
        this.requirements,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le Cahier des Charges a bien été enregistré", type: "success"})
        this.$router.push(`/etudes/${this.$route.params.id}/voir?active=CdC`)
      }).catch((err) => {
        if (err.response && err.response.status === 400) {
          this.$message({message: "Le formulaire comporte des erreurs.",
            type: "error",
            offset: 40})
        } else {
          this.$message({message: "Impossible d'enregistrer les Cahier des Charges pour le moment",
            type: "error",
            offset: 40})
        }
        this.loading = false
      })
    }
  }
}
</script>

