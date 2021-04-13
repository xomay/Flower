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
            <el-row
              v-if="!reaVue"
              v-show="scope.row.methodologie != ''"
              style="margin-bottom: 20px;"
            >
              <b>Méthodologie :</b><br>
              <p>{{ scope.row.methodologie }}</p>
              <hr
                style="border-width: 1px; border-color: #bfbfd7; width: 30%; margin: auto auto;"
              >
            </el-row>
            <el-row>
              <USManager
                :uss="scope.row.uss"
                :loading="loading"
                :rea-vue="reaVue"
                @us-change="updateUS"
              />
            </el-row>
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
          v-if="!reaVue"
          width="100"
          label="Prix JEH"
          prop="priceJEH"
          :formatter="euroFormatter"
        />
        <el-table-column
          v-if="!reaVue"
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
    editable: { type: Boolean, required: true },
    reaVue: { type: Boolean, default: false }
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