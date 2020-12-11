<template>
  <BaseComponent
    title="Modification d'un employé"
    :breadcrumb="breadcrumb"
  >
    <EmployesForm
      v-model="employe"
      :loading="loading"
      :deletable="true"
      @save="registerEmploye"
      @delete="deleteEmploye"
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
      breadcrumb: [
        {
          name: "Lister des prospects",
          link: "/prospects"
        },
        {
          name: "Prospect",
          link: `/prospects/${this.$route.params.id}/voir`
        },
        {
          name: "",
          link: `/prospects/${this.$route.params.id}/employes/${this.$route.params.employe_id}/modifier`
        }
      ]
    }
  },
  created () {
    this.getEmploye()
  },
  methods: {
    getEmploye () {
      axios.get(
        `/api/prospects/${this.$route.params.id}/employes/${this.$route.params.employe_id}/`,
        {withCredentials: true}
      ).then((res) => {
        this.employe = res.data
        this.breadcrumb[2].name = `${this.employe.firstname} ${this.employe.lastname}`
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        })
    },
    registerEmploye () {
      this.loading = true
      axios.put(
        `/api/prospects/${this.$route.params.id}/employes/${this.$route.params.employe_id}/`,
        this.employe,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'employé(e) a bien été mis à jour",
          type: "success"})
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    },
    deleteEmploye () {
      axios.delete(
        `/api/prospects/${this.$route.params.id}/employes/${this.$route.params.employe_id}/`,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'employé a bien été retiré",
          type: "success"})
        this.$router.push(`/prospects/${this.$route.params.id}/voir`)
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        })
    }
  }
}
</script>

<style>

</style>
