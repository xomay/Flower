<template>
  <div>
      <template slot="title">
        <b><u>Note :</u> Il ne s'agit pas des phases originales de l'étude, mais celles d'un avenant.</b>
      </template>
    <router-link :to="{ name: 'etudes-phases', params: { id: this.$route.params.id } }">
      <el-button
        v-if="editable"
        type="primary"
        icon="EditPen"
        :loading="loading"
        :disabled="etude.isAborted"
      >
        {{ this.phases.length > 0 ? "Modifier les phases" : "Créer les phases" }}
      </el-button>
    </router-link>
      <el-table
        class="grid"
        :data="phases.sort((a, b) => a.index - b.index)"
        style="color: black; width: 100%;"
        :header-row-style="{color: 'black'}"
        :row-key="row => row.id"
      >
        <el-table-column type="expand" >
          <template #default="{ row }">
            <div style="margin-left: 40px; margin-top: 10px;">
              <el-row
              v-if="!reaVue"
              v-show="row.methodologie != ''"
              style="margin-bottom: 20px;"
              >
              <b>Méthodologie :</b><br>
              <div style="white-space: pre-wrap;">
                {{ row.methodologie }}
              </div>
              <hr
              style="border-width: 1px; border-color: #bfbfd7; width: 30%; margin: auto auto;"
              >
            </el-row>
            <USManager
            :uss="row.uss"
            :loading="loading"
            :rea-vue="reaVue"
            :disabled="etude.isAborted"
            @us-change="updateUS"
            />
            </div>
          </template>
        </el-table-column>
        <el-table-column
          label="Titre"
          prop="title"
        >
          <template #default="{row}">
            {{ row.title }} : <i><p color="gray">{{ row.description }}</p></i>
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
    phases: { type: Array, required: true },
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