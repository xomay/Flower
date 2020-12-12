<template>
  <BaseComponent
    title="Modification d'un membre"
    :breadcrumb="breadcrumb"
  >
    <MemberForm
      v-model="member"
      :loading="loading"
      @save="saveMember"
    />
  </BaseComponent>
</template>

<script>
import MemberForm from "../components/MemberForm"

const axios = require("axios")

export default {
  name: "EtudeCreer",
  components: {MemberForm},
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
      `/api/membres/${this.$route.params.id}`,
      {withCredentials: true}
    ).then((res) => {
      this.member = res.data
      this.breadcrumb[1].name = `${this.member.firstname} ${this.member.lastname}`
    }).
      catch((err) => {
        this.$message({message: err,
          type: "error"})
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
        this.$message({message: "Le membre a bien été enregistré",
          type: "success"})
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    }
  }
}
</script>

<style>

</style>
