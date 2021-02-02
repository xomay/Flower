<template>
  <BaseComponent
    title="Création d'action commerciale"
    :breadcrumb="breadcrumb"
  >
    <h1 class="text-xl">
      Action commerciale
    </h1>
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
      console.log(this.actionCommerciale)
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