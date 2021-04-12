<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
  >
    <el-row>
      <el-col :span="10">
        <Summary
          :etude="etude"
          :getgantt="false"
        />
      </el-col>
      <el-col :span="14">
        <el-row class="factRow">
          <h1 class="h1Styled">
            Factures :
          </h1>
          <el-table
            class="grid"
            :border="true"
            :data="etude.invoices"
          >
            <el-table-column
              prop="invoiceNumber"
              label="Référence"
              align="center"
              fixed="left"
              width="140px"
              sortable
            >
              <template slot-scope="scope">
                {{ scope.row.invoiceType }}_{{ scope.row.invoiceNumber }}
              </template>
            </el-table-column>
            <el-table-column
              prop="description"
              label="Objet"
              align="center"
            />
            <el-table-column
              prop="accountingPeriod"
              label="Exercice comptable"
              fixed="right"
              align="center"
              width="160px"
            />
            <el-table-column
              label="Opérations"
              fixed="right"
              align="center"
              width="180px"
            >
              <template slot-scope="scope">
                <el-button
                  type="text"
                  icon="el-icon-download"
                  :loading="loading"
                  @click="downloadInvoice(scope.row.id)"
                />
                <router-link :to="`/etudes/${$route.params.id}/factures/modifier/${scope.row.id}`">
                  <el-button
                    type="text"
                    icon="el-icon-edit"
                  />
                </router-link>
                <el-popconfirm
                  confirm-button-text="Oui"
                  confirm-button-type="error"
                  cancel-button-text="Finalement non"
                  cancel-button-type="primary"
                  icon="el-icon-delete"
                  icon-color="red"
                  title="Voulez-vous vraiment supprimer cette facture ?"
                  @onConfirm="deleteInvoice(scope.row.id)"
                >
                  <el-button
                    slot="reference"
                    type="text"
                    icon="el-icon-delete"
                    :loading="loading"
                  />
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
        </el-row>
        <el-row class="factRow">
          <router-link :to="`/etudes/${$route.params.id}/factures/ajouter`">
            <el-button
              type="success"
              class="factButton"
              icon="el-icon-plus"
            >
              Ajouter une facture
            </el-button>
          </router-link>
        </el-row>
        <hr class="factBr">
        <el-row class="factRow">
          <h1 class="h1Styled">
            Bulletins de Versement :
          </h1>
          <el-table
            class="grid"
            :border="true"
            :data="bvs"
          >
            <el-table-column
              prop="reference"
              label="Référence"
              align="center"
              fixed="left"
              width="140px"
              sortable
            />
            <el-table-column
              prop="date"
              label="Date de paiement"
              align="center"
              fixed="left"
              width="170px"
              sortable
            />
            <el-table-column
              label="Étudiant"
              align="center"
              fixed="left"
            >
              <template slot-scope="scope">
                <el-button
                  type="text"
                  size="small"
                  @click="pushToRealisateur(scope.row.realisateur.id)"
                >
                  {{ nicePeople(scope.row.realisateur) }}
                </el-button>
              </template>
            </el-table-column>
            <el-table-column
              prop="montant_net"
              label="Montant net étudiant"
              align="center"
              fixed="right"
              :formatter="euroFormatter"
              sortable
            />
            <el-table-column
              label="Opérations"
              fixed="right"
              align="center"
              width="118px"
            >
              <template slot-scope="scope">
                <el-button
                  type="text"
                  icon="el-icon-download"
                  :loading="loading"
                  @click="downloadBV(scope.row)"
                />
                <router-link :to="`/tresorerie/etudes/${$route.params.id}/bvs/modifier/${scope.row.id}/`">
                  <el-button
                    type="text"
                    icon="el-icon-edit"
                  />
                </router-link>
              </template>
            </el-table-column>
          </el-table>
        </el-row>
        <el-row class="factRow">
          <el-button
            v-show="can_add_bv"
            type="success"
            class="factButton"
            icon="el-icon-plus"
            @click="pushToAddBV()"
          >
            Ajouter un BV
          </el-button>
          <el-alert
            v-show="!can_add_bv"
            type="info"
            title="Impossible de rajouter plus de BV"
            :closable="false"
            center
            show-icon
          />
        </el-row>
        <hr class="factBr">
        <el-row class="factRow">
          <el-button
            type="info"
            class="factButton"
            plain
            disabled
          >
            Facture pro format
          </el-button>
        </el-row>
        <!--
        <el-row class="factRow">
          <el-button
            type="warning"
            class="factButton"
            plain
          >
            Facture d'achat liée à une étude
          </el-button>
        </el-row>-->
        <hr class="factBr">
        <FacturesMessages
          :etude="etude"
        />
      </el-col>
    </el-row>
    <hr style="margin-top: 20px;">
    <el-row style="margin-top: 20px;">
      <b>Fichiers associés :</b>
      <UploaderLocal
        :inital-list="etude.linkedFiles"
        :loading="loading"
        api-base-url="etudes"
      />
    </el-row>
  </BaseComponent>
