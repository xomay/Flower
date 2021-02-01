<template>
  <BaseComponent
    title="Modification d'action commerciale"
    :breadcrumb="breadcrumb"
  >
    <h1 class="text-xl">
      Action commerciale
    </h1>
    <ACForm
      v-model="actionCommerciale"
      :loading="loading"
      :deletable="true"
      @save="updateAction"
      @delete="deleteAction"
    />
  </BaseComponent>
</template>

<script>
import ACForm from "../components/ACForm"

const axios = require("axios")

export default {
  name: "ActionCommercialeModifier",
  components: {ACForm},
  data () {
    return {
      breadcrumb: [
        {
          name: "Lister des actions commerciales",
          link: "/prospects/actionCommerciale/"
        },
        {
          name: "<loading>",
          link: `/prospects/actionCommerciale/${this.$route.params.id}/voir`
        },
        {
          name: "Modifier",
          link: `/prospects/actionCommerciale/${this.$route.params.id}/modifier`
        }
      ],
      loading: false,
      // Données exportées au final
      actionCommerciale: {}
    }
  },
  created () {
    this.getAction()
  },
  methods: {
    getAction () {
      this.loading = true
      axios.get(
        `/api/actioncom/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then((res) => {
        this.actionCommerciale = res.data
        this.breadcrumb[1].name = res.data.name
      }).catch((err) => {
        this.$message({message: "Impossible de modifier le prospect"+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    updateAction () {
      this.loading = true
      axios.put(
        `/api/actioncom/${this.$route.params.id}/`,
        this.actionCommerciale,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'action commerciale a bien été mise à jour", type: "success"})
        this.$router.push("/prospects/actionCommerciale/")
      }).catch((err) => {
        this.$message({message: "Impossible de modifier le prospect"+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deleteAction () {
      this.loading = true
      axios.delete(
        `/api/actioncom/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'action commerciale a bien été retiré", type: "success"})
        this.$router.push("/prospects/actionCommerciale/")
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer l'action : "+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    }
  }
}
</script>