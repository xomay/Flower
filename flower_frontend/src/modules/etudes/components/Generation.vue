<template>
  <div>
    <el-button
      type="success"
      :loading="loading"
      :disabled="!allowDevisGenerate"
      icon="Download"
      @click="downloadDevis"
    >
      Générer le devis
    </el-button>
    <el-collapse
      v-model="activeCollapses"
      class="mt-2"
    >
      <el-collapse-item name="0">
        <template #title>
          <span class="mr-2 text-lg">{{ etude.hasCC ? 'Bon de Commande' : "Convention d'Étude" }}</span>
        </template>
        <router-link
          class="mr-2"
          :to="`/etudes/${$route.params.id}/convention-etude`"
        >
          <el-button
            type="primary"
            icon="Edit"
            :disabled="etude.isAborted"
          >
            Rédiger {{ etude.hasCC ? 'le BC' : "la CE" }}
          </el-button>
        </router-link>
        <el-button
          v-if="displaysCE"
          type="success"
          :loading="loading"
          icon="Download"
          @click="downloadCE"
        >
          Générer {{ etude.hasCC ? 'le BC' : "la CE" }}
        </el-button>
        <el-button
          v-else
          type="success"
          plain
          disabled
        >
          Générer {{ etude.hasCC ? 'le BC' : "la CE" }}
        </el-button>
      </el-collapse-item>
      <el-collapse-item name="1">
        <template #title>
          <span class="mr-2 text-lg">Récapitulatifs de mission</span> <router-link :to="`/etudes/${$route.params.id}/missions`">
            <el-button
              type="text"
              icon="Edit"
              :disabled="etude.isAborted"
            >
              Modifier
            </el-button>
          </router-link>
        </template>
        <el-table
          class="grid"
          :data="etude.missions"
        >
          <el-table-column
            label="Consultant"
            align="center"
          >
            <template #default="{row}">
              <el-link
                type="primary"
                :style="'margin-left: 6px'"
                @click="pushToConsultant(row)"
              >
                {{ nicePeople(row.consultant) }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column
            prop="missionBegin"
            label="Date de début"
            align="center"
            :formatter="niceDateFormatter"
          />
          <el-table-column
            prop="missionEnd"
            label="Date de fin"
            align="center"
            :formatter="niceDateFormatter"
          />
          <el-table-column
            label="Nombre de phases"
            align="center"
          >
            <template #default="{row}">
              <span>{{ row.phases.length }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="JEHNumber"
            label="Nombre de JEH"
            align="center"
          />
          <el-table-column
            label="Montant brut"
            align="center"
          >
            <template #default="{row}">
              <span>{{ row.remunerationRaw }}€</span>
            </template>
          </el-table-column>
          <el-table-column
            label="Opérations"
            align="center"
            fixed="right"
          >
            <template #default="{row}">
              <el-button
                type="text"
                icon="Download"
                :loading="loading"
                @click="downloadRDM(row.id)"
              >
                RDM
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
      <el-collapse-item name="2">
        <template #title>
          <span class="mr-2 text-lg">PVR</span> <router-link :to="`/etudes/${$route.params.id}/pvr/ajouter`">
            <el-button
              type="text"
              icon="Plus"
              :disabled="etude.isAborted"
            >
              Ajouter
            </el-button>
          </router-link>
        </template>
        <el-table
          class="grid"
          :data="etude.pvr"
        >
          <el-table-column
            prop="documentType"
            label="Type de PVR"
            align="center"
            fixed="left"
          >
            <template #default="{row}">
              <span v-if="row.documentType === 'I'">PVRI</span>
              <span v-else>PVRF</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="deliverable"
            label="Description"
            align="center"
          />
          <el-table-column
            prop="signingDate"
            label="Date de signature"
            align="center"
            :formatter="niceDateFormatter"
          />
          <el-table-column
            label="Opérations"
            align="center"
            fixed="right"
          >
            <template #default="{ row, $index }">
              <el-button
                type="text"
                icon="Download"
                :loading="loading"
                @click="downloadPVR(row.id)"
              />
              <router-link :to="`/etudes/${$route.params.id}/pvr/modifier/${scope.row.id}`">
                <el-button
                  type="text"
                  icon="Edit"
                  :disabled="etude.isAborted"
                />
              </router-link>
              <el-button
                type="text"
                icon="Delete"
                :loading="loading"
                :disabled="etude.isAborted"
                @click="deletePVR(row.id, $index)"
              />
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
const axios = require("axios")
import Publishing from "@/mixins/Publishing"
import Utils from "@/mixins/Utils"

export default {
  name: "Generation",
  mixins: [Publishing, Utils],
  props: {
    etude: { type: Object, required: true }
  },
  data () {
    return {
      displaysCE: null,
      loading: false,
      activeCollapses: []
    }
  },
  computed: {
    allowDevisGenerate () { return this.etude.currentGroupes.groupes.length > 0 }
  },
  created () {
    axios.get(
      `/api/etudes/${this.$route.params.id}/ce/`,
      {withCredentials: true}
    ).then((response) => {
      this.displaysCE = response.data.description != ""
    }).catch(err => {
      this.$message({ message: "Erreur lors de la récupération de l'étude : " + err, type: "error" })
    })
  },
  methods: {
    deleteInvoice (invoiceId) {
      this.loading = true
      axios.delete(
        `/api/tresorerie/factures/${invoiceId}/`,
        { withCredentials: true}
      ).then(() => {
        this.$message({message: "Facture supprimée avec succès.", type: "success"})
        this.$emit("deleteInvoice", invoiceId)
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer la facture : " + err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deletePVR (pvrId, index) {
      axios.delete(`/api/pvr/${pvrId}`, { withCredentials: true }).then(() => {
        this.etude.pvr.splice(index, 1)
      }).catch(err => {
        this.$message({ message: err, type: "error", offset: 40 })
      })
    },
    pushToConsultant (mission) {
      if(mission.consultant != undefined) {
        this.$router.push(`/realisateurs/${mission.consultant.id}/voir`)
      }
    }
  }
}
</script>
