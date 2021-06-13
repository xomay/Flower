<template>
  <BaseComponent
    :title="etude.name"
    :breadcrumb="breadcrumb"
  >
    <template v-slot:action>
      <router-link :to="`/etudes/${$route.params.id}/modifier`">
        <el-button
          type="text"
          icon="el-icon-edit"
        >
          Modifier
        </el-button>
      </router-link>
    </template>
    <el-alert
      v-if="no_phases"
      title="Attention"
      description="Aucune phase n'a été définie pour cette étude."
      type="error"
      show-icon
      :closable="false"
    />
    <el-tabs
      v-model="currentTab"
      @tab-click="handleTabChange"
    >
      <el-tab-pane
        label="Récapitulatif"
        name="Récapitulatif"
      />
      <el-tab-pane
        label="Phases"
        name="Phases"
      />
      <el-tab-pane
        v-if="!no_phases"
        label="Rédaction"
        name="Rédaction"
      />
      <el-tab-pane
        v-if="!no_phases"
        label="Avenants"
        name="Avenants"
      />
      <el-tab-pane
        label="Avancement"
        name="Avancement"
      />
    </el-tabs>
    <div v-show="currentTab === 'Récapitulatif'">
      <Summary
        :etude="etude"
      />
      <hr style="margin: 12px; margin-bottom: 25px">
      <div>
        <b>Fichiers associés :</b>
        <UploaderLocal
          :inital-list="etude.linkedFiles"
          :loading="loading"
          api-base-url="etudes"
        />
      </div>
    </div>
    <Phases
      v-show="currentTab === 'Phases'"
      :groupes="etude.currentGroupes.groupes"
      :are-groupes-originals="etude.isOriginalGroupes"
      :etude="etude"
      :editable="true"
      :loading="loading"
      @us-change="usChanged"
    />
    <Generation
      v-show="currentTab === 'Rédaction'"
      :etude="etude"
      @deleteInvoice="deleteInvoice"
    />
    <Avenants
      v-show="currentTab === 'Avenants'"
      :can-add-avenant="etude.state < 6"
      :avenants="etude.avenants"
    />
    <ManageStep
      v-show="currentTab === 'Avancement'"
      :etude="etude"
    />
  </BaseComponent>
</template>

<script>
import Summary from "../../components/Summary"
import Phases from "../../components/Phases"
import Generation from "../../components/Generation"
import ManageStep from "../../components/ManageStep"
import UploaderLocal from "@/components/UploaderLocal"
import Avenants from "../../components/Avenants"

const axios = require("axios")

export default {
  name: "EtudeDetail",
  components: {Summary, Phases, Generation, ManageStep, UploaderLocal, Avenants},
  data () {
    return {
      currentTab: this.$route.query.active || "Récapitulatif",
      loading: false,
      etude: {
        name: "", // valeurs par défault afin d'éviter des warnings inutiles.
        currentGroupes: {groupes:[]},
        linkedFiles: [],
        isOriginalGroupes: true,
        avenants: []
      },
      no_phases: false,
      breadcrumb: [
        {
          name: "Suivi d'étude",
          link: "/etudes"
        },
        {
          name: "<loading>",
          link: `/etudes/${this.$route.params.id}/voir`
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.etude = res.data
      this.breadcrumb[1].name = this.etude.name
      this.no_phases = this.etude.currentGroupes.groupes.length < 1
    }).catch(() => {
      this.$message({ message: "Impossible de récupérer l'étude pour le moment", type: "error" })
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    handleTabChange (tab) {
      this.$router.push({query: {active: tab.label}})
    },
    deleteInvoice (invoiceId) {
      this.etude.invoices = this.etude.invoices.filter(i => i.id !== invoiceId)
    },
    usChanged (us, newState) {
      this.loading = true
      axios.put(
        `/api/etudes/uss/${us.id}/`,
        {
          ...us,
          state: newState
        },
        { withCredentials: true }
      ).then(() => {
        this.$message({message: "US mis à jour", type: "success"})
        us.state = newState
      }).catch((err) => {
        this.$message({message: "Impossible de mettre à jour l'US : " + err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    }
  }
}
</script>
