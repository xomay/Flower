<template>
  <div>
    <div
      v-for="(groupe, index) in value"
      :key="index"
      class="my-4"
    >
      <h2>
        Groupe {{ index + 1 }}
        <el-button
          type="text"
          icon="el-icon-caret-top"
          :disabled="index === 0"
          @click="exchangeGroupes(index, index-1)"
        />
        <el-button
          type="text"
          icon="el-icon-caret-bottom"
          :disabled="index === (value.length - 1)"
          @click="exchangeGroupes(index, index+1)"
        />
        <el-button
          type="text"
          icon="el-icon-delete"
          @click="deleteGroupe(groupe.id, index)"
        />
      </h2>
      <el-input v-model="groupe.title" />
      <el-input
        v-model="groupe.description"
        type="textarea"
      />
      <el-table
        class="grid"
        :data="groupe.phases"
      >
        <el-table-column type="expand">
          <template slot-scope="props">
            <div class="flex flew-row">
              <div class="flex-grow">
                <span>Description :</span>
                <el-input
                  v-model="props.row.description"
                  type="textarea"
                />
              </div>
              <div class="flex-grow">
                <span>Objectifs :</span>
                <el-input
                  v-model="props.row.goals"
                  type="textarea"
                />
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          label="Titre"
        >
          <template slot-scope="props">
            <el-input v-model="props.row.title" />
          </template>
        </el-table-column>
        <el-table-column
          width="110"
          label="Nb JEH"
        >
          <template slot-scope="props">
            <el-input-number
              v-model="props.row.nbJEH"
              controls-position="right"
              :min="1"
              :max="99"
              style="width: 90%"
              size="small"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="100"
          label="Prix JEH"
        >
          <template slot-scope="props">
            <el-input v-model="props.row.priceJEH" />
          </template>
        </el-table-column>
        <el-table-column
          v-if="!small"
          width="150"
          label="Date de début"
        >
          <template slot-scope="props">
            <!-- <el-input v-model="props.row.beginDate"/> -->
            <el-date-picker
              v-model="props.row.beginDate"
              type="date"
              placeholder="Choississez un jour"
              width="200"
              size="mini"
              format="dd-MM-yyyy"
              value-format="yyyy-MM-dd"
            />
          </template>
        </el-table-column>
        <el-table-column
          v-if="!small"
          width="110"
          label="Durée (jours)"
        >
          <template slot-scope="props">
            <el-input-number
              v-model="props.row.period"
              controls-position="right"
              :min="1"
              :max="99"
              style="width: 90%"
              size="small"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="50"
        >
          <template slot-scope="props">
            <el-button
              type="text"
              icon="el-icon-caret-top"
              @click="exchangeItems(index, props.$index, props.$index - 1)"
            /><br>
            <el-button
              type="text"
              icon="el-icon-caret-bottom"
              @click="exchangeItems(index, props.$index, props.$index + 1)"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="50"
        >
          <template slot-scope="props">
            <el-button
              type="text"
              icon="el-icon-delete"
              @click="deletePhase(props.row, groupe)"
            />
          </template>
        </el-table-column>
      </el-table>
      <div class="flex justify-center">
        <el-button
          type="text"
          icon="el-icon-plus"
          @click="addPhase(groupe)"
        >
          Ajouter une phase
        </el-button>
      </div>
    </div>
    <div class="flex justify-center">
      <el-button @click="addGroupe">
        Ajouter un groupe
      </el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "PhasesForm",
  props: {
    value: { type: Array, required: true },
    small: { type: Boolean, required: true }
  },
  methods: {
    addGroupe () {
      this.$emit("add-groupe")
    },
    addPhase (groupe) {
      this.$emit(
        "add-phase",
        groupe
      )
    },
    exchangeGroupes (index1, index2) {
      if (index1 < 0 || index1 >= this.value.length || index2 < 0 || index2 >= this.value.length) {
        return
      }
      [
        this.value[index1].index,
        this.value[index2].index
      ] = [
        this.value[index2].index,
        this.value[index1].index
      ]
      this.value = this.value.sort((a, b) => a.index - b.index)
    },
    exchangeItems (groupe_index, index1, index2) {
      //console.log(`inverting ${index1} and ${index2} in array of length ${this.value[groupe_index].phases.length}`)
      if (index1 < 0 || index1 >= this.value[groupe_index].phases.length || index2 < 0 || index2 >= this.value[groupe_index].phases.length) {
        return
      }
      [
        this.value[groupe_index].phases[index1].index,
        this.value[groupe_index].phases[index2].index
      ] = [
        this.value[groupe_index].phases[index2].index,
        this.value[groupe_index].phases[index1].index
      ]
      this.value[groupe_index].phases = this.value[groupe_index].phases.sort((a, b) => a.index - b.index)
      //console.log(this.value[groupe_index].phases)
    },
    deleteGroupe (groupeId, groupeIndex) {
      this.$emit(
        "delete-groupe",
        {groupeId,
          groupeIndex}
      )
    },
    deletePhase (phase, groupe) {
      this.$emit(
        "delete-phase",
        {phase,
          groupe}
      )
    }
  }
}
</script>
