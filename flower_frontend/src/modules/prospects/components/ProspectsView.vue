<template>
  <div>
    <span>Nom : {{ prospect.name }}</span><br>
    <span>Adresse : {{ prospect.address }}</span><br>
    <span>Code postal : {{ prospect.postcode }}</span><br>
    <span>Ville : {{ prospect.town }}</span><br><br>
    <span
      v-if="prospect.contactWay"
    >
      <u>Moyens de contact :</u>
      <ul>
        <li
          v-for="item in prospect.contactWay"
          :key="item"
          class="liPrView"
        >
          {{ item }}
        </li>
      </ul>
    </span>
  </div>
</template>

<script>
export default {
  name: "ProspectView",
  props: {
    prospect: { type: Object, required: true }
  }
}
</script>

<style scoped>
  .liPrView {
    list-style-type: square;
    margin-left: 40px
  }
</style>
