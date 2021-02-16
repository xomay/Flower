<template>
  <div class="flex flex-col">
    <div class="flex-1">
      <span v-if="etude.prospect">
        <i class="el-icon-user-solid" /> <u>Prospect :</u>
        <el-link
          type="primary"
          :style="'margin-left: 12px'"
          @click="$router.push('/prospects/'+etude.prospect.id+'/voir')"
        >
          {{ etude.prospect.name }}
        </el-link>
      </span><br><br>
      <span>
        <i class="el-icon-date" /> <u>Mandat:</u> {{ etude.mandat }}
      </span><br>
      <span>
        <i class="el-icon-star-off" /> Numéro de l'étude : <b>{{ etude.number }}</b>.
      </span><br><br>
      <span>
        <i class="el-icon-document" /> <u>Description :</u>
        <br>{{ etude.description }}
      </span><br><br>
      <span v-if="etude.projectManager">
        <i class="el-icon-user" /> Chargé d'étude :
        <el-link
          type="primary"
          :style="'margin-left: 12px'"
          @click="$router.push('/membres/'+etude.projectManager.id+'/voir')"
        >
          {{ etude.projectManager.firstname }} {{ etude.projectManager.lastname }}
        </el-link>
      </span><br>
      <span v-if="etude.qualityManager">
        <i class="el-icon-user" /> Suiveur qualité :
        <el-link
          type="primary"
          :style="'margin-left: 12px'"
          @click="$router.push('/membres/'+etude.qualityManager.id+'/voir')"
        >
          {{ etude.qualityManager.firstname }} {{ etude.qualityManager.lastname }}
        </el-link>
      </span><br>
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
      `/api/gantt/etude/${this.$route.params.id}/`,
      {
        withCredentials: true,
        responseType: "arraybuffer"
      }
    ).then((res) => {
      this.ganttJPG = Buffer.from(
        res.data,
        "binary"
      ).toString("base64")
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le graphe : "+err, type: "error", offset: 40})
    })
  }
}
</script>

<style>

</style>
