<template>
  <BaseComponent
    title="Liste des membres"
    :breadcrumb="breadcrumb"
  >
    <el-table
      v-loading="loading"
      class="grid"
      :data="membres"
      :stripe="true"
    >
      <el-table-column
        prop="firstname"
        label="Prénom"
        sortable
      >
        <template slot-scope="scope">
          <router-link :to="`/membres/${scope.row.id}/voir`">
            <el-button
              type="text"
              size="small"
            >
              {{ scope.row.firstname }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        prop="lastname"
        label="Nom"
        sortable
      />
      <el-table-column
        prop="promotion"
        label="Promotion"
        sortable
      />
    </el-table>
  </BaseComponent>
</template>

<script>
const axios = require("axios")

export default {
  name: "EtudeVoir",
  data () {
    return {
      membres: [],
      loading: true,
      breadcrumb: [
        {
          name: "Lister des membres",
          link: "/membres"
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/membres/",
      {withCredentials: true}
    ).then((res) => {
      this.membres = res.data
    }).
      catch(() => {
        this.$message({message: "Impossible de récupérer les membres pour le moment",
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
