const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;
export default {
  methods: {
    calculateDates () {
      const formatDate = (date) => {
        if (!(date instanceof Date)) date = new Date(date)
        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const day = String(date.getDate()).padStart(2, '0')
        return `${year}-${month}-${day}`
      }
      const sortedPhases = [...this.etude.phases].sort((a, b) => a.index - b.index)
      
      for (let i = 0; i < sortedPhases.length; i++) {
        const phase = sortedPhases[i]
        if (i === 0) {
          if (!phase.beginDate || isNaN(new Date(phase.beginDate))) continue
          const begin = new Date() // On initialise avec la date actuelle
          const finish = new Date(begin)
          finish.setDate(begin.getDate() + (phase.period || 0) - 1)
          phase.beginDate = formatDate(begin)
          phase.finishDate = formatDate(finish)
        } else {
          const previous = sortedPhases[i - 1]
          if (!previous.finishDate || isNaN(new Date(previous.finishDate))) continue
          const begin = new Date(previous.finishDate)
          begin.setDate(begin.getDate() + 1)
          const finish = new Date(begin)
          finish.setDate(begin.getDate() + (phase.period || 0) - 1)
          phase.beginDate = formatDate(begin)
          phase.finishDate = formatDate(finish)
        }
      }
      this.etude.phases = sortedPhases
    },
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
      this.calculateDates()
      axios.put("/api/etudes/phases/",
        this.etude.phases,
        {withCredentials: true}
      ).then(() => {
        axios.get(`/api/publish/etude/${this.etude.id}/devis/`, { withCredentials: true, responseType: "blob" }).then((response) => {
          this.createDownloadElement(response.data, "DEVIS-" + this.etude.name + ".docx")
        }).catch(err => {
          this.$message({ message: "Une erreur est survenue lors de la génération du devis : " + err, type: "error" })
        }).finally(() => {
          this.loading = false
        })  
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la mise à jour des phases : " + err, type: "error" })
        this.loading = false
      })
    },
    downloadCE () {
      this.loading = true
      if (!this.etude.docEtude.signDate){

        this.etude.docEtude.signDate = new Date()
        this.calculateDates()
        axios.put(
        `/api/etudes/${this.etude.id}/ce/`,
        {
          ...this.etude.docEtude,
          signer1 : this.etude.docEtude.signer1.id,
          signer2 : this.etude.docEtude.signer2.id
        },
        {withCredentials: true}
      ).then(() => {
        axios.put("/api/etudes/phases/",
          this.etude.phases,
          {withCredentials: true}
        ).then(() => {
          axios.get(`/api/publish/etude/${this.etude.id}/ce/`, { withCredentials: true, responseType: "blob" }).then((response) => {
            if (this.etude.cc){
              this.createDownloadElement(response.data, "BC-" + this.etude.name + ".docx")
            }else {
              this.createDownloadElement(response.data, "CE-" + this.etude.name + ".docx")
            }
          }).catch((err) => {
            this.$message({ message: "Une erreur est survenue lors de la génération du document : " + err, type: "error" })
            this.loading = false
          }).finally(() => {
            this.loading = false
          })   
        }).catch(err => {
          this.$message({ message: "Une erreur est survenue lors de la mise à jour des phases : " + err, type: "error" })
          this.loading = false
        })
      }).catch((err) => {
        this.$message({message: "Erreur d'enregistrement de la date : "+err, type: "error"})
        this.loading = false
      })
      }else {
        axios.get(`/api/publish/etude/${this.etude.id}/ce/`, { withCredentials: true, responseType: "blob" }).then((response) => {
          if (this.etude.cc){
            this.createDownloadElement(response.data, "BC-" + this.etude.name + ".docx")
          }else {
            this.createDownloadElement(response.data, "CE-" + this.etude.name + ".docx")
          }
        }).catch((err) => {
          this.$message({ message: "Une erreur est survenue lors de la génération du document : " + err, type: "error" })
          this.loading = false
        }).finally(() => {
          this.loading = false
        })   
      }
    },
    downloadCEPdf () {
      this.loading = true
      if (!this.etude.docEtude.signDate) {
        this.etude.docEtude.signDate = new Date()
        this.calculateDates()
        axios.put(
        `/api/etudes/${this.etude.id}/ce/`,
        {
          ...this.etude.docEtude,
          signer1 : this.etude.docEtude.signer1.id,
          signer2 : this.etude.docEtude.signer2.id
        },
        {withCredentials: true}
      ).then(() => {
        axios.put("/api/etudes/phases/",
          this.etude.phases,
          {withCredentials: true}
        ).then(() => {
          axios.get(`/api/publish/etude/${this.etude.id}/ce/pdf/`, { withCredentials: true, responseType: "blob" }).then((response) => {
            if (this.etude.cc){
              this.createDownloadElement(response.data, "BC-" + this.etude.name + ".pdf")
            }else {
              this.createDownloadElement(response.data, "CE-" + this.etude.name + ".pdf")
            }  
          }).catch(err => {
            this.$message({ message: "Une erreur est survenue lors de la génération du document : " + err, type: "error" })
          }).finally(() => {
            this.loading = false
          })   
        }).catch(err => {
          this.$message({ message: "Une erreur est survenue lors de la mise à jour des phases : " + err, type: "error" })
          this.loading = false
        })
      }).catch((err) => {
        this.$message({message: "Erreur d'enregistrement de la date : "+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
      } else {
        axios.get(`/api/publish/etude/${this.etude.id}/ce/pdf/`, { withCredentials: true, responseType: "blob" }).then((response) => {
          if (this.etude.cc){
            this.createDownloadElement(response.data, "BC-" + this.etude.name + ".pdf")
          }else {
            this.createDownloadElement(response.data, "CE-" + this.etude.name + ".pdf")
          }  
        }).catch(err => {
          this.$message({ message: "Une erreur est survenue lors de la génération du document : " + err, type: "error" })
        }).finally(() => {
          this.loading = false
        })   
      }
    },
    downloadCC (cc) {
      this.$emit('update:loading', true)
      cc.signDate = new Date()
      axios.put(
        `/api/etudes/${cc.id}/cc/`,
        cc,
        {withCredentials: true}
      ).then(() => {
        axios.get(`/api/publish/etude/${cc.id}/cc/`, { withCredentials: true, responseType: "blob" }).then((response) => {
          this.createDownloadElement(response.data, "CC-" + cc.name + ".docx")
          
        }).catch(err => {
          this.$message({ message: "Une erreur est survenue lors de la génération du document : " + err, type: "error" })
        }).finally(() => {
          this.$emit('update:loading', false)
        })
      }).catch((err) => {
        this.$message({message: "Erreur d'enregistrement de la date : "+err, type: "error"})
      }).finally(() => {
        this.$emit('update:loading', false)
      })
    },
    downloadCCPdf (cc) {
      this.$emit('update:loading', true)
      cc.signDate = new Date()
      axios.put(
        `/api/etudes/${cc.id}/cc/`,
        cc,
        {withCredentials: true}
      ).then(() => {
        axios.get(`/api/publish/etude/${cc.id}/cc/pdf/`, { withCredentials: true, responseType: "blob" }).then((response) => {
          this.createDownloadElement(response.data, "CC-" + cc.name + ".pdf")
          
        }).catch(err => {
          this.$message({ message: "Une erreur est survenue lors de la génération du document : " + err, type: "error" })
        }).finally(() => {
          this.$emit('update:loading', false)
        })
      }).catch((err) => {
        this.$message({message: "Erreur d'enregistrement de la date : "+err, type: "error"})
      }).finally(() => {
        this.$emit('update:loading', false)
      })
    },
    downloadRDM (rdmId) {
      this.loading = true
      axios.get(`/api/publish/rdm/${rdmId}`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, "RDM-" + this.etude.name + ".docx")
      }).catch(err => {
        if (err.response && err.response.status === 404) {
          this.$message({ message: "Le BA n'a pas été généré pour l'intervenant", type: "warning" })
        } else {
          this.$message({ message: "Une erreur est survenue lors de la génération du RDM : " + err, type: "error" })
        }
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