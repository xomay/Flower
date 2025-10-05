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
    <el-row style="margin: 20px 0;display: flex; justify-content: start;">
      <el-input
        v-model="nameFilterValue"
        style="width: 70%; height: 80%; margin-top: 10px;"
        size="large"
        placeholder="Entrez un nom"
        prefix-icon="Search"
        @change="updateFilters"
        @input="updateFilters"
        />
    </el-row>
    <el-row style="margin: 20px 0; display: flex; justify-content: start;">
      <el-checkbox
        v-model="showRealisateurs"
        size="large"
        border
        @change="updateFilters"
      >
        Réalisateurs
      </el-checkbox>
      <el-checkbox
        v-model="showPool"
        size="large"
        border
        @change="updateFilters"
      >
        Pool d'intervenants
      </el-checkbox>
      <el-select style="width: 20%; margin: 0 30px;" v-model="selectedDepart" multiple size="large" placeholder="Départements" @change="updateFilters">
        <el-option
          v-for="depart in departs"
          :key="depart"
          :label="depart"
          :value="depart"
          :style="{ 'color': departColors[depart], 'font-weight': 'bold' }"
        />
      </el-select>
    </el-row>
    <el-table
      class="grid"
      :data="filteredReas"
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
          <el-tag 
          v-if="!(row.ba && row.security_social_number)"
          type="warning"
          >Pool d'intervenants</el-tag>
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
        prop="filiere"
        label="Département"
        width="120px"
        fixed="left"
        sortable
      >
        <template #default="{ row }">
          <el-tag 
            effect="dark"
            round
            :color="departColors[row.filiere]">{{ row.filiere }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        prop="description"
        label="Présentation"
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
        width="100px"
        fixed="right"
        sortable
      />
      <el-table-column
        align="center"
        prop="rating"
        label="Note moyenne"
        width="100px"
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
      nameFilterValue: "",
      filteredReas: [],
      showRealisateurs: false,
      showPool: false,
      selectedDepart: [],
      departs: ["INFO", "EII", "GMA", "E&T", "MA", "GCU", "GPM", "STPI"],
      departColors: {
        "INFO": "#409EFF",
        "EII": "#67C23A",
        "GMA": "#E6A23C",
        "E&T": "#A45E8D",
        "MA": "#F56C6C",
        "GCU": "#00BFFF",
        "GPM": "#20B2AA",
        "STPI": "#8B4513"
      },
      breadcrumb: [
        {
          name: "Liste des réalisateurs",
          link: "/membres"
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
      this.reas.forEach((rea) => rea.value = rea.firstname + " " + rea.lastname)
      this.filteredReas = [...this.reas]
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
    },
    updateFilters () {
      let filtered = [...this.reas]
      
      // Si aucune checkbox n'est sélectionnée, afficher tous
      if (!this.showRealisateurs && !this.showPool) {
        // Pas de filtre par type
      } else {
        // Filtrer selon les checkboxes sélectionnées
        filtered = filtered.filter(rea => {
          const isRealisateur = rea.ba && rea.security_social_number
          const isPool = !(rea.ba && rea.security_social_number)
          
          return (this.showRealisateurs && isRealisateur) || (this.showPool && isPool)
        })
      }
      
      // Filtrer par nom
      if (this.nameFilterValue) {
        filtered = filtered.filter(rea => 
          rea.value.toLowerCase().includes(this.nameFilterValue.toLowerCase())
        )
      }

      if (this.selectedDepart.length > 0) {
        filtered = filtered.filter(rea => 
          this.selectedDepart.includes(rea.filiere)
        )
      }
      
      this.filteredReas = filtered
    },
  }
}
</script>

<style scoped>
.filterRow {
  margin-top: 30px;
  margin-bottom: 20px; 
  justify-content: center; 
  align-items: center;
}
</style>