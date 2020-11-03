<template>
  <BaseComponent :title="'Ajouter une facture'">
    <InvoiceForm
      v-model="invoice"
      :loading="loading"
      :prospects="prospects"
      :errors="errors"
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
        details: []
      },
      errors: {},
      prospects: this.getProspects()
    }
  },
  methods: {
    createInvoice () {
      this.loading = true
      this.errors = {}
      axios.post(
        `${this.$server_url}/tresorerie/factures/`,
        this.invoice,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Facture créée.",
          type: "success",
          offset: 40})
        this.$router.push(`/etudes/${this.route.params.id}/voir?active=Rédaction`)
      }).
        catch((err) => {
          this.errors = err.response.data
        }).
        finally(() => {
          this.loading = false
        })
    },
    getProspects () {
      axios.get(
        `${this.$server_url}/prospects`,
        {withCredentials: true}
      ).then((res) => {
        this.prospects = res.data
      }).
        catch(() => {
          this.$message({message: "Impossible de récupérer la liste des prospects",
            type: "error",
            offset: 40})
        })
    }
  }
}
</script>

<style>

</style>
