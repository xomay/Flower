<template>
  <BaseComponent
    title="Ajouter un avenant"
    :breadcrumb="breadcrumb"
  >
    <el-form
      ref="formAvenant"
      :model="avenant"
      :rules="formRules"
      label-position="left"
    >
      <el-row>
        <el-col :span="12">
          <el-form-item
            label="Référence :"
            prop="displayRef"
            label-width="100px"
          >
            <el-input
              v-model="avenant.displayRef"
              :disabled="true"
            />
          </el-form-item>
        </el-col>
        <el-col
          :offset="2"
          :span="10"
          style="margin-top: 5px;"
        >
          Il s'agit du <b>{{ avenant.number + (avenant.number == 1 ? "er" : "ème" ) }}</b> avenant pour cette étude.
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item
            label="Signataire JE"
            prop="signataire_junior"
            label-width="140px"
          >
            <MemberPicker
              v-model="avenant.signataire_junior"
              :item-list="membres"
              placeholder="Signataire JE"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item
            label="Date de la signature"
            prop="signature_date"
          >
            <el-date-picker
              v-model="avenant.signature_date"
              type="date"
              placeholder="Choisissez un jour"
              width="200"
              size="medium"
              format="dd/MM/yyyy"
              value-format="yyyy-MM-dd"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-form-item
            label="Signataire Prospect"
            prop="signataire_prospect"
            label-width="140px"
          >
            <MemberPicker
              v-model="avenant.signataire_prospect"
              :item-list="employes"
              placeholder="Signataire Prospect"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-form-item
          label="Commentaire"
          prop="comment"
          label-width="140px"
        >
          <el-input
            v-model="avenant.comment"
            type="textarea"
            :rows="2"
            placeholder="Expliquez les raisons de cet avenant."
          />
        </el-form-item>
      </el-row>
      <el-row>
        <el-checkbox
          v-model="avenant.is_delais"
          @change="updateReference"
        >
          Avenant délai
        </el-checkbox>
      </el-row>
      <el-row>
        <el-checkbox
          v-model="avenant.is_methodo"
          @change="updateReference"
        >
          Avenant méthodologique
        </el-checkbox>
      </el-row>
      <el-row>
        <el-checkbox
          v-model="avenant.is_cdc"
          @change="updateReference"
        >
          Avenant du cahier des charges
        </el-checkbox>
      </el-row>
      <el-row>
        <el-checkbox
          v-model="avenant.is_budget"
          @change="updateReference"
        >
          Avenant budget
        </el-checkbox>
      </el-row>
    </el-form>
    <el-row v-show="before_phases">
      <el-button
        :disabled="!(avenant.is_delais || avenant.is_methodo || avenant.is_cdc || avenant.is_budget)"
        type="success"
        style="margin-top: 20px;"
        @click="startModifPhases()"
      >
        Modifier les phases
      </el-button>
      <el-alert
        v-show="!(avenant.is_delais || avenant.is_methodo || avenant.is_cdc || avenant.is_budget)"
        type="warning"
        title="Il faut sélectionner au moins un type d'avenant."
        show-icon
        :closable="false"
      />
    </el-row>
    <PhasesForm
      v-show="!before_phases"
      v-model="avenant.groupes.groupes"
      :small="false"
      @add-us="addUS"
      @add-groupe="addGroupe"
      @add-phase="addPhase"
      @delete-groupe="deleteGroupe"
      @delete-phase="deletePhase"
      @delete-us="deleteUS"
    />
    <el-button
      v-show="!before_phases"
      type="success"
      style="margin-top: 20px;"
      @click="validatePhases()"
    >
      Valider les phases
    </el-button>
  </BaseComponent>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"
