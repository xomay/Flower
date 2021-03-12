<template>
  <BaseComponent
    title="Affichage d'un membre"
    :breadcrumb="breadcrumb"
  >
    <template v-slot:action>
      <router-link :to="`/membres/${$route.params.id}/modifier`">
        <el-button
          type="text"
          icon="el-icon-edit"
        >
          Modifier
        </el-button>
      </router-link>
    </template>
    <span><span v-if="member.gender !== ''">{{ member.gender }}</span>  {{ member.firstname }} {{ member.lastname }}</span><br>
    <span v-if="member.poste !== null && member.poste != undefined"><i class="el-icon-monitor" /> Poste : {{ member.poste.name }}</span><br>
    <span><i class="el-icon-school" /> Promotion {{ member.promotion }}</span><br>
    <span><i class="el-icon-message" /> {{ member.email }}</span><br>
    <span><i class="el-icon-message" /> {{ member.email_junior }}</span><br>
    <span><i class="el-icon-mobile-phone" /> {{ member.mobile }}</span><br>
    <span><i class="el-icon-location-outline" /> {{ member.address }} à {{ member.town }} {{ member.postcode }}</span><br>
    <span><i class="el-icon-place" /> {{ member.country }}</span><br>
    <span><i class="el-icon-wallet" /> {{ member.nationality }}</span><br>
    <span><i class="el-icon-present" /> Né(e) le {{ member.birth_date }} à {{ member.birth_place }}</span><br>
    <br>
    <div v-if="subordinates.length > 0">
      Liste des subordonnés :
      <div
        v-for="sub in subordinates"
        :key="sub.id"
      >
        - <el-button
          type="text"
          size="small"
          @click="pushToSubordinate(sub.id)"
        >
          {{ nicePeople(sub) }}
        </el-button>
        ( {{ sub.poste }} )
      </div>
    </div>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import Utils from "@/mixins/Utils"
export default {
  name: "EtudeDetail",
  mixins: [Utils],
  data () {
    return {
      member: {},
      subordinates: [],
      breadcrumb: [
        {
          name: "Lister des membres",
          link: "/membres"
        },
        {
          name: "<loading>",
          link: `/membres/${this.$route.params.id}/voir`
        }
      ]
    }
  },
  beforeCreate () {
    axios.get(
      `/api/membres/${this.$route.params.id}`,
      {withCredentials: true}
    ).then((res) => {
      this.member = res.data
      this.breadcrumb[1].name = `${this.member.firstname} ${this.member.lastname}`
      // Chargement des subordonnés :
      if(this.member.poste != undefined) {
        const subs = this.member.poste.subordinates
        axios.get(
          "/api/membres/",
          {withCredentials: true}
        ).then((res) => {
          this.subordinates = res.data.filter((m) => m.poste != undefined && subs.indexOf(m.poste.id) >= 0)
          this.subordinates.forEach(m => m.poste = (m.gender == "M." ? m.poste.name : m.poste.name_feminine))
        }).catch((err) => {
          this.$message({message: "Impossible de récupérer les autres membres : " + err, type: "error"})
        })
      }
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le membre : " + err, type: "error"})
    })
  },
  methods: {
    pushToSubordinate (sub_id) {
      this.$router.push(`/membres/${sub_id}/redirect`)
    }
  }
}
</script>
