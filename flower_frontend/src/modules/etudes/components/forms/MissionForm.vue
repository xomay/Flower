<template>
  <div>
    <el-form
      v-for="(mission, index) in modelValue"
      :key="index"
      ref="refFormMission"
      :model="mission"
      class="mb-4"
      label-position="left"
    >
      <el-row>
        <el-col :span="10">
          <el-form-item
            label="Consultant"
            prop="consultant"
            :rules="[{required: true, message: 'Champs obligatoire', trigger: 'change'}]"
          >
            <MemberPicker
              v-model="mission.consultant"
              :item-list="consultants"
              placeholder="Consultant"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-button
            type="danger"
            icon="Delete"
            :style="'margin-left: 5%'"
            @click="deleteMission(mission, index)"
          >
            Supprimer la mission
          </el-button>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item
            label="Date de début"
            prop="missionBegin"
            :rules="[{required: true, message: 'Date obligatoire', trigger: 'change'}]"
          >
            <el-date-picker
              v-model="mission.missionBegin"
              format="DD-MM-YYYY"
              value-format="YYYY-MM-DD"
              type="date"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item
            label="Date de fin"
            prop="missionEnd"
            :rules="[{required: true, message: 'Date obligatoire', trigger: 'change'}]"
          >
            <el-date-picker
              v-model="mission.missionEnd"
              format="DD/MM/YYYY"
              value-format="YYYY-MM-DD"
              type="date"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">
          <el-form-item
            label="Pourcentage Junior"
            prop="percentageJunior"
            label-width="50%"
            :rows="1"
            :rules="[
              {required: true, message: 'Pourcentage obligatoire', trigger: 'blur'},
              {required: true, pattern: /^(1(|\.[0]+)|0\.[0-9]+)$/, message: 'Entrez une valeur entre 0 et 1.', trigger: 'change'}
            ]"
          >
            <el-input
              v-model="mission.percentageJunior"
              label="%"
            />
          </el-form-item>
          <el-form-item
            label="Prix du JEH"
            prop="JEH_price"
            label-width="50%"
            :rows="1"
            :rules="[
              {required: true, message: 'Prix du JEH obligatoire', trigger: 'blur'},
            ]"
          >
            <el-input-number
              v-model="mission.JEH_price"
              controls-position="right"
              :min="80"
              :max="300"
              @change="applyJEHPrice(mission)"
            />
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item
            label="Phases"
            prop="phases"
            :rules="[
              {required: true, message: 'Entrez au moins une phase.', trigger: 'blur'}
            ]"
          >
            <el-select
              v-model="mission.phases"
              class="w-full"
              multiple
              placeholder="Phases"
              @change="phases_updated($event, mission)"
            >
              <el-option
                v-for="item in getAvailablePhases(mission)"
                :key="item.id"
                :label="`${item.title} (${getRemainingJEH(item.id, mission)} JEH restants)`"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-table
        class="grid"
        :data="mission.phasesMission"
        :row-key="row => row.id"
      >
        <el-table-column
          label="Phases"
        >
          <template #default="{row}">
            <span><b>Titre de la phase : </b>{{ row.title }}</span>
          </template>
        </el-table-column>
        <el-table-column
          width="140"
          label="Nb JEH"
        >
          <template #default="{row}">
            <el-input-number
              v-model="row.nbJEH"
              controls-position="right"
              :min="1"
              :max="getRemainingJEH(row.phaseEtude, mission)"
              style="width: 90%"
              size="small"
            />
          </template>
        </el-table-column>
      </el-table>
      <el-divider />
    </el-form>
    <el-alert
      v-show="modelValue.length == 0"
      title="Vous n'avez ajouté aucune RdM"
      type="warning"
      description="Apputez sur le bouton ci-dessus pour en ajouter."
      :closable="false"
      center
      effect="dark"
      show-icon
    />
    <el-button
      :loading="loading"
      type="success"
      @click="validateForm"
    >
      Enregistrer les missions
    </el-button>
  </div>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"

