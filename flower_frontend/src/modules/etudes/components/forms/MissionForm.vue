<template>
  <div>
    <el-form
      v-for="(mission, index) in modelValue"
      :key="index"
      :ref="'refFormMission' + index"
      :model="mission"
      class="mb-4"
      label-position="left"
    >
      <el-row>
        <el-col :span="10">
          <el-form-item
            label="Intervenant"
            prop="consultant"
            :rules="[{required: true, message: 'Champs obligatoire', trigger: 'change'}]"
          >
            <div style="display: flex; align-items: center; gap: 8px;">
              <el-tooltip
                effect="dark"
                placement="top"
              >
                <template #content>Veuillez compléter l'intégralité des informations du réalisateur<br/>
                ainsi que générer son BA pour le voir apparaitre ici</template>
                <el-icon><InfoFilled /></el-icon>
              </el-tooltip>
              <MemberPicker
                v-model="mission.consultant"
                :item-list="consultants"
                placeholder="Intervenant"
                style="flex: 1;"
              />
            </div>
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
        :row-key="row => row.index"
      >
        <el-table-column type="expand">
          <template #default="{ row }">
            <el-row>
                <el-col :span="16">
                  <el-row>
                    Description :
                    <el-input
                      v-model="row.description"
                      type="textarea"
                      :autosize="{ minRows: 5, maxRows: 7}"
                      placeholder="Description de la phase"
                    />
                  </el-row>
                  <el-row>
                    Méthodologie :
                    <el-input
                      v-model="row.methodologie"
                      type="textarea"
                      :autosize="{ minRows: 5, maxRows: 7}"
                      placeholder="Méthodologie de la phase"
                    />
                  </el-row>
                </el-col>
                <el-col :span="6" :offset="1">
                  <el-table :data=" [row] ">
                    <el-table-column
                      label="Cahier des charges liés"
                      prop="requirements"
                      align="center"
                      >
                      <template #default="{ row }">
                        <el-select v-model="row.requirements" multiple placeholder="Sélectionner les références">
                          <el-option
                            v-for="req in requirements"
                            :key="req.id"
                            :label="`[${req.reference}]`"
                            :value="req.id"
                          />
                        </el-select>
                      </template>

                    </el-table-column>
                  </el-table>
                </el-col>
            </el-row>
          </template>
        </el-table-column>
        <el-table-column
          label="Titre"
        >
          <template #default="{row}">
            <el-input
              v-model="row.title"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="110"
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
        <el-table-column
          width="100"
          label="Prix JEH"
        >
          <template #default="{row}">
            <el-input
              v-model="row.priceJEH"
              :min="80"
              :max="300"
            />
          </template>
        </el-table-column>
      </el-table>
      <el-divider />
    </el-form>
    <el-alert
      v-show="modelValue.length == 0"
      title="Vous n'avez ajouté aucun RdM"
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
    requirements: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    phases: { type: Array, required: true },
    consultants: { type: Array, required: true }
  },
  emits: ["save", "phases-selection"],
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

      let validations = []
      for (let i = 0; i < this.modelValue.length; i++) {
        const form = this.$refs['refFormMission' + i][0];
        if (form) {
          validations.push(new Promise((resolve) => {
            form.validate((valid) => {
              if (!valid) {
                result = false
              }
              resolve(valid)
            })
          }))
        }
      }

      Promise.all(validations).then(() => {
        if (result) {
          this.$emit("save", this.deletedMissions, this.deletedPhases)
        } else {
          this.$message({
            message: "Certains champs sont invalides ou les JEH ne sont pas bien répartis.",
            type: "error"
          })
        }
      })
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
            mission.phasesMission.push(originalPhase)
          } else {
            const phase = this.phases.find(phase => phase.id === id)
            phase.priceJEH = 220; // Valeur par défaut
            if (phase) {
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
