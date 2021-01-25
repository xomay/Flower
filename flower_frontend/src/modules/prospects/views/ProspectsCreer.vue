<template>
  <BaseComponent
    title="Ajout d'un prospect"
    :breadcrumb="breadcrumb"
  >
    <ProspectsForm
      v-model="prospect"
      :loading="loading"
      @save="registerProspect"
    />
  </BaseComponent>
</template>

<script>
import ProspectsForm from "../components/ProspectsForm"
const axios = require("axios")

export default {
  name: "ProspectsCreer",
  components: {ProspectsForm},
  data () {
    return {
      prospect: {},
      loading: false,
      breadcrumb: [
        {
          name: "Liste des prospects",
          link: "/prospects"
        },
        {
          name: "Ajouter un prospect",
          link: "/prospects/ajouter"
        }
      ]
    }
  },
  created () {
    this.getAllContactWays()
  },
  methods: {
    registerProspect (contactsList) {
      this.loading = true
      this.verifContacts(contactsList)
      axios.post(
        "/api/prospects/",
        this.prospect,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le prospect a bien été ajouté",
          type: "success"})
        this.$router.push("/prospects")
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    },
    getAllContactWays () {
      this.loading = true
      axios.get(
        "/api/contactway/",
        {withCredentials: true}
      ).then((res) => {
        this.contactsWays = res.data
      }).
        catch((err) => {
          this.$message({message: "Erreur lors de la récupération des contactways : "+err,
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    },
    verifContacts (contactList) {
      this.prospect.contactWay = []
      contactList.forEach(contact => {
        var contactObject = this.contactsWays.find(c => c.contactWay === contact)
        if(contactObject == undefined) {
          // non trouvé
          contactObject = this.createContact(contact)
        }
        if(contactObject != undefined) {
          this.prospect.contactWay.push(contactObject.id)
        }
      })
    },
    createContact (content) {
      const newObject = {
        contactWay: content
      }
      axios.post(
        "/api/contactway/",
        newObject,
        {withCredentials: true}
      ).then((res) => {
        return res.data
      }).
        catch((err) => {
          this.$message({message: "Impossible d'ajouter un contactway :"+err,
            type: "error"})
          return undefined
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
