<template>
  <BaseComponent
    title="Ajout d'un membre"
    :breadcrumb="breadcrumb"
  >
    <MemberForm
      v-model="form"
      :loading="loading"
      @save="registerMember"
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
      form: {
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
          link: "/membres/ajouter"
        }
      ]
    }
  },
  methods: {
    registerMember () {
      this.loading = true
      axios.post(
        "/api/membres/",
        this.form,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le membre a bien été ajouté",
          type: "success"})
        this.$router.push("/membres")
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
