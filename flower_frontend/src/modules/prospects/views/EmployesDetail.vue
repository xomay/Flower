<template>
  <BaseComponent
    title="Détail d'un employé"
    :breadcrumb="breadcrumb"
  >
    <template v-slot:action>
      <router-link :to="`/prospects/${$route.params.id}/employes/${$route.params.employe_id}/modifier`">
        <el-button
          type="text"
          icon="Edit"
        >
          Modifier
        </el-button>
      </router-link>
    </template>
    <EmployesView :employe="employe" />
  </BaseComponent>
</template>

<script>
import EmployesView from "../components/EmployesView"
const axios = require("axios")

export default {
  name: "EmployesCreer",
  components: {EmployesView},
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
          link: `/prospects/${this.$route.params.id}/employes/${this.$route.params.employe_id}/voir`
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
    }
  }
}
</script>

<style>

</style>
