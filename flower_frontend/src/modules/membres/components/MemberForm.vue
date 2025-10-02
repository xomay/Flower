<template>
  <el-form
    ref="memFormRef"
    :model="modelValue"
    :rules="formRules"
    label-position="left"
    :style="'margin: 15px'"
  >
    <el-row :gutter="5">
      <el-col :span="12">
        <el-form-item
          label="Prénom"
          prop="firstname"
          label-width="26%"
        >
          <el-input
            v-model="modelValue.firstname"
            placeholder="Prénom du membre de la JE"
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
            v-model="modelValue.lastname"
            placeholder="Nom du membre de la JE"
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
          <el-select v-model="modelValue.gender" placeholder="Sélectionner le genre">
            <el-option value="M.">M.</el-option>
            <el-option value="Mme.">Mme.</el-option>
            <el-option value="">Non renseigné</el-option>
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
            v-model="modelValue.promotion"
            controls-position="right"
            :min="2020"
            :max="2050"
            placeholder="Année de promotion"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Poste"
          prop="poste"
          label-width="13%"
        >
          <ItemPicker
            v-model="modelValue.poste"
            :item-list="postes"
            placeholder="Sélectionner un poste"
            :style="'width: 100%'"
            @input="editPoste"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Email INSA"
          prop="email"
          label-width="13%"
        >
          <el-input
            v-model="modelValue.email"
            placeholder="Email INSA"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Email Juniors"
          prop="email_junior"
          label-width="13%"
        >
          <el-input
            v-model="modelValue.email_junior"
            placeholder="Email Juniors"
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
            v-model="modelValue.mobile"
            placeholder="Numéro de téléphone personnel"
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
            v-model="modelValue.address"
            placeholder="Adresse (numéro et rue)"
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
        >
          <el-input
            v-model="modelValue.town"
            placeholder="Ville"
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
            v-model="modelValue.country"
            placeholder="Pays"
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
            v-model="modelValue.nationality"
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
            v-model="modelValue.birth_date"
            format="DD/MM/YYYY"
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
        >
          <el-input
            v-model="modelValue.birth_place"
            placeholder="Ville de naissance"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item >
          <el-button
            :loading="loading"
            type="success"
            style="margin-top: 40px"
            @click="validateForm()"
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
import ItemPicker from "@/components/ItemPicker"
export default {
  name: "MemberForm",
  components: { ItemPicker },
  props: {
    modelValue: { type: Object, required: true },
    postes: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    canOpenAccount: { type: Boolean, default: false },
    deletable: { type: Boolean, default: false }
  },
  emits: ["update:modelValue", "save", "openaccount", "deleted"],
  data () {
    return {
      formRules: {
        firstname: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        lastname: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        gender: [
          { required: true, message: "Obligatoire", trigger: "change" }
        ],
        promotion: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        email: [
          {
            required: true,
            message: "Obligatoire",
            trigger: "blur"
          },
          {
            pattern: /^[\w\.-]+@insa-rennes\.fr$/,
            message: "Email INSA valide requis.",
            trigger: "blur"
          }
        ],
        email_junior: [
          {
            required: true,
            message: "Obligatoire",
            trigger: "blur"
          },
          {
            pattern: /^[\w\.-]+@ouest-insa\.fr$/,
            message: "Email Juniors valide requis.",
            trigger: "blur"
          }
        ],
        mobile: [
          {
            required: false,
            pattern: /^(?:(?:\+|00)33[\s.-]?(?:\(0\)[\s.-]?)?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})$/,
            message: "Numéro de téléphone valide requis.",
            trigger: "blur"
          }
        ],
        address: [
          { required: false, message: "Obligatoire", trigger: "blur" }
        ],
        postcode: [
          {
            required: false,
            message: "Obligatoire",
            trigger: "blur"
          },
          {
            pattern: /^[0-9]{5}$/,
            message: "Code postal valide requis.",
            trigger: "blur"
          }
        ],
        town: [
          { required: false, message: "Obligatoire", trigger: "blur" }
        ],
        poste: [
          { required: true, message: "Obligatoire", trigger: "blur" },
          { validator: this.validatePoste, trigger: "blur" }
        ],
        country: [
          { required: false, message: "Obligatoire", trigger: "blur" }
        ],
        nationality: [
          { required: false, message: "Obligatoire", trigger: "blur" }
        ],
        birth_date: [
          { required: false, message: "Obligatoire", trigger: "blur" }
        ],
        birth_place: [
          { required: false, message: "Obligatoire", trigger: "blur" }
        ]
      }
    }
  },
  methods: {
    validateForm() {
      this.$refs.memFormRef.validate((valid) => {
        if (valid) {
          this.$emit("save");
        } else {
          this.$message({
            message: "Certains champs ne sont pas valides !",
            type: "error"
          });
        }
      });
    },
    validatePoste(rule, value, callback) {
      if (value < 1) {
        callback(new Error("Poste non défini !"));
      } else {
        callback();
      }
    },
    autoFillEmails() {
      if (this.modelValue.firstname && this.modelValue.lastname) {
        const prefix = this.handleToEmail(`${this.modelValue.firstname}.${this.modelValue.lastname}`);
        this.modelValue.email = `${prefix}@insa-rennes.fr`;
        this.modelValue.email_junior = `${prefix}@ouest-insa.fr`;
      }
    },
    handleToEmail(text) {
      return text.toLowerCase()
        .replace(/é|è|ê|ë/g, "e")
        .replace(/à|â/g, "a")
        .replace(/ô/g, "o")
        .replace(/ï|î/g, "i")
        .replace(/ /g, "-");
    },
    editPoste(newPoste) {
      this.modelValue.poste = newPoste;
    }
  }
}
</script>
