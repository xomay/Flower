<template>
  <div>
    
    <router-link :to="{ name: 'etudes-cdc', params: { id: this.$route.params.id } }">
      <el-button
        v-if="editable"
        type="primary"
        icon="EditPen"
        :loading="loading"
        :disabled="etude.isAborted || this.phases.length === 0"
      >
        {{ "Modifier le Cahier des Charges" }}
      </el-button>
    </router-link>
    <div style="margin-top: 20px;">
      <el-table
      :data="phases">
        <el-table-column
          label="Cahier des Charges"
          prop="CdC"
          >
          <template #default="{ row }">
            <div style="white-space: pre-wrap;">
              {{ row.spec || "Aucun cahier des charges défini pour cette phase." }}
            </div>
          </template>
          
        </el-table-column>
        <el-table-column
          label="Phase"
          prop="index"
          width="100px"
          align="center"
          >
          <template #default="{ row }">
            <span>{{ row.index }}</span>
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
    phases: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    editable: { type: Boolean, required: true }
  },
  emits: [],
}
</script>
