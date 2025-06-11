<template>
  <BaseComponent
    title="Modifier les Cahier des Charges"
    :breadcrumb="breadcrumb"
  >
    <el-input
      v-model="spec"
      type="textarea"
      :autosize="{ minRows: 25}"
      placeholder="Cahier des Charges de l'étude"
      :disabled="disabled"
    />
    <el-button
      type="primary"
      style="margin-top: 20px;"
      @click="submitCdC"
    >
      Enregistrer
    </el-button>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

export default {
  name: "CdCModifier",
  components: {},
  data () {
    return {
      loading: true,
      spec: "",
      docEtude: {},
      isOriginalGroupes: true,
      originalGroupOwner: -1,
      breadcrumb: [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: "<loading>",
          link: `/etudes/${this.$route.params.id}/voir`
        },
        {
          name: "Cahier des Charges",
          link: `/etudes/${this.$route.params.id}/cdc`
        }
      ]
    }
  },
  created () {
    this.loading = true
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.isOriginalGroupes = res.data.isOriginalGroupes
      this.originalGroupOwner = res.data.currentGroupes.id
      res.data.groupes = res.data.currentGroupes.groupes.sort((a, b) => a.index - b.index)
      res.data.groupes.forEach((groupe) => {
        groupe.phases = groupe.phases.sort((a, b) => a.index - b.index)
      })
      this.spec = res.data.docEtude.spec
      this.docEtude = res.data.docEtude
      this.breadcrumb[1].name = res.data.name
    }).catch(() => {
      this.$message({message: "Impossible de récupérer les groupes pour le moment", type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    submitCdC () {
      this.loading = true
      axios.put(
        "/api/etudes/" + this.docEtude.id + "/ce/",
        {
          spec: this.spec,
          id: this.docEtude.id,
        },
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le Cahier des Charges a bien été enregistré", type: "success"})
        this.$router.push(`/etudes/${this.$route.params.id}/voir?active=CdC`)
      }).catch((err) => {
        this.$message({message: "Erreur lors de l'enregistrement : " + err, type: "error"})
        if (err.response && err.response.status === 400) {
          this.$message({message: "Le formulaire comporte des erreurs. Vérifiez les descriptions et les objectifs des phases (menu déroulant)",
            type: "error",
            offset: 40})
        } else {
          this.$message({message: "Impossible d'enregistrer le Cahier des Charges pour le moment",
            type: "error",
            offset: 40})
        }
        this.loading = false
      })
    }
  }
}
</script>

