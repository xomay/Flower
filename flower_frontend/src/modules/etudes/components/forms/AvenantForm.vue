<template>
    <el-form
      v-show="create"
      ref="formAvenant"
      :model="globalForm"
      :rules="formClientRules"
      label-position="left"
    >
      <el-form-item
        label="Cible de l'avenant"
        prop="avenantTarget"
        label-width="140px">
        <el-row>
          <el-checkbox-button 
          v-model="globalForm.is_client" 
          label="Délai" border
          @change="updateReference">
            <el-icon><OfficeBuilding /></el-icon>
            Client
          </el-checkbox-button>
          <el-checkbox-button 
          v-model="globalForm.is_inter" 
          label="Méthodologie" border
          @change="updateReference">
            <el-icon><User /></el-icon>
            Intervenant
          </el-checkbox-button>
        </el-row>
      </el-form-item>
    </el-form>
    <el-divider v-if="globalForm.is_client">
      <span class="text-lg mr-2">{{avenant.type === 'bc' ? 'Bon de Commande Rectificatif' 
      : 'Avenant à la CE'}}</span>
    </el-divider>
    <!-- ---------------------Avenant Client--------------------- -->
    <el-form
      ref="formAvenantClient"
      v-if="globalForm.is_client"
      :model="avenant.doc_etude"
      :rules="formClientRules"
      label-position="left"
    >
    <el-alert
      v-show="!(avenant.is_delai || avenant.is_methodo || avenant.is_cdc || avenant.is_budget)"
      type="error"
      title="Il faut sélectionner au moins un type d'avenant."
      show-icon
      :closable="false"
      style="margin: 10px 0;"
    />
      <el-form-item
        label="Type d'avenant"
        prop="avenantType"
        label-width="140px">
        <el-row>
          <el-checkbox-button 
          v-model="avenant.is_delai" 
          label="Délai" border
          @change="updateReference">
            <el-icon><Timer /></el-icon>
            Délai
          </el-checkbox-button>
          <el-checkbox-button 
          v-model="avenant.is_methodo" 
          label="Méthodologie" border
          @change="updateReference">
            <el-icon><Reading /></el-icon>
            Méthodologie
          </el-checkbox-button>
          <el-checkbox-button 
          v-model="avenant.is_cdc" 
          label="Méthodologie" border
          @change="updateReference">
            <el-icon><Memo /></el-icon>
            Cahier des Charges
          </el-checkbox-button>
          <el-checkbox-button 
          v-model="avenant.is_budget" 
          label="Méthodologie" border
          @change="updateReference">
            <el-icon><Money /></el-icon>
            Budget
          </el-checkbox-button>
        </el-row>
      </el-form-item>
      <el-form-item
        label="Description"
        prop="description"
        label-width="140px"
      >
        <el-input
          v-model="avenant.description"
          type="textarea"
          :rows="6"
          placeholder="Expliquez les raisons de cet avenant."
          width="100%"
        />
      </el-form-item>
      <el-row>
        <el-col :span="12">
          <el-form-item
            label="Référence :"
            prop="ref"
            label-width="140px"
          >
            <el-input
              v-model="avenant.ref"
              :disabled="true"
            />
          </el-form-item>
        </el-col>
        <el-col
          :offset="2"
          :span="10"
          style="margin-top: 5px;"
        >
          Il s'agit du <b>{{ avenant.index + (avenant.index == 1 ? "er" : "ème" ) }}</b> avenant pour cette étude.
        </el-col>
      </el-row>
      <el-row style="margin-bottom: 20px;">
        <el-col :span="8">
          <el-form-item
            label="Signataire JE"
            prop="signer1"
            label-width="140px"
          >
            <MemberPicker
              v-model="avenant.doc_etude.signer1"
              :item-list="membres"
              placeholder="Signataire JE"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8" :offset="1">
          <el-form-item
            label="Signataire Prospect"
            prop="signer2"
            label-width="140px"
          >
            <MemberPicker
              v-model="avenant.doc_etude.signer2"
              :item-list="employes"
              placeholder="Signataire Prospect"
            />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div v-if="globalForm.is_client">
    <el-divider v-if="(avenant.is_budget)" 
    content-position="left">Modifier les frais</el-divider>
    <el-form
      v-if="(avenant.is_budget)"
      ref="formBudget"
      :model="avenant"
      :rules="budgetFormRules"
      label-position="left"
    >
      <el-form-item
        label="Montant des frais"
        label-width="140px"
        prop="application_fees"
        style="margin-bottom: 40px;"
      >
        <el-input-number
          v-model="avenant.doc_etude.application_fees"
          controls-position="right"
          :min="0"
        />
      </el-form-item>
      <el-form-item
        label="Frais matériels ou de déplacements"
        label-width="140px"
        style="margin-bottom: 40px;"
      >
        <el-checkbox v-model="avenant.doc_etude.hasMaterialFees" />
      </el-form-item>
      <el-form-item
        v-if="avenant.doc_etude.hasMaterialFees"
        label="Montant des frais matériels"
        label-width="140px"
        style="margin-bottom: 40px;"
      >
        <el-input-number
          v-model="avenant.doc_etude.materialFees"
          controls-position="right"
          :min=0
          :max=1000
        />
      </el-form-item>
      <el-form-item
        v-if="avenant.doc_etude.hasMaterialFees"
        label="Description des frais matériels"
        label-width="140px"
        style="margin-bottom: 40px;"
      >
        <el-input
          v-model="avenant.doc_etude.materialDesc"
          type="textarea"
          :rows="3"
          placeholder="Description des frais matériels ou de déplacements"
        />
      </el-form-item>
    </el-form>
    <el-divider v-if="(avenant.is_delai || avenant.is_methodo || avenant.is_budget || avenant.is_cdc)" 
    content-position="left">Sélectionner les phases</el-divider>
    <el-select
      v-if="(avenant.is_delai || avenant.is_methodo || avenant.is_budget || avenant.is_cdc)"
      v-model="idx"
      class="w-full"
      multiple
      placeholder="Sélectionner les phases"
    >
      <el-option
        v-for="item in etude.phases"
        :key="item.id"
        :label="`Phase ${item.index < 0 ? 'transverse ' + Math.abs(item.index) : item.index} : ${item.title}`"
        :value="item.index"
      />
    </el-select>
    <el-divider v-if="(avenant.is_delai || avenant.is_methodo || avenant.is_budget)" 
    content-position="left">Modifier les phases</el-divider>
    <PhasesForm
      v-if="(avenant.is_delai || avenant.is_methodo || avenant.is_budget)"
      v-model="avenant.phasesReal"
      :requirements="avenant.requirements"
      :is_delai="avenant.is_delai"
      :is_methodo="avenant.is_methodo"
      :is_budget="avenant.is_budget"
      :is_cdc="avenant.is_cdc"
      :small="false"
      @add-phase="addPhase(false)"
      @delete-phase="deletePhase"
    />
    <PhasesForm
      v-if="(avenant.is_delai || avenant.is_methodo || avenant.is_budget)"
      v-model="avenant.phasesTransverse"
      :requirements="avenant.requirements"
      :is_delai="avenant.is_delai"
      :is_methodo="avenant.is_methodo"
      :is_budget="avenant.is_budget"
      :is_cdc="avenant.is_cdc"
      :is_transverse="true"
      :small="false"
      @add-phase="addPhase(true)"
      @delete-phase="deletePhase"
    />
    <el-divider v-if="(avenant.is_cdc)" 
    content-position="left">Modifier le cahier des charges</el-divider>
    <div v-if="(avenant.is_cdc)" v-for="(phase, idx) in avenant.phases" :key="phase.index" style="margin-top: 20px;">
      <span>Cahier des Charges lié à la phase {{ phase.index }}</span>
      <el-input
        v-model="phase.spec"
        type="textarea"
        :autosize="{ minRows: 10 }"
        placeholder="Cahier des charges de la phase"
      />
    </div>
    </div>
    <!-- ---------------------Avenant aux RMs--------------------- -->
     <el-divider v-if="globalForm.is_inter && create" content-position="left">
      <span class="text-lg mr-2">Sélectionner les intervenants</span>
    </el-divider>
    <el-select
      v-if="(globalForm.is_inter) && create"
      v-model="RMidx"
      class="w-full"
      multiple
      placeholder="Sélectionner les intervenants"
    >
      <el-option
        v-for="item in avenantsRM"
        :key="item.id"
        :label="`${item.inter.firstname} ${item.inter.lastname}`"
        :value="item.id"
      />
    </el-select>
    <div v-for="avenantRM in filteredAvenantsRM" v-if="globalForm.is_inter">
      <el-form
      :rules="formRMRules"
      :ref="`formAvenantInter-${avenantRM.id}`"
      :model="avenantRM"
      label-position="left"
      >
        <el-divider>
          <span class="text-lg mr-2">Avenant au RM de {{ avenantRM.inter.firstname + " " + avenantRM.inter.lastname }}</span>
        </el-divider>
        <el-alert
          v-show="!(avenantRM.is_delai || avenantRM.is_methodo || avenantRM.is_cdc || avenantRM.is_budget)"
          type="error"
          title="Il faut sélectionner au moins un type d'avenant."
          show-icon
          :closable="false"
          style="margin: 10px 0;"
        />
        <el-form-item
          label="Type d'avenant"
          prop="avenantType"
          label-width="140px">
          <el-row>
            <el-checkbox-button 
            v-model="avenantRM.is_delai" 
            label="Délai" border
            @change="updateRMReference(avenantRM)">
              <el-icon><Timer /></el-icon>
              Délai
            </el-checkbox-button>
            <el-checkbox-button 
            v-model="avenantRM.is_methodo" 
            label="Méthodologie" border
            @change="updateRMReference(avenantRM)">
              <el-icon><Reading /></el-icon>
              Méthodologie
            </el-checkbox-button>
            <el-checkbox-button 
            v-model="avenantRM.is_cdc" 
            label="Méthodologie" border
            @change="updateRMReference(avenantRM)">
              <el-icon><Memo /></el-icon>
              Cahier des Charges
            </el-checkbox-button>
            <el-checkbox-button 
            v-model="avenantRM.is_budget" 
            label="Méthodologie" border
            @change="updateRMReference(avenantRM)">
              <el-icon><Money /></el-icon>
              Budget
            </el-checkbox-button>
          </el-row>
        </el-form-item>
        <el-form-item
          label="Intervenant"
          prop="consultant"
          label-width="140px"
        >
          <MemberPicker
            v-model="avenantRM.consultant"
            :item-list="intervenants"
            placeholder="Intervenant"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item
          label="Référence :"
          prop="ref"
          label-width="140px"
        >
          <el-input
            v-model="avenantRM.ref"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item
          label="Description"
          prop="description"
          label-width="140px"
        >
          <el-input
            v-model="avenantRM.description"
            type="textarea"
            :rows="6"
            placeholder="Expliquez les raisons de cet avenant."
            width="100%"
          />
        </el-form-item>
      </el-form>
      <el-divider v-if="(avenantRM.is_delai || avenantRM.is_methodo || avenantRM.is_budget || avenantRM.is_cdc)" 
      content-position="left">Sélectionner les phases</el-divider>
      <el-select
        v-if="(avenantRM.is_delai || avenantRM.is_methodo || avenantRM.is_budget || avenantRM.is_cdc)"
        v-model="avenantRM.phases_idx"
        class="w-full"
        multiple
        placeholder="Sélectionner les phases"
        @change="phasesRM_updated($event, avenantRM)"
      >
        <el-option
          v-for="item in avenantRM.mission.phasesMission"
          :key="item.id"
          :label="`Phase ${item.index < 0 ? 'transverse ' + Math.abs(item.index) : item.index} : ${item.title}`"
          :value="item.index"
        />
      </el-select>
      <el-divider v-if="(avenantRM.is_delai || avenantRM.is_methodo || avenantRM.is_budget)" 
        content-position="left">Modifier les phases</el-divider>
      <PhasesForm
        v-if="(avenantRM.is_delai || avenantRM.is_methodo || avenantRM.is_budget)"
        v-model="avenantRM.phases"
        :is_delai="avenantRM.is_delai"
        :is_methodo="avenantRM.is_methodo"
        :is_budget="avenantRM.is_budget"
        :is_cdc="avenantRM.is_cdc"
        :small="false"
      />
      <el-divider v-if="(avenantRM.is_cdc)" 
        content-position="left">Modifier le cahier des charges</el-divider>
        <div v-if="(avenantRM.is_cdc)" v-for="(phase, idx) in avenantRM.phases" :key="phase.index" style="margin-top: 20px;">
          <span>Cahier des Charges lié à la phase {{ phase.index }}</span>
          <el-input
            v-model="phase.spec"
            type="textarea"
            :autosize="{ minRows: 10 }"
            placeholder="Cahier des charges de la phase"
          />
        </div>
    </div>
    <!-- ---------------------Bouton Enregistrement--------------------- -->
    <el-button
      v-show="(globalForm.is_client || (globalForm.is_inter && filteredAvenantsRM.length > 0))"
      type="success"
      :disabled="loading"
      style="margin-top: 20px; margin-bottom: 100px;"
      @click="validateAvenant()"
    >
      Enregistrer l'avenant
    </el-button>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"
