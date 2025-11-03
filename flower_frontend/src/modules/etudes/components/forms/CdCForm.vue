<template>
    <el-table
      :data="modelValue"
      style="margin-top: 20px;"
    >
      <el-table-column
        label="Référence"
        prop="reference"
        width="150"
        >
        <template #default="{ row }">
          <el-input
            v-model="row.reference"
            type="text"
            :formatter="(value) => value.toUpperCase()"
            :parser="(value) => value.toUpperCase()"
            placeholder="Référence du point"
          />
        </template>
        
      </el-table-column>
      <el-table-column
        label="Description"
        prop="description"
        >
        <template #default="{ row }">
          <el-input
            v-model="row.description"
            type="textarea"
            :autosize="{ minRows: 4}"
            placeholder="Description de la référence"
          />
        </template>
        
      </el-table-column>
      <el-table-column
        label="Phases liées"
        prop="phases"
        width="150px"
        align="center"
        >
        <template #default="{ row }">
          <el-select v-model="row.phases" multiple placeholder="Sélectionner les phases">
            <el-option
              v-for="phase in phases"
              :key="phase.id"
              :label="`Phase ${phase.index > 0 ? phase.index : 'Transverse ' + Math.abs(phase.index)} : ${phase.title}`"
              :value="phase.index"
            />
          </el-select>
        </template>

      </el-table-column>
      <el-table-column
        width="50"
        align="center"
      >
        <template #default="{row}">
          <el-button
            type="text"
            :disabled="disabled"
            icon="Delete"
            @click="deleteRequirement(row)"
          />
        </template>
      </el-table-column>
    </el-table>
    <div class="flex justify-center">
      <el-button
        type="text"
        icon="Plus"
        @click="addRequirement()"
      >
        Ajouter un point au Cahier des Charges
      </el-button>
    </div>
</template>

<script>
export default {
  name: "CdCForm",
  components: {  },
  props: {
    modelValue: { type: Object, required: true },
    phases: { type: Array, required: true },
    disabled: { type: Boolean, default: false },
    loading: { type: Boolean, default: false }
  },
  emits: ["update:modelValue", "add-requirement", "delete-requirement"],
  methods: {
    addRequirement() {
      this.$emit("add-requirement")
    },
    deleteRequirement(row) {
      this.$emit("delete-requirement", row)
    }
  }
}

</script>