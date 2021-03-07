<template>
  <el-form
    ref="memFormRef"
    :model="value"
    :rules="formRules"
    label-position="left"
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
            placeholder="Prénom du membre de la JE"
            @input="autoFillEmails()"
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
            placeholder="Nom du membre de la JE"
            @input="autoFillEmails()"
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
      <el-col :span="24">
        <el-form-item
          label="Poste :"
          prop="poste"
          label-width="13%"
        >
          <MemberPicker
            v-model="value.poste"
            :item-list="postes"
            placeholder="Poste"
            :style="'width: 100%'"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Email INSA"
          prop="email"
          label-width="13%"
        >
          <el-input v-model="value.email" />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Email Juniors"
          prop="email_junior"
          label-width="13%"
        >
          <el-input v-model="value.email_junior" />
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
            placeholder="Numéro de téléphone personnel du membre"
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
            placeholder="Addresse (numéro et rue)"
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
            placeholder="Addresse (code postal)"
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
            placeholder="Addresse (ville)"
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
            placeholder="Addresse (pays)"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Nationalité"
          prop="nationality"
          label-width="13%"
        >
          <el-input
            v-model="value.nationality"
            placeholder="Nationalité"
          />
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
      <el-col :span="24">
        <el-form-item>
          <el-button
            :loading="loading"
            type="success"
            @click="validateForm('save')"
          >
            Enregistrer
          </el-button>
        </el-form-item>
      </el-col>
      <el-col
        v-if="!value.user && canOpenAccount"
        :span="24"
      >
        <el-form-item>
          <el-button
            :loading="loadingopenaccount"
            type="warning"
            @click="validateForm('openaccount')"
          >
            Ouvrir un compte utilisateur
          </el-button>
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
</template>

<script>
import MemberPicker from "./MemberPicker"
export default {
  name: "MemberForm",
  components: { MemberPicker },
  props: {
    value: { type: Object, required: true },
    postes: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    loadingopenaccount: { type: Boolean, required: true },
    canOpenAccount: { type: Boolean, default () { return false } }
  },
  data () {
    return {
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
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        email: [
          {
            required: true,
            message: "Obligatoire",
            trigger: "blur"
          },
          {
            required: true,
            pattern: /^[\w\\.=-]+@insa-rennes.fr$/,
            message: "Cette valeur doit être un email INSA valide.",
            trigger: "change"
          }
        ],
        email_junior: [
          {
            required: true,
            message: "Obligatoire",
            trigger: "blur"
          },
          {
            required: true,
            pattern: /^[\w\\.=-]+@ouest-insa.fr$/,
            message: "Cette valeur doit être un email ouest-insa valide.",
            trigger: "change"
          }
        ],
        mobile: [
          {
            required: true,
            message: "Obligatoire",
            trigger: "blur"
          },
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
          {
            required: true,
            message: "Obligatoire",
            trigger: "blur"
          },
          {
            required: true,
            pattern: /^[ 0-9]+$/,
            message: "Cette valeur doit être un code postal valide"
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
  methods: {
    validateForm (mode) {
      this.$refs.memFormRef.validate((r) => {
        if(r) {
          if(mode == "save")
            this.$emit("save")
          else if(mode == "openaccount")
            this.$emit("openaccount")
        } else {
          this.$message({
            message: "Certains champs ne sont pas valides !",
            type:"error",
            offset: 40
          })
        }
      })
    },
    autoFillEmails () {
      if(this.value.firstname != "" && this.value.lastname != "") {
        const prefix = this.handleToEmail(this.value.firstname + "." + this.value.lastname)
        this.value.email = prefix + "@insa-rennes.fr"
        this.value.email_junior = prefix + "@ouest-insa.fr"
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
