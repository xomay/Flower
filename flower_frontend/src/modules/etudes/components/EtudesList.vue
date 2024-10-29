<template>
  <el-table
    v-loading="loading"
    class="grid"
    :data="etudes"
    :stripe="true"
    :border="true"
  >
    <el-table-column
      prop="name"
      label="Nom de l'étude"
      fixed="left"
      sortable
    >
      <template v-slot="scope">
        <el-button
          :style="scope.row.isAborted ? 'color: red;' : (scope.row.isFinished ? 'color: green;' : '')"
          type="text"
          @click="clicked(scope.row.id)"
        >
          {{ scope.row.name }}
        </el-button>
        <span
          v-if="scope.row.confidential && !scope.row.isAborted"
          class="bigGray"
          style="margin-right: 12px;"
        >
          [Confidentielle]
        </span>
        <span
          v-if="scope.row.isAborted"
          class="bigRed"
        >
          [Étude avortée]
        </span>
        <span
          v-if="scope.row.isFinished"
          class="bigGreen"
        >
          [Étude terminée]
        </span>
      </template>
    </el-table-column>
    <el-table-column
      prop="number"
      label="Numéro de l'étude"
      align="center"
      fixed="left"
      width="180px"
      sortable
    />
    <el-table-column
      prop="avenantsAmount"
      label="Nombre d'avenants"
      align="center"
      fixed="right"
      width="180px"
      sortable
    />
    <el-table-column
      label="Avancement"
      class="back"
      fixed="right"
      align="center"
    >
      <template v-slot="scope">
        <div v-if="scope.row.isAborted">
          <p style="color: rgb(97, 4, 4); font-size:120%;">
            <b>Étude avortée.</b>
          </p>
        </div>
        <div v-else>
          <el-col>
            <div class="progress">
              <div
                class="progress-value"
                :style="getPercentage(scope.row.state)"
              />
            </div>
          </el-col>
          <el-col
            style="text-align: left !important;"
          >
            {{ getState(scope.row.state) }}
          </el-col>
        </div>
      </template>
    </el-table-column>
    <el-table-column
      prop="mandat"
      label="Mandat"
      align="center"
      fixed="right"
      width="120px"
      sortable
    />
  </el-table>
</template>

<script>
import Utils from "@/mixins/Utils"
export default {
  name: "EtudesList",
  mixins: [Utils],
  props: {
    etudes: {type : Array, required: true },
    loading: {type : Boolean, required: true },
    discret: {type : Boolean, default () { return false } }
  },
  methods: {
    clicked (id) {
      this.$emit("select", id)
    },
    getPercentage (state) {
      if(state == undefined)
        return "width: 0%"
      return "width: "+(state*10)+"%"
    },
    getState (state) {
      if(state == undefined || this.discret)
        return ""
      switch (state) {
      case 0: return "Les groupes sont à rédiger, le devis à envoyer."
      case 1: return "La CE est à rédiger, envoyer et faire signer."
      case 2: return "Les RM sont à rédiger et faire signer."
      case 3: return "La FA doit être envoyée et payée."
      case 4: return "Le PVRI doit être envoyé et accepté."
      case 5: return "La FI (optionnelle) soit être payée."
      case 6: return "Le PVRF doit être envoyé et accepté."
      case 7: return "La FS doit être envoyée et payée."
      case 8: return "Les rapports pédas doit être remplis."
      case 9: return "Le BV doit être payé."
      case 10: return "Étude terminée."
      }
      return "Étude avortée."
    }
  }
}
</script>

<style scoped>
  .back {
    justify-content: center;
    align-items: center;
    background: #000;
    display: flex;
    height: 100vh;
    padding: 0;
    margin: 0;
  }

  .progress {
    background: rgb(161, 153, 153) !important;
    justify-content: flex-start;
    border-radius: 100px;
    align-items: center;
    position: relative;
    padding: 1px 1px;
    display: flex;
    height: 20px;
    width: 100%;
  }

  .progress-value {
    animation: load 3s normal forwards;
    box-shadow: 0 10px 40px -10px rgba(58, 219, 9, 0.144);
    background: rgb(31, 148, 2);
    border-radius: 100px;
    height: 100%;
  }

  .bigRed {
    color: rgb(165, 27, 27);
    font-weight: bold;
  }
  .bigGreen {
    color: rgb(23, 197, 38);
    font-weight: bold;
  }
  .bigGray {
    color: rgb(17, 55, 70);
    font-weight: bold;
  }
</style>