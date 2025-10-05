<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
  >
    <MemberForm
      v-model="member"
      :postes="postes"
      :loading="loading"
      :can-open-account="isAdmin()"
      :deletable="true"
      @deleted="this.isAdmin()"
      @save="saveMember"
    />
  </BaseComponent>
</template>

<script>
import MemberForm from "../components/MemberForm"
import { registerMemberMixin } from "../mixins/RegisterMember.js"
import { Permissions } from "@/mixins/Permissions"

const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.withCredentials = true

export default {
  name: "MembresModifier",
  components: {MemberForm},
  mixins: [registerMemberMixin, Permissions],
  data () {
    return {
      title: "Modifier : <loading>",
      member: {
        firstname: "",
        lastname: "",
        gender: "",
        poste: 0,
        promotion: 2025,
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
      "/api/administration/postes/",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.postes = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les postes : "+ err, type: "error"})
    })
  },
  created () {
    axios.get(
      `/api/membres/${this.$route.params.id}`,
      {withCredentials: true}
    ).then((res) => {
      this.member = res.data
      if(this.member.poste != undefined)
        this.member.poste = this.member.poste.id
      this.title = `Modifier : ${this.member.firstname} ${this.member.lastname}`
      this.breadcrumb[1].name = `${this.member.firstname} ${this.member.lastname}`
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le membre : "+ err, type: "error"})
    })
  },
  methods: {
    deleted () {
      this.loading = true
      axios.delete(
        `/api/membres/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le membre a bien été supprimé.", type: "success"})
        this.$router.push("/membres")
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer le membre : "+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
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
  }
}
</script>
