<template>
  <BaseComponent
    title="Ajout d'un prospect"
    :breadcrumb="breadcrumb"
  >
    <ProspectsForm
      v-model="prospect"
      :loading="loading"
      @save="registerProspect"
    />
  </BaseComponent>
</template>

<script>
import ProspectsForm from "../components/ProspectsForm"
const axios = require("axios")

export default {
  name: "ProspectsCreer",
  components: {ProspectsForm},
  data () {
    return {
      prospect: {},
      loading: false,
      breadcrumb: [
        {
          name: "Liste des prospects",
          link: "/prospects"
        },
        {
          name: "Ajouter un prospect",
          link: "/prospects/ajouter"
        }
      ]
    }
  },
  methods: {
    registerProspect () {
      this.loading = true
      axios.post(
        `${this.$server_url}/prospects/`,
        this.prospect,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le prospect a bien été ajouté",
          type: "success"})
        this.$router.push("/prospects")
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

<style>

</style>
