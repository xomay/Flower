<template>
  <el-form
    ref="formProject"
    :model="modelValue"
    :rules="formRules"
    label-position="left"
  >
    <el-form-item
      label="Prospect"
      prop="prospect"
      label-width="150px"
    >
      <MemberPicker
        v-model="modelValue.prospect"
        :item-list="prospects"
        placeholder="Prospect"
        @clear="clearEmploye()"/>
    </el-form-item>
    <el-form-item
      label="Signataire prospect"
      prop="signer2"
      label-width="150px"
    >
      <MemberPicker
        ref="employesInput"
        v-model="modelValue.signer2"
        :item-list="employes"
        placeholder="Entrez le nom du signataire du prospect"/>
    </el-form-item>
    <el-form-item
      label="Signataire Junior"
      prop="signer1"
      label-width="150px"
    >
      <MemberPicker
        v-model="modelValue.signer1"
        :item-list="members"
        placeholder="Entrez le nom du signataire de la junior"/>
    </el-form-item>
    <el-form-item
      label="Nom de l'étude"
      prop="name"
      label-width="150px"
    >
      <el-input
        v-model="modelValue.name"
        placeholder="Entrez le nom de la future étude"
      />
    </el-form-item>
    <el-form-item
      label="Présentation du contexte et objectifs de l'étude"
      prop="description"
      label-width="150px"
    >
      <el-input
        v-model="modelValue.description"
        type="textarea"
        placeholder="Définir la raison de la collaboration et ses objectifs"
        :rows="6"
      />
    </el-form-item>
    <el-row>
      <el-col :span="12">
        <el-form-item
          label="Numéro de la convention"
          prop="number"
          label-width="150px"
          style="margin-bottom: 30px"
        >
          <el-input-number
            v-model="modelValue.number"
            controls-position="right"
            :min="21000"
            :max="50000"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
        label="Période de validité (ans)"
        prop="period"
        label-width="150px"
        >
        <el-input-number
        v-model="modelValue.period"
        controls-position="right"
        :min="0"
        :max="5"
        />
      </el-form-item>
    </el-col>
    </el-row>
    <el-form-item
      label="Date de signature"
      prop="signDate"
      label-width="150px"
    >
      <el-date-picker
        v-model="modelValue.signDate"
        type="date"
        placeholder="Choisissez un jour"
      />
    </el-form-item>
    <el-form-item
      label="Confidentialité"
      prop="confidential"
      label-width="150px"
    >
      <el-checkbox v-model="modelValue.confidential" />
    </el-form-item>
    <el-form-item>
      <el-button
        :loading="loading"
        icon="Plus"
        type="success"
        @click="validateForm"
      >
        Enregistrer la convention
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"
const axios = require("axios")
export default {
  name: "ConventionCadreForm",
  components: {MemberPicker},
  props: {
    modelValue: { type: Object, required: true },
    loading: { type: Boolean, required: true },
    members: { type: Array, required: true },
    prospects: { type: Array, required: true },
    takenIds: { type: Array, default () { return [] } }
  },
  emits: ["save"],
  data () {
    return {
      employes: [],
      formRules: {
        prospect: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        signer2: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        signer1: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        name: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        description: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        mandat: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        number: [
          {required: true, message: "Obligatoire", trigger: "blur"},
          {required: true, validator: this.checkNumber, trigger: "change"}
        ],
        period: [
          {required: true, message: "Obligatoire", trigger: "blur"},
          {required: true, validator: this.checkNumber, trigger: "change"}
        ],
        signDate: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        confidential: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ]
      }
    }
  },
  watch: {
    'modelValue.prospect'(newVal, oldVal) {
      this.updateEmployes(true)
    },
    prospects () {
      this.updateEmployes(false)
    }
  },
  methods: {
    validateForm () {
      this.$refs.formProject.validate((r) => {
        if(r) {
          this.$emit("save")
        } else {
          this.$message({ message: "Le formulaire n'est pas valide.", type: "error" })
        }
      })
    },
    checkNumber (rule, value, callback) {
      if (this.takenIds.includes(value)) {
        callback(new Error("Ce nom d'étude est déjà pris."))
      } else {
        callback()
      }
    },
    mandatEdited (nv) {
      const lastYear = nv.toString().slice(-2)
      const lastNumber = this.modelValue.number.toString().slice(-3)
      this.modelValue.number = parseInt(lastYear+lastNumber)
    },
    updateEmployes (remove) {
      if(remove) {
        this.modelValue.clientSigner = ""
      }
      if(this.modelValue.prospect !== undefined && this.modelValue.prospect > 0) {
        axios.get(
          `/api/prospects/${this.modelValue.prospect}/employes/`,
          { withCredentials: true }
        ).then((res) => {
          res.data.forEach((elt) => elt.value = `${elt.firstname} ${elt.lastname}`)
          this.employes = res.data
          if(this.employes.length === 0)
            this.$message({message: "Ce prospect n'a aucun employé...", trype: "warning"})
        }).catch((err) => {
          this.$message({message: "Impossible de récupérer les employés de ce prospect : " + err, type: "error"})
        })
      }
    },
    clearEmploye () {
      this.$refs.employesInput.clear()
      this.modelValue.clientSigner = ""
    }
  }
}
</script>
