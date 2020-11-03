<template>
  <div>
    <span>Nom : {{ employe.gender }} {{ employe.firstname }} {{ employe.lastname }}</span><br>
    <span>Email : {{ employe.email }}</span><br>
    <span>Mobile : {{ employe.mobile }}</span><br>
    <span>Poste : {{ employe.position }}</span><br>
  </div>
</template>

<script>
export default {
  name: "EmployesView",
  props: {
    employe: { type: Object, required: true }
  }
}
</script>

<style>

</style>
