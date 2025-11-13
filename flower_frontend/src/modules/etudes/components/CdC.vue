<template>
  <div>
    <el-alert
      v-if="etude.avenants.filter(avenant => avenant.is_cdc).length > 0"
      title="Note"
      description="Il ne s'agit pas du cahier des charges original de l'étude, mais celui d'un avenant."
      type="info"
      show-icon
      :closable="false"
      style="margin-bottom: 20px;"
    />
    <router-link :to="{ name: 'etudes-cdc', params: { id: this.$route.params.id } }">
      <el-button
        v-if="editable"
        type="primary"
        icon="EditPen"
        :loading="loading"
        :disabled="etude.isAborted || etude.state >= 3"
      >
        {{ "Modifier le Cahier des Charges" }}
      </el-button>
    </router-link>
    <div style="margin-top: 20px;">
      <el-table
      :data="requirements">
        <el-table-column
          label="Référence"
          prop="reference"
          width="150px"
          align="center"
          >
          <template #default="{ row }">
            <div style="white-space: pre-wrap;">
              [{{ row.reference }}]
            </div>
          </template>
          
        </el-table-column>
        <el-table-column
          label="Description"
          prop="description"
          >
          <template #default="{ row }">
            <div style="white-space: pre-wrap;">
              {{ row.description }}
            </div>
          </template>
          
        </el-table-column>
        <el-table-column
          label="Phases liées"
          prop="phases"
          width="150px"
          align="center"
          >
          <template #default="{ row }">
            <span>Phase{{ row.phases.length > 1 ? 's' : '' }} : {{ row.phases.map(p => p < 0 ? 'Transverse' : p).join(', ') }}</span>
          </template>

        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import UtilsMixin from "@/mixins/Utils"
export default {
  name: "CdC",
  components: {  },
  mixins: [UtilsMixin],
  props: {
    etude: { type: Object, required: true },
    requirements: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    editable: { type: Boolean, required: true }
  },
  emits: [],
}
</script>
