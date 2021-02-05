<template>
  <BaseComponent
    title="Suivi d'études"
    :breadcrumb="breadcrumb"
  >
    <el-table
      v-loading="loading"
      class="grid"
      :data="etudes"
      :stripe="true"
    >
      <el-table-column
        prop="name"
        label="Nom de l'étude"
        sortable
      >
        <template slot-scope="scope">
          <router-link :to="`/etudes/${scope.row.id}/voir`">
            <el-button type="text">
              {{ scope.row.name }}
            </el-button>
            <span
              v-if="scope.row.confidential"
              class="confiStyle"
            >
              Confidentielle
            </span>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        prop="number"
        label="Numéro de l'étude"
        sortable
      />
      <el-table-column
        prop="mandat"
        label="Mandat"
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
      etudes: [],
      loading: true,
      breadcrumb: [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/etudes/",
      {withCredentials: true}
    ).then((res) => {
      this.etudes = res.data
    }).
      catch(() => {
        this.$message({message: "Impossible de récupérer les études pour le moment",
          type: "error"})
      }).
      finally(() => {
        this.loading = false
      })
  }
}
</script>

<style>
  .confiStyle {
    color: rgb(165, 27, 27);
    font-weight: bold;
  }
</style>
