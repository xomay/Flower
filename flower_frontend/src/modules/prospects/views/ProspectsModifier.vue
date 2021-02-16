<template>
  <div>
    <BaseComponent
      title="Modification d'un prospect"
      :breadcrumb="breadcrumb"
    >
      <ProspectsForm
        v-model="prospect"
        :loading="loading"
        :deletable="true"
        :members="members"
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
      members: [],
      loading: false,
      breadcrumb: [
        {
          name: "Lister des prospects",
          link: "/prospects"
        },
        {
          name: "<loading>",
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
    this.getMembers()
  },
  methods: {
    getProspect () {
      axios.get(
        `/api/prospects/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then((res) => {
        this.prospect = res.data
        this.breadcrumb[1].name = this.prospect.name
        if(this.prospect.contactWay.length == 0)
          this.prospect.contactWay = [""]
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer le prospect : "+err, type: "error"})
      })
    },
    updateProspect () {
      this.loading = true
      axios.put(
        `/api/prospects/${this.$route.params.id}/`,
        this.prospect,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le prospect a bien été mis à jour", type: "success"})
        this.$router.push(`/prospects/${this.$route.params.id}/voir`)
      }).catch((err) => {
        this.$message({message: err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deleteProspect () {
      axios.delete(
        `/api/prospects/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le prospect a bien été retiré", type: "success"})
        this.$router.push("/prospects")
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer le prospect : "+err, type: "error"})
      })
    },
    getMembers () {
      axios.get(
        "/api/membres/",
        {withCredentials: true}
      ).then((res) => {
        res.data.forEach((mem) => mem.value = `${mem.firstname} ${mem.lastname}`)
        this.members = res.data
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer les membres : "+err, type: "error"})
      })
    }
  }
}
</script>
