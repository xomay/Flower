<template>
  <BaseComponent
    title="Ajouter une facture"
    :breadcrumb="breadcrumb"
  >
    <InvoiceForm
      v-model="invoice"
      :loading="loading"
      :prospects="prospects"
      @save="createInvoice"
    />
  </BaseComponent>
</template>

<script>
import InvoiceForm from "../../components/invoice/InvoiceForm"

const axios = require("axios")

export default {
  name: "InvoiceCreate",
  components: {InvoiceForm},
  data () {
    return {
      loading: false,
      invoice: {
        project: this.$route.params.id,
        accountingPeriod: 2021,
        invoiceNumber: "",
        invoiceType: "",
        issueDate: "",
        paymentDate: "",
        description: "",
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
          name: "Ajouter une facture",
          link: `/etudes/${this.$route.params.id}/factures/ajouter`
        }
      ]
    }
  },
  created () {
    this.getProspects()
    this.getEtude()
  },
  methods: {
    createInvoice () {
      this.loading = true
      axios.post(
        "/api/tresorerie/factures/",
        this.invoice,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Facture créée avec succès.", type: "success", offset: 40})
        this.$router.push(`/tresorerie/etudes/${this.$route.params.id}`)
      }).catch((err) => {
        this.$message({message: "Impossible de créer la facture : " + err, type: "error", offset: 40})
      }).finally(() => {
        this.loading = false
      })
    },
    getProspects () {
      axios.get(
        "/api/prospects",
        {withCredentials: true}
      ).then((res) => {
        this.prospects = res.data
      }).catch(() => {
        this.$message({message: "Impossible de récupérer la liste des prospects", type: "error", offset: 40})
      })
    },
    getEtude () {
      axios.get(
        `/api/etudes/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then((res) => {
        this.breadcrumb[1].name = res.data.name
      }).catch(() => {
        this.$message({message: "Impossible de récupérer la liste des prospects", type: "error", offset: 40})
      })
    }
  }
}
</script>