export default {
  name: "MissionForm",
  components: {MemberPicker},
  props: {
    modelValue: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    phases: { type: Array, required: true },
    consultants: { type: Array, required: true }
  },
  data () {
    return {
      deletedMissions: []
    }
  },
  methods: {
    deleteMission (mission, index) {
      if(mission.id != undefined) {
        this.deletedMissions.push(mission.id)
      }
      this.modelValue.splice(index, 1)
    },
    applyJEHPrice (mission) {
      mission.phasesMission.map(phase => {
        phase.priceJEH = mission.JEH_price
      })
    },
    getTotalJEHAllocated(phaseId) {
      return this.modelValue.reduce((total, mission) => {
        const matching = mission.phasesMission.find(p => p.phaseEtude === phaseId)
        return total + (matching ? Number(matching.nbJEH || 0) : 0)
      }, 0)
    },
    getRemainingJEH(phaseId, currentMissionId) {
      const phase = this.phases.find(p => p.id === phaseId)
      const totalAvailable = phase ? phase.nbJEH : 0
      const totalAllocatedElsewhere = this.modelValue.reduce((total, mission) => {
        if (mission === currentMissionId) return total
        const match = mission.phasesMission.find(p => p.phaseEtude === phaseId)
        return total + (match ? Number(match.nbJEH || 0) : 0)
      }, 0)
      return Math.max(totalAvailable - totalAllocatedElsewhere, 0)
    },
    getAvailablePhases (currentMission) {
      return this.phases.filter(phase => {
        const totalAllocated = this.modelValue.reduce((total, mission) => {
          if (mission === currentMission) return total
          const match = mission.phasesMission.find(p => p.phaseEtude === phase.id)
          return total + (match ? Number(match.nbJEH || 0) : 0)
        }, 0)

        return totalAllocated < phase.nbJEH || currentMission.phases.includes(phase.id)
      })
    },
    validateForm () {
      let result = true

      // Contrôle des JEH globaux
      for (const phase of this.phases) {
        const total = this.getTotalJEHAllocated(phase.id)
        if (total !== Number(phase.nbJEH)) {
          this.$message({
            message: `La phase "${phase.title}" a ${total}/${phase.nbJEH} JEH alloués. Vérifiez les répartitions.`,
            type: "error"
          })
          result = false
        }
      }

      for (const form of this.$refs.refFormMission) {
        form.validate((r) => {
          if (!r) result = false
        })
      }

      if (result) {
        this.$emit("save", this.deletedMissions, this.deletedPhases)
      } else {
        this.$message({
          message: "Certains champs sont invalides ou les JEH ne sont pas bien répartis.",
          type: "error"
        })
      }
    },
    goBack () {
      this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Rédaction`)
    },
    phases_updated (rdms_ids, mission) {
      //mission.phasesMission = this.phases.filter(phase => rdms_ids.includes(phase.id))
      mission.phasesMission = mission.phasesMission.filter(phase => rdms_ids.includes(phase.phaseEtude))
      rdms_ids.forEach(id => {
        if (!mission.phasesMission.some(pm => pm.phaseEtude === id)) {
          if (mission.originalPMs.some(pm => pm.phaseEtude === id)) {
            // Si la phase était déjà présente, on la réutilise
            const originalPhase = mission.originalPMs.find(pm => pm.phaseEtude === id)
            originalPhase.priceJEH = mission.JEH_price
            mission.phasesMission.push(originalPhase)
          } else {
            const phase = this.phases.find(phase => phase.id === id)
            if (phase) {
              phase.priceJEH = mission.JEH_price
              mission.phasesMission.push({
                ...phase,
                phaseEtude: phase.id,
                id: undefined
              })
            }
          }
        }
      })
      this.$emit("phases-selection", rdms_ids)
    }
  }
}
</script>
