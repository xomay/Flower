<template>
  <BaseComponent
    title="Modifier une étude"
    :breadcrumb="breadcrumb"
  >
    <ProjectForm
      v-model="etude"
      :loading="loading"
      @save="saveProject"
    />
  </BaseComponent>
</template>

<script>
import ProjectForm from "../../components/forms/ProjectForm"

const axios = require("axios")

export default {
  name: "EtudeCreer",
  components: {ProjectForm},
  data () {
    return {
      loading: false,
      breadcrumb: [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: "Modifier une étude",
          link: `/etudes/${this.$route.params.id}/modifier`
        }
      ],
      etude: {
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
  beforeCreate () {
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.etude = res.data
      this.breadcrumb = [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: this.etude.name,
          link: `/etudes/${this.etude.id}/voir`
        },
        {
          name: "Modifier une étude",
          link: `/etudes/${this.etude.id}/modifier`
        }
      ]
    }).
      catch(() => {
        this.$message({
          message: "Impossible de récupérer l'études pour le moment",
          type: "error"})
      })
  },
  methods: {
    saveProject () {
      this.loading = true
      axios.put(
        `/api/etudes/${this.etude.id}/`,
        this.etude,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'étude a bien été modifié.",
          type: "success",
          offset: 40})
        //this.$router.push("/etudes/"+this.etude.id+"/voir") // uncomment it to go back to etude after editing
      }).
        catch((err) => {
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
