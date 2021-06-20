<template>
  <dir>
    <el-alert
      v-if="avenants.length == 0"
      title="Note"
      description="Aucun avenant n'a été créé pour cette étude."
      type="info"
      show-icon
      :closable="false"
      style="margin-bottom: 20px;"
    />
    <el-timeline>
      <el-timeline-item
        v-show="avenants.length > 0"
        placement="top"
        type="primary"
        :hide-timestamp="true"
      >
        <el-card>
          Étude originelle
        </el-card>
      </el-timeline-item>
      <el-timeline-item
        v-for="avenant in avenants"
        :key="avenant.id"
        :timestamp="sqlToDisplayDate(avenant.signature_date)"
        placement="top"
        type="success"
        size="large"
      >
        <el-card>
          <!-- TITRE -->
          <el-row>
            <p class="cardTitle">
              {{ avenant.reference }}
            </p>
          </el-row>
          <!-- TAGS -->
          <el-row>
            <el-tag
              v-show="avenant.is_delais"
              :hit="true"
              class="tagAv"
              color="#459ff477"
              effect="plain"
            >
              Avenant délais
            </el-tag>
            <el-tag
              v-show="avenant.is_methodo"
              :hit="true"
              class="tagAv"
              color="#c674e477"
              effect="dark"
            >
              Avenant méthodologie
            </el-tag>
            <el-tag
              v-show="avenant.is_cdc"
              :hit="true"
              class="tagAv"
              color="#b5cc2677"
              effect="light"
            >
              Avenant cahier des charges
            </el-tag>
            <el-tag
              v-show="avenant.is_budget"
              :hit="true"
              class="tagAv"
              color="#da952477"
              effect="plain"
            >
              Avenant budget
            </el-tag>
          </el-row>
          <!-- Commentaire -->
          <el-row>
            <div class="leftCol">
              <b>Commentaire :</b>
            </div>
            <div class="rightCol">
              {{ avenant.comment }}
            </div>
          </el-row>
          <el-row v-show="avenant.is_delais">
            <div class="leftCol">
              <b>Nouveau délai :</b>
            </div>
            <div class="rightCol">
              {{ sqlToDisplayDate(avenant.new_dates) }}
            </div>
          </el-row>
        </el-card>
      </el-timeline-item>
      <el-timeline-item
        placement="top"
        type="info"
        :hide-timestamp="true"
      >
        <el-button
          :disabled="!canAddAvenant"
          type="warning"
          @click="requestNewAvenant()"
        >
          Ajouter un avenant
        </el-button>
      </el-timeline-item>
    </el-timeline>
  </dir>
</template>

<script>
import Utils from "@/mixins/Utils"
export default {
  name: "Avenants",
  mixins: [Utils],
  props: {
    avenants: { type: Array, required: true },
    canAddAvenant: { type: Boolean, default: true }
  },
  methods: {
    requestNewAvenant () {
      this.$router.push(`/etudes/${this.$route.params.id}/avenants/ajouter`)
    }
  }
}
</script>

<style>
  .cardTitle {
    font-size: 120%;
    font-weight: bold;
    color: black;
    margin-bottom: 10px;
  }
  .tagAv {
    margin-right: 5px;
    color: rgb(37, 37, 37);
  }
  /* Override le truc de base */
  .el-timeline-item__timestamp {
    color: #121213;
    line-height: 1;
    font-size: 13px;
    font-weight: 600;
  }
  /* colonnes */
  .leftCol {
    width: 110px;
    float:left;
  }
  .rightCol {
    float:left;
    margin-left: 20px;
    margin-bottom: 20px;
  }
</style>