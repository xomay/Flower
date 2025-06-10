<template>
  <el-row>
    <el-steps
      :active="getCurrentEtudeStep()"
      style="margin-bottom: 30px; margin-top: 30px;"
      process-status="finish"
      finish-status="success"
      align-center
    >
      <el-step
        title="PC"
        :description="descriptions ? 'Proposition Commerciale rédigé et envoyé' : ''"
      />
      <el-step
        :title="etude.hasCC ? 'BC' : 'CE'"
        :description="descriptions ? 
        etude.hasCC ? 'Bon de Commande rédigé et envoyé' : 'Convention d\'Étude rédigée et envoyée' : 
        ''"
      />
      <el-step
        title="RDM"
        :description="descriptions ? 'Récapitulatif De Mission rédigé et envoyé' : ''"
      />
      <el-step
        title="FA"
        :description="descriptions ? 'Facture d\'accompte payéee' : ''"
      />
      <el-step
        title="PVRI"
        :description="descriptions ? 'PVR rédigée et envoyée' : ''"
      />
      <el-step
        title="FI"
        :description="descriptions ? 'Facture intermédiaire payée' : ''"
      />
      <el-step
        title="PVRF"
        :description="descriptions ? 'PVR Final rédigé et envoyé' : ''"
      />
      <el-step
        title="FS"
        :description="descriptions ? 'Facture de solde payée' : ''"
      />
      <el-step
        title="Péda"
        :description="descriptions ? 'Rapports péda rendu par les réas' : ''"
      />
      <el-step
        title="BV"
        :description="descriptions ? 'Buletin de versement' : ''"
      />
    </el-steps>
  </el-row>
</template>

<script>
export default {
  name: "EtudeSteps",
  props: {
    etude: { type: Object, required: true },
    descriptions: { type: Boolean, default: true }
  },
  methods: {
    getCurrentEtudeStep () {
      return this.etude.state
    }
  }
}
</script>