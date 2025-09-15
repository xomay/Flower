<template>
  <BaseComponent
    title="Signalement - Ticket"
    :breadcrumb="breadcrumb"
  >
    <el-form
        ref="formTicket"
        :model="ticket"
        :rules="formRules"
        label-position="left"
    >
        <el-form-item
        label="Titre du signalement"
        prop="title"
        label-width="200px"
        >
        <el-input
            v-model="ticket.title"
            placeholder="Entrez le titre du signalement"
        />
        </el-form-item>
        <el-form-item
        label="Description du signalement"
        prop="description"
        label-width="200px"
        >
        <el-input
            v-model="ticket.description"
            type="textarea"
            placeholder="Définir la raison du signalement"
            :rows="6"
        />
        </el-form-item>
        <el-form-item
        label="Type de signalement"
        prop="bug"
        label-width="200px">
        <el-radio-group 
            v-model="ticket.bug" 
            size="large" 
            :max="1">
            <el-radio-button label="Signalement de bug/problème" :value="true" border>
            <el-icon><Warning /></el-icon>
            Bug/Problème
            </el-radio-button>
            <el-radio-button label="Recommendation d'amélioration" :value="false" border>
            <el-icon><MagicStick /></el-icon>
            Amélioration
            </el-radio-button>
        </el-radio-group>
        </el-form-item>
        <el-form-item
        label="Section concernée"
        prop="labels"
        label-width="200px">
        <el-checkbox-group
            v-model="ticket.labels"
            size="large"
            >
            <el-checkbox-button label="Gestion Associative" value="Gestion asso" border>
            <el-icon><UserFilled /></el-icon>
            Gestion Associative
            </el-checkbox-button>
            <el-checkbox-button label="Suivi d'Étude" value="Suivi étude" border>
            <el-icon><Files /></el-icon>
            Suivi d'Étude
            </el-checkbox-button>
            <el-checkbox-button label="Performance" value="Performance" border>
            <el-icon><DataLine /></el-icon>
            Performance
            </el-checkbox-button>
            <el-checkbox-button label="Prospection" value="Prospection" border>
            <el-icon><Phone /></el-icon>
            Prospection
            </el-checkbox-button>
            <el-checkbox-button label="Trésorerie" value="Trésorerie" border>
            <el-icon><Money /></el-icon>
            Trésorerie
            </el-checkbox-button>
            <el-checkbox-button label="Administration" value="Administration" border>
            <el-icon><Tools /></el-icon>
            Administration
            </el-checkbox-button>
            <el-checkbox-button label="Général" value="Général" border>
            <el-icon><DataBoard /></el-icon>
            Général
            </el-checkbox-button>
        </el-checkbox-group>
        </el-form-item>
        <el-form-item>
        <el-button
            icon="Plus"
            type="success"
            style="margin-top: 20px;"
            @click="validateForm"
        >
            Enregistrer le signalement
        </el-button>
        </el-form-item>
    </el-form>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

export default {
  name: "Ticket",
  data () {
    return {
      breadcrumb: [
        {
          name: "Signalement - Ticket",
          link: "/performances/ticket"
        }
      ],
      ticket: {
        title: "",
        description: "",
        labels: [],
        bug: true
      },
      formRules: {
        title: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        description: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        labels: [
            {required: true,
             message: "Obligatoire",
             trigger: "blur"}
        ]
      }
    }
  },
  methods: {
    validateForm () {
      this.$refs.formTicket.validate((r) => {
        if(r) {
          axios.post(
            "/api/issues/",
            {
                title: this.ticket.title,
                description: this.ticket.description,
                labels: this.ticket.labels.concat(this.ticket.bug ? ["Prod bug"] : [""])
            },
            {
              withCredentials: true,
              headers: {
                "PRIVATE-TOKEN": process.env.API_TOKEN,
                "Content-Type": "application/json",
              },
            }
            ).then(() => {
              this.$message({ message: "Merci pour votre signalement !", type: "success" })
              this.$router.push(`/`)
            }).catch((err) => {
            this.$message({ message: "Impossible de créer le ticket : " + err, type: "error" })
            })
        } else {
          this.$message({ message: "Le formulaire n'est pas valide.", type: "error" })
        }
      })
    },
  }
}
</script>