<template>
  <el-form
    :model="ce"
    label-position="left"
  >
    <el-form-item
      label="Signataire Junior"
      label-width="20%"
    >
      <el-autocomplete
        v-model="autocomplete.signer1"
        class="inline-input"
        :fetch-suggestions="querySearchMember"
        placeholder="Entrez le nom du signataire de la junior"
        @select="handleSelectSigner1"
      />
    </el-form-item>
    <el-form-item
      label="Signataire prospect"
      label-width="20%"
    >
      <el-autocomplete
        v-model="autocomplete.signer2"
        class="inline-input"
        :fetch-suggestions="querySearchEmployee"
        placeholder="Entrez le nom du signataire du prospect"
        @select="handleSelectSigner2"
      />
    </el-form-item>
    <el-form-item
      label="Date de signature"
      label-width="20%"
    >
      <el-date-picker
        v-model="ce.signDate"
        type="date"
        placeholder="Choisissez un jour"
      />
    </el-form-item>
    <el-form-item
      label="Acompte"
      label-width="20%"
    >
      <el-checkbox v-model="ce.deposit" />
    </el-form-item>
    <el-form-item
      label="Pourcentage acompte"
      label-width="20%"
    >
      <el-input-number
        v-model="ce.depositAmount"
        controls-position="right"
        :min="0"
        :max="100"
        :disabled="!ce.deposit"
      />
    </el-form-item>
    <el-form-item
      label="Nombre d'intervenants"
      label-width="20%"
    >
      <el-input-number
        v-model="ce.consultantNumber"
        controls-position="right"
        :min="1"
      />
    </el-form-item>
    <el-form-item label="Ouest INSA réalisera, pour le compte du Client, une étude consistant en">
      <el-input
        v-model="ce.description"
        type="textarea"
        :rows="4"
        placeholder="Description de la prestation proposée"
      />
    </el-form-item>
    <el-form-item>
      <el-button
        type="success"
        @click="saveCE"
      >
        Enregistrer
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
const axios = require("axios")
export default {
  name: "ConventionEtudeForm",
  props: {
    etude: { type: Object, required: true }
  },
  data () {
    return {
      ce: {},
      autocomplete: {},
      members: [],
      employees: []
    }
  },
  watch: {
    etude () {
      this.getCE(this.etude.id)
      this.getEmployees(this.etude.prospect.id)
    }
  },
  created () {
    this.getMembers()
  },
  methods: {
    handleSelectSigner1 (member) {
      this.ce.signer1 = member.id
    },
    querySearchMember (queryString, cb) {
      const results = queryString ? this.members.filter((member) => this.personFullname(member).toLowerCase().
        includes(queryString)) : this.members
      results.forEach((result) => result.value = this.personFullname(result))
      cb(results)
    },
    handleSelectSigner2 (employee) {
      this.ce.signer2 = employee.id
    },
    querySearchEmployee (queryString, cb) {
      const results = queryString ? this.employees.filter((employee) => this.personFullname(employee).toLowerCase().
        includes(queryString)) : this.employees
      results.forEach((result) => result.value = this.personFullname(result))
      cb(results)
    },
    personFullname (person) {
      if (person) {
        return `${person.firstname} ${person.lastname}`
      }
      return ""
    },
    saveCE () {
      axios.put(
        `/api/etudes/${this.$route.params.id}/ce/`,
        this.ce,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "La CE a bien été mis à jour", type: "success"})
        this.$router.push(`/etudes/${this.$route.params.id}/voir`)
      }).catch((err) => {
        this.$message({message: "Impossinle de sauvegarder la CE : "+err, type: "error"})
      })
    },
    getMembers () {
      axios.get(
        "/api/membres",
        {withCredentials: true}
      ).then((res) => {
        this.members = res.data
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error",
            offset: 40})
        })
    },
    getEmployees (prospectId) {
      axios.get(
        `/api/prospects/${prospectId}/employes/`,
        {withCredentials: true}
      ).then((res) => {
        this.employees = res.data
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error",
            offset: 40})
        })
    },
    getCE (projectId) {
      axios.get(
        `/api/etudes/${projectId}/ce/`,
        {withCredentials: true}
      ).then((res) => {
        this.ce = res.data
        this.autocomplete = {signer1: this.personFullname(this.ce.signer1),
          signer2: this.personFullname(this.ce.signer2)}
        this.ce.signer1 = this.ce.signer1 ? this.ce.signer1.id : null
        this.ce.signer2 = this.ce.signer2 ? this.ce.signer2.id : null
      }).catch((err) => {
        this.$message({message: err, type: "error"})
      })
    }
  }
}
</script>
