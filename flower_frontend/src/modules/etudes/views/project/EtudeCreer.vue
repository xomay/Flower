<template>
  <BaseComponent
    title="Ajouter une étude"
    :breadcrumb="breadcrumb"
  >
    <ProjectForm
      v-model="form"
      :loading="loading"
      @save="submitProject"
    />
  </BaseComponent>
</template>

<script>
import ProjectForm from "../../components/forms/ProjectForm"

const axios = require("axios")

export default {
  name: "EtudeCreer",
  components: { ProjectForm },
  data () {
    return {
      loading: false,
      breadcrumb: [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: "Ajouter une étude",
          link: "/etudes/ajouter"
        }
      ],
      form: {
        prospect: "",
        name: "",
        description: "",
        mandat: "",
        number: "",
        confidential: false,
        projectManager: "",
        qualityManager: ""
      }
    }
  },
  methods: {
    submitProject () {
      this.loading = true
      this.form.prospect = this.form.prospect.toString()
      axios.post(
        `${this.$server_url}/etudes/`,
        this.form,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'étude a bien été créée.",
          type: "success",
          offset: 40})
        this.$router.push("/etudes")
      }).catch((err) => {
        console.log(err)
        if (err.response && err.response.status === 400) {
          this.$message({message: "Le formulaire comporte des erreurs.",
            type: "error",
            offset: 40})
        } else {
          this.$message({message: "Impossible de créer l'étude pour le moment.",
            type: "error",
            offset: 40})
        }
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
