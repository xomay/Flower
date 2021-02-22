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
      <h2 class="fatH2">
        Groupe {{ index + 1 }} : {{ groupe.title }}
      </h2>
      <small>{{ groupe.description }}</small>
      <el-table
        class="grid"
        :data="groupe.phases"
        style="color: black;"
        :header-row-style="{color: 'black'}"
      >
        <el-table-column type="expand">
          <template slot-scope="props">
            <div
              class="flex flew-row"
              style="color: #606266;"
            >
              <div class="flex-grow">
                <span>Description :</span><br>
                <i>{{ props.row.description }}</i>
              </div>
              <div class="flex-grow">
                <span>Objectifs :</span><br>
                <i>{{ props.row.goals }}</i>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          label="Titre"
          prop="title"
        />
        <el-table-column
          width="120"
          label="Date de début"
          prop="beginDate"
        >
          <template slot-scope="scope">
            {{ niceDate(scope.row.beginDate) }}
          </template>
        </el-table-column>
        <el-table-column
          width="120"
          label="Date de fin"
          prop="finishDate"
        >
          <template slot-scope="scope">
            {{ niceDate(scope.row.finishDate) }}
          </template>
        </el-table-column>
        <el-table-column
          width="70"
          label="Nb JEH"
          prop="nbJEH"
        />
        <el-table-column
          width="100"
          label="Prix JEH"
          prop="priceJEH"
        >
          <template slot-scope="scope">
            {{ scope.row.priceJEH }} €
          </template>
        </el-table-column>
        <el-table-column
          width="100"
          label="Prix total"
          prop="totalPrice"
        >
          <template slot-scope="scope">
            {{ scope.row.totalPrice }} €
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import UtilsMixin from "@/mixins/Utils"
export default {
  name: "Phases",
  mixins: [UtilsMixin],
  props: {
    etude: { type: Object, required: true },
    groupes: { type: Array, required: true }
  }
}
</script>

<style scoped>
  .fatH2 {
    font-size: 1.2em;
    font-weight: bold;
  }
</style>