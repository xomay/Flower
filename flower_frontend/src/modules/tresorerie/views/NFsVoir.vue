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
    >
      <el-table-column
        label="Date"
        sortable
      >
        <template slot-scope="scope">
          {{ niceDate(scope.row.date) }}
        </template>
      </el-table-column>
      <el-table-column
        prop="reference"
        label="Référence"
        sortable
      >
        <template slot-scope="scope">
          <router-link :to="`tresorerie/nfs/${scope.row.id}/voir`">
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
      >
        <template slot-scope="scope">
          {{ scope.row.montantHT + " €" }}
        </template>
      </el-table-column>
      <el-table-column
        label="Montant TVA"
      >
        <template slot-scope="scope">
          {{ scope.row.montantTVA + " €" }}
        </template>
      </el-table-column>
      <el-table-column
        label="Montant TTC"
        sortable
      >
        <template slot-scope="scope">
          {{ scope.row.montantTTC + " €" }}
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
      console.log(this.nfs[0])
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les NF : " + err, type: "error"})
    })
  }
}
</script>