</template>

<script>
import Summary from "@/modules/etudes/components/Summary"
import FacturesMessages from "../components/FacturesMessages"
import UploaderLocal from "@/components/UploaderLocal"
import Utils from "@/mixins/Utils"
const axios = require("axios")

export default {
  name: "FactureAboutEtude",
  components: { Summary, FacturesMessages, UploaderLocal },
  mixins: [Utils],
  data () {
    return {
      etude: {
        invoices: [],
        pvr: [],
        linkedFiles: [],
        bvData: {full:true}
      },
      bvs: [],
      can_add_bv: false,
      title: "<loading>",
      loading: true,
      breadcrumb: [
        {
          name: "Études (trésorerie)",
          link: "/tresorerie/etudes/"
        },
        {
          name: "<loading>",
          link: `/tresorerie/etudes/${this.$route.params.id}/`
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/etudes/${this.$route.params.id}`,
      {withCredentials: true}
    ).then((res) => {
      this.etude = res.data
      this.breadcrumb[1].name = res.data.name
      this.title = res.data.name + " - Vue trésorerie"
      this.can_add_bv = ! res.data.bvData.full
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer l'étude pour le moment: "+err, type: "error"})
    }).finally(() => {
      this.loading = false
    })
    axios.get(
      `/api/etudes/${this.$route.params.id}/bvs/`,
      {withCredentials: true}
    ).then((res) => {
      this.bvs = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les BV pour le moment: "+err, type: "error"})
    })
  },
  methods: {
    pushToAddBV () {
      this.$router.push(`/tresorerie/etudes/${this.$route.params.id}/bvs/ajouter`)
    },
    deletePVR (pvrId) {
      this.loading = true
      axios.delete(`/api/pvr/${pvrId}`, { withCredentials: true }).then(() => {
        this.$message({ message: "PVR supprimée avec succès.", type: "success"})
        this.etude.pvr = this.etude.pvr.filter(emlt => emlt.id !== pvrId)
      }).catch(err => {
        this.$message({ message: "Impossible de supprimer le PVR : "+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deleteInvoice (invoiceId) {
      this.loading = true
      axios.delete(
        `/api/tresorerie/factures/${invoiceId}/`,
        { withCredentials: true}
      ).then(() => {
        this.$message({message: "Facture supprimée avec succès.", type: "success"})
        this.etude.invoices = this.invoi.invoices.filter(emlt => emlt.id !== invoiceId)
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer la facture : " + err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
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
    downloadBV (bv) {
      this.loading = true
      axios.get(`/api/publish/bv/${bv.id}/`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, bv.reference + ".docx")
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération du BV : " + err, type: "error" })
      }).finally(() => {
        this.loading = false
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
    pushToRealisateur (rea_id) {
      this.$router.push(`/realisateurs/${rea_id}/voir`)
    }
  }
}
</script>

<style scoped>
  .factButton {
    margin-left: 30%;
    width: 40%;
  }
  .factRow {
    margin-bottom: 20px;
  }
  .factBr {
    width: 10%;
    border-width: 1px;
    border-color: rgb(33, 91, 179);
    margin: 0 auto 0 auto;
    margin-bottom: 20px;
  }
  .h1Styled {
    font-size: 1.2em;
    color: rgb(121, 121, 121);
    font-weight: bold;
    margin: 3px auto 16px 25px;
  }
</style>
