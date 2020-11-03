<template>
  <div class="flex flex-col">
    <div class="flex-1">
      <span v-if="etude.prospect">Prospect : {{ etude.prospect.name }}</span><br>
      <span>Description : {{ etude.description }}</span><br>
      <span>Numéro de l'étude : {{ etude.number }}</span><br>
      <span v-if="etude.projectManager">Chargé d'étude : {{ etude.projectManager.firstname }} {{ etude.projectManager.lastname }}</span><br>
      <span v-if="etude.qualityManager">Suiveur qualité : {{ etude.qualityManager.firstname }} {{ etude.qualityManager.lastname }}</span><br>
    </div>
    <div
      v-loading="!ganttJPG"
      class="flex-1"
    >
      <img :src="`data:image/jpeg;base64,${ganttJPG}`">
    </div>
  </div>
</template>

<script>
const axios = require("axios")

export default {
  name: "Summary",
  props: {
    etude: { type: Object, required: true }
  },
  data () {
    return {
      ganttJPG: ""
    }
  },
  created () {
    axios.get(
      `${this.$server_url}/gantt/etude/${this.$route.params.id}/`,
      {withCredentials: true,
        responseType: "arraybuffer"}
    ).then((res) => {
      this.ganttJPG = Buffer.from(
        res.data,
        "binary"
      ).toString("base64")
    }).
      catch((err) => {
        this.$message({message: err,
          type: "error",
          offset: 40})
      })
  }
}
</script>

<style>

</style>
