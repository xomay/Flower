<template>
  <el-table
    v-loading="loading"
    class="grid"
    :data="etudes"
    :stripe="true"
  >
    <el-table-column
      prop="name"
      label="Nom de l'étude"
      sortable
    >
      <template slot-scope="scope">
        <el-button
          type="text"
          @click="clicked(scope.row.id)"
        >
          {{ scope.row.name }}
        </el-button>
        <span
          v-if="scope.row.confidential"
          class="confiStyle"
        >
          Confidentielle
        </span>
      </template>
    </el-table-column>
    <el-table-column
      prop="number"
      label="Numéro de l'étude"
      sortable
    />
    <el-table-column
      label="Avancement"
      class="back"
    >
      <template slot-scope="scope">
        <el-col>
          <div class="progress">
            <div
              class="progress-value"
              :style="getPercentage(scope.row.state)"
            />
          </div>
        </el-col>
        <el-col>
          {{ getState(scope.row.state) }}
        </el-col>
      </template>
    </el-table-column>
    <el-table-column
      prop="mandat"
      label="Mandat"
      sortable
    />
  </el-table>
</template>

<script>
export default {
  name: "EtudesList",
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
    width: 80%;
  }

  .progress-value {
    animation: load 3s normal forwards;
    box-shadow: 0 10px 40px -10px rgba(58, 219, 9, 0.144);
    border-radius: 100px;
    background: rgb(49, 122, 15);
    height: 100%;
  }
</style>