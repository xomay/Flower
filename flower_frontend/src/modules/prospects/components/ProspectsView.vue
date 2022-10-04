<template>
  <div>
    <span><i class="el-icon-user-solid" /> Nom : {{ prospect.name }}</span><br>
    <span><i class="el-icon-location" /> Adresse : {{ prospect.address }}; {{ prospect.postcode }}, {{ prospect.town }}</span><br>
    <span><i class="el-icon-doc-text" /> Type d'entreprise : {{ prospect.type }}</span><br>
    <span><i class="el-icon-chart-pie" /> Domaine : {{ prospect.domain }}</span><br>
    <div v-if="prospect.address_tresorerie != null && prospect.address_tresorerie != ''">
      <span><i class="el-icon-location" /> Adresse de trésorerie : {{ prospect.address_tresorerie }}</span><br><br>
    </div>
    <span v-show="displayCharge">
      <i class="el-icon-user" /> Chargé dev'co :
      <el-link
        type="primary"
        :style="'margin-left: 12px'"
        @click="$router.push('/membres/'+prospect.charge+'/voir')"
      >
        {{ chargeName }}
      </el-link>
    </span><br><br>
    <p v-if="prospect.advancement === 'AR'">
      <i class="el-icon-view" /> <u>Dernier contact :</u> {{ niceDate (prospect.nextDate) }}
    </p>
    <p v-if="prospect.advancement === 'RDV'">
      <i class="el-icon-date" /> <u>Date du rendez-vous :</u> {{ niceDate (prospect.nextDate) }}
    </p>
    <p v-if="prospect.advancement === 'DS'">
      <i class="el-icon-date" /> <u>Deadline du devis :</u> {{ niceDate (prospect.nextDate) }}
    </p>
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
      chargeName: "",
      displayCharge: false
    }
  },
  watch: {
    prospect (nv) {
      if(nv.charge != null && nv.charge != undefined && nv.charge > 0) {
        axios.get(
          `/api/membres/${nv.charge}/`,
          {withCredentials: true}
        ).then((res) => {
          this.chargeName = res.data.firstname + " " + res.data.lastname
          this.displayCharge = true
        }).catch((err) => {
          this.$message({message: "Impossible de récupérer le dev'co : "+err, type: "error", offset: 40})
        })
      }
    }
  },
  methods: {
    niceDate (dateString) {
      if(dateString == undefined || dateString == null) {
        return "non défini."
      } else {
        const tokens = dateString.split("-")
        return tokens[2] + "/" + tokens[1] + "/" + tokens[0]
      }
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
