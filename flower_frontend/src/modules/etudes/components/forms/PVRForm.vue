<template>
  <el-form
    label-width="30%"
    label-position="left"
  >
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="Type de PVR">
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
        <el-form-item label="Date de signature">
          <el-date-picker
            v-model="value.signingDate"
            format="dd-MM-yyyy"
            value-format="yyyy-MM-dd"
            type="date"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="Signataire Junior">
          <MemberPicker
            v-model="value.signer1"
            :item-list="members"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="Signataire Prospect">
          <MemberPicker
            v-model="value.signer2"
            :item-list="employees"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Description des livrables"
          label-width="auto"
        >
          <el-input
            v-model="value.deliverable"
            type="textarea"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item label-width="0">
          <el-button
            :loading="loading"
            icon="el-icon-plus"
            type="success"
            @click="$emit('save')"
          >
            Enregistrer le PVR
          </el-button>
        </el-form-item>
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
      employees: []
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
        `${this.$server_url}/membres`,
        {withCredentials: true}
      ).then((res) => {
        res.data.forEach((elt) => elt.value = `${elt.firstname} ${elt.lastname}`)
        this.members = res.data
      }).
        catch((err) => {
          console.log(err)
          this.$message({message: "Impossible de récupérer la liste des Membres",
            type: "error",
            offset: 40})
        })
    },
    getEmployees (prospectId) {
      axios.get(
        `${this.$server_url}/prospects/${prospectId}/employes/`,
        {withCredentials: true}
      ).then((res) => {
        res.data.forEach((elt) => elt.value = `${elt.firstname} ${elt.lastname}`)
        this.employees = res.data
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error",
            offset: 40})
        })
    }
  }
}
</script>

<style>

</style>
