<template>
  <BaseComponent
    title="Liste des NF"
    :breadcrumb="breadcrumb"
  >
    <el-table
      :data="nfs"
      :loading="loading"
      class="grid"
      :stripe="true"
      :border="true"
      :default-sort="{prop: 'reference', order: 'descending'}"
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
        <template slot-scope="scope">
          <router-link :to="`/tresorerie/nfs/${scope.row.id}/voir`">
            <el-button
              type="text"
              size="small"
            >
              {{ scope.row.reference }}
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
        <template slot-scope="scope">
          <router-link :to="`/membres/${scope.row.demandeur.id}/voir`">
            <el-button
              type="text"
              size="small"
            >
              {{ scope.row.demandeur.firstname + " " + scope.row.demandeur.lastname }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        label="Objet de la demande"
        prop="objet"
      />
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
      breadcrumb: [
        {
          name: "Liste des NF normales",
          link: "tresorerie/nfs/voir/normales"
        }
      ]
    }
  },
  beforeCreate () {
    axios.get(
      "api/ndfs/",
      { withCredentials: true }
    ).then((res) => {
      this.nfs = res.data
      if(this.nfs.length == 0)
        this.$message({message: "Aucune NF n'est enregistrée.", type: "warning"})
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les NF : " + err, type: "error"})
    })
  }
}
</script>