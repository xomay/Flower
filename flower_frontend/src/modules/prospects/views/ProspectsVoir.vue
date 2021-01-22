<template>
  <BaseComponent
    title="Prospection"
    :breadcrumb="breadcrumb"
  >
    <h1
      class="text-xl"
      :style="{margin:'3vh auto 2vh 1vw'}"
    >
      Actions commerciales :
    </h1>
    <el-row>
      <el-col>
        <el-button
          type="primary"
          @click="goVoirAC()"
        >
          Voir les actions commerciales
        </el-button>
        <el-button
          type="success"
          @click="goCreateAC()"
        >
          Créer une action commerciale
        </el-button>
      </el-col>
    </el-row>
    <h1
      class="text-xl"
      :style="{margin:'3vh auto 2vh 1vw'}"
    >
      Lister les prospects :
    </h1>
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
  },
  methods: {
    goVoirAC () {
      console.log("voir")
    },
    goCreateAC () {
      console.log("create")
    }
  }
}
</script>
