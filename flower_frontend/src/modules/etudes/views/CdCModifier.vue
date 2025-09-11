<template>
  <BaseComponent
    title="Modifier le Cahier des Charges"
    :breadcrumb="breadcrumb"
  >
    <div v-for="(phase, idx) in phases" :key="phase.id" style="margin-top: 20px;">
      <el-col>
      <span>Cahier des Charges lié à la phase {{ phase.index }} : {{ phase.title }}</span>
      </el-col>
      <span style="margin-top: 10px;"><b>Description :</b> {{ phase.description }}</span>
      <el-col>
      <span style="margin-top: 10px;"><b>Méthodologie :</b> {{ phase.methodologie }}</span>
      </el-col>
      <el-input
        v-model="phase.spec"
        type="textarea"
        :autosize="{ minRows: 10 }"
        placeholder="Cahier des charges de la phase"
      />
    </div>
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
      phases: [],
      docEtude: {},
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
      res.data.phases.sort((a, b) => a.index - b.index)
      this.phases = res.data.phases
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
        "/api/etudes/phases/",
        this.phases,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Les Cahier des Charges ont bien été enregistrés", type: "success"})
        this.$router.push(`/etudes/${this.$route.params.id}/voir?active=CdC`)
      }).catch((err) => {
        if (err.response && err.response.status === 400) {
          this.$message({message: "Le formulaire comporte des erreurs. Vérifiez les descriptions et les objectifs des phases (menu déroulant)",
            type: "error",
            offset: 40})
        } else {
          this.$message({message: "Impossible d'enregistrer les Cahier des Charges pour le moment",
            type: "error",
            offset: 40})
        }
        this.loading = false
      })
    }
  }
}
</script>

