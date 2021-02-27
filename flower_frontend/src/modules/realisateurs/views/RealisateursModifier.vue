<template>
  <BaseComponent
    title="Modifier le réalisateur"
    :breadcrumb="breadcrumb"
    :loading="loading"
  >
    <RealisateurForm
      :value="realisateur"
      :deletable="true"
      :loading="loading"
      :ecole-suffix="mailSuffix"
      @deleted="deleted"
      @edited="edit"
    />
  </BaseComponent>
</template>

<script>
import RealisateurForm from "../components/RealisateurForm.vue"
import GlobalData from "@/mixins/GlobalData"
const axios = require("axios")

export default {
  name: "RealisateurModifier",
  components: { RealisateurForm },
  mixins: [GlobalData],
  data () {
    return {
      mailSuffix: "",
      realisateur: {},
      loading: true,
      breadcrumb: [
        {
          name: "Liste des réalisateurs",
          link: "/realisateurs"
        },
        {
          name: "<loading>",
          link: `/realisateurs/${this.$route.params.id}/voir`
        },
        {
          name: "Modifier",
          link: `/realisateurs/${this.$route.params.id}/modifier`
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/realisateurs/${this.$route.params.id}`,
      {withCredentials: true}
    ).then((res) => {
      this.realisateur = res.data
      this.breadcrumb[1].name = `${this.realisateur.firstname} ${this.realisateur.lastname}`
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le réalisateur pour le moment : " + err,
        type: "error",
        offset: 40})
    }).finally(() => {
      this.loading = false
    })
  },
  created () {
    this.queryData(axios, "mail_suffix")
      .then((res) => this.mailSuffix = "@" + res.data[0])
      .catch((err) => this.$message({message: "Erreur: " + err, type: "error"}))
  },
  methods: {
    deleted () {
      this.loading = true
      axios.delete(
        `/api/realisateurs/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le réalisateur a bien été supprimé.", type: "success"})
        this.$router.push("/realisateurs")
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer le réalisateur : "+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    edit () {
      this.loading = true
      axios.put(
        `/api/realisateurs/${this.$route.params.id}/`,
        this.realisateur,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le réalisateur a bien été modifié.", type: "success"})
        this.$router.push(`/realisateurs/${this.$route.params.id}/voir`)
      }).catch((err) => {
        this.$message({message: "Impossible de modifier le réalisateur : "+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    }
  }
}
</script>
