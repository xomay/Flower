<template>
  <div>
      <el-table
        class="grid"
        :data="modelValue.sort((a, b) => a.index - b.index)"
        :row-key="row => row.id"
      >
        <el-table-column type="expand">
          <template #default="{ row }">
            <el-row>
                <el-col :span="12">
                  <el-row>
                    Description :
                    <el-input
                      v-model="row.description"
                      type="textarea"
                      :autosize="{ minRows: 5, maxRows: 7}"
                      placeholder="Description de la phase"
                      :disabled="disabled"
                    />
                  </el-row>
                  <el-row>
                    Méthodologie :
                    <el-input
                      v-model="row.methodologie"
                      type="textarea"
                      :autosize="{ minRows: 5, maxRows: 7}"
                      placeholder="Méthodologie de la phase"
                      :disabled="disabled"
                    />
                  </el-row>
                </el-col>
                <el-col
                  :span="10"
                  :offset="1"
                >
                  <el-table
                    :data="row.uss"
                  >
                    <el-table-column
                      label="Liste des US"
                      align="center"
                    >
                      <template #default="{ row : usRow}">
                        <el-input
                          v-model="usRow.name"
                          type="text"
                          placeholder="Nom de l'US"
                          :disabled="disabled"
                        />
                      </template>
                    </el-table-column>
                    <el-table-column
                      label=""
                      align="center"
                      width="80px"
                      fixed="right"
                    >
                      <template #default="{ row: usRow }">
                        <el-button
                          icon="Minus"
                          type="danger"
                          plain
                          :disabled="disabled"
                          @click="deleteUS(usRow, row)"
                        />
                      </template>
                    </el-table-column>
                  </el-table>
                  <el-button
                    type="text"
                    icon="Plus"
                    :disabled="disabled"
                    @click="addUS(row)"
                  >
                    Ajouter une US
                  </el-button>
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
              :disabled="disabled"
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
              :max="99"
              style="width: 90%"
              :disabled="disabled"
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
              :disabled="disabled"
            />
          </template>
        </el-table-column>
        <el-table-column
          v-if="!small"
          width="150"
          label="Date de début"
        >
          <template #default="{row}">
            <el-date-picker
              v-model="row.beginDate"
              type="date"
              placeholder="Choisissez un jour"
              width="200"
              format="DD-MM-YYYY"
              value-format="YYYY-MM-DD"
              :disabled="disabled || row.index !== 1"
              @change="calculateDates"
            />
          </template>
        </el-table-column>
        <el-table-column
          v-if="!small"
          width="110"
          label="Durée (jours)"
        >
          <template #default="{row}">
            <el-input-number
              v-model="row.period"
              controls-position="right"
              :min="1"
              :max="99"
              style="width: 90%"
              :disabled="disabled"
              @change="calculateDates"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="50"
        >
          <template #default="{ row, $index }">
            <el-button
              type="text"
              icon="Top"
              :disabled="disabled"
              @click="exchangePhases($index, $index - 1)"
            /><br>
            <el-button
              type="text"
              icon="Bottom"
              :disabled="disabled"
              @click="exchangePhases($index, $index + 1)"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="50"
        >
          <template #default="{row}">
            <el-button
              type="text"
              :disabled="disabled"
              icon="Delete"
              @click="deletePhase(row, groupe)"
            />
          </template>
        </el-table-column>
      </el-table>
      <div class="flex justify-center">
        <el-button
          type="text"
          icon="Plus"
          :disabled="disabled"
          @click="addPhase()"
        >
          Ajouter une phase
        </el-button>
      </div>
    </div>
</template>

<script>
import phases from "@/modules/etudes/components/Phases.vue";

export default {
  name: "PhasesForm",
  computed: {
    phases() {
      return phases
    }
  },
  props: {
    modelValue: { type: Array, required: true },
    small: { type: Boolean, required: true },
    disabled: { type: Boolean, default: false }
  },
  emits: ["update:modelValue","add-groupe", "add-phase", "add-us", "delete-phase", "delete-group", "delete-us"],
  methods: {
    addPhase () {
      this.$emit("add-phase")
    },
    addUS (phase) {
      this.$emit("add-us", phase)
    },
    exchangePhases (index1, index2) {
      console.log("exchangePhases", index1, index2)
      if (index1 < 0 || index1 >= this.modelValue.length || index2 < 0 || index2 >= this.modelValue.length) {
        return
      }
      [
        this.modelValue[index1].index,
        this.modelValue[index2].index
      ] = [
        this.modelValue[index2].index,
        this.modelValue[index1].index
      ]
      // Crée une nouvelle copie triée
      const sorted = [...this.modelValue].sort((a, b) => a.index - b.index)
      // Émet la mise à jour vers le parent
      this.$emit('update:modelValue', sorted)
    },
    deletePhase (phase) {
      this.$emit("delete-phase", {phase})
    },
    deleteUS (us, phase) {
      this.$emit("delete-us", {us, phase})
    },
    calculateDates () {
      const formatDate = (date) => {
        if (!(date instanceof Date)) date = new Date(date)
        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const day = String(date.getDate()).padStart(2, '0')
        return `${year}-${month}-${day}`
      }
      const sortedPhases = [...this.modelValue].sort((a, b) => a.index - b.index)
      
      for (let i = 0; i < sortedPhases.length; i++) {
        const phase = sortedPhases[i]
        if (i === 0) {
          if (!phase.beginDate || isNaN(new Date(phase.beginDate))) continue
          const begin = new Date(phase.beginDate)
          const finish = new Date(begin)
          finish.setDate(begin.getDate() + (phase.period || 0) - 1)
          phase.beginDate = formatDate(begin)
          phase.finishDate = formatDate(finish)
        } else {
          const previous = sortedPhases[i - 1]
          if (!previous.finishDate || isNaN(new Date(previous.finishDate))) continue
          const begin = new Date(previous.finishDate)
          begin.setDate(begin.getDate() + 1)
          const finish = new Date(begin)
          finish.setDate(begin.getDate() + (phase.period || 0) - 1)
          phase.beginDate = formatDate(begin)
          phase.finishDate = formatDate(finish)
        }
      }

      this.$emit('update:modelValue', sortedPhases)
    }
  }
}
</script>
