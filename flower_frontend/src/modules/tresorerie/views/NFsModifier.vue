<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
  >
    <NFsForm
      :nf="nf"
      :membres="membres"
      @save="saveNF"
      @deleteBloc="deleteNFDetail"
      @delete="deleteNF"
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
          name: "Liste des NF",
          link: "/tresorerie/nfs/voir/"
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
  },
  methods: {
    saveNF () {
      axios.put(
        `api/ndfs/${this.$route.params.id}/`,
        this.nf,
        { withCredentials: true }
      ).then(() => {
        this.$message({message: "NF enregistrée avec succès.", type: "success"})
        this.$router.push("/tresorerie/nfs/voir/")
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer la NF : " + err, type: "error"})
      })
    },
    deleteNF () {
      axios.delete(
        `api/ndfs/${this.$route.params.id}/`,
        { withCredentials: true }
      ).then(() => {
        this.$message({message: "NF supprimée avec succès.", type: "success"})
        this.$router.push("/tresorerie/nfs/voir/")
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer la NF : " + err, type: "error"})
      })
    },
    deleteNFDetail (detailID, blocIndex) {
      axios.delete(
        `/api/ndfs/details/${detailID}/`,
        {withCredentials: true}
      ).then(() => {
        this.nf.details.splice(
          blocIndex,
          1
        )
        this.$message({message: "La dépense a bien été supprimé", type: "success"})
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer cette dépense pour le moment :"+err, type: "error"})
      })
    }
  }
}
</script>
