<template>
  <el-form
    ref="reaForm"
    :model="modelValue"
    label-position="left"
    size="default"
    :rules="formRules"
    :style="'margin: 15px'"
  >
  <el-form-item
      v-if="create"
      label="Réalisateur"
      prop="isMember"
      label-width="140px">
      <el-radio-group 
      v-model="modelValue.isMember" 
      size="large" 
      :max="1">
      <el-radio-button label="Nouveau réalisateur" :value="false" border>
        <el-icon><Plus /></el-icon>
        Nouveau Réalisateur
      </el-radio-button>
      <el-radio-button label="Membre existant" :value="true" border>
        <el-icon><User /></el-icon>
        Membre existant
      </el-radio-button>
    </el-radio-group>
  </el-form-item>
    <el-form-item
      label="Membre"
      v-if="modelValue.isMember === true"
      prop="member"
      label-width="140px"
    >
      <MemberPicker
        v-model="modelValue.member"
        :item-list="members"
        placeholder="Membre de la JE"
        @update:modelValue="updateReal"
        @clear="clearMember"/>
    </el-form-item>
    <el-row :gutter="5">
      <el-col :span="12">
        <el-form-item
          label="Prénom"
          prop="firstname"
          label-width="26%"
          v-if="modelValue.isMember === false"
        >
          <el-input
            v-model="modelValue.firstname"
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
          v-if="modelValue.isMember === false"
        >
          <el-input
            v-model="modelValue.lastname"
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
          v-if="modelValue.isMember === false"
        >
          <el-select v-model="modelValue.gender">
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
          v-if="modelValue.isMember === false"
        >
        <el-tooltip
          effect="dark"
          content="Indiquez l'année de fin d'études à l'INSA (hors double diplôme)"
          placement="top"
        >
          <el-input-number
            v-model="modelValue.promotion"
            controls-position="right"
            :min="2020"
          />
        </el-tooltip>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Filière"
          prop="filiere"
          label-width="26%"
        >
          <el-select v-model="modelValue.filiere">
            <el-option
              label="INFO"
              value="INFO"
            />
            <el-option
              label="EII"
              value="EII"
            />
            <el-option
              label="E&T"
              value="E&T"
            />
            <el-option
              label="MA"
              value="MA"
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
              label="GPM"
              value="GPM"
            />
            <el-option
              label="STPI"
              value="STPI"
            />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Email INSA"
          prop="email_insa"
          label-width="13%"
          v-if="modelValue.isMember === false"
        >
          <el-input
            v-model="modelValue.email_insa"
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
            v-model="modelValue.email"
            placeholder="E-mail officieux"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Mobile"
          prop="mobile"
          label-width="13%"
          v-if="modelValue.isMember === false"
        >
          <el-input
            v-model="modelValue.mobile"
            placeholder="N° de portable personnel"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Présentation du réalisateur"
          prop="description"
          label-width="13%"
          v-if="modelValue.isMember === false"
        >
          <el-input
            v-model="modelValue.description"
            row="4"
            type="textarea"
            placeholder="Présentation du réalisateur"
          />
        </el-form-item>
      </el-col>
      <el-checkbox
        v-model="rea_form"
        label="Compléter les informations pour une mission"
        size="large"
        style="margin-bottom: 10px;"
        :disabled="!this.$store.currentUser.roles.includes('ROLE_ADMIN') && !create"
        border
      />
      <el-col v-if="rea_form">
      <el-col :span="24">
        <el-form-item
          label="Adresse"
          prop="address"
          label-width="13%"
          v-if="modelValue.isMember === false"
        >
          <el-input
            v-model="modelValue.address"
            placeholder="Numéro et nom de rue"
          />
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item
          label="Code postal"
          prop="postcode"
          label-width="39%"
          v-if="modelValue.isMember === false"
        >
          <el-input
            v-model="modelValue.postcode"
            placeholder="Code postal"
          />
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item
          label="Ville"
          prop="town"
          label-width="39%"
          v-if="modelValue.isMember === false"
        >
          <el-input
            v-model="modelValue.town"
            placeholder="Ville de résidence"
          />
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item
          label="Pays"
          prop="country"
          label-width="39%"
          v-if="modelValue.isMember === false"
        >
          <el-input
            v-model="modelValue.country"
            placeholder="Pays de résidence"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Nationalité"
          prop="nationality"
          label-width="13%"
          v-if="modelValue.isMember === false"
        >
          <el-input v-model="modelValue.nationality" />
        </el-form-item>
      </el-col>
        <el-col :span="12">
          <el-form-item
            label="Date de naissance"
            prop="birth_date"
            label-width="26%"
            v-if="modelValue.isMember === false"
          >
            <el-date-picker
              v-model="modelValue.birth_date"
              format="DD-MM-YYYY"
              value-format="YYYY-MM-DD"
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
            v-if="modelValue.isMember === false"
          >
            <el-input
              v-model="modelValue.birth_place"
              placeholder="Ville de naissance"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item
            label="Numéro de sécurité sociale :"
            prop="security_social_number"
            label-width="26%"
            >
            <el-input
            v-model="modelValue.security_social_number"
            :maxlength="15"
            :minlength="15"
            show-word-limit
            placeholder="N° de sécurité sociale"
            />
          </el-form-item>
        </el-col>
      </el-col>
      <el-col
        :span="24"
        style="display: inline-flex;"
      >
        <el-transfer
          v-model="modelValue.skills"
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
import MemberPicker from "@/modules/membres/components/MemberPicker"

