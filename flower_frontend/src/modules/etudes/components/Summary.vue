<template>
  <div class="flex flex-col">
    <EtudeSteps
      :etude="etude"
      :descriptions="getgantt"
    />
    <div
      class="flex-1"
    >
      <span v-if="etude.prospect && !reaVue">
        <i class="el-icon-user-solid" /> <u>Prospect :</u>
        <el-link
          type="primary"
          :style="'margin-left: 12px'"
          @click="$router.push(`/prospects/${etude.prospect.id}/voir`)"
        >
          {{ etude.prospect.name }}
        </el-link>
        <br>
      </span>
      <span v-if="etude.clientContact && !reaVue">
        <i class="el-icon-user-solid" /> <u>Contact client :</u>
        <el-link
          type="primary"
          :style="'margin-left: 12px'"
          @click="$router.push(`/prospects/${etude.prospect.id}/employes/${etude.clientContact.id}/voir`)"
        >
          {{ etude.clientContact.firstname + " " + etude.clientContact.lastname }}
        </el-link>
        <br><br>
      </span>
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
          v-if="!reaVue"
          type="primary"
          :style="'margin-left: 12px'"
          @click="$router.push('/membres/'+etude.projectManager.id+'/voir')"
        >
          {{ etude.projectManager.firstname }} {{ etude.projectManager.lastname }}
        </el-link>
        <span v-else>
          {{ etude.projectManager.firstname }} {{ etude.projectManager.lastname }}
        </span>
        <br>
      </span>
      <span v-if="etude.qualityManager && !reaVue">
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
      v-if="getgantt"
      v-show="displaysGantt"
      v-loading="!ganttJPG"
      class="flex-1"
    >
      <img
        :src="`data:image/jpeg;base64,${ganttJPG}`"
        width="55%"
      >
    </div>
  </div>
</template>

<script>
import EtudeSteps from "./graphics/EtudeSteps"
const axios = require("axios")

export default {
  name: "Summary",
  components: { EtudeSteps },
  props: {
    etude: { type: Object, required: true },
    getgantt: { type: Boolean, default: true },
    reaVue: { type: Boolean, default: false }
  },
  data () {
    return {
      ganttJPG: "",
      displaysGantt: true
    }
  },
  created () {
    if(this.getgantt) {
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
        if(err.message == "Request failed with status code 404")
          this.$message({message: "Il n'y a pas de groupes dans cette étude !", type: "error"})
        else
          this.$message({message: "Impossible de récupérer le graphe : "+err, type: "error"})
        this.displaysGantt = false
      })
    }
  }
}
</script>
