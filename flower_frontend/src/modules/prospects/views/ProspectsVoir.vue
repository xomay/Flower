<template>
  <BaseComponent
    title="Prospection"
    :breadcrumb="breadcrumb"
  >
    <el-row
      :style="{margin:'3vh auto 2vh 1vw'}"
    >
      <el-col
        :span="3"
      >
        <h1
          class="text-xl"
        >
          Actions commerciales
        </h1>
      </el-col>
      <el-col
        :span="3"
        :offset="1"
      >
        <router-link to="/prospects/actionCommerciale/">
          <el-button
            type="primary"
          >
            Voir les actions commerciales
          </el-button>
        </router-link>
      </el-col>
    </el-row>
    <el-row
      :style="{margin:'3vh auto 2vh 1vw'}"
    >
      <el-col
        :span="3"
      >
        <h1
          class="text-xl"
        >
          Ajouter un prospect :
        </h1>
      </el-col>
      <el-col
        :span="3"
        :offset="1"
      >
        <router-link to="/prospects/ajouter/">
          <el-button
            type="success"
            icon="el-icon-plus"
          />
        </router-link>
      </el-col>
    </el-row>
    <el-table
      v-loading="loading"
      class="grid"
      :style="{margin:'1vh auto 2vh 1vw'}"
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
          name: "Liste des prospects",
          link: "/prospects"
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/prospects/",
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
  }
}
</script>
