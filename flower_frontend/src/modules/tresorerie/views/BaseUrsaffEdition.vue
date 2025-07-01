<template>
  <BaseComponent
    title="Base Ursaff"
    :breadcrumb="breadcrumb"
  >
    <el-row style="margin-top: 12px;">
      Mandat actuel :
    </el-row>
    <el-row style="margin-top: 25px;">
      <el-form
        v-model="currentBase"
        label-position="left"
        :hide-required-asterisk="true"
      >
        <el-col :span="5">
          <el-form-item
            prop="mandat"
            label="Mandat :"
          >
            <el-input-number
              v-model="currentBase.mandat"
              :disabled="true"
              controls-position="right"
              :min="2021"
              :max="2100"
            />
          </el-form-item>
        </el-col>
        <el-col :span="9">
          <el-form-item
            ref="currentSH"
            prop="smic_horaire"
            label="Smic horaire :"
          >
            <el-input
              v-model="currentBase.smic_horaire"
              :disabled=" ! currentBaseEditable"
              style="width: 80%; margin-left: 10px;"
              @input="smicHoraireChanged"
            >
              <template #append>
                €
              </template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="9">
          <el-form-item
            prop="baseValue"
            label="Base URSAFF :"
          >
            <el-input
              v-model="currentBase.baseValue"
              :disabled="true"
              style="width: 80%; margin-left: 10px;"
            >
              <template #append>
                €
              </template>
            </el-input>
          </el-form-item>
        </el-col>
      </el-form>
    </el-row>
    <el-row
      v-show="currentBaseEditable"
    >
      <el-button
        type="success"
        :disabled="!currentBaseValid"
        @click="saveCurrentBase"
      >
        Enregistrer
      </el-button>
    </el-row>
    <el-row
      v-if="basesUrsaff.length > 0"
      style="margin-top: 25px;"
    >
      Mandats passés :
    </el-row>
    <el-row
      v-if="basesUrsaff.length > 0"
    >
      <el-table
        :data="basesUrsaff"
        class="grid"
        :stripe="true"
        :border="true"
      >
        <el-table-column
          prop="mandat"
          label="Mandat"
          :sortable="true"
          align="center"
        />
        <el-table-column
          prop="smic_horaire"
          label="Smic horaire"
          align="center"
          :formatter="euroFormatter"
        />
        <el-table-column
          prop="baseValue"
          label="Base URSAFF"
          align="center"
          :formatter="euroFormatter"
        />
      </el-table>
    </el-row>
  </BaseComponent>
</template>

<script>
import Utils from "@/mixins/Utils"
const axios = require("axios")
export default {
  name: "BaseUrsaffEdition",
  mixins: [Utils],
  data () {
    return {
      breadcrumb: [
        {
          name: "Base Ursaff",
          link: "/administration/base-ursaff"
        }
      ],
      loading: true,
      currentMandat: new Date().getFullYear(),
      basesUrsaff: [],
      currentBase: {},
      currentBaseValid: false,
      currentBaseEditable: false
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/administration/base-ursaff/",
      { withCredentials: true }
    ).then((res) => {
      this.basesUrsaff = res.data
      const currentBaseTemp = this.basesUrsaff.find(b => b.mandat === this.currentMandat)
      if(currentBaseTemp != undefined) {
        this.currentBase = currentBaseTemp
      } else {
        this.currentBase = {
          mandat: this.currentMandat,
          smic_horaire: "",
          baseValue: 0,
        }
        this.currentBaseEditable = true
      }
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les bases Ursaff : " + err, type: "error"})
    }).finally(() => this.loading = false)
  },
  methods: {
    smicHoraireChanged (value) {
      if(/[0-9]+(|.[0-9]{1,2})/.test(value)) {
        this.currentBase.baseValue = (4 * value)
        this.currentBaseValid = true
        this.$refs.currentSH.validateMessage = ""
        this.$refs.currentSH.validateState = null
      } else {
        this.currentBaseValid = false
        this.$refs.currentSH.validateMessage = "Cette valeur n'est pas un prix valide."
        this.$refs.currentSH.validateState = "error"
      }
    },
    saveCurrentBase () {
      this.loading = true
      axios.post(
        "/api/administration/base-ursaff/",
        this.currentBase,
        { withCredentials: true }
      ).then(() => {
        this.$message({message: "Base URSAFF mise à jour avec succès pour ce mandat.", type: "success"})
        this.currentBaseEditable = false
      }).catch((err) => {
        this.$message({message: "Impossible de sauvegarder la base URSAFF : " + err, type: "error"})
      }).finally(() => this.loading = false)
    }
  }
}
</script>
