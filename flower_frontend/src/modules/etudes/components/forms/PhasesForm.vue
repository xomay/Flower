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
                      :disabled="disabled || !is_methodo"
                    />
                  </el-row>
                  <el-row>
                    Méthodologie :
                    <el-input
                      v-model="row.methodologie"
                      type="textarea"
                      :autosize="{ minRows: 5, maxRows: 7}"
                      placeholder="Méthodologie de la phase"
                      :disabled="disabled || !is_methodo"
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
                          :disabled="disabled || !is_methodo || !is_budget || !is_delai"
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
                          :disabled="disabled || !is_methodo || !is_budget || !is_delai"
                          @click="deleteUS(usRow, row)"
                        />
                      </template>
                    </el-table-column>
                  </el-table>
                  <el-button
                    type="text"
                    icon="Plus"
                    :disabled="disabled || !is_methodo || !is_budget || !is_delai"
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
              :disabled="disabled || !is_methodo"
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
              :disabled="disabled || !is_budget"
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
              :disabled="disabled || !is_budget"
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
              :disabled="disabled || !is_delai"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="50"
        >
          <template #default="{row}">
            <el-button
              type="text"
              :disabled="disabled || !is_methodo"
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
          :disabled="disabled || !is_methodo || !is_budget || !is_delai"
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
    disabled: { type: Boolean, default: false },
    is_delai: { type: Boolean, default: true },
    is_methodo: { type: Boolean, default: true },
    is_budget: { type: Boolean, default: true },
  },
  emits: ["update:modelValue", "add-phase", "add-us", "delete-phase", "delete-group", "delete-us"],
  computed: {
    sortedPhases() {
      return [...this.modelValue].sort((a, b) => a.index - b.index)
    }
  },
  methods: {
    addPhase () {
      this.$emit("add-phase")
    },
    addUS (phase) {
      this.$emit("add-us", phase)
    },
    exchangePhases (index1, index2) {
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
    }
  }
}
</script>
