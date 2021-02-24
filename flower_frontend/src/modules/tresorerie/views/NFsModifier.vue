<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
  >
    <NFsForm
      :nf="nf"
    />
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import NFsForm from "../components/NFsForm.vue"
export default {
  name: "NFsVoir",
  components: { NFsForm },
  data () {
    return {
      nf: {
        demandeur: 0,
        reference: "",
        details: []
      },
      membres: [],
      title: "<loading>",
      loading: true,
      breadcrumb: [
        {
          name: "Liste des NF normales",
          link: "/tresorerie/nfs/voir/normales"
        },
        {
          name: "<loading>",
          link: `/tresorerie/nfs/${this.$route.params.id}/voir/`
        },
        {
          name: "Modifier",
          link: `/tresorerie/nfs/${this.$route.params.id}/modifier/`
        }
      ]
    }
  },
  beforeCreate () {
    axios.get(
      `api/ndfs/${this.$route.params.id}/`,
      { withCredentials: true }
    ).then((res) => {
      this.nf = res.data
      this.nf.demandeur = this.nf.demandeur.id
      this.breadcrumb[1].name = this.nf.reference
      this.title = "Modification de " + this.nf.reference
      axios.get(
        "/api/membres/",
        {withCredentials: true}
      ).then((res) => {
        this.membres = res.data.map(obj => ({...obj, value: obj.firstname+" "+obj.lastname}))
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer les membres pour le moment : "+err, type: "error"})
      })
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la NF : " + err, type: "error"})
    })
  }
}
</script>
