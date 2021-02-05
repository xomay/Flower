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
          {{ getContact(item) }}
        </li>
      </ul>
    </span>
  </div>
</template>

<script>
export default {
  name: "ProspectView",
  props: {
    prospect: { type: Object, required: true },
    contacts: { type: Array, required: true }
  },
  methods: {
    getContact (id) {
      const found = this.contacts.find(c => c.id === id)
      return found != undefined ? found.contactWay : "<loading>"
    }
  }
}
</script>

<style scoped>
  .liPrView {
    list-style-type: square;
    margin-left: 40px
  }
</style>
