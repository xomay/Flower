<template>
  <BaseComponent
    title="Création d'action commerciale"
    :breadcrumb="breadcrumb"
  >
    <p class="mb-4"><b>Action commerciale</b></p>
    <ACForm
      v-model="actionCommerciale"
      :loading="loading"
      :deletable="false"
      @save="sendForm"
    />
  </BaseComponent>
</template>

<script>
import ACForm from "../components/ACForm"

const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.withCredentials = true

export default {
  name: "ActionCommerciale",
  components: {ACForm},
  data () {
    return {
      breadcrumb: [
        {
          name: "Lister des actions commerciales",
          link: "/prospects/actionCommerciale/"
        },
        {
          name: "Créer une action commerciale",
          link: "/prospects/actionCommerciale/ajouter"
        }
      ],
      loading: false,
      // Données exportées au final
      actionCommerciale: {
        type: "",
        name: "",
        date: "",
        participants: [],
        instructions: ""
      }
    }
  },
  methods: {
    sendForm () {
      this.loading = true
      axios.post(
        "/api/actioncom/",
        this.actionCommerciale,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'action commerciale a bien été ajouté",
          type: "success"})
        this.$router.push("/prospects/actionCommerciale/")
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    }
  }
}
</script>