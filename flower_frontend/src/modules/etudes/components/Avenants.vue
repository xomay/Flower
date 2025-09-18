<template>
  <div>
    <el-alert
      v-if="avenants.length == 0"
      title="Note"
      description="Aucun avenant n'a été créé pour cette étude."
      type="info"
      show-icon
      :closable="false"
      style="margin-bottom: 20px;"
    />
    <el-row>
      <el-button
      :disabled="!canAddAvenant"
      @click="requestNewAvenant()"
      style="margin-bottom: 20px;"
      type="primary"
      icon="Plus"
      >Ajouter un avenant</el-button>
    </el-row>
    <el-timeline>
      <div
        v-for="(avenant, index) in avenants.slice().sort((a, b) => {
          // Les avenants sans date de signature sont considérés comme les plus récents
          if (!a.doc?.signDate && !b.doc?.signDate) return 0;
          if (!a.doc?.signDate) return -1;
          if (!b.doc?.signDate) return 1;
          return new Date(b.doc.signDate) - new Date(a.doc.signDate);
        })"
        :key="index"
        class="timeline-row"
        :class="{ right: avenant?.mission, left: avenant?.etude }"
      >
      <el-timeline-item
        :key="avenant.id"
        :timestamp="avenant?.doc?.signDate ? 'Signé le ' + sqlToDisplayDate(avenant.doc.signDate) : 'En cours d\'édition'"
        placement="top"
        :type="avenant?.doc?.signDate ? 'success' : 'primary'"
        style="width: 50%;"
      >
        <el-card class="timeline-card">
          <el-col>
          <!-- TITRE -->
          <el-row>
            <p class="cardTitle">
              {{ avenant.ref }}
            </p>
          </el-row>
          <!-- TAGS -->
          <el-row style="margin-bottom: 10px;">
            <el-tag
              v-show="avenant.is_delai"
              :hit="true"
              class="tagAv"
              color="#459ff477"
              effect="plain"
            >
              Avenant délai
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
          <span><b>Description : </b>{{ avenant.description }}</span>
          <el-row style="margin-top: 10px;">
            <el-button
            v-show="!avenant?.doc?.signDate"
            icon="Edit"
            type="primary"
            plain
            @click="avenant.etude ? this.$router.push(`/etudes/${this.$route.params.id}/avenants/client/modifier/${avenant.id}`) : this.$router.push(`/etudes/${this.$route.params.id}/avenants/mission/modifier/${avenant.id}`)"
            />
            <el-button
            icon="Download"
            type="primary"
            plain
            @click="infoPopup = true"
            />
            <el-button
            icon="DocumentChecked"
            type="success"
            plain
            @click="signDateForm = true; form.docId = avenant.doc?.id; avenant.etude ? form.is_client = true : form.is_client = false"
            />
            <el-popconfirm 
            title="Etes-vous sûr de vouloir supprimer cet avenant ?"
            confirm-button-text="Oui"
            cancel-button-text="Non"
            confirm-button-type="success"
            cancel-button-type="warning"
            hide-icon
            @confirm="deleteAvenant(avenant)"
            >
              <template #reference>
                <el-button
                icon="Delete"
                type="danger"
                plain
                v-show="!avenant?.doc?.signDate"
                />
              </template>
            </el-popconfirm>
            
          </el-row>
          </el-col>
        </el-card>

        <el-dialog v-model="signDateForm" title="Date de signature du document" width="500">
              <el-form :model="form">
                <el-form-item
                  label="Référence :"
                  prop="ref"
                  label-width="140px"
                >
                  <el-date-picker
                    v-model="form.signDate"
                    format="DD/MM/YYYY"
                    value-format="YYYY-MM-DD"
                    type="date"
                    placeholder="Sélectionnez une date"
                  />
                </el-form-item>
              </el-form>
              <template #footer>
                <div class="dialog-footer">
                  <el-button @click="signDateForm = false">Annuler</el-button>
                  <el-button type="primary" @click="signAvenant(form.docId); signDateForm = false;">
                    Confirmer
                  </el-button>
                </div>
              </template>
            </el-dialog>

            <el-dialog v-model="infoPopup" title="Pas disponible" width="500">
              <span>Le téléchargement n'est pas encore disponible</span>
              <template #footer>
                <div class="dialog-footer">
                  <el-button @click="infoPopup = false">Ok</el-button>
                </div>
              </template>
            </el-dialog>
      </el-timeline-item>
      </div>
    </el-timeline>
  </div>
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
  data() {
    return {
      signDateForm: false,
      infoPopup: false,
      form: {
        signDate: null,
        docId: null,
        is_client: true
      },
    }
  },
  methods: {
    requestNewAvenant () {
      this.$router.push(`/etudes/${this.$route.params.id}/avenants/client/ajouter`)
    },
    deleteAvenant (avenant) {
      this.$emit('delete-avenant', avenant)
    },
    signAvenant (id) {
      this.$emit('sign-avenant', id, this.form.signDate, this.form.is_client)
    }
  }
}
</script>

<style scoped>
  .cardTitle {
    font-size: 120%;
    font-weight: bold;
    color: black;
    margin-bottom: 10px;
  }
  .avenantCard {
    display: flex;
    flex-direction: row-reverse;
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
  .left {
    justify-content: flex-start;
  }
  .right {
    justify-content: flex-end;
  }
  .timeline-row {
    display: flex;
    align-items: center;
    position: relative;
  }
  .timeline-card {
    max-width: 800px;
  }
</style>