<template>
  <el-table
    class="grid"
    :data="modelValue"
  >
    <el-table-column
      prop="documentType"
      label="Type de PVR"
    >
      <template slot-scope="scope">
        <span v-if="scope.row.documentType === 'I'">PVRI</span>
        <span v-else>PVRF</span>
      </template>
    </el-table-column>
    <el-table-column
      prop="deliverable"
      label="Description"
    />
    <el-table-column
      prop="signingDate"
      label="Date de signature"
    />
    <el-table-column
      label="Opérations"
    >
      <template slot-scope="scope">
        <el-button
          type="text"
          icon="Download"
          :loading="loading"
          @click="$emit('download', scope.row.id)"
        />
        <router-link :to="`/etudes/${$route.params.id}/pvr/modifier/${scope.row.id}`">
          <el-button
            type="text"
            icon="Edit"
          />
        </router-link>
        <el-button
          type="text"
          icon="Delete"
          :loading="loading"
          @click="$emit('delete', scope.row.id, scope.$index)"
        />
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  name: "PVRTable",
  props: {
    modelValue: { type: Array, required: true },
    loading: { type: Boolean, required: true }
  },
  emits: ["download", "delete"],
  methods: {
    clickDownload (id) {
      this.$emit("download", id)
    },
    clickDelete (id, index) {
      this.$emit("delete", id, index)
    }
  }
}
</script>