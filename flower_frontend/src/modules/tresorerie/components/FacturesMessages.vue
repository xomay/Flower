<template>
  <div>
    <!-- (3) : FA -->
    <el-row v-show="etude.state == 3">
      <el-alert
        title="Valider la FA"
        type="warning"
        description="Vous devez signer la FA !"
        :closable="false"
        center
        effect="dark"
        show-icon
      />
      <el-col v-show="fas.length == 0" align="center">
        <el-alert
          title="Il n'existe aucune Facture d'Accompte."
          type="error"
          description=""
          :closable="false"
          center
          effect="dark"
          show-icon
          style="margin-top: 10px;"
        />
        <router-link :to="`/etudes/${$route.params.id}/factures/ajouter`">
          <el-button
            icon="Edit"
            type="primary"
            style="margin: 10px auto;"
          >
            Ajouter une facture
          </el-button>
        </router-link>
      </el-col>
      <el-col v-show="fas.length > 0" align="center">
        <el-button
          type="success"
          icon="Check"
          style="margin: 10px auto;"
          @click="levelupTo(4)"
        >
          La FA a été signée
        </el-button>
      </el-col>
    </el-row>
    <!-- (5) : FI -->
    <el-row v-show="etude.state == 5">
      <el-alert
        title="Valider la FI"
        type="warning"
        description="Vous devez signer la FI !"
        :closable="false"
        center
        effect="dark"
        show-icon
      />
      <el-col v-show="fis.length == 0" align="center">
        <el-alert
          title="Il n'existe aucune Facture Intermédiaire."
          type="error"
          description=""
          :closable="false"
          center
          effect="dark"
          show-icon
          style="margin-top: 10px;"
        />
        <router-link :to="`/etudes/${$route.params.id}/factures/ajouter`">
          <el-button
            icon="Edit"
            type="primary"
            style="margin: 10px auto;"
          >
            Ajouter une facture
          </el-button>
        </router-link>
      </el-col>
      <el-col v-show="fis.length > 0" align="center">
        <el-button
          type="success"
          icon="Check"
          style="margin: 10px auto;"
          @click="levelupTo(6)"
        >
          La FI a été signée
        </el-button>
      </el-col>
    </el-row>
    <!-- (7) : FS -->
    <el-row v-show="etude.state == 7">
      <el-alert
        title="Valider la FS"
        type="warning"
        description="Vous devez signer la FS !"
        :closable="false"
        center
        effect="dark"
        show-icon
      />
      <el-col v-show="fss.length == 0" align="center">
        <el-alert
          title="Il n'existe aucune Facture de Solde."
          type="error"
          description=""
          :closable="false"
          center
          effect="dark"
          show-icon
          style="margin-top: 10px;"
        />
        <router-link :to="`/etudes/${$route.params.id}/factures/ajouter`">
          <el-button
            icon="Edit"
            type="primary"
            style="margin: 10px auto;"
          >
            Ajouter une facture
          </el-button>
        </router-link>
      </el-col>
      <el-col v-show="fss.length > 0" align="center">
        <el-button
          type="success"
          icon="Check"
          style="margin: 10px auto;"
          @click="levelupTo(8)"
        >
          La FS a été signée
        </el-button>
      </el-col>
    </el-row>
    <!-- (9) : BV -->
    <el-row v-show="etude.state == 9">
      <el-alert
        title="Valider les BV"
        type="warning"
        description="Vous devez valider les BV !"
        :closable="false"
        center
        effect="dark"
        show-icon
      />
      <el-button
        v-show="etude.bvData.full"
        type="success"
        icon="Check"
        style="margin: 10px 40%; width: 20%;"
        @click="levelupTo(10)"
      >
        Les BV ont été signés
      </el-button>
      <el-alert
        v-show=" ! etude.bvData.full"
        title="Tous les BV n'existent pas encore."
        type="error"
        description="Ajouter les BV pour les phases manquantes dans le tableau juste au dessus !"
        center
        :closable="false"
        effect="dark"
        show-icon
      />
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
    fas () { return this.etude.invoices.filter(i => i.invoiceType == "SU") },
    fis () { return this.etude.invoices.filter(i => i.invoiceType == "I") },
    fss () { return this.etude.invoices.filter(i => i.invoiceType == "S") }
  },
  methods: {
    levelupTo (new_state) {
      this.loading = true
      this.etude.docEtude = this.etude.docEtude.id
      axios.put(
        `/api/etudes/${this.etude.id}/`,
        {
          ...this.etude,
          state: new_state,
          prospect: this.etude.prospect.id,
          qualityManager: this.etude.qualityManager.id,
          projectManager: this.etude.projectManager.id,
          clientContact: this.etude.clientContact.id,
          linkedFiles: this.etude.linkedFiles.map(lf => lf.id)
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