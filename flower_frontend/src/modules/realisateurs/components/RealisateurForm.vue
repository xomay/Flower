<template>
  <el-form
    ref="reaForm"
    :model="value"
    label-position="left"
    size="small"
    :rules="formRules"
  >
    <el-row :gutter="5">
      <el-col :span="12">
        <el-form-item
          label="Prénom"
          prop="firstname"
          label-width="26%"
        >
          <el-input
            v-model="value.firstname"
            placeholder="Prénom du réalisateur"
            @input="autoFillEmails"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Nom"
          prop="lastname"
          label-width="26%"
        >
          <el-input
            v-model="value.lastname"
            placeholder="Nom du réalisateur"
            @input="autoFillEmails"
          />
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
            placeholder="N° de sécurité sociale"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Email INSA"
          prop="email_insa"
          label-width="13%"
        >
          <el-input
            v-model="value.email_insa"
            placeholder="Cet email sera utilisé officiellement"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Email personnel"
          prop="email"
          label-width="13%"
        >
          <el-input
            v-model="value.email"
            placeholder="E-mail officieux"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Mobile"
          prop="mobile"
          label-width="13%"
        >
          <el-input
            v-model="value.mobile"
            placeholder="N° de portable personnel"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Adresse"
          prop="address"
          label-width="13%"
        >
          <el-input
            v-model="value.address"
            placeholder="Numéro et nom de rue"
          />
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item
          label="Code postal"
          prop="postcode"
          label-width="39%"
        >
          <el-input
            v-model="value.postcode"
            placeholder="Code postal"
          />
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item
          label="Ville"
          prop="town"
          label-width="39%"
        >
          <el-input
            v-model="value.town"
            placeholder="Ville de résidence"
          />
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item
          label="Pays"
          prop="country"
          label-width="39%"
        >
          <el-input
            v-model="value.country"
            placeholder="Pays de résidence"
          />
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
          <el-input
            v-model="value.birth_place"
            placeholder="Ville de naissance"
          />
        </el-form-item>
      </el-col>
      <el-col
        :span="24"
        style="display: inline-flex;"
      >
        <el-transfer
          v-model="value.skills"
          :data="competences_objs"
          filterable
          :filter-method="filterSkill"
          filter-placeholder="Recherche"
          :titles="['Choix', 'Compétences']"
          style="margin: 10px auto 10px auto;"
        />
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
const axios = require("axios")
export default {
  name: "RealisateurForm",
  props: {
    value: { type: Object, required: true },
    deletable: { type: Boolean, default: false },
    loading: { type: Boolean, default: false },
    ecoleSuffix: { type: String, default () { return "@" } }
  },
  data () {
    return {
      competences_objs: [],
      formRules: {
        firstname: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        lastname: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        gender: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        promotion: [
          {required: true, message: "Obligatoire", trigger: "blur"},
          {
            required: true,
            pattern: /^20[23][0-9]$/,
            message: "Entrez une année cohérente.",
            trigger: "change"
          }
        ],
        filiere: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        security_social_number: [
          {required: true, message: "Obligatoire", trigger: "blur"},
          {
            required: true,
            pattern: /^[12][0-9]{14}$/,
            message: "Entrez un numéro de sécurité sociale valide.",
            trigger: "change"
          }
        ],
        email: [
          {required: true, message: "Obligatoire", trigger: "blur"},
          {
            required: true,
            pattern: /^[\w\\.=-]+@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
            message: "Cette valeur doit être un email valide.",
            trigger: "change"
          }
        ],
        email_insa: [
          {required: true, message: "Obligatoire", trigger: "blur"},
          {
            required: true,
            pattern: /^[\w\\.=-]+@insa-rennes.fr$/,
            message: "Cette valeur doit être un email insa-rennes valide.",
            trigger: "change"
          }
        ],
        mobile: [
          {required: true, message: "Obligatoire", trigger: "blur"},
          {
            required: true,
            pattern: /^(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})$/,
            message: "Cette valeur doit être un numéro de téléphone valide.",
            trigger: "change"
          }
        ],
        address: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        postcode: [
          {required: true, message: "Obligatoire", trigger: "blur"},
          {
            required: true,
            pattern: /^[ 0-9]+$/,
            message: "Cette valeur doit être un code postal valide",
            trigger: "change"
          }
        ],
        town: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        country: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        nationality: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        birth_date: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        birth_place: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ]
      }
    }
  },
  beforeCreate () {
    axios.get(
      "/api/realisateurs/skills",
      {withCredentials: true}
    ).then((res) => {
      for (const skill of res.data) {
        this.competences_objs.push({
          key: skill.id,
          label: skill.name,
          disabled: false
        })
      }
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les compétences : " + err,
        type: "error",
        offset: 40})
    })
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
    },
    filterSkill (query, item) {
      return item.label.toLowerCase().indexOf(query.toLowerCase()) > -1
    },
    autoFillEmails () {
      if(this.value.firstname != "" && this.value.lastname != "") {
        const prefix = this.handleToEmail(this.value.firstname + "." + this.value.lastname)
        this.value.email_insa = prefix + this.ecoleSuffix
      }
    },
    handleToEmail (text) {
      return text.toLowerCase()
        .replaceAll("é", "e").replaceAll("è", "e").replaceAll("ê", "e").replaceAll("ë", "e")
        .replaceAll("à", "a").replaceAll("â", "a").replaceAll("ô", "o").replaceAll("ï", "i").replaceAll("î", "i")
        .replaceAll(" ", "-")
    }
  }
}
</script>