<template>
  <div>
    <el-button
      type="success"
      :loading="loading"
      icon="el-icon-download"
      @click="downloadDevis"
    >
      Générer le devis
    </el-button>
    <el-collapse
      v-model="activeCollapses"
      class="mt-2"
    >
      <el-collapse-item name="0">
        <template slot="title">
          <span class="mr-2 text-lg">Convention Etude</span>
        </template>
        <router-link
          class="mr-2"
          :to="`/etudes/${$route.params.id}/convention-etude`"
        >
          <el-button
            type="primary"
            icon="el-icon-edit"
          >
            Rédiger la CE
          </el-button>
        </router-link>
        <el-button
          type="success"
          :loading="loadingCE"
          icon="el-icon-download"
          @click="downloadCE"
        >
          Générer la CE
        </el-button>
      </el-collapse-item>
      <el-collapse-item name="1">
        <template slot="title">
          <span class="mr-2 text-lg">Récapitulatifs de mission</span> <router-link :to="`/etudes/${$route.params.id}/missions`">
            <el-button
              type="text"
              icon="el-icon-edit"
            >
              Modifier
            </el-button>
          </router-link>
        </template>
        <el-table
          class="grid"
          :data="etude.missions"
        >
          <el-table-column
            label="Consultant"
          >
            <template slot-scope="scope">
              <span>{{ getConsultant (scope.row) }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="missionBegin"
            label="Date de début"
          />
          <el-table-column
            prop="missionEnd"
            label="Date de fin"
          />
          <el-table-column
            label="Nombre de phases"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.phases.length }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="JEHNumber"
            label="Nombre de JEH"
          />
          <el-table-column
            label="Montant brut"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.JEHNumber * scope.row.JEHPrice }}€</span>
            </template>
          </el-table-column>
          <el-table-column
            label="Opérations"
          >
            <template slot-scope="scope">
              <el-button
                type="text"
                icon="el-icon-download"
                :loading="loadingRDM"
                @click="downloadRDM(scope.row.id)"
              >
                RDM
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
      <el-collapse-item name="2">
        <template slot="title">
          <span class="mr-2 text-lg">Factures</span> <router-link :to="`/etudes/${$route.params.id}/factures/ajouter`">
            <el-button
              type="text"
              icon="el-icon-plus"
            >
              Ajouter
            </el-button>
          </router-link>
        </template>
        <el-table
          class="grid"
          :data="etude.invoices"
        >
          <el-table-column
            prop="invoiceNumber"
            label="Référence"
            width="100"
          />
          <el-table-column
            prop="description"
            label="Objet"
          />
          <el-table-column
            label="Opérations"
            width="200"
          >
            <template slot-scope="scope">
              <el-button
                type="text"
                icon="el-icon-download"
                :loading="loadingInvoice"
                @click="downloadInvoice(scope.row.id)"
              />
              <router-link :to="`/etudes/${$route.params.id}/factures/modifier/${scope.row.id}`">
                <el-button
                  type="text"
                  icon="el-icon-edit"
                />
              </router-link>
              <el-button
                type="text"
                icon="el-icon-delete"
                :loading="loadingInvoice"
                @click="deleteInvoice(scope.row.id)"
              />
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
      <el-collapse-item name="3">
        <template slot="title">
          <span class="mr-2 text-lg">PVR</span> <router-link :to="`/etudes/${$route.params.id}/pvr/ajouter`">
            <el-button
              type="text"
              icon="el-icon-plus"
            >
              Ajouter
            </el-button>
          </router-link>
        </template>
        <el-table
          class="grid"
          :data="etude.pvr"
        >
          <el-table-column
            prop="documentType"
            label="Type de PVR"
            width="200"
          >
            <template slot-scope="scope">
              <span v-if="scope.row.documentType === 'I'">PVRI</span>
              <span v-else>PVRF</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="signingDate"
            label="Date de signature"
          />
          <el-table-column
            label="Opérations"
            width="200"
          >
            <template slot-scope="scope">
              <el-button
                type="text"
                icon="el-icon-download"
                :loading="loadingPVR"
                @click="downloadPVR(scope.row.id)"
              />
              <router-link :to="`/etudes/${$route.params.id}/pvr/modifier/${scope.row.id}`">
                <el-button
                  type="text"
                  icon="el-icon-edit"
                />
              </router-link>
              <el-button
                type="text"
                icon="el-icon-delete"
                :loading="loadingPVR"
                @click="deletePVR(scope.row.id, scope.$index)"
              />
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
const axios = require("axios")

export default {
  name: "Generation",
  props: {
    etude: { type: Object, required: true }
  },
  data () {
    return {
      loading: false,
      loadingCE: false,
      loadingRDM: false,
      loadingInvoice: false,
      loadingPVR: false,
      activeCollapses: []
    }
  },
  methods: {
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
      this.loadingCE = true
      axios.get(`/api/publish/etude/${this.etude.id}/ce/`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, "CE-" + this.etude.name + ".docx")
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération du devis : " + err, type: "error" })
      }).finally(() => {
        this.loadingCE = false
      })
    },
    downloadRDM (rdmId) {
      this.loadingRDM = true
      axios.get(`/api/publish/rdm/${rdmId}`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, "RDM-" + this.etude.name + ".docx")
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération du RDM : " + err, type: "error" })
      }).finally(() => {
        this.loadingRDM = false
      })
    },
    downloadInvoice (invoiceId) {
      this.loadingInvoice = true
      axios.get(`/api/publish/facture/${invoiceId}`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, "FA-" + this.etude.name + ".docx")
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération de la facture : " + err, type: "error" })
      }).finally(() => {
        this.loadingInvoice = false
      })
    },
    deleteInvoice (invoiceId) {
      console.log("delete invoice id " + invoiceId)
    },
    downloadPVR (pvrId) {
      this.loadingPVR = true
      axios.get(`/api/publish/pvr/${pvrId}`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, "PVR-" + this.etude.name + ".docx")
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération du PVR : " + err, type: "error" })
      }).finally(() => {
        this.loadingPVR = false
      })
    },
    deletePVR (pvrId, index) {
      axios.delete(`/api/pvr/${pvrId}`, { withCredentials: true }).then(() => {
        this.etude.pvr.splice(index, 1)
      }).catch(err => {
        this.$message({ message: err, type: "error", offset: 40 })
      })
    },
    createDownloadElement (data, filename) {
      let fileURL = window.URL.createObjectURL(new Blob([data]))
      let fileLink = document.createElement("a")

      fileLink.href = fileURL
      fileLink.setAttribute("download", filename)
      document.body.appendChild(fileLink)

      fileLink.click()
    },
    getConsultant (mission) {
      if(mission.consultant == undefined) {
        return "(vide)"
      } else {
        return mission.consultant.firstname + " " + mission.consultant.lastname
      }
    }
  }
}
</script>

<style>

</style>