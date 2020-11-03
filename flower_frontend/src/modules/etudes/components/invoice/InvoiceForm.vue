<template>
  <el-form
    :model="value"
    label-position="left"
    label-width="30%"
  >
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="Exercice comptable">
          <el-input
            v-model="value.accountingPeriod"
            :class="{'error': errors.accountingPeriod }"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="Numéro de la facture">
          <el-input
            v-model="value.invoiceNumber"
            :class="{'error': errors.invoiceNumber }"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Facture émise pour"
          label-width="15%"
        >
          <el-autocomplete
            v-model="value.autocompletePayee"
            :class="{'error': errors.payee }"
            class="inline-input"
            :fetch-suggestions="querySearchProspects"
            placeholder="Entrez le nom du prospect"
            @select="handleSelectPayee"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="Date d'émission">
          <el-date-picker
            v-model="value.issueDate"
            :class="{'error': errors.issueDate }"
            format="dd-MM-yyyy"
            value-format="yyyy-MM-dd"
            type="date"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="Date de versement">
          <el-date-picker
            v-model="value.paymentDate"
            :class="{'error': errors.paymentDate }"
            format="dd-MM-yyyy"
            value-format="yyyy-MM-dd"
            type="date"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="Type de la facture">
          <el-select
            v-model="value.invoiceType"
            :class="{'error': errors.invoiceType }"
          >
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
        >
          <el-input
            v-model="value.description"
            :class="{'error': errors.description }"
          />
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
      <el-col :span="24">
        <el-form-item
          label="Catégorie"
          label-width="15%"
        >
          <el-input
            v-model="detail.category"
            :class="{'error': errors.category }"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Description"
          label-width="15%"
        >
          <el-input
            v-model="detail.description"
            :class="{'error': errors.description }"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="Prix HT">
          <el-input
            v-model="detail.taxFreeAmount"
            :class="{'error': errors.taxFreeAmount }"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="TVA">
          <el-input
            v-model="detail.taxes"
            :class="{'error': errors.taxes }"
          />
        </el-form-item>
      </el-col>
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
      @click="$emit('save')"
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
    prospects: { type: Array, required: true },
    errors: { type: Object, required: true }
  },
  watch: {
  },
  methods: {
    addDetail () {
      this.value.details.push({
        invoice: this.value.id
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
          `${this.$server_url}/tresorerie/factures/detail/${detailId}`,
          {withCredentials: true}
        ).then(() => {
          this.$message({message: "Ligne supprimée de la facture.",
            type: "success",
            offset: 40})
          this.value.details.splice(
            index,
            1
          )
        }).
          catch((err) => {
            console.error(err)
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

<style scoped>
::v-deep .error .el-input__inner {
    @apply border-2 border-red-600;
}
</style>
