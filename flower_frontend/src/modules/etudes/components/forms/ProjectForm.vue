<template>
  <el-form
    ref="formProject"
    :model="modelValue"
    :rules="formRules"
    label-position="left"
  >
    <el-form-item
      label="Type d'étude"
      prop="docType"
      label-width="140px">
      <el-radio-group 
        v-model="modelValue.docType" 
        size="large" 
        @change="onDocTypeChange"
        :max="1">
        <el-radio-button label="Convention d'Étude" value="ce" border>
          <el-icon><Document /></el-icon>
          Convention d'Étude
        </el-radio-button>
        <el-radio-button label="Bon de Commande" value="bc" border>
          <el-icon><DocumentCopy /></el-icon>
          Bon de Commande
        </el-radio-button>
      </el-radio-group>
    </el-form-item>
    <el-form-item 
      label="Réf de la CC"
      v-if="modelValue.docType === 'bc'"
      prop="cc"
      label-width="140px">
      <el-autocomplete
        v-model="cc_number"
        class="inline-input"
        :fetch-suggestions="querySearchCC"
        placeholder="Entrez la référence de la Convention Cadre"
        @select="handleSelectCC"
        @change="updateEmployes(true)"
      />
    </el-form-item>
    <el-form-item
      label="Prospect"
      v-if="modelValue.docType === 'ce'"
      prop="prospect"
      label-width="140px"
    >
      <MemberPicker
        v-model="modelValue.prospect"
        :item-list="prospects"
        placeholder="Prospect"
        @update:modelValue="updateEmployes(true)"
        @clear="clearEmploye"/>
    </el-form-item>
    <el-form-item
      label="Contact client"
      prop="clientContact"
      label-width="140px"
    >
      <MemberPicker
        ref="employesInput"
        v-model="modelValue.clientContact"
        :item-list="employes"
        placeholder="Contact client"/>
    </el-form-item>
    <el-form-item
      label="Nom de l'étude"
      prop="name"
      label-width="140px"
    >
      <el-input
        v-model="modelValue.name"
        :placeholder="modelValue.docType === 'ce' ? 'Entrez le nom de la future étude' : 'Entrez le nom de la future étude (Ex : Amphiv BC1)'"
      />
    </el-form-item>
    <el-form-item
      :label="modelValue.docType === 'ce' ? 'Présentation de l\'étude' : 'Présentation du Bon de Commande'"
      prop="description"
      label-width="140px"
    >
      <el-input
        v-model="modelValue.description"
        type="textarea"
        placeholder="Description succincte de l'étude"
        :rows="5"
      />
    </el-form-item>
    <el-row>
      <el-col :span="12">
        <el-form-item
          label="Mandat"
          prop="mandat"
          label-width="140px"
        >
          <el-input-number
            v-model="modelValue.mandat"
            controls-position="right"
            :min="2020"
            :max="2050"
            @change="mandatEdited"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          :label="modelValue.docType === 'ce' ? 'Numéro de l\'étude' : 'Référence du BC'"
          prop="number"
          label-width="140px"
        >
          <el-input-number
            v-model="modelValue.number"
            controls-position="right"
            :min="21000"
            :max="50000"
          />
        </el-form-item>
      </el-col>
    </el-row>
    <el-form-item
      label="Confidentialité"
      prop="confidential"
      label-width="140px"
    >
      <el-checkbox v-model="modelValue.confidential" />
    </el-form-item>
    <el-form-item
      label="Suiveur de projet"
      prop="projectManager"
      label-width="140px"
    >
      <MemberPicker
        v-model="modelValue.projectManager"
        :item-list="members"
        placeholder="Suiveur de projet"/>
    </el-form-item>
    <el-form-item
      label="Suiveur qualité"
      prop="qualityManager"
      label-width="140px"
    >
      <MemberPicker
        v-model="modelValue.qualityManager"
        :item-list="members"
        placeholder="Suiveur qualité"/>
    </el-form-item>
    <el-form-item>
      <el-button
        :loading="loading"
        icon="Plus"
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
    modelValue: { type: Object, required: true },
    loading: { type: Boolean, required: true },
    members: { type: Array, required: true },
    prospects: { type: Array, required: true },
    takenIds: { type: Array, default () { return [] } }
  },
  emits: ["update:modelValue", "save"],
  data () {
    return {
      employes: [],
      cc_number: "",
      cc: {},
      formRules: {
        docType: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        cc: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
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
      if (this.modelValue.cc) {
        this.getCC(this.modelValue.cc)
      }
      this.updateEmployes(false)
    },
  },
  created () {
    this.getCCList()
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
    onDocTypeChange () {
      this.modelValue.cc = ""
      this.cc_number = ""
      this.modelValue.prospect = null
      this.modelValue.clientContact = null
      this.modelValue.name = ""
      this.modelValue.confidential = false
      this.modelValue.description = ""
      this.modelValue.projectManager = null
      this.modelValue.qualityManager = null
      this.employes = []
    },
    getCCList () {
      axios.get(
        "/api/etudes/cc/",
        {withCredentials: true}
      ).then((res) => {
        this.ccs = res.data
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error",
            offset: 40})
        })
    },
    querySearchCC (queryString, cb) {
      const results = queryString ? this.ccs.filter((cc) => String(this.ccNumber(cc)).
        includes(queryString)) : this.ccs
      results.forEach((result) => result.value = this.ccNumber(result))
      cb(results)
    },
    handleSelectCC (cc) {
      this.modelValue.cc = cc.id
      this.getCC(cc.id)
    },
    ccNumber(cc){
      if (cc){
        return cc.number
      }else {
        return ""
      }
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
        this.modelValue.clientContact = ""
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
      this.modelValue.clientContact = ""
    },
    getCC (ccId) {
      if(ccId){
        axios.get(
          `/api/etudes/${ccId}/cc/`,
          {withCredentials: true}
        ).then((res) => {
          this.cc = res.data
          this.modelValue.prospect = this.cc.prospect.id
          this.updateEmployes(false)
          //this.modelValue.clientContact = this.cc.signer2.id
          //this.modelValue.name = this.cc.name
          this.modelValue.confidential = this.cc.confidential
          this.cc_number = this.cc.number
        }).catch((err) => {
          this.$message({message: err, type: "error"})
        })
      }
    }
  }
}
</script>
