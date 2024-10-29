<template>
  <el-form
    ref="PVRFormRef"
    :model="value"
    :rules="formRules"
    label-width="30%"
    label-position="left"
  >
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item
          label="Type de PVR"
          prop="documentType"
        >
          <el-select v-model="value.documentType">
            <el-option
              value="I"
              label="PVRI"
            />
            <el-option
              value="F"
              label="PVRF"
            />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Date de signature"
          prop="signingDate"
        >
          <el-date-picker
            v-model="value.signingDate"
            format="DD-MM-YYYY"
            value-format="YYYY-MM-DD"
            type="date"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Durée de garantie"
          prop="guaranteeDuration"
        >
          <el-input-number
            v-model="guaranteeDuration"
            controls-position="right"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Signataire Junior"
          prop="signer1"
        >
          <MemberPicker
            v-model="value.signer1"
            :item-list="members"
            placeholder="Signataire Junior"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Signataire Prospect"
          prop="signer2"
        >
          <MemberPicker
            v-model="value.signer2"
            :item-list="employees"
            placeholder="Signataire Prospect"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Description des livrables"
          prop="deliverable"
        >
          <el-input
            v-model="value.deliverable"
            type="textarea"
            placeholder="Décrire les livrables."
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-button
          :loading="loading"
          icon="el-icon-plus"
          type="success"
          @click="validateForm"
        >
          Enregistrer le PVR
        </el-button>
      </el-col>
    </el-row>
  </el-form>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"

const axios = require("axios")

export default {
  name: "PVRForm",
  components: {MemberPicker},
  props: {
    value: { type: Object, required: true },
    etude: { type: Object, required: true },
    loading: { type: Boolean, required: true }
  },
  data () {
    return {
      members: [],
      employees: [],
      guaranteeDuration: 90,
      formRules: {
        documentType: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        signingDate: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        guaranteeDuration: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        signer1: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        signer2: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        deliverable: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ]
      }
    }
  },
  watch: {
    etude () {
      if (this.etude) {
        this.getEmployees(this.etude.prospect.id)
      }
    }
  },
  created () {
    this.getMembers()
  },
  methods: {
    getMembers () {
      axios.get(
        "/api/membres",
        {withCredentials: true}
      ).then((res) => {
        res.data.forEach((elt) => elt.value = `${elt.firstname} ${elt.lastname}`)
        this.members = res.data
      }).catch(() => {
        this.$message({message: "Impossible de récupérer la liste des Membres",
          type: "error",
          offset: 40})
      })
    },
    validateForm () {
      this.value.guaranteeDuration = this.guaranteeDuration
      this.$refs.PVRFormRef.validate((r) => {
        if(r) {
          this.$emit("save")
        } else {
          this.$message({
            message: "Certains champs ne sont pas valides !",
            type:"error",
            offset: 40
          })
        }
      })
    },
    getEmployees (prospectId) {
      axios.get(
        `/api/prospects/${prospectId}/employes/`,
        {withCredentials: true}
      ).then((res) => {
        res.data.forEach((elt) => elt.value = `${elt.firstname} ${elt.lastname}`)
        this.employees = res.data
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer les employés : "+err,
          type: "error",
          offset: 40})
      })
    }
  },
}
</script>
