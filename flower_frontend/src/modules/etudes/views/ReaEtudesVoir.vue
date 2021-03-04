<template>
  <BaseComponent
    title="Suivi de vos études"
    :breadcrumb="breadcrumb"
  >
    <EtudesList
      v-show="etudes.length > 0"
      :etudes="etudes"
      :discret="true"
      :loading="loading"
      @select="goToEtude"
    />
    <el-row v-show="etudes.length == 0">
      <el-col
        style="text-align: center; text-weight: bold;"
      >
        Vous n'apparaissez dans aucune étude.
      </el-col>
    </el-row>
  </BaseComponent>
</template>

<script>
import EtudesList from "../components/EtudesList.vue"
const axios = require("axios")

export default {
  name: "ReaEtudeVoir",
  components: { EtudesList },
  data () {
    return {
      etudes: [],
      loading: true,
      breadcrumb: [
        {
          name: "Mes études",
          link: "/etudes/acces-rea"
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/etudes/getReaEtudes/",
      {withCredentials: true}
    ).then((res) => {
      this.etudes = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer vos études pour le moment: "+err, type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    goToEtude (id) {
      this.$router.push(`/etudes/acces-rea/${id}/voir`)
    }
  }
}
</script>

<style>
  .confiStyle {
    color: rgb(165, 27, 27);
    font-weight: bold;
  }
</style>
