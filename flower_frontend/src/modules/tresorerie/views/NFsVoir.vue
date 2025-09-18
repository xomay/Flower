<template>
  <BaseComponent
    title="Liste des NF"
    :breadcrumb="breadcrumb"
  >
    <el-row>
      <el-col
        :span="2"
        :offset="1"
      >
        <router-link :to="'/tresorerie/nfs/ajouter'">
          <el-button
            type="primary"
            icon="Plus"
            plain
          >
            Ajouter une NF
          </el-button>
        </router-link>
      </el-col>
      <el-col
        :span="4"
        :offset="1"
      >
        <h1>
          Trier les notes de frais :
        </h1>
      </el-col>
      <el-col :span="16">
        <el-radio-group
          v-model="filtreChoice"
          style="margin-bottom: 30px; margin-top: 5px;"
        >
          <el-radio :label="1">
            Ne pas filtrer
          </el-radio>
          <el-radio :label="2">
            Seulement les NF normales
          </el-radio>
          <el-radio :label="3">
            Seulement les NF kilométriques
          </el-radio>
        </el-radio-group>
      </el-col>
    </el-row>
    <el-table
      :data="displayedNFs"
      :loading="loading"
      class="grid"
      :border="true"
      :default-sort="{prop: 'reference', order: 'descending'}"
      :cell-style="calculateStyle"
    >
      <el-table-column
        label="Date"
        prop="date"
        fixed="left"
        width="100px"
        align="center"
        :formatter="niceDateFormatter"
        sortable
      />
      <el-table-column
        prop="reference"
        label="Référence"
        fixed="left"
        width="120px"
        align="center"
        sortable
      >
        <template #default="{ row, $index }">
          <router-link :to="`/tresorerie/nfs/${row.id}/voir`">
            <el-button
              type="text"
              size="small"
            >
              {{ row.reference }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        label="Demandeur"
        fixed="left"
        width="160px"
        align="center"
        sortable
      >
        <template #default="{ row, $index }">
          <router-link :to="`/membres/${row.demandeur.id}/voir`">
            <el-button
              type="text"
              size="small"
            >
              {{ row.demandeur.firstname + " " + row.demandeur.lastname }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        label="Objet de la demande"
        prop="objet"
      />
      <el-table-column
        label="Type"
        fixed="right"
        align="center"
        width="120px"
      >
        <template #default="{ row, $index }">
          <span v-if="row.isKilometrique">
            Kilométrique
          </span>
          <span v-else>
            Normale
          </span>
        </template>
      </el-table-column>
      <el-table-column
        label="Montant HT"
        fixed="right"
        prop="montantHT"
        :formatter="euroFormatter"
        align="center"
        width="120px"
      />>
      <el-table-column
        label="Montant TVA"
        fixed="right"
        prop="montantTVA"
        :formatter="euroFormatter"
        align="center"
        width="120px"
      />
      <el-table-column
        label="Montant TTC"
        fixed="right"
        prop="montantTTC"
        :formatter="euroFormatter"
        align="center"
        width="130px"
        sortable
      />
      <el-table-column
        label="Télécharger"
        fixed="right"
        align="center"
        width="100px"
      >
        <template #default="{ row, $index }">
          <el-button
            type="text"
            icon="Download"
            :loading="loading"
            @click="downloadNF(row)"
          />
        </template>
      </el-table-column>
    </el-table>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import UtilsMixin from "@/mixins/Utils"
export default {
  name: "NFsVoir",
  mixins: [UtilsMixin],
  data () {
    return {
      nfs: [],
      loading: true,
      filtreChoice: 1,
      breadcrumb: [
        {
          name: "Liste des NF",
          link: "/tresorerie/nfs/voir/"
        }
      ]
    }
  },
  computed: {
    displayedNFs () {
      switch(this.filtreChoice) {
      case 1: return this.nfs
      case 2: return this.nfs.filter(nf => ! nf.isKilometrique)
      case 3: return this.nfs.filter(nf => nf.isKilometrique)
      default: return []
      }
    }
  },
  beforeCreate () {
    axios.get(
      "/api/ndfs/",
      { withCredentials: true }
    ).then((res) => {
      this.nfs = res.data
      if(this.nfs.length == 0)
        this.$message({message: "Aucune NF n'est enregistrée.", type: "warning"})
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les NF : " + err, type: "error"})
    }).finally(() => this.loading = false)
  },
  methods: {
    calculateStyle ({row, columnIndex}) {
      if(columnIndex !== 4)
        return ""
      else
        return /*"font-weight: bold; "+*/(row.isKilometrique ? "background: rgba(112, 177, 157, 0.2);" : "background: rgba(177, 168, 168, 0.2);")
    },
    downloadNF (ndf) {
      this.loading = true
      axios.get(`/api/publish/ndf/${ndf.id}`, { withCredentials: true, responseType: "blob" }).then((response) => {
        this.createDownloadElement(response.data, ndf.reference + ".docx")
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération de la NF : " + err, type: "error" })
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
    }
  }
}
</script>
