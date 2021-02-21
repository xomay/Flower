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
        title="Devis"
        description="Devis rédigé et envoyé"
      />
      <el-step
        title="CE"
        description="Convention d'Étude rédigée et envoyée"
      />
      <el-step
        title="RDM"
        description="Revelé De Mission rédigé et envoyé"
      />
      <el-step
        title="FA"
        description="Facture d'accompte payéee"
      />
      <el-step
        title="PVRI"
        description="PVR rédigée et envoyée"
      />
      <el-step
        title="FI"
        description="Facture intermédiaire payée"
      />
      <el-step
        title="PVRF"
        description="PVR Final rédigé et envoyé"
      />
      <el-step
        title="FS"
        description="Facture de solde payée"
      />
      <el-step
        title="Péda"
        description="Rapport péda rendu par le réa"
      />
      <el-step
        title="BV"
        description="Buletin de versement"
      />
    </el-steps>
  </el-row>
</template>

<script>
export default {
  name: "EtudeSteps",
  props: {
    etude: { type: Object, required: true }
  },
  methods: {
    getCurrentEtudeStep () {
      return this.etude.state
    }
  }
}
</script>