import PhasesForm from "@/modules/etudes/components/forms/PhasesForm"
import MissionForm from "@/modules/etudes/components/forms/MissionForm"
import Utils from "@/mixins/Utils"
const axios = require("axios")
export default {
  name: "AvenantForm",
  components: {MemberPicker, PhasesForm, MissionForm},
  props: {
    create: { type: Boolean, required: true },
    avenant: { type: Object, required: true },
    etude: { type: Object, required: true },
    avenantsRM: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    intervenants: { type: Array, required: true },
    membres: { type: Array, required: true },
    employes: { type: Array, required: true },
    isClient: { type: Boolean, required: true, default: false },
    isInter: { type: Boolean, required: true, default: false },
  },
  emits: ["update-reference", "update-rm-reference", "validate-avenant", "add-phase", "delete-phase"],
  mixins: [Utils],
  data () {
    return {
      idx: [],
      RMidx: [],
      filteredAvenantsRM: [], // Copie locale pour la filtration
      initialized: false,
      globalForm: {
        is_client: false,
        is_inter: false,
      },
      formClientRules: {
        signer1: [{required: true, message: "Obligatoire", trigger: "change"}],
        signer2: [{required: true, message: "Obligatoire", trigger: "change"}],
        //description: [{required: true, message: "Obligatoire", trigger: "blur"}],
      },
      formRMRules: {
        description: [{required: true, message: "Obligatoire", trigger: "blur"}],
      },
      budgetFormRules: {
        application_fees: [
          { required: true, message: "Le montant des frais est obligatoire", trigger: "blur" }
        ]
      },
    }
  },
  watch: {
    idx () {
      this.avenant.phases = this.etude.phases
      .filter(phase => this.idx.includes(phase.index) && !this.avenant.originalPhases.some(p => p.index === phase.index))
      .map(phase => {
        const { id, uss, ...newPhase } = JSON.parse(JSON.stringify(phase))
        newPhase.state = 'PENDING'
        newPhase.uss = []
        return newPhase
      }).concat(this.avenant.originalPhases.filter(p => this.idx.includes(p.index)))
      this.update_phases()
    },
    RMidx () {
      this.filteredAvenantsRM = this.avenantsRM.filter(avenantRM => this.RMidx.includes(avenantRM.id))
    },
    avenant () {
      if (!this.initialized && this.avenant.phases && this.avenant.phases.length > 0) {
        this.idx = this.avenant.phases.map(phase => phase.index)
        this.globalForm = {
          is_client: this.isClient,
          is_inter: this.isInter
        }
        this.initialized = true
      }
      this.update_phases()
    },
    avenantsRM () {
      if (!this.initialized && this.avenantsRM.length > 0) {
        this.filteredAvenantsRM = [...this.avenantsRM]
        this.RMidx = this.avenantsRM.map(rm => rm.index)
        this.globalForm = {
          is_client: this.isClient,
          is_inter: this.isInter
        }
        this.initialized = true
      }
    }
  },
  methods: {
    updateReference () {
      this.$emit("update-reference", this.avenant)
    },
    updateRMReference (avenantRM) {
      this.$emit("update-rm-reference", avenantRM)
    },
    update_phases(){
      this.avenant.phasesReal = this.avenant.phases.filter(phase => phase.index >= 0)
      this.avenant.phasesTransverse = this.avenant.phases.filter(phase => phase.index < 0)
    },
    addPhase (trans) {
      if (trans){
        if (this.etude.phases.filter(phase => phase.index < 0).length > 0){
          this.$message({message: "Impossible d'ajouter une nouvelle phase transverse car une phase transverse existe déjà.", type: "error"})
          return
        }
      }
      const newIndex = this.etude.phases.length + 1,
        newPhase = {
          index: trans ? -1 : newIndex,
          title: "",
          description: "",
          methodologie: "",
          spec: "",
          nbJEH: 0,
          period: "",
          priceJEH: 450,
          uss: [],
          requirements: [],
          state: 'PENDING',
          avenant_creer: this.avenant.id,
          avenant_edit: null,
          etude: this.etude.id,
        }
      this.avenant.phases.push(newPhase)
      this.update_phases()
    },
    deletePhase ({phase}) {
      this.avenant.phases = this.avenant.phases.filter(p => p.index !== phase.index)
      if (this.idx.includes(phase.index)) {
        this.idx = this.idx.filter(i => i !== phase.index)
      }
      this.update_phases()
    },
    getAvailablePhases () {
      // Vérifier si la phase est déjà sélectionnée dans l'avenant via la liste de phases qui ont le meme index que la phase
      return this.etude.phases.filter(phase => {
        return this.avenant.phases.findIndex(p => p.index === phase.index) === -1
      })
    },
    phases_updated (idx) {
      if (this.avenant.is_delai){
        this.avenant.phases = this.etude.phases.filter(phase => phase.index >= Math.min(...idx))
        this.idx = this.avenant.phases.map(phase => phase.index)
      }
    },
    phasesRM_updated (idx, avenantRM) {
      avenantRM.phases = avenantRM.mission.phasesMission
      .filter(phase => idx.includes(phase.index) && !avenantRM.originalPhases.some(p => p.index === phase.index))
      .map(phase => {
        const { id, uss, ...newPhase } = JSON.parse(JSON.stringify(phase))
        newPhase.state = 'PENDING'
        newPhase.uss = []
        return newPhase
      }).concat(avenantRM.originalPhases.filter(p => avenantRM.phases_idx.includes(p.index)))
    },
    validateAvenant () {
      let allFormsValid = true
      
      // Validation du formulaire global (si create = true)
      if (this.create) {
        this.$refs.formAvenant.validate((valid) => {
          if (!valid) {
            this.$message({ message: "Veuillez corriger les erreurs dans le formulaire général.", type: "error" })
            allFormsValid = false
          }
        })
      }
      
      // Validation du formulaire client
      if (this.globalForm.is_client) {
        this.$refs.formAvenantClient.validate((validClient) => {
          if (!validClient) {
            this.$message({ message: "Veuillez corriger les erreurs dans le formulaire client.", type: "error" })
            allFormsValid = false
          }
        })
      }
      
      // Validation des formulaires d'avenants RM
      if (this.globalForm.is_inter) {
        for (const avenantRM of this.filteredAvenantsRM) {
          const formRef = this.$refs[`formAvenantInter-${avenantRM.id}`]
          if (formRef && formRef[0]) {
            formRef[0].validate((validRM) => {
              if (!validRM) {
                this.$message({ message: `Veuillez corriger les erreurs dans le formulaire intervenant de ${avenantRM.inter.firstname} ${avenantRM.inter.lastname}.`, type: "error" })
                allFormsValid = false
              }
            })
          }
        }
      }
      
      // Si tous les formulaires sont valides, émettre l'événement
      if (allFormsValid) {
        this.$emit("validate-avenant", this.filteredAvenantsRM, this.globalForm)
      }
    }
  }
}
</script>