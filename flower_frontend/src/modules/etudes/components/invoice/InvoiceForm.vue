<template>
  <el-form
    ref="refFacture"
    :model="value"
    label-position="left"
    label-width="30%"
    :rules="formRules"
  >
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item
          label="Exercice comptable"
          prop="accountingPeriod"
        >
          <el-input-number
            v-model="value.accountingPeriod"
            controls-position="right"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Numéro de la facture"
          prop="invoiceNumber"
        >
          <el-input v-model="value.invoiceNumber">
            <template slot="prepend">
              {{ value.invoiceType }}_
            </template>
          </el-input>
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Facture émise pour"
          label-width="15%"
          prop="autocompletePayee"
        >
          <el-autocomplete
            v-model="value.autocompletePayee"
            class="inline-input"
            :fetch-suggestions="querySearchProspects"
            placeholder="Entrez le nom du prospect"
            @select="handleSelectPayee"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Date d'émission"
          prop="issueDate"
        >
          <el-date-picker
            v-model="value.issueDate"
            format="dd-MM-yyyy"
            value-format="yyyy-MM-dd"
            placeholder="Date d'émission"
            type="date"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Date de versement"
          prop="paymentDate"
        >
          <el-date-picker
            v-model="value.paymentDate"
            format="dd-MM-yyyy"
            value-format="yyyy-MM-dd"
            placeholder="Date de paiement"
            type="date"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Type de la facture"
          prop="invoiceType"
        >
          <el-select v-model="value.invoiceType">
            <el-option
              value="FA"
              label="Facture d'Achat"
            />
            <el-option
              value="FVA"
              label="Facture d'Acompte"
            />
            <el-option
              value="FVS"
              label="Facture de Solde"
            />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Objet de la facture"
          label-width="15%"
          prop="description"
        >
          <el-input v-model="value.description" />
        </el-form-item>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="24">
        <span class="mr-2">Détails</span><el-button
          type="text"
          icon="el-icon-plus"
          @click="addDetail"
        >
          Ajouter un détail
        </el-button>
      </el-col>
    </el-row>
    <el-row
      v-for="(detail, index) in value.details"
      :key="index"
      :gutter="20"
    >
      <!-- DETAILS -->
      <el-form
        ref="refFactureDetails"
        :model="detail"
      >
        <el-col :span="24">
          <el-form-item
            label="Description"
            label-width="15%"
            prop="description"
            :rules="[{required: true, message: 'Obligatoire', trigger: 'blur'}]"
          >
            <el-input v-model="detail.description" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item
            label="Prix HT"
            prop="taxFreeAmount"
            :rules="[
              {required: true, pattern: /^[0-9]+(|.[0-9]+)$/, message: 'Entrez un prix valide.', trigger: 'change'},
              {required: true, message: 'Obligatoire', trigger: 'change'}
            ]"
          >
            <el-input
              v-model="detail.taxFreeAmount"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item
            label="TVA"
            prop="taxes"
            :rules="[
              {required: true, pattern: /^0.[0-9]+$/, message: 'Entrez un pourcentage valide.', trigger: 'change'},
              {required: true, message: 'Obligatoire', trigger: 'change'}
            ]"
          >
            <el-input
              v-model="detail.taxes"
            />
          </el-form-item>
        </el-col>
      </el-form>
      <el-col :span="24">
        <el-form-item label-width="0">
          <el-button
            type="danger"
            @click="removeDetail(index, detail.id)"
          >
            Supprimer
          </el-button>
        </el-form-item>
      </el-col>
      <el-col>
        <el-divider />
      </el-col>
    </el-row>
    <el-button
      type="success"
      :loading="loading"
      @click="validateForm"
    >
      Enregistrer la facture
    </el-button>
  </el-form>
</template>

<script>
const axios = require("axios")

export default {
  name: "InvoiceForm",
  props: {
    value: { type: Object, required: true },
    loading: { type: Boolean, required: true },
    prospects: { type: Array, required: true }
  },
  data () {
    return {
      formRules: {
        invoiceNumber: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        accountingPeriod: [
          {required: true, message: "Obligatoire", trigger: "blur"},
          {
            required: true,
            pattern: /^20[0-9]{2}$/,
            message: "Entrez une année cohérente.",
            trigger: "change"
          }
        ],
        autocompletePayee: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        issueDate: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        paymentDate: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        invoiceType: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        description: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ]
      }
    }
  },
  methods: {
    validateForm () {
      var result = true
      this.$refs.refFacture.validate(r => result = r)
      if(this.$refs.refFactureDetails != undefined) { // C'est undefined avant d'avoir ajouté des détails.
        this.$refs.refFactureDetails.forEach(f => {
          f.validate(r => result = (r ? result : false))
        })
      }
      if(result) {
        this.$emit("save")
      } else {
        this.$message({message: "Le formulaire contient des erreurs.", type:"error", offset:40})
      }
    },
    addDetail () {
      this.value.details.push({
        invoice: this.value.id,
        taxes: 0.2
      })
    },
    removeDetail (index, detailId) {
      if (!detailId) {
        this.value.details.splice(
          index,
          1
        )
      } else {
        axios.delete(
          `/api/tresorerie/factures/detail/${detailId}`,
          {withCredentials: true}
        ).then(() => {
          this.$message({message: "Ligne supprimée de la facture.",
            type: "success",
            offset: 40})
          this.value.details.splice(
            index,
            1
          )
        }).catch((err) => {
          this.$message({message: "Impossible de supprimer la ligne de la facture : " + err,
            type: "error",
            offset: 40})
        })
      }
    },
    querySearchProspects (queryString, cb) {
      const results = queryString ? this.prospects.filter((prospect) => prospect.name.toLowerCase().includes(queryString.toLowerCase())) : this.prospects
      results.forEach((result) => result.value = result.name)
      cb(results)
    },
    handleSelectPayee (prospect) {
      this.value.payee = prospect.id
    }
  }
}
</script>