import PhasesForm from "@/modules/etudes/components/forms/PhasesForm"
import Utils from "@/mixins/Utils"
const axios = require("axios")
export default {
  name: "AvenantCreer",
  components: {MemberPicker, PhasesForm},
  mixins: [Utils],
  data () {
    return {
      membres: [],
      employes: [],
      loading: true,
      before_phases: true,
      amountOfAvenants: 0,
      etude_num: "",
      sourceGroupes: [],
      avenant: {
        displayRef: "AVx",
        project: this.$route.params.id,
        number: 1,
        comment: "",
        signataire_junior: null,
        signataire_prospect: null,
        is_delais: false,
        is_methodo: false,
        is_cdc: false,
        is_budget: false,
        signature_date: null,
        new_dates: null,
        groupes: {id: -1, groupes: []}
      },
      formRules: {
        signataire_junior: [{required: true, message: "Obligatoire", trigger: "change"}],
        signataire_prospect: [{required: true, message: "Obligatoire", trigger: "change"}],
        signature_date: [{required: true, message: "Obligatoire", trigger: "change"}]
      },
      breadcrumb: [
        {
          name: "Suivi d'étude",
          link: "/etudes"
        },
        {
          name: "<loading>",
          link: `/etudes/${this.$route.params.id}/voir`
        },
        {
          name: "Ajouter un avenant",
          link: `/etudes/${this.$route.params.id}/avenants/ajouter`
        },
      ]
    }
  },
  beforeCreate () {
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.etude_num = res.data.number
      this.avenant.number = res.data.avenants.length + 1
      this.sourceGroupes = res.data.currentGroupes.groupes
      this.breadcrumb[1].name = res.data.name
      this.updateReference()
      // get employés :
      axios.get(
        `/api/prospects/${res.data.prospect.id}/employes/`,
        {withCredentials: true}
      ).then((resEmpl) => {
        resEmpl.data.forEach((elt) => elt.value = this.nicePeople(elt))
        this.employes = resEmpl.data
      }).catch((err) => {
        this.$message({ message: "Impossible de récupérer les employés de cete étude : " + err, type: "error" })
      }).finally(() => {
        this.loading = false
      })
    }).catch((err) => {
      this.$message({ message: "Impossible de récupérer l'étude pour le moment : " + err, type: "error" })
      this.loading = false
    })
    axios.get(
      "/api/membres/",
      {withCredentials: true}
    ).then((resMembers) => {
      resMembers.data.forEach((elt) => elt.value = this.nicePeople(elt))
      this.membres = resMembers.data
    }).catch((err) => {
      this.$message({ message: "Impossible de récupérer les membres de la JE : " + err, type: "error" })
    })
  },
  methods: {
    validatePhases () {
      this.loading = true
      axios.put(
        "/api/etudes/groupes/",
        this.avenant.groupes.groupes,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Les Groupes et Phases ont bien été enregistrés", type: "success"})
        this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Avenants`)
      }).catch((err) => {
        this.$message({message: "Erreur lors de l'enregistrement : " + err, type: "error"})
        if (err.response && err.response.status === 400) {
          this.$message({message: "Le formulaire comporte des erreurs. Vérifiez les descriptions et les objectifs des phases (menu déroulant)",
            type: "error",
            offset: 40})
        } else {
          this.$message({message: "Impossible d'enregistrer les Groupes et Phases pour le moment",
            type: "error",
            offset: 40})
        }
        this.loading = false
      })
    },
    startModifPhases () {
      this.$refs.formAvenant.validate((valid) => {
        if(valid) {
          this.loading = true
          axios.post(
            "/api/avenants/",
            this.avenant,
            {withCredentials:true}
          ).then(res => {
            // L'intéret de la manipulation est de créer l'avenant, et puis d'ensuite seulement ajouter les US et faire les manip dasn le GroupesSet
            this.before_phases = false // on passe en mode 'modif de phase'
            this.avenant.groupes = res.data
            this.$message({ message: "L'avenant a été créé. Merci de paramétrer les nouvelles phases." , type: "success" })
            this.updateReference()
          }).catch(err => {
            this.$message({ message: "Impossible de créer l'avenant : " + err , type: "error" })
          }).finally(this.loading = false)
        } else {
          this.$message({ message: "Précisez les signataires de l'avenant." , type: "error" })
        }
      })
    },
    updateReference () {
      this.avenant.displayRef = "AV" // 'AV'
      + this.avenant.number // numéro de l'avenant pour cette étude
      + ((this.avenant.is_delais ? "D," : "")
        + (this.avenant.is_methodo ? "M," : "")
        + (this.avenant.is_cdc ? "C," : "")
        + (this.avenant.is_budget ? "B," : "")).slice(0, -1) // bloc pour afficher les lettres du type (multiple) d'avenant
      + "_" + this.etude_num // numéro de l'étude
    },
    addGroupe () {
      this.loading = true
      const newGroup = {
        title: "Titre",
        description: "Description",
        project: this.$route.params.id,
        index: this.avenant.groupes.groupes.length + 1,
        owner: this.avenant.groupes.id,
        phases: []
      }
      axios.post(
        "/api/etudes/groupes/",
        newGroup,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "Le groupe a bien été créé", type: "success"})
        this.avenant.groupes.groupes.push(res.data)
      }).catch(() => {
        this.$message({message: "Impossible de créer un groupe pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    addPhase (groupe) {
      this.loading = true
      const newIndex = (Math.max.apply(
          Math,
          groupe.phases.map((phase) => phase.index)
        ) | 0) + 1,
        newPhase = {
          index: newIndex,
          uss: [],
          groupe: groupe.id
        }
      axios.post(
        "/api/etudes/phases/",
        newPhase,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "La phase a bien été ajoutée.", type: "success"})
        groupe.phases.push(res.data)
      }).catch(() => {
        this.$message({message: "Impossible de créer une phase pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    addUS (phase) {
      this.loading = true
      const newIndex = (Math.max.apply(
          Math,
          phase.uss.map((us) => us.index)
        ) | 0) + 1,
        newUS = {
          index: newIndex,
          uss: [],
          name: "US",
          phase: phase.id
        }
      axios.post(
        "/api/etudes/uss/",
        newUS,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "L'US a bien été ajouté.", type: "success"})
        phase.uss.push(res.data)
      }).catch(() => {
        this.$message({message: "Impossible de créer une US pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deleteGroupe ({groupeId, groupeIndex}) {
      this.loading = true
      axios.delete(
        `/api/etudes/groupes/${groupeId}/`,
        {withCredentials: true}
      ).then(() => {
        this.avenant.groupes.groupes.splice(
          groupeIndex,
          1
        )
        this.$message({message: "Le groupe a bien été supprimé", type: "success"})
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer ce groupe pour le moment :"+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deletePhase ({phase, groupe}) {
      this.loading = true
      axios.delete(
        `/api/etudes/phases/${phase.id}/`,
        {withCredentials: true}
      ).then(() => {
        const index = groupe.phases.indexOf(phase)
        if (index > -1) {
          groupe.phases.splice(
            index,
            1
          )
        }
        this.$message({message: "La phase a bien été supprimée.", type: "success"})
      }).catch(() => {
        this.$message({message: "Impossible de supprimer cette phase pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deleteUS ({us, phase}) {
      this.loading = true
      axios.delete(
        `/api/etudes/uss/${us.id}/`,
        {withCredentials: true}
      ).then(() => {
        const index = phase.uss.indexOf(us)
        if (index > -1) {
          phase.uss.splice(
            index,
            1
          )
        }
        this.$message({message: "L'US a bien été supprimée.", type: "success"})
      }).catch(() => {
        this.$message({message: "Impossible de supprimer cette US pour le moment", type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
  }
}
</script>