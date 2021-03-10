<template>
  <BaseComponent
    title="Modification d'un membre"
    :breadcrumb="breadcrumb"
  >
    <MemberForm
      v-model="member"
      :postes="postes"
      :loading="loading"
      :loadingopenaccount="loadingOpenAccount"
      :can-open-account="isAdmin()"
      @save="saveMember"
      @openaccount="openAccount"
    />
  </BaseComponent>
</template>

<script>
import MemberForm from "../components/MemberForm"
import { registerMemberMixin } from "../mixins/RegisterMember.js"
import { Permissions } from "@/mixins/Permissions"

const axios = require("axios")

export default {
  name: "EtudeCreer",
  components: {MemberForm},
  mixins: [registerMemberMixin, Permissions],
  data () {
    return {
      member: {
        firstname: "",
        lastname: "",
        gender: "",
        promotion: "2021",
        email: "",
        email_junior: "",
        mobile: "",
        address: "",
        postcode: "",
        town: "",
        country: "",
        nationality: "",
        birth_date: "",
        birth_place: ""
      },
      postes: [],
      loading: false,
      loadingOpenAccount: false,
      breadcrumb: [
        {
          name: "Liste des membres",
          link: "/membres"
        },
        {
          name: "Ajouter un membre",
          link: `/membres/${this.$route.params.id}/voir`
        },
        {
          name: "Modifier",
          link: `/membres/${this.$route.params.id}/modifier`
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
      if(this.member.poste != undefined)
        this.member.poste = this.member.poste.id
      this.breadcrumb[1].name = `${this.member.firstname} ${this.member.lastname}`
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le membre : "+ err, type: "error"})
    })
    axios.get(
      "/api/administration/postes/",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.postes = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les postes : "+ err, type: "error"})
    })
  },
  methods: {
    saveMember () {
      this.loading = true
      axios.put(
        `/api/membres/${this.member.id}/`,
        this.member,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le membre a bien été enregistré", type: "success"})
        this.$router.push(`/membres/${this.member.id}/voir`)
      }).catch((err) => {
        this.$message({message: "Erreur lors de l'enregistrement : "+err,type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    openAccount () {
      this.loadingOpenAccount = true
      this.mixinRegisterMember(axios, this.member)
      this.loadingOpenAccount = false
    }
  }
}
</script>
