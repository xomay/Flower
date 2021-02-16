<template>
  <div>
    <span><i class="el-icon-user-solid" />Nom : {{ prospect.name }}</span><br>
    <span><i class="el-icon-location" />Adresse : {{ prospect.address }}; {{ prospect.postcode }}, {{ prospect.town }}</span><br><br>
    <span v-if="prospect.charge">
      <i class="el-icon-user" /> Chargé dev'co :
      <el-link
        type="primary"
        :style="'margin-left: 12px'"
        @click="$router.push('/membres/'+prospect.charge+'/voir')"
      >
        {{ chargeName }}
      </el-link>
    </span><br><br>
    <span
      v-if="prospect.contactWay && prospect.contactWay.length > 0"
    >
      <i class="el-icon-service" /> Moyens de contact :
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
const axios = require("axios")

export default {
  name: "ProspectView",
  props: {
    prospect: { type: Object, required: true }
  },
  data () {
    return {
      chargeName: ""
    }
  },
  watch: {
    prospect (nv) {
      axios.get(
        `/api/membres/${nv.charge}/`,
        {withCredentials: true}
      ).then((res) => {
        this.chargeName = res.data.firstname + " " + res.data.lastname
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer le dev'co : "+err, type: "error", offset: 40})
      })
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
