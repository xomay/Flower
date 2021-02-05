<template>
  <div>
    <router-link :to="{ name: 'etudes-phases', params: { id: this.$route.params.id } }">
      <el-button
        type="primary"
        icon="el-icon-edit"
      >
        Modifier les phases
      </el-button>
    </router-link>
    <div
      v-for="(groupe, index) in groupes"
      :key="index"
      class="my-4"
    >
      <h2>Groupe {{ index + 1 }} : {{ groupe.title }}</h2>
      <small>{{ groupe.description }}</small>
      <el-table
        class="grid"
        :data="groupe.phases"
      >
        <el-table-column
          label="Titre"
          prop="title"
        />
        <el-table-column
          width="70"
          label="Nb JEH"
          prop="nbJEH"
        />
        <el-table-column
          width="100"
          label="Prix JEH"
          prop="priceJEH"
        />
      </el-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "Phases",
  props: {
    etude: { type: Object, required: true },
    groupes: { type: Array, required: true }
  }
}
</script>

<style>

</style>
