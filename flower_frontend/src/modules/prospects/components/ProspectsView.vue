<template>
  <div>
    <span>Prospect : {{ prospect.name }}</span><br>
    <span>Adresse : {{ prospect.address }}</span><br>
    <span>Code postal : {{ prospect.postcode }}</span><br>
    <span>Ville : {{ prospect.town }}</span><br>
  </div>
</template>

<script>
export default {
  name: "ProspectView",
  props: {
    prospect: {
      type: Object,
      required: true
    }
  }
}
</script>

<style>

</style>
