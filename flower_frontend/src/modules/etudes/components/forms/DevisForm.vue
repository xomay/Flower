<template>
  <el-form
    :model="pc"
    ref="pcForm"
    :rules="formRules"
    label-position="left"
  >
    <el-form-item
      label="Acompte"
      label-width="140px"
      style="margin-top: 30px;"
    >
      <el-checkbox v-model="pc.deposit" />
    </el-form-item>
    <el-form-item
      label="Pourcentage acompte"
      label-width="140px"
      style="margin-bottom: 40px;"
    >
      <el-input-number
        v-model="pc.depositAmount"
        controls-position="right"
        :min=0
        :max=100
        :disabled="!pc.deposit"
      />
    </el-form-item>
    <el-form-item
      label="Montant des frais"
      label-width="140px"
      prop="application_fees"
    >
      <el-input-number
        v-model="pc.application_fees"
        controls-position="right"
        :min=0
        :max=500
      />
    </el-form-item>
    <el-col :span="24" v-if="etude.prospect">
      <el-form-item
        label="Adresse"
        prop="address"
        label-width="140px"
      >
        <el-input v-model="pc.address" />
      </el-form-item>
    </el-col>
    <el-row v-if="etude.prospect">
      <el-col :span="12">
        <el-form-item
          label="Code postal"
          prop="postcode"
          label-width="140px"
          >
          <el-input v-model="pc.postcode" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Ville"
          prop="town"
          label-width="140px"
          disabled="true"
          :style="'margin-left: 20px'"
          >
          <el-input v-model="pc.town" />
        </el-form-item>
      </el-col>
    </el-row>
    <el-form-item 
      label="Contexte et objectifs de l'étude" 
      prop="deliverable"
      label-width="140px">
      <el-input
        v-model="pc.description"
        type="textarea"
        :rows="7"
        placeholder="Description concise de l’entreprise et de l’activité du client dans un premier paragraphe. (5-6 lignes)
Description du contexte du client et des raisons qui l’amène à l’émission de cette CC en un ou deux paragraphes.
Présentation de la solution livrée au client."
      />
    </el-form-item>
    <el-form-item 
      label="Description du livrable" 
      prop="deliverable"
      label-width="140px">
      <el-input
        v-model="pc.deliverable"
        type="textarea"
        :rows="7"
        placeholder="Description du livrable de l'étude"
      />
    </el-form-item>
    <el-form-item>
      <el-button
        type="success"
        @click="savePC"
      >
        Enregistrer
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;
export default {
  name: "DevisForm",
  props: {
    etude: { type: Object, required: true }
  },
  data () {
    return {
      pc: {},
      autocomplete: {},
      members: [],
      employees: [],
      formRules: {
        signDate: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        address: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        postcode: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        town: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        deliverable: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        application_fees: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
      }
    }
  },
  watch: {
    etude () {
      this.getPC(this.etude.id)
      this.getEmployees(this.etude.prospect.id)
    },
  },
  created () {
    this.getMembers()
  },
  methods: {
    savePC () {
      this.pc.signDate = new Date()
      this.etude.prospect.address = this.pc.address
      this.etude.prospect.postcode = this.pc.postcode
      this.etude.prospect.town = this.pc.town
      this.etude.application_fees = this.pc.application_fees
      axios.put(
        `/api/etudes/${this.$route.params.id}/ce/`,
        {
          signDate: this.pc.signDate,
          deposit: this.pc.deposit,
          depositAmount: this.pc.depositAmount,
          deliverable: this.pc.deliverable,
          description: this.pc.description,
          signer1: this.etude.docEtude.signer1.id,
          signer2: this.etude.docEtude.signer2.id,
          id: this.pc.id,
        },
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "La PC a bien été mise à jour", type: "success"})
        axios.put(
          `/api/prospects/${this.etude.prospect.id}/`,
          {
            address: this.pc.address,
            postcode: this.pc.postcode,
            town: this.pc.town,
            name: this.etude.prospect.name,
            id: this.etude.prospect.id
          },
          {withCredentials: true}
        ).then(() => {
          axios.put(
            `/api/etudes/${this.$route.params.id}/`,
            {
              prospect: this.etude.prospect.id,
              application_fees: this.etude.application_fees,
              confidential: this.etude.confidential,
              name: this.etude.name,
              description: this.etude.description,
              mandat: this.etude.mandat,
              number: this.etude.number,
              id: this.etude.id
            },
            {withCredentials: true}
          ).then(() => {
            this.$router.push(`/etudes/${this.$route.params.id}/voir`)
          }).catch((err) => {
            this.$message({message: "Impossible de sauvegarder la PC : "+err, type: "error"})
          })
        }).catch((err) => {
          this.$message({message: err, type: "error"})
        }).finally(() => {
          this.loading = false
        })
      }).catch((err) => {
        this.$message({message: "Impossible de sauvegarder la PC : "+err, type: "error"})
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
    personFullname (person) {
      if (person) {
        return `${person.firstname} ${person.lastname}`
      }
      return ""
    },
    getPC (projectId) {
      axios.get(
        `/api/etudes/${projectId}/ce/`,
        {withCredentials: true}
      ).then((res) => {
        this.pc = res.data
        this.pc.address = this.etude.prospect.address
        this.pc.postcode = this.etude.prospect.postcode
        this.pc.town = this.etude.prospect.town
        this.pc.prospect = this.etude.prospect.id
        this.pc.application_fees = Number(this.etude.application_fees)
        this.autocomplete = {signer1: this.personFullname(this.pc.signer1),
          signer2: this.personFullname(this.pc.signer2)}
        this.pc.signer1 = this.pc.signer1 ? this.pc.signer1.id : null
        this.pc.signer2 = this.pc.signer2 ? this.pc.signer2.id : null
      }).catch((err) => {
        this.$message({message: err, type: "error"})
      })
    }
  }
}
</script>
