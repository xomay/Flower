<template>
  <BaseComponent
    title="Ajout d'un employé"
    :breadcrumb="breadcrumb"
  >
    <EmployesForm
      v-model="employe"
      :loading="loading"
      @save="registerEmploye"
    />
  </BaseComponent>
</template>

<script>
import EmployesForm from "../components/EmployesForm"
const axios = require("axios")

export default {
  name: "EmployesCreer",
  components: {EmployesForm},
  data () {
    return {
      employe: {},
      loading: false,
      breadcrumb: []
    }
  },
  methods: {
    registerEmploye () {
      this.loading = true
      axios.post(
        `${this.$server_url}/prospects/${this.$route.params.id}/employes/`,
        this.employe,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'employé(e) a bien été ajouté",
          type: "success"})
        this.$router.push(`/prospects/${this.$route.params.id}/voir`)
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
