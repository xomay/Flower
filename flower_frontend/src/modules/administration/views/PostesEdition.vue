<template>
  <BaseComponent
    title="Édition des postes"
    :breadcrumb="breadcrumb"
  >
    <el-col
      v-for="(poste, index) in postes"
      :key="index"
      style="margin-bottom: 20px"
    >
      <el-col :span="1">
        Nom :
      </el-col>
      <el-col :span="5">
        <el-input
          v-model="poste.name"
          type="text"
          style="margin-top: -6px"
          @input="poste.isModified = true"
        />
      </el-col>
      <el-col
        :span="2"
        style="margin-left: 12px"
      >
        , au féminin :
      </el-col>
      <el-col :span="5">
        <el-input
          v-model="poste.name_feminine"
          type="text"
          placeholder="Identique au nom masculin"
          style="margin-top: -6px"
          @input="poste.isModified = true"
        />
      </el-col>
      <el-col
        :span="1"
        style="padding-left: 12px; margin-right: -8px;"
      >
        =>
      </el-col>
      <el-col :span="7">
        <el-select
          v-model="poste.subordinates"
          class="w-full"
          multiple
          placeholder="Subordonnés"
          style="margin-top: -6px"
          @change="poste.isModified = true"
        >
          <el-option
            v-for="(subordinate, index_s) in postes"
            :key="index_s"
            :label="subordinate.name"
            :value="subordinate.id"
          />
        </el-select>
      </el-col>
      <el-col :span="1">
        <el-button
          icon="el-icon-check"
          style="margin-left: 8px; margin-top: -6px"
          :loading="loading"
          :disabled="poste.isModified == false"
          :plain="poste.isModified == false"
          type="success"
          @click="savePoste(poste)"
        />
      </el-col>
      <el-col :span="1">
        <el-button
          icon="el-icon-delete"
          style="color: red; margin-top: -6px"
          :loading="loading"
          @click="removePoste(poste, index)"
        />
      </el-col>
    </el-col>
    <el-button
      icon="el-icon-plus"
      type="success"
      :loading="loading"
      @click="addPoste()"
    >
      Ajouter un poste
    </el-button>
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
      postes: []
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