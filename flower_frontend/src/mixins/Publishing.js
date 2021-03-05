const axios = require("axios")
export default {
  methods: {
    createDownloadElement (data, filename) {
      let fileURL = window.URL.createObjectURL(new Blob([data]))
      let fileLink = document.createElement("a")
      fileLink.href = fileURL
      fileLink.setAttribute("download", filename)
      document.body.appendChild(fileLink)
      fileLink.click()
    },
    // DOWNLOAD
    downloadDevis () {
      this.loading = true
      axios.get(`/api/publish/etude/${this.etude.id}/devis/`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, "DEVIS-" + this.etude.name + ".docx")
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération du devis : " + err, type: "error" })
      }).finally(() => {
        this.loading = false
      })
    },
    downloadCE () {
      this.loading = true
      axios.get(`/api/publish/etude/${this.etude.id}/ce/`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, "CE-" + this.etude.name + ".docx")
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération du devis : " + err, type: "error" })
      }).finally(() => {
        this.loading = false
      })
    },
    downloadRDM (rdmId) {
      this.loading = true
      axios.get(`/api/publish/rdm/${rdmId}`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, "RDM-" + this.etude.name + ".docx")
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération du RDM : " + err, type: "error" })
      }).finally(() => {
        this.loading = false
      })
    },
    downloadPVR (pvrId) {
      this.loading = true
      axios.get(`/api/publish/pvr/${pvrId}`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, "PVR-" + this.etude.name + ".docx")
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération du PVR : " + err, type: "error" })
      }).finally(() => {
        this.loading = false
      })
    },
    downloadInvoice (invoiceId) {
      this.loading = true
      axios.get(`/api/publish/facture/${invoiceId}`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, "FA-" + this.etude.name + ".docx")
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération de la facture : " + err, type: "error" })
      }).finally(() => {
        this.loading = false
      })
    },
    // DELETE
    deletePVR (pvrId, index) {
      this.loading = true
      axios.delete(`/api/pvr/${pvrId}`, { withCredentials: true }).then(() => {
        this.etude.pvr.splice(index, 1)
      }).catch(err => {
        this.$message({ message: err, type: "error", offset: 40 })
      }).finally(() => {
        this.loading = false
      })
    },
  }
}