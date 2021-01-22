<template>
  <BaseComponent
    title="Lister les actions commerciales"
    :breadcrumb="breadcrumb"
  >
    <el-table
      v-loading="loading"
      :data="actionsComs"
      :default-sort="{prop: 'date', order: 'descending'}"
      :row-class-name="colorRow"
    >
      <el-table-column
        prop="name"
        label="Nom de l'action"
        sortable
      />
      <el-table-column
        prop="date"
        label="Date"
        sortable
      />
      <el-table-column
        prop="prospect"
        label="Prospect"
        sortable
      >
        <template slot-scope="scope">
          {{ getProspect(scope.row.prospect) }}
        </template>
      </el-table-column>
      <el-table-column
        prop="actionType"
        label="Type d'action"
        sortable
      />
    </el-table>
  </BaseComponent>
</template>

<script>

const axios = require("axios")

export default {
  name: "ActionCommerciale",
  data () {
    return {
      breadcrumb: [],
      loading: false,
      actionsComs: [],
      prospects: []
    }
  },
  created () {
    axios.get(
      "/api/actioncom",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.actionsComs = res.data
    }).
      catch((err) => {
        console.log(err)
        this.$message({message: "Impossible de récupérer la liste des actions commerciales.",
          type: "error",
          offset: 40})
      })
    axios.get(
      "/api/prospects",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.prospects = res.data
    }).
      catch((err) => {
        console.log(err)
        this.$message({message: "Impossible de récupérer la liste des prospects.",
          type: "error",
          offset: 40})
      })
  },
  methods: {
    getProspect (id) {
      return this.prospects.find(pr => pr.id === id).name
    },
    colorRow ({row}) {
      const todayDate = Date.now()
      const tokens = row.date.split("-")
      const actionDate = Date.parse(new Date(tokens[1]+" "+tokens[2]+" "+tokens[0]))
      const twoDays = 1000*60*60*24 * 2
      if(!(actionDate < todayDate)) {
        console.log(row.name+" => d="+(actionDate - todayDate)+", 2jours=" + twoDays+". Diff =  " + (actionDate - todayDate - twoDays))
      }
      if(actionDate < todayDate) {
        return "old-row"
      } else if ((actionDate - todayDate - twoDays) < 0) {
        return "almost-row"
      } else {
        return "future-row"
      }
    }
  }
}
</script>

<style>
  .el-table .old-row {
    background: rgba(94, 93, 92, 0.336);
  }
  .el-table .almost-row {
    background: rgba(167, 139, 14, 0.486);
  }
  .el-table .future-row {
    background: rgba(66, 153, 153, 0.336);
  }
</style>
