<template>
  <div>
    <BaseComponent
      title="Modification d'un prospect"
      :breadcrumb="breadcrumb"
    >
      <ProspectsForm
        v-model="prospect"
        :loading="false"
        :deletable="true"
        @save="updateProspect"
        @delete="deleteProspect"
      />
    </BaseComponent>
  </div>
</template>

<script>
import ProspectsForm from "../components/ProspectsForm"
const axios = require("axios")

export default {
  name: "ProspectsModifier",
  components: {ProspectsForm},
  data () {
    return {
      prospect: {},

      employes: [],
      loading: false,
      breadcrumb: [
        {
          name: "Lister des prospects",
          link: "/prospects"
        },
        {
          name: "",
          link: `/prospects/${this.$route.params.id}/voir`
        },
        {
          name: "Modifier",
          link: `/prospects/${this.$route.params.id}/modifier`
        }
      ]
    }
  },
  created () {
    this.getProspect()
    this.getEmployes()
    this.getAllContactWays()
  },
  methods: {
    getProspect () {
      axios.get(
        `/api/prospects/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then((res) => {
        this.prospect = res.data
        this.breadcrumb[1].name = this.prospect.name
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        })
    },
    updateProspect () {
      this.loading = true
      axios.put(
        `/api/prospects/${this.$route.params.id}/`,
        this.prospect,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le prospect a bien été mis à jour",
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
    deleteProspect () {
      axios.delete(
        `/api/prospects/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le prospect a bien été retiré",
          type: "success"})
        this.$router.push("/prospects")
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        })
    },
    getEmployes () {
      axios.get(
        `/api/prospects/${this.$route.params.id}/employes/`,
        {withCredentials: true}
      ).then((res) => {
        this.employes = res.data
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
