<template>
  <BaseComponent
    title="Liste des réalisateurs"
    :breadcrumb="breadcrumb"
  >
    <el-table
      v-loading="loading"
      class="grid"
      :data="reas"
      :stripe="true"
      :border="true"
    >
      <el-table-column
        align="center"
        prop="firstname"
        label="Réalisateur"
        sortable
      >
        <template slot-scope="scope">
          <router-link :to="`/realisateurs/${scope.row.id}/voir`">
            <el-button
              type="text"
              size="small"
            >
              {{ scope.row.firstname + " " + scope.row.lastname }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        prop="promotion"
        label="Promotion"
        sortable
      />
      <el-table-column
        align="center"
        prop="email_insa"
        label="Mail INSA"
        sortable
      />
      <el-table-column
        align="center"
        prop="skills"
        label="Compétences"
        sortable
      >
        <template slot-scope="scope">
          {{ niceArray(scope.row.skillsArray) }}
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        prop="rating"
        label="Nombre d'études"
        sortable
      >
        <template slot-scope="scope">
          {{ scope.row.etudesAmount }}
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        prop="rating"
        label="Note moyenne"
        sortable
      >
        <template slot-scope="scope">
          <font
            v-if="scope.row.rating == -1"
            color="gray"
          >
            <i>néant</i>
          </font>
          <font
            v-else
            :color="getRatingColor(scope.row.rating)"
          >
            {{ scope.row.rating }} / 10
          </font>
        </template>
      </el-table-column>
    </el-table>
  </BaseComponent>
</template>

<script>
const axios = require("axios")

export default {
  name: "RealisateursVoir",
  data () {
    return {
      reas: [],
      loading: true,
      breadcrumb: [
        {
          name: "Liste des réalisateurs",
          link: "/realisateurs"
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/realisateurs/",
      {withCredentials: true}
    ).then((res) => {
      this.reas = res.data
    }).catch(() => {
      this.$message({message: "Impossible de récupérer les membres pour le moment",
        type: "error",
        offset: 40})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    getRatingColor (rating) {
      if(rating < 1) {
        return "red"
      } else if(rating < 3) {
        return "orange"
      } else {
        return "green"
      }
    },
    niceArray (array) {
      var str = ""
      const MAX = 5
      var count = 1
      for (const c of array) {
        if(str !== "")
          str += ", "
        if(count > MAX) {
          const remaining = array.length - MAX
          str += remaining + " autre"+(remaining>1?"s":"")+"."
          break
        }
        str += c
        count ++
      }
      return str
    }
  }
}
</script>
