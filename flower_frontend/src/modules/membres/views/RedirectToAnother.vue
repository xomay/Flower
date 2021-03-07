<!--
  Cette classe ne sert qu'à rediriger le push d'une vue MembresDetail à un autre. En effet, sinon on reste dans le même type de vue.
  Car si l'URL s'update bien, ce n'est pas le cas du renderer qui reste à l'ancien.
-->

<template>
  <div>
    Loading
  </div>
</template>

<script>
export default {
  name: "RedirectToAnother",
  created () {
    this.$router.push(`/membres/${this.$route.params.id}/voir`)
  }
}
</script>