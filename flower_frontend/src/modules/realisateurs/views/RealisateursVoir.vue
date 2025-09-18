<template>
  <BaseComponent
    title="Liste des réalisateurs"
    :breadcrumb="breadcrumb"
  >
    <template #action>
      <router-link to="/realisateurs/ajouter">
        <el-button
          type="primary"
          icon="Plus"
          plain
          style="margin: 0 10px;"
        >
          Ajouter un réalisateur
        </el-button>
      </router-link>
    </template>
    <el-table
      class="grid"
      :data="reas"
      :stripe="true"
      :border="true"
    >
      <el-table-column
        align="center"
        prop="firstname"
        label="Réalisateur"
        width="170px"
        fixed="left"
        sortable
      >
        <template #default="{ row }">
          <router-link :to="`/realisateurs/${row.id}/voir`">
            <el-button
              type="text"
              size="small"
            >
              {{ row.firstname + " " + row.lastname }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        prop="promotion"
        label="Promotion"
        width="120px"
        fixed="left"
        sortable
      />
      <el-table-column
        align="center"
        prop="email_insa"
        label="Mail INSA"
        width="250px"
        fixed="left"
        sortable
      />
      <el-table-column
        align="center"
        prop="skills"
        label="Compétences"
        sortable
      >
        <template #default="{ row }">
          {{ niceArray(row.skillsArray) }}
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        prop="etudesAmount"
        label="Nombre d'études"
        width="165px"
        fixed="right"
        sortable
      />
      <el-table-column
        align="center"
        prop="rating"
        label="Note moyenne"
        width="150px"
        fixed="right"
        sortable
      >
        <template #default="{ row }">
          <p
            v-if="row.rating == -1"
            color="gray"
          >
            <i>néant</i>
          </p>
          <p
            v-else
            :color="getRatingColor(row.rating)"
          >
            {{ row.rating }} / 10
          </p>
        </template>
      </el-table-column>
      <el-table-column
        v-show="isAdmin()"
        label="Compte"
        width="100px"
        fixed="right"
        align="center"
        v-if="false"
      >
        <template #default="{ row }">
          <el-button
            v-show="row.user == null"
            type="warning"
            icon="Plus"
            :loading="loading"
            @click="createReaAcccount(row)"
          />
          <!-- Utilisation de v-show car ça peut changer (genre une fois qu'on a appuyé sur le bouton quoi) -->
          <el-button
            v-show="row.user != null"
            type="danger"
            icon="Minus"
            :loading="loading"
            @click="deleteReaAcccount(row)"
          />
        </template>
      </el-table-column>
    </el-table>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import { Permissions } from "@/mixins/Permissions"
export default {
  name: "RealisateursVoir",
  mixins: [Permissions],
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
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les réalisateurs pour le moment : " +err, type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    getRatingColor (rating) {
      if(rating < 3.33) {
        return "red"
      } else if(rating < 6.67) {
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
    },
    createReaAcccount (rea) {
      this.loading = true
      axios.put(
        `/api/realisateurs/openaccount/${rea.id}/`,
        {},
        { withCredentials: true }
      ).then((res) => {
        this.$message({ message: "Compte créé avec succès.", type: "success" })
        rea.user = res.data
      }).catch((err) => {
        this.$message({ message: "Impossible de créer le compte : " + err, type: "error" })
      }).finally(() => this.loading = false)
    },
    deleteReaAcccount (rea) {
      this.loading = true
      axios.put(
        `/api/realisateurs/deleteaccount/${rea.id}/`,
        {},
        { withCredentials: true }
      ).then(() => {
        this.$message({ message: "Compte supprimé avec succès.", type: "success" })
        rea.user = null
      }).catch((err) => {
        this.$message({ message: "Impossible de supprimer le compte : " + err, type: "error" })
      }).finally(() => this.loading = false)
    }
  }
}
</script>
