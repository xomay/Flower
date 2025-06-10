<template>
  <div>
    <div
      v-for="(groupe, index) in modelValue"
      :key="index"
      class="my-4"
    >
      <el-table
        class="grid"
        :data="groupe.phases"
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
              size="small"
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
              size="small"
              format="DD-MM-YYYY"
              value-format="YYYY-MM-DD"
              :disabled="disabled"
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
              size="small"
              :disabled="disabled"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="50"
        >
          <template v-slot="props">
            <el-button
              type="text"
              icon="Top"
              :disabled="disabled"
              @click="exchangeItems(index, props.$index, props.$index - 1)"
            /><br>
            <el-button
              type="text"
              icon="Bottom"
              :disabled="disabled"
              @click="exchangeItems(index, props.$index, props.$index + 1)"
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
          @click="addPhase(groupe)"
        >
          Ajouter une phase
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PhasesForm",
  props: {
    modelValue: { type: Array, required: true },
    small: { type: Boolean, required: true },
    disabled: { type: Boolean, default: false }
  },
  emits: ["update:modelValue","add-groupe", "add-phase", "add-us", "delete-phase", "delete-group", "delete-us"],
  methods: {
    addGroupe () {
      this.$emit("add-groupe")
    },
    addPhase (groupe) {
      this.$emit("add-phase", groupe)
    },
    addUS (phase) {
      this.$emit("add-us", phase)
    },
    exchangeGroupes (index1, index2) {
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
      this.modelValue = this.modelValue.sort((a, b) => a.index - b.index)
    },
    exchangeItems (groupe_index, index1, index2) {
      if (index1 < 0 || index1 >= this.modelValue[groupe_index].phases.length || index2 < 0 || index2 >= this.modelValue[groupe_index].phases.length) {
        return
      }
      [
        this.modelValue[groupe_index].phases[index1].index,
        this.modelValue[groupe_index].phases[index2].index
      ] = [
        this.modelValue[groupe_index].phases[index2].index,
        this.modelValue[groupe_index].phases[index1].index
      ]
      this.modelValue[groupe_index].phases = this.modelValue[groupe_index].phases.sort((a, b) => a.index - b.index)
    },
    deleteGroupe (groupeId, groupeIndex) {
      this.$emit("delete-groupe", {groupeId, groupeIndex})
    },
    deletePhase (phase, groupe) {
      this.$emit("delete-phase", {phase, groupe})
    },
    deleteUS (us, phase) {
      this.$emit("delete-us", {us, phase})
    }
  }
}
</script>
