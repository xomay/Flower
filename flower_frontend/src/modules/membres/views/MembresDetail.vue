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
    <span><i class="el-icon-school" /> Promotion {{ member.promotion }}</span><br>
    <span><i class="el-icon-message" /> {{ member.email }}</span><br>
    <span><i class="el-icon-message" /> {{ member.email_junior }}</span><br>
    <span><i class="el-icon-mobile-phone" /> {{ member.mobile }}</span><br>
    <span><i class="el-icon-location-outline" /> {{ member.address }} à {{ member.town }} {{ member.postcode }}</span><br>
    <span><i class="el-icon-place" /> {{ member.country }}</span><br>
    <span><i class="el-icon-wallet" /> {{ member.nationality }}</span><br>
    <span><i class="el-icon-present" /> Né(e) le {{ member.birth_date }} à {{ member.birth_place }}</span><br>
  </BaseComponent>
</template>

<script>
const axios = require("axios")

export default {
  name: "EtudeDetail",
  data () {
    return {
      member: {},
      breadcrumb: [
        {
          name: "Lister des membres",
          link: "/membres"
        },
        {
          name: "",
          link: "/membres/ajouter"
        }
      ]
    }
  },
  created () {
    this.getMember()
  },
  methods: {
    getMember () {
      this.loading = true
      axios.get(
        `${this.$server_url}/membres/${this.$route.params.id}`,
        {withCredentials: true}
      ).then((res) => {
        this.member = res.data
        this.breadcrumb[1].name = `${this.member.firstname} ${this.member.lastname}`
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        })
    }
  }
}
</script>

<style>

</style>
