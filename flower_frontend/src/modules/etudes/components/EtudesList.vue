<template>
  <el-table
    v-loading="loading"
    class="grid"
    :data="etudes"
    :stripe="true"
  >
    <el-table-column
      prop="name"
      label="Nom de l'étude"
      sortable
    >
      <template slot-scope="scope">
        <el-button
          type="text"
          @click="clicked(scope.row.id)"
        >
          {{ scope.row.name }}
        </el-button>
        <span
          v-if="scope.row.confidential"
          class="confiStyle"
        >
          Confidentielle
        </span>
      </template>
    </el-table-column>
    <el-table-column
      prop="number"
      label="Numéro de l'étude"
      sortable
    />
    <el-table-column
      prop="mandat"
      label="Mandat"
      sortable
    />
  </el-table>
</template>

<script>
export default {
  name: "EtudesList",
  props: {
    etudes: {type : Array, required: true },
    loading: {type : Boolean, required: true }
  },
  methods: {
    clicked (id) {
      this.$emit("select", id)
    }
  }
}
</script>