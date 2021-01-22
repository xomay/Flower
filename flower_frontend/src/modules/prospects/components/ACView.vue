<template>
  <div>
    <span>Nom de l'action : {{ actionCommerciale.name }}</span><br>
  </div>
</template>

<script>
export default {
  name: "ACView",
  props: {
    actionCommerciale: {
      type: Object,
      required: true
    }
  }
}
</script>

<style>

</style>
