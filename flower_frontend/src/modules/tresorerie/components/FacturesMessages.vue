<template>
  <div>
    <!-- (3) : FA -->
    <el-row v-show="etude.state == 3">
      <span class="message-alert">Vous devez signer la FA !</span>
      <el-col v-show="fas.length == 0">
        Il n'existe aucune Facture d'Accompte.
        <router-link :to="`/etudes/${$route.params.id}/factures/ajouter`">
          <el-button
            icon="el-icon-edit"
            type="primary"
          >
            Ajouter une facture
          </el-button>
        </router-link>
      </el-col>
      <el-col v-show="fas.length > 0">
        <el-button
          type="success"
          icon="el-icon-check"
          @click="levelupTo(4)"
        >
          La FA a été signée
        </el-button>
      </el-col>
    </el-row>
    <!-- (5) : FA -->
    <el-row v-show="etude.state == 5">
      <span class="message-alert">Vous devez signer la FI !</span>
      <el-col v-show="fis.length == 0">
        Il n'existe aucune Facture Intermédiaire.
        <router-link :to="`/etudes/${$route.params.id}/factures/ajouter`">
          <el-button
            icon="el-icon-edit"
            type="primary"
          >
            Ajouter une facture
          </el-button>
        </router-link>
      </el-col>
      <el-col v-show="fis.length > 0">
        <el-button
          type="success"
          icon="el-icon-check"
          @click="levelupTo(6)"
        >
          La FI a été signée
        </el-button>
      </el-col>
    </el-row>
    <!-- (7) : FS -->
    <el-row v-show="etude.state == 7">
      <span class="message-alert">Vous devez signer la FS !</span>
      <el-col v-show="fss.length == 0">
        Il n'existe aucune Facture de Solde.
        <router-link :to="`/etudes/${$route.params.id}/factures/ajouter`">
          <el-button
            icon="el-icon-edit"
            type="primary"
          >
            Ajouter une facture
          </el-button>
        </router-link>
      </el-col>
      <el-col v-show="fss.length > 0">
        <el-button
          type="success"
          icon="el-icon-check"
          @click="levelupTo(8)"
        >
          La FS a été signée
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
const axios = require("axios")
export default {
  name: "FacturesMessages",
  props: {
    etude: { type: Object, required: true },
  },
  computed: {
    fas () { return this.etude.invoices.filter(i => i.invoiceType == "FVA") },
    fis () { return this.etude.invoices.filter(i => i.invoiceType == "FVI") },
    fss () { return this.etude.invoices.filter(i => i.invoiceType == "FVS") }
  },
  methods: {
    levelupTo (new_state) {
      this.loading = true
      axios.put(
        `/api/etudes/${this.etude.id}/`,
        {
          ...this.etude,
          state: new_state,
          prospect: this.etude.prospect.id,
          qualityManager: this.etude.qualityManager.id,
          projectManager: this.etude.projectManager.id,
          clientContact: this.etude.clientContact.id
        },
        { withCredentials: true }
      ).then(() => {
        this.$message({ message: "Étude mise à jour avec succès.", type: "success" })
        this.etude.state = new_state
      }).catch(err => {
        this.$message({ message: "Impossible de mettre à jour l'étude : " + err, type: "error" })
      }).finally(() => {
        this.loading = false
      })
    }
  }
}
</script>

<style scoped>
  .message-alert {
    margin: 1em;
    background: rgba(214, 44, 44, 0.6);
  }
</style>