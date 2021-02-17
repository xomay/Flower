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
          name: "Suivi d'étude",
          link: "/etudes"
        },
        {
          name: "<loading>",
          link: `/etudes/${this.$route.params.id}/voir?active=Rédaction`
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
        this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Rédaction`)
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
        //console.log(this.invoice)
        this.getProspects().then((res) => {
          this.prospects = res.data
          this.$set(
            this.invoice,
            "autocompletePayee",
            this.prospects.find((prospect) => prospect.id === this.invoice.payee).name
          )
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
        this.$message({message: "Impossible de récupérer la liste des prospects", type: "error", offset: 40})
      })
    }
  }
}
</script>

<style>

</style>
