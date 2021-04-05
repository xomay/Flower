<template>
  <tr>
    <td class="tg-y6fn">
      {{ title }}
    </td>
    <td class="tg-lqy6">
      <b>{{ (cotisation.montant_base).toFixed(2) }} €</b>
    </td>
    <td class="tg-baqh">
      <el-input-number
        v-model="cotisation.taux_junior"
        :precision="4"
        :step="0.0001"
        :min="0"
        :max="1"
        controls-position="right"
      />
    </td>
    <td class="tg-c3ow">
      {{ cotisation.taux_junior > 0 ? (cotisation.montant_base * cotisation.taux_junior).toFixed(2)+" €" : "-" }}
    </td>
    <td class="tg-c3ow">
      <el-input-number
        v-model="cotisation.taux_realisateur"
        :precision="4"
        :step="0.0001"
        :min="0"
        :max="1"
        controls-position="right"
      />
    </td>
    <td class="tg-c3ow">
      {{ cotisation.taux_realisateur > 0 ? (cotisation.montant_base * cotisation.taux_realisateur).toFixed(2)+" €" : "-" }}
    </td>
  </tr>
</template>

<script>
export default {
  name: "BVCotisationLine",
  props: {
    title: { type: String, required: true },
    cotisation: { type: Object, required: true }
  }
}
</script>
