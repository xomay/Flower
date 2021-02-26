<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
  >
    <NFsForm
      :nf="nf"
      :membres="membres"
      :loading="loading"
      :deletable="true"
      :default-tva="defaultTVA"
      @save="saveNF"
      @deleteBloc="deleteNFDetail"
      @addBloc="addNFDetail"
      @delete="deleteNF"
    />
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import NFsForm from "../components/NFsForm.vue"
import GlobalData from "@/mixins/GlobalData"
export default {
  name: "NFsVoir",
  components: { NFsForm },
  mixins: [GlobalData],
  data () {
    return {
      nf: {
        demandeur: 0,
        reference: "",
        details: []
      },
      membres: [],
      defaultTVA: 0.2,
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
      }).finally(() => this.loading = false)
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la NF : " + err, type: "error"})
      this.loading = false
    })
  },
  created () {
    this.queryData(axios, "global_tva")
      .then((res) => this.defaultTVA = res.data[0])
      .catch((err) => this.$message({message: "Erreur: " + err, type: "error"}))
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
        this.$message({message: "Impossible de sauvegarder la NF : " + err, type: "error"})
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
      /*this.loading = false
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
      }).finally(() => {
        this.loading = false
      })*/
      this.nf.details.splice(
        blocIndex,
        1
      )
    },
    addNFDetail (newDepense) {
      /*this.loading = true
      axios.post(
        "/api/ndfs/details/",
        newDepense,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "La dépense a bien été ajoutée.", type: "success"})
        this.nf.details.push(res.data)
      }).catch((err) => {
        this.$message({message: "Impossible de créer une dépense pour le moment: " +err, type: "error"})
      }).finally(() => {
        this.loading = false
      })*/
      console.log("add " + newDepense)
      this.nf.details.push({
        ndf: this.nf.id,
        index: this.nf.details.length + 1,
        description: "",
        detailType: "N",
        prixHT: 0,
        tva: 0.2,
        nbKilometres: 0,
        prixCentimesKilometres: 6
      })
    }
  }
}
</script>
