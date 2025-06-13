<template>
  <div>
    <span><el-icon><UserFilled/></el-icon> Nom : {{ prospect.name }}</span><br>
    <span><el-icon><Location/></el-icon> Adresse : {{ prospect.address }}; {{ prospect.postcode }}, {{ prospect.town }}</span><br>
    <span><el-icon><Document/></el-icon> Type d'entreprise : {{ prospect.type }}</span><br>
    <span><el-icon><PieChart/></el-icon> Domaine : {{ prospect.domain }}</span><br>
    <div v-if="prospect.address_tresorerie != null && prospect.address_tresorerie != ''">
      <span><el-icon><Location/></el-icon> Adresse de trésorerie : {{ prospect.address_tresorerie }}</span><br><br>
    </div>
    <span v-show="displayCharge">
      <el-icon><User/></el-icon> Chargé dev'co :
      <el-link
        type="primary"
        :style="'margin-left: 12px'"
        @click="$router.push('/membres/'+prospect.charge+'/voir')"
      >
        {{ chargeName }}
      </el-link>
    </span><br><br>
    <p v-if="prospect.advancement === 'AR'">
      <el-icon><View/></el-icon> <u>Dernier contact :</u> {{ niceDate (prospect.nextDate) }}
    </p>
    <p v-if="prospect.advancement === 'RDV'">
      <el-icon><Date/></el-icon> <u>Date du rendez-vous :</u> {{ niceDate (prospect.nextDate) }}
    </p>
    <p v-if="prospect.advancement === 'DS'">
      <el-icon><Date/></el-icon> <u>Deadline du devis :</u> {{ niceDate (prospect.nextDate) }}
    </p>
    <span
      v-if="prospect.contactWay && prospect.contactWay.length > 0"
    >
      <el-icon><Service/></el-icon> Moyens de contact :
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
