<template>
  <BaseComponent
    title="Édition des postes"
    :breadcrumb="breadcrumb"
  >
    <template #action>
      <el-button
        icon="Plus"
        type="success"
        :loading="loading"
        @click="addPoste()"
      >
        Ajouter un poste
      </el-button>
    </template>
    
    <el-table
      :data="postes"
      :loading="loading"
      class="grid"
      :stripe="true"
    >
      <el-table-column
        label="Nom du poste"
        prop="name"
        width="200"
      >
        <template #default="{row}">
          <el-input
            v-model="row.name"
            placeholder="Nom du poste"
            @input="row.isModified = true"
          />
        </template>
      </el-table-column>
      
      <el-table-column
        label="Nom au féminin"
        prop="name_feminine"
        width="200"
      >
        <template #default="{row}">
          <el-input
            v-model="row.name_feminine"
            placeholder="Identique au nom masculin"
            @input="row.isModified = true"
          />
        </template>
      </el-table-column>
      
      <el-table-column
        label="Subordonnés"
        prop="subordinates"
        min-width="150"
      >
        <template #default="{row}">
          <el-select
            v-model="row.subordinates"
            class="w-full"
            multiple
            placeholder="Sélectionner les subordonnés"
            @change="row.isModified = true"
          >
            <el-option
              v-for="subordinate in postes"
              :key="subordinate.id"
              :label="subordinate.name"
              :value="subordinate.id"
              :disabled="subordinate.id === row.id"
            />
          </el-select>
        </template>
      </el-table-column>

      <el-table-column
        label="Rôles"
        prop="roles"
        min-width="150"
      >
        <template #default="{row}">
          <el-select
            v-model="row.role"
            class="w-full"
            multiple
            placeholder="Sélectionner les rôles"
            @change="row.isModified = true"
            >
            <el-option
              v-for="role in roles"
              :key="role.id"
              :label="role.name"
              :value="role.name"
            />
          </el-select>
        </template>
      </el-table-column>
      
      <el-table-column
        label=""
        width="60"
        align="center"
      >
        <template #default="{row, $index}">
          <el-button
            icon="Check"
            :loading="loading"
            :disabled="!row.isModified"
            :type="row.isModified ? 'success' : 'info'"
            :plain="!row.isModified"
            @click="savePoste(row)"
          />
        </template>
      </el-table-column>
      <el-table-column
        label=""
        width="60"
        align="center"
      >
        <template #default="{row, $index}">
          <el-button
            icon="Delete"
            type="danger"
            :loading="loading"
            @click="removePoste(row, $index)"
          />
        </template>
      </el-table-column>
    </el-table>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
export default {
  name: "PostesEdition",
  data () {
    return {
      breadcrumb: [
        {
          name: "Liste des postes",
          link: "/administration/postes"
        }
      ],
      loading: true,
      postes: [],
      roles: [{id:1, name:"ROLE_ADMIN"}, {id:2, name:"ROLE_BUREAU"}, {id:3, name:"ROLE_CA"}, {id:4, name:"ROLE_QUALI"}, {id:5, name:"ROLE_SUIVEUR"}, {id:6, name:"ROLE_TRESO"}]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/administration/postes/",
      { withCredentials: true }
    ).then((res) => {
      res.data.forEach(elt => elt.isModified = false)
      this.postes = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les postes : " + err, type: "error"})
    }).finally(() => this.loading = false)
  },
  methods: {
    nameOfPoste (poste_id) {
      const found = this.postes.find(p => p.id === poste_id)
      return found == undefined ? "undefined" : found.name
    },
    savePoste (poste) {
      this.loading = true
      axios.put(
        `/api/administration/postes/${poste.id}/`,
        poste,
        { withCredentials: true }
      ).then(() => {
        this.$message({message: "Poste mis à jour avec succès.", type: "success"})
        poste.isModified = false
      }).catch((err) => {
        this.$message({message: "Impossible de sauvegarder le poste : " + err, type: "error"})
      }).finally(() => this.loading = false)
    },
    removePoste (poste, index) {
      this.loading = true
      axios.delete(
        `/api/administration/postes/${poste.id}/`,
        { withCredentials: true }
      ).then(() => {
        this.$message({message: "Poste supprimé avec succès.", type: "success"})
        this.postes.splice(index, 1)
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer le poste : " + err, type: "error"})
      }).finally(() => this.loading = false)
    },
    addPoste () {
      this.loading = true
      const newPoste = {
        name: "<poste>",
          role: [],
      }
      axios.post(
        "/api/administration/postes/",
        newPoste,
        { withCredentials: true }
      ).then((res) => {
        this.$message({message: "Poste ajouté avec succès.", type: "success"})
        res.data.name_feminine = undefined
        this.postes.push(res.data)
      }).catch((err) => {
        this.$message({message: "Impossible de créer un poste : " + err, type: "error"})
      }).finally(() => this.loading = false)
    }
  }
}
</script>