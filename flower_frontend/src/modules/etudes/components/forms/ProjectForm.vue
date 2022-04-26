<template>
  <el-form
    ref="formProject"
    :model="value"
    :rules="formRules"
    label-position="left"
  >
    <el-form-item
      label="Prospect"
      prop="prospect"
      label-width="140px"
    >
      <MemberPicker
        v-model="value.prospect"
        :item-list="prospects"
        placeholder="Prospect"
        @input="updateEmployes(true)"
        @clear="clearEmploye()"
      />
    </el-form-item>
    <el-form-item
      label="Contact client"
      prop="clientContact"
      label-width="140px"
    >
      <MemberPicker
        ref="employesInput"
        v-model="value.clientContact"
        :item-list="employes"
        placeholder="Contact client"
      />
    </el-form-item>
    <el-form-item
      label="Nom de l'étude"
      prop="name"
      label-width="140px"
    >
      <el-input
        v-model="value.name"
        placeholder="Entrez le nom de la future étude"
      />
    </el-form-item>
    <el-form-item
      label="Présentation de l'étude"
      prop="description"
      label-width="140px"
    >
      <el-input
        v-model="value.description"
        type="textarea"
        placeholder="Description succincte de l'étude"
      />
    </el-form-item>
    <el-form-item
      label="Type de contrat"
      prop="contractType"
      label-width="140px"
    >
      <el-select v-model="value.contractType">
        <el-option value="CE">
          Convention étude
        </el-option>
        <el-option value="CCA">
          Convention cadre agile
        </el-option>
      </el-select>
    </el-form-item>
    <el-col :span="12">
      <el-form-item
        label="Mandat"
        prop="mandat"
        label-width="140px"
      >
        <el-input-number
          v-model="value.mandat"
          controls-position="right"
          :min="2020"
          :max="2050"
          @change="mandatEdited"
        />
      </el-form-item>
    </el-col>
    <el-col :span="12">
      <el-form-item
        label="Numéro de l'étude"
        prop="number"
        label-width="140px"
      >
        <el-input-number
          v-model="value.number"
          controls-position="right"
          :min="21000"
          :max="50000"
        />
      </el-form-item>
    </el-col>
    <el-form-item
      label="Confidentialité"
      prop="confidential"
      label-width="140px"
    >
      <el-checkbox v-model="value.confidential" />
    </el-form-item>
    <el-form-item
      label="Suiveur de projet"
      prop="projectManager"
      label-width="140px"
    >
      <MemberPicker
        v-model="value.projectManager"
        :item-list="members"
        placeholder="Suiveur de projet"
      />
    </el-form-item>
    <el-form-item
      label="Suiveur qualité"
      prop="qualityManager"
      label-width="140px"
    >
      <MemberPicker
        v-model="value.qualityManager"
        :item-list="members"
        placeholder="Suiveur qualité"
      />
    </el-form-item>
    <el-form-item>
      <el-button
        :loading="loading"
        icon="el-icon-plus"
        type="success"
        @click="validateForm"
      >
        Enregistrer l'étude
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"
const axios = require("axios")
export default {
  name: "ProjectForm",
  components: {MemberPicker},
  props: {
    value: { type: Object, required: true },
    loading: { type: Boolean, required: true },
    members: { type: Array, required: true },
    prospects: { type: Array, required: true },
    takenIds: { type: Array, default () { return [] } }
  },
  data () {
    return {
      employes: [],
      formRules: {
        prospect: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        clientContact: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        name: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        description: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        contractType: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        mandat: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        number: [
          {required: true, message: "Obligatoire", trigger: "blur"},
          {required: true, validator: this.checkNumber, trigger: "change"}
        ],
        confidential: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        projectManager: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        qualityManager: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ]
      }
    }
  },
  watch: {
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
      const lastNumber = this.value.number.toString().slice(-3)
      this.value.number = parseInt(lastYear+lastNumber)
    },
    updateEmployes (remove) {
      if(remove) {
        this.value.clientContact = ""
      }
      if(this.value.prospect != undefined && this.value.prospect > 0) {
        axios.get(
          `/api/prospects/${this.value.prospect}/employes/`,
          { withCredentials: true }
        ).then((res) => {
          res.data.forEach((elt) => elt.value = `${elt.firstname} ${elt.lastname}`)
          this.employes = res.data
          if(this.employes.length == 0)
            this.$message({message: "Ce prospect n'a aucun employé...", trype: "warning"})
        }).catch((err) => {
          this.$message({message: "Impossible de récupérer les employés de ce prospect : " + err, type: "error"})
        })
      }
    },
    clearEmploye () {
      this.$refs.employesInput.clear()
      this.value.clientContact = ""
    }
  }
}
</script>