export default {
  name: "RealisateurForm",
  components: {MemberPicker},
  props: {
    modelValue: { type: Object, required: true },
    members: { type: Array, required: true },
    deletable: { type: Boolean, default: false },
    loading: { type: Boolean, default: false },
    ecoleSuffix: { type: String, default () { return "@" } },
    create: { type: Boolean, default: true }
  },
  emits: ["update:modelValue", "edited", "deleted"],
  data () {
    return {
      competences_objs: [],
      rea_form: false,
      formRules: {
        isMember : [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        member: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
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
          {required: false, message: "Obligatoire", trigger: "blur"},
          {
            required: false,
            pattern: /^(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})$/,
            message: "Cette valeur doit être un numéro de téléphone valide.",
            trigger: "change"
          }
        ],
        address: [
          {required: false, message: "Obligatoire", trigger: "blur"}
        ],
        postcode: [
          {required: false, message: "Obligatoire", trigger: "blur"},
          {
            required: false,
            pattern: /^[ 0-9]+$/,
            message: "Cette valeur doit être un code postal valide",
            trigger: "change"
          }
        ],
        town: [
          {required: false, message: "Obligatoire", trigger: "blur"}
        ],
        country: [
          {required: false, message: "Obligatoire", trigger: "blur"}
        ],
        nationality: [
          {required: false, message: "Obligatoire", trigger: "blur"}
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
        if(valid) {
          this.$emit("edited")
        }
      })
    },
    filterSkill (query, item) {
      return item.label.toLowerCase().indexOf(query.toLowerCase()) > -1
    },
    autoFillEmails () {
      if(this.modelValue.firstname != "" && this.modelValue.lastname != "") {
        const prefix = this.handleToEmail(this.modelValue.firstname + "." + this.modelValue.lastname)
        this.modelValue.email_insa = prefix + this.ecoleSuffix
      }
    },
    handleToEmail (text) {
      return text.toLowerCase()
        .replaceAll("é", "e").replaceAll("è", "e").replaceAll("ê", "e").replaceAll("ë", "e")
        .replaceAll("à", "a").replaceAll("â", "a").replaceAll("ô", "o").replaceAll("ï", "i").replaceAll("î", "i")
        .replaceAll(" ", "-")
    },
    updateReal (id) {
      if (id) {
        const member = this.members.find(m => m.id === id)
        if (!member) {
          return
        }
        this.modelValue.firstname = member.firstname
        this.modelValue.lastname = member.lastname
        this.modelValue.gender = member.gender
        this.modelValue.promotion = member.promotion
        this.modelValue.mobile = member.mobile
        this.modelValue.email_insa = member.email
        this.modelValue.address = member.address
        this.modelValue.postcode = member.postcode
        this.modelValue.town = member.town
        this.modelValue.country = member.country
        this.modelValue.nationality = member.nationality
        this.modelValue.birth_date = member.birth_date
        this.modelValue.birth_place = member.birth_place
        this.modelValue.ba = member.ba
        this.modelValue.ba_id = member.ba_id
      }
    },
    clearMember () {
      this.modelValue.member = ""
      this.modelValue.firstname = ""
      this.modelValue.lastname = ""
      this.modelValue.gender = "M."
      this.modelValue.promotion = 2025
      this.modelValue.mobile = ""
      this.modelValue.email_insa = "@insa-rennes.fr"
      this.modelValue.address = ""
      this.modelValue.postcode = ""
      this.modelValue.town = "Rennes"
      this.modelValue.country = "France"
      this.modelValue.nationality = "Française"
      this.modelValue.birth_date = ""
      this.modelValue.birth_place = ""
      this.modelValue.ba = null
      this.modelValue.ba_id = null
    }
  }
}
</script>