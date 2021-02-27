<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
  >
    <el-col :span="10">
      <Summary
        :etude="etude"
        :getgantt="false"
      />
    </el-col>
    <el-col :span="14">
      <el-row class="factRow">
        Facture :
        <el-table
          class="grid"
          :data="etude.invoices"
        >
          <el-table-column
            prop="invoiceNumber"
            label="Référence"
            sortable
          >
            <template slot-scope="scope">
              {{ scope.row.invoiceType }}_{{ scope.row.invoiceNumber }}
            </template>
          </el-table-column>
          <el-table-column
            prop="description"
            label="Objet"
          />
          <el-table-column
            prop="accountingPeriod"
            label="Exercice comptable"
            sortable
          />
          <el-table-column
            label="Opérations"
          >
            <template slot-scope="scope">
              <!--<el-button
                type="text"
                icon="el-icon-download"
                :loading="loading"
                @click="downloadInvoice(scope.row.id)"
              />-->
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
        <el-button
          type="success"
          class="factButton"
          icon="el-icon-plus"
        >
          Ajouter une facture
        </el-button>
      </el-row>
      <hr class="factBr">
      <el-row class="factRow">
        PVR :
        <el-table
          class="grid"
          :data="etude.pvr"
        >
          <el-table-column
            prop="display"
            label="Type"
          />
          <el-table-column
            prop="reference"
            label="Référence"
            sortable
          />
          <el-table-column
            prop="deliverable"
            label="Description"
          />
          <el-table-column
            prop="signingDate"
            label="Date de signature"
            sortable
          />
          <el-table-column
            label="Opérations"
          >
            <template slot-scope="scope">
              <!--<el-button
                type="text"
                icon="el-icon-download"
                :loading="loading"
                @click="downloadInvoice(scope.row.id)"
              />-->
              <router-link :to="`/etudes/${$route.params.id}/pvr/modifier/${scope.row.id}`">
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
                title="Voulez-vous vraiment supprimer ce PVR ?"
                @onConfirm="deletePVR(scope.row.id)"
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
        <el-button
          type="success"
          class="factButton"
          icon="el-icon-plus"
        >
          Ajouter un PVR
        </el-button>
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
      <el-row class="factRow">
        <el-button
          type="warning"
          class="factButton"
          plain
        >
          Facture d'achat liée à une étude
        </el-button>
      </el-row>
      <hr class="factBr">
      <FacturesMessages
        :etude="etude"
      />
    </el-col>
  </BaseComponent>
</template>

<script>
import Summary from "@/modules/etudes/components/Summary"
import FacturesMessages from "../components/FacturesMessages"
const axios = require("axios")

export default {
  name: "FactureAboutEtude",
  components: { Summary, FacturesMessages },
  data () {
    return {
      etude: {
        invoices: [],
        pvr: []
      },
      title: "",
      loading: true,
      breadcrumb: [
        {
          name: "Factures",
          link: "/tresorerie/factures"
        },
        {
          name: "<loading>",
          link: `/tresorerie/factures/${this.$route.params.id}/`
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
      this.title = res.data.name + " - Type de facture"
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer l'étude pour le moment: "+err, type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
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
</style>
