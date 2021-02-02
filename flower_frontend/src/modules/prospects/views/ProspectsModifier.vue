<template>
  <div>
    <BaseComponent
      title="Modification d'un prospect"
      :breadcrumb="breadcrumb"
    >
      <ProspectsForm
        v-model="prospect"
        :loading="false"
        :deletable="true"
        :all-contacts="contactsWays"
        @save="updateProspect"
        @delete="deleteProspect"
      />
    </BaseComponent>
  </div>
</template>

<script>
import ProspectsForm from "../components/ProspectsForm"
const axios = require("axios")

export default {
  name: "ProspectsModifier",
  components: {ProspectsForm},
  data () {
    return {
      prospect: {},
      contactsWays: [],
      employes: [],
      loading: false,
      breadcrumb: [
        {
          name: "Lister des prospects",
          link: "/prospects"
        },
        {
          name: "",
          link: `/prospects/${this.$route.params.id}/voir`
        },
        {
          name: "Modifier",
          link: `/prospects/${this.$route.params.id}/modifier`
        }
      ]
    }
  },
  created () {
    this.getProspect()
    this.getEmployes()
    this.getAllContactWays()
  },
  methods: {
    getProspect () {
      axios.get(
        `/api/prospects/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then((res) => {
        this.prospect = res.data
        this.breadcrumb[1].name = this.prospect.name
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        })
    },
    updateProspect (contactsList) {
      this.loading = true
      this.verifContacts(contactsList).then((result) => {
        result.forEach(contact_o => {
          this.prospect.contactWay.push(contact_o.id)
        })
        axios.put(
          `/api/prospects/${this.$route.params.id}/`,
          this.prospect,
          {withCredentials: true}
        ).then(() => {
          this.$message({message: "Le prospect a bien été mis à jour", type: "success"})
        }).catch((err) => {
          this.$message({message: err, type: "error"})
        }).finally(() => {
          this.loading = false
        })
      })
    },
    verifContacts (contactList) {
      this.prospect.contactWay = []
      return Promise.all(contactList.map(contact => {
        const contactObject = this.contactsWays.find(c => c.contactWay === contact)
        if(contactObject == undefined) {
          return this.createContact(contact)
        } else {
          return new Promise((resolve) => resolve(contactObject.id))
        }
      }))
    },
    deleteProspect () {
      axios.delete(
        `/api/prospects/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le prospect a bien été retiré",
          type: "success"})
        this.$router.push("/prospects")
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        })
    },
    getEmployes () {
      axios.get(
        `/api/prospects/${this.$route.params.id}/employes/`,
        {withCredentials: true}
      ).then((res) => {
        this.employes = res.data
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
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
    createContact (content) {
      return new Promise( (resolve, reject) => {
        axios.post(
          "/api/contactway/",
          { contactWay: content},
          {withCredentials: true}
        ).then((res) => {
          resolve(res.data)
        }).catch((err) => {
          this.$message({message: "Impossible d'ajouter un contactway :"+err,type: "error"})
          reject(err)
        }).finally(() => {
          this.loading = false
        })
      })
    }
  }
}
</script>

<style>

</style>
