<template>
  <BaseComponent
    title="Créer une NF"
    :breadcrumb="breadcrumb"
  >
    <NFsForm
      :nf="nf"
      :membres="membres"
      :loading="loading"
      :default-tva="defaultTVA"
      @save="submitNF"
    />
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import NFsForm from "../components/NFsForm.vue"
import GlobalData from "@/mixins/GlobalData"
export default {
  name: "NFsCreer",
  components: { NFsForm },
  mixins: [GlobalData],
  data () {
    return {
      nf: {
        demandeur: 0,
        objet: "",
        mandat: 2021,
        date: "",
        details: []
      },
      membres: [],
      defaultTVA: 0.2,
      loading: true,
      breadcrumb: [
        {
          name: "Liste des NF",
          link: "/tresorerie/nfs/voir/"
        },
        {
          name: "Créer une NF",
          link: "/tresorerie/nfs/ajouter/"
        }
      ]
    }
  },
  beforeCreate () {
    axios.get(
      "/api/membres/",
      {withCredentials: true}
    ).then((res) => {
      this.membres = res.data.map(obj => ({...obj, value: obj.firstname+" "+obj.lastname}))
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les membres pour le moment : "+err, type: "error"})
    }).finally(() => this.loading = false)
  },
  created () {
    this.queryData(axios, "global_tva")
      .then((res) => this.defaultTVA = res.data[0])
      .catch((err) => this.$message({message: "Erreur: " + err, type: "error"}))
  },
  methods: {
    submitNF () {
      axios.post(
        "/api/ndfs/",
        this.nf,
        { withCredentials: true }
      ).then((res) => {
        this.$message({message: "NF ajoutée avec succès.", type: "success"})
        this.$router.push(`/tresorerie/nfs/${res.data}/voir/`)
      }).catch((err) => {
        this.$message({message: "Impossible d'ajouter la NF : " + err, type: "error"})
      })
    }
  }
}
</script>
