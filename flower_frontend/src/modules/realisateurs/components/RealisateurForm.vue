<template>
  <el-form
    ref="reaForm"
    :model="value"
    label-position="left"
    size="small"
  >
    <el-row :gutter="5">
      <el-col :span="12">
        <el-form-item
          label="Prénom"
          prop="firstname"
          label-width="26%"
        >
          <el-input v-model="value.firstname" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Nom"
          prop="lastname"
          label-width="26%"
        >
          <el-input v-model="value.lastname" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Genre"
          prop="gender"
          label-width="26%"
        >
          <el-select v-model="value.gender">
            <el-option value="M.">
              M.
            </el-option>
            <el-option value="Mme.">
              Mme.
            </el-option>
            <el-option value="">
              Non renseigné
            </el-option>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Promotion"
          prop="promotion"
          label-width="26%"
        >
          <el-input-number
            v-model="value.promotion"
            controls-position="right"
            :min="2020"
            :max="2050"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Filière"
          prop="filiere"
          label-width="26%"
        >
          <el-select v-model="value.filiere">
            <el-option
              label="INFO"
              value="INFO"
            />
            <el-option
              label="EII"
              value="EII"
            />
            <el-option
              label="E-CDTI"
              value="ECDTI"
            />
            <el-option
              label="SRC"
              value="SRC"
            />
            <el-option
              label="GM"
              value="GM"
            />
            <el-option
              label="GCU"
              value="GCU"
            />
            <el-option
              label="GMA"
              value="GMA"
            />
            <el-option
              label="SGM"
              value="SGM"
            />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Numéro de sécurité sociale :"
          prop="security_social_number"
          label-width="26%"
        >
          <el-input
            v-model="value.security_social_number"
            :maxlength="15"
            :minlength="15"
            show-word-limit
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Email INSA"
          prop="email_insa"
          label-width="13%"
        >
          <el-input v-model="value.email_insa" />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Email personnel"
          prop="email"
          label-width="13%"
        >
          <el-input v-model="value.email" />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Mobile"
          prop="mobile"
          label-width="13%"
        >
          <el-input v-model="value.mobile" />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Adresse"
          prop="address"
          label-width="13%"
        >
          <el-input v-model="value.address" />
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item
          label="Code postal"
          prop="postcode"
          label-width="39%"
        >
          <el-input v-model="value.postcode" />
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item
          label="Ville"
          prop="town"
          label-width="39%"
        >
          <el-input v-model="value.town" />
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item
          label="Pays"
          prop="country"
          label-width="39%"
        >
          <el-input v-model="value.country" />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Nationalité"
          prop="nationality"
          label-width="13%"
        >
          <el-input v-model="value.nationality" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Date de naissance"
          prop="birth_date"
          label-width="26%"
        >
          <el-date-picker
            v-model="value.birth_date"
            format="dd-MM-yyyy"
            value-format="yyyy-MM-dd"
            type="date"
            placeholder="Date de naissance"
            :first-day-of-week="1"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Lieu de naissance"
          prop="birth_place"
          label-width="26%"
        >
          <el-input v-model="value.birth_place" />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item>
          <el-button
            :loading="loading"
            type="success"
            @click="validateForm"
          >
            Enregistrer
          </el-button>
        </el-form-item>
        <el-form-item v-if="deletable">
          <el-button
            :loading="loading"
            type="danger"
            @click="$emit('deleted')"
          >
            Supprimer
          </el-button>
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
</template>

<script>
export default {
  name: "RealisateurForm",
  props: {
    value: { type: Object, required: true },
    deletable: { type: Boolean, default: false },
    loading: { type: Boolean, default: false }
  },
  methods: {
    validateForm () {
      var valid = true
      this.$refs.reaForm.validate((r) => {
        if(!r) {
          this.$message({message: "Erreur : Ce formulaire présente des erreurs.", type: "error"})
          valid = false
        }
      })
      if(valid) {
        this.$emit("edited")
      }
    }
  }
}
</script>