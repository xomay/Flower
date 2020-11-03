<template>
  <BaseComponent
    title="Liste des Prospects"
    :breadcrumb="breadcrumb"
  >
    <el-table
      v-loading="loading"
      class="grid"
      :data="prospects"
      :stripe="true"
    >
      <el-table-column
        prop="name"
        label="Nom"
        sortable
      >
        <template slot-scope="scope">
          <router-link :to="'/prospects/' + scope.row.id + '/voir'">
            <el-button
              type="text"
              size="small"
            >
              {{ scope.row.name }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        prop="town"
        label="Ville"
        sortable
      />
    </el-table>
  </BaseComponent>
</template>

<script>
const axios = require("axios")

export default {
  name: "ProspectsVoir",
  data () {
    return {
      prospects: [],
      loading: true,
      breadcrumb: [
        {
          name: "Lister des prospects",
          link: "/prospects"
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `${this.$server_url}/prospects/`,
      {withCredentials: true}
    ).then((res) => {
      this.prospects = res.data
    }).
      catch(() => {
        this.$message({message: "Impossible de récupérer les prospects pour le moment",
          type: "error"})
      }).
      finally(() => {
        this.loading = false
      })
  },
  methods: {
    display (scope) {
      console.log(scope)
    }
  }
}
</script>

<style>

</style>
