<template>
  <BaseComponent
    title="Modifier une facture"
    :breadcrumb="breadcrumb"
  >
    <InvoiceForm
      v-model="invoice"
      :loading="loading"
      :prospects="prospects"
      @save="saveInvoice"
    />
  </BaseComponent>
</template>

<script>
import InvoiceForm from "../../components/invoice/InvoiceForm"

const axios = require("axios")

export default {
  name: "InvoiceModify",
  components: {InvoiceForm},
  data () {
    return {
      loading: false,
      invoice: {
        project: this.$route.params.id,
        details: []
      },
      prospects: [],
      breadcrumb: [
        {
          name: "Étude (trésorerie)",
          link: "/etudes"
        },
        {
          name: "<loading>",
          link: `/tresorerie/etudes/${this.$route.params.id}/`
        },
        {
          name: "Modifier une facture"
          // pas la peine d'en mettre : par défaut c'est là où on se trouve.
        }
      ]
    }
  },
  created () {
    this.getInvoice()
    this.getEtude()
  },
  methods: {
    saveInvoice () {
      this.loading = true
      axios.put(
        `/api/tresorerie/factures/${this.$route.params.facture_id}/`,
        this.invoice,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Facture enregistrée", type: "success", offset: 40})
        this.$router.push(`/tresorerie/etudes/${this.$route.params.id}`)
      }).catch((err) => {
        this.$message({message: "Impossible d'enregister la facture : "+err, type: "error", offset: 40})
      }).finally(() => {
        this.loading = false
      })
    },
    getInvoice () {
      axios.get(
        `/api/tresorerie/factures/${this.$route.params.facture_id}`,
        {withCredentials: true}
      ).then((res) => {
        this.invoice = res.data
        axios.get(
          "/api/prospects",
          {withCredentials: true}
        ).then((res) => {
          this.prospects = res.data
          const foundProspect = this.prospects.find((prospect) => prospect.id === this.invoice.payee)
          this.invoice.autocompletePayee = foundProspect ? foundProspect.name : ""
        }).catch((err) => {
          this.$message({message: "Impossible de récupérer la liste des prospects : " + err, type: "error", offset: 40})
        })
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer la facture : " + err, type: "error", offset: 40})
      })
    },
    getProspects () {
      return axios.get(
        "/api/prospects",
        {withCredentials: true}
      )
    },
    getEtude () {
      axios.get(
        `/api/etudes/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then((res) => {
        this.breadcrumb[1].name = res.data.name
      }).catch(() => {
        this.$message({message: "Impossible de récupérer les infos de l'étude", type: "error", offset: 40})
      })
    }
  }
}
</script>

<style>

</style>
