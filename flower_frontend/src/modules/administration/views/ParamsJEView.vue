<template>
  <BaseComponent
    title="Paramètres de la JE"
    :breadcrumb="breadcrumb"
  >
    <el-form
      ref="paramsJeForm"
      :model="paramsData"
      :rules="formRules"
      label-position="top"
    >
      <el-collapse
        v-model="activeCollapses"
        class="bigClps"
        :style="'margin-bottom: 20px'"
      >
        <el-collapse-item
          title="Paramètres généraux"
          name="1"
        >
          <el-row>
            <el-col :span="11">
              <el-form-item
                label="Nom de la Junior Entreprise :"
                prop="je_name"
              >
                <el-input v-model="paramsData.je_name" />
              </el-form-item>
            </el-col>
            <el-col
              :span="12"
              :offset="1"
            >
              <el-form-item
                label="Abrévation de la Junior Entreprise :"
                prop="je_abbrevation"
              >
                <el-input v-model="paramsData.je_abbrevation" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="11">
              <el-form-item
                label="Email de contact :"
                prop="je_contact"
              >
                <el-input v-model="paramsData.je_contact" />
              </el-form-item>
            </el-col>
            <el-col
              :span="12"
              :offset="1"
            >
              <el-form-item
                label="Url du site web :"
                prop="je_url"
              >
                <el-input v-model="paramsData.je_url" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item
                label="Addresse postale :"
                prop="je_address"
              >
                <el-input v-model="paramsData.je_address" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <el-form-item
                label="Suffixe des emails de l'école (après le '@') :"
                prop="mail_suffix"
              >
                <el-input v-model="paramsData.mail_suffix" />
              </el-form-item>
            </el-col>
          </el-row>
        </el-collapse-item>
        <el-collapse-item
          title="Titres des rôles majeurs"
          name="2"
        >
          <el-divider
            content-position="left"
            class="diviStyle"
          >
            Président
          </el-divider>
          <el-row>
            <el-col :span="11">
              <el-form-item
                label="Prénom du président :"
                prop="president_firstname"
              >
                <el-input v-model="paramsData.president_firstname" />
              </el-form-item>
            </el-col>
            <el-col
              :span="12"
              :offset="1"
            >
              <el-form-item
                label="Nom du président :"
                prop="president_lastname"
              >
                <el-input v-model="paramsData.president_lastname" />
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item
                label="Texte introductif du président :"
                prop="president_text"
              >
                <el-input v-model="paramsData.president_text" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-divider
            content-position="left"
            class="diviStyle"
          >
            Trésorier
          </el-divider>
          <el-row>
            <el-col :span="11">
              <el-form-item
                label="Prénom du trésorier :"
                prop="treso_firstname"
              >
                <el-input v-model="paramsData.treso_firstname" />
              </el-form-item>
            </el-col>
            <el-col
              :span="12"
              :offset="1"
            >
              <el-form-item
                label="Nom du trésorier :"
                prop="treso_lastname"
              >
                <el-input v-model="paramsData.treso_lastname" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item
                label="Texte introductif du trésorier :"
                prop="treso_text"
              >
                <el-input v-model="paramsData.treso_text" />
              </el-form-item>
            </el-col>
          </el-row>
        </el-collapse-item>
        <el-collapse-item
          title="Autre"
          name="3"
        >
          <el-row>
            <el-col :span="11">
              <el-form-item
                label="Taux de TVA (20% = 0.2) :"
                prop="global_tva"
              >
                <el-input v-model="paramsData.global_tva" />
              </el-form-item>
            </el-col>
            <el-col
              :span="12"
              :offset="1"
            >
              <el-form-item
                label="Frais de dossier :"
                prop="global_frais"
              >
                <el-input v-model="paramsData.global_frais" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="11">
              <el-form-item
                label="Pourcentage d'accompte par défault :"
                prop="global_accompte"
              >
                <el-input v-model="paramsData.global_accompte" />
              </el-form-item>
            </el-col>
            <el-col
              :span="12"
              :offset="1"
            >
              <el-form-item
                label="Année d'utilisation de Flower :"
                prop="je_startFlower"
              >
                <el-input-number v-model="paramsData.je_startFlower" />
              </el-form-item>
            </el-col>
          </el-row>
        </el-collapse-item>
      </el-collapse>
      <el-button
        type="success"
        @click="validateForm"
      >
        Enregistrer
      </el-button>
    </el-form>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
export default {
  name: "ParamsJEView",
  data () {
    return {
      paramsData: {},
      loading: true,
      breadcrumb: [
        {
          name: "Paramètres Junior",
          link: "/administration/params"
        }
      ],
      formRules: {
        // JE
        je_name: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        je_abbrevation: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        je_contact: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        je_address: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        je_url: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        mail_suffix: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        // Préz / tréso
        president_firstname: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        president_lastname: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        president_text: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        treso_lastname: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        treso_firstname: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        treso_text: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        // Autre
        global_accompte: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        global_frais: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        global_tva: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
        je_startFlower: [
          { required: true, message: "Obligatoire", trigger: "blur" }
        ],
      },
      activeCollapses: []
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/administration/params",
      { withCredentials: true }
    ).then((res) => {
      this.paramsData = res.data
    }).catch(() => { // erreur en cas de 404 <=> pas de params d'instancié.
      this.fatalNotParametred()
      this.$message({message: "ATTENTION : vous n'avez pas créé d'instance de paramètres sur le panel admin.", type: "error"})
    }).finally(() => {
      this.loading = true
    })
  },
  methods: {
    validateForm () {
      this.$refs.paramsJeForm.validate((result) => {
        if(result) {
          this.updateParams()
        } else {
          this.$message({message: "Le formulaire présente des erreurs", type: "error"})
        }
      })
    },
    updateParams () {
      axios.put(
        "api/administration/params",
        this.paramsData,
        { withCredentials: true }
      ).then(() => {
        this.$message({message: "Les paramètres ont été mis à jour.", type: "success"})
      }).catch((err) => {
        this.$message({message: "Impossible d'update les paramètres : " + err, type: "error"})
      }).finally(() => {
        this.loading = true
      })
    },
    fatalNotParametred () {
      this.$alert(
        "<b>Vous n'avez pas créé d'instance de ParamsJE.</b><br>Connectez-vous à <u>l'interface admin</u> pour le faire.",
        "Erreur",
        {
          confirmButtonText: "OK",
          dangerouslyUseHTMLString: true
        }
      )
    }
  }
}
</script>

<style scoped>
  .bigClps {
    font-weight: bold;
  }
</style>