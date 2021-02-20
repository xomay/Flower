<template>
  <BaseComponent
    title="Facture - Choix de l'étude"
    :breadcrumb="breadcrumb"
  >
    soon
  </BaseComponent>
</template>

<script>
export default {
  name: "FactureSelectEtude",
  data () {
    return {
      breadcrumb: [
        {
          name: "Factures",
          link: "tresorerie/factures"
        }
      ]
    }
  }
}
</script>