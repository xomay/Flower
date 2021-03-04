<template>
  <div>
    <router-link :to="{ name: 'etudes-phases', params: { id: this.$route.params.id } }">
      <el-button
        v-if="editable"
        type="primary"
        icon="el-icon-edit"
        :loading="loading"
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
          <template slot-scope="scope">
            <USManager
              :uss="scope.row.uss"
              :loading="loading"
              @us-change="updateUS"
            />
          </template>
        </el-table-column>
        <el-table-column
          label="Titre"
          prop="title"
        >
          <template slot-scope="scope">
            {{ scope.row.title }} : <i><font color="gray">{{ scope.row.description }}</font></i>
          </template>
        </el-table-column>
        <el-table-column
          width="120"
          label="Date de début"
          prop="beginDate"
          :formatter="niceDateFormatter"
        />
        <el-table-column
          width="120"
          label="Date de fin"
          prop="finishDate"
          :formatter="niceDateFormatter"
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
          :formatter="euroFormatter"
        />
        <el-table-column
          width="100"
          label="Prix total"
          prop="totalPrice"
          :formatter="euroFormatter"
        />
      </el-table>
    </div>
  </div>
</template>

<script>
import UtilsMixin from "@/mixins/Utils"
import USManager from "./USManager"
export default {
  name: "Phases",
  components: { USManager },
  mixins: [UtilsMixin],
  props: {
    etude: { type: Object, required: true },
    groupes: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    editable: { type: Boolean, required: true }
  },
  methods: {
    updateUS (us, newState) {
      this.$emit("us-change", us, newState)
    }
  }
}
</script>

<style scoped>
  .fatH2 {
    font-size: 1.2em;
    font-weight: bold;
  }
</style>