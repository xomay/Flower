<template>
  <div class="flex flex-col">
    <el-steps
      direction="vertical"
      process-status="finish"
      finish-status="success"
      :active="etude.state"
    >
      <!-- DEVIS (0) -->
      <el-step title="Proposition Commerciale">
        <template #description>
          <el-card>
            <div>
              Une fois l'étude enregistrée et les phases renseignées, la <b>PC</b> peut être générée. Elle doit être envoyé au prospect.
            </div>
            <el-row class="stCardRw">
              <el-button
                :disabled="!btn_devis_generate"
                :loading="loading"
                type="primary"
                plain
                icon="Download"
              >
                Générer la PC
              </el-button>
              <el-button
                v-show="btn_devis_levelup"
                :loading="loading"
                type="success"
                icon="Check"
                @click="levelupTo(1)"
              >
                La PC a été acceptée
              </el-button>
              <el-alert
                v-show="btn_devis_help"
                title="Phases non rédigées"
                type="warning"
                description="Appuyez sur Phases puis 'Modifier les phases' afin de créer les phases de cette étude."
                :closable="false"
                center
                effect="dark"
                show-icon
              />
            </el-row>
          </el-card>
        </template>
      </el-step>
      <!-- CE (1) -->
      <el-step :title="etude.hasCC ? 'BC' : 'CE'">
        <template #description>
          <el-card>
            <template v-if="etude.hasCC">
              Le <b>B</b>on de <b>C</b>ommande doit être rédigé puis envoyé au client. Il contient la proposition commerciale.
            </template>
            <template v-else>
              La <b>C</b>onvention d'<b>É</b>tude doit être rédigée puis envoyé au client. Elle contient la proposition commerciale.
            </template>
            <el-row class="stCardRw">
              <el-button
                type="primary"
                :loading="loading"
                icon="Download"
                :disabled="!btn_ce_generate"
                plain
                @click="downloadCE"
              >
                Générer {{ etude.hasCC ? 'le BC' : "la CE" }}
              </el-button>
              <router-link
                v-show="!btn_ce_generate"
                class="mr-2"
                :to="`/etudes/${$route.params.id}/convention-etude`"
              >
                <el-button
                  type="primary"
                  :loading="loading"
                  icon="Download"
                  :disabled="!btn_ce_generate"
                  plain
                  @click="downloadCE"
                >
                  Générer {{ etude.hasCC ? 'le BC' : "la CE" }}
                </el-button>
              </router-link>
              <el-button
                v-show="btn_ce_levelup"
                :loading="loading"
                type="success"
                icon="Check"
                @click="levelupTo(2)"
              >
                {{ etude.hasCC ? 'Le BC' : "La CE" }} a été signé
              </el-button>
              <el-alert
                v-show="btn_ce_help"
                :title="etude.hasCC ? 'BC non rédigé' : 'CE non rédigée'"
                type="warning"
                description="Appuyez sur 'Rédaction' puis 'Convention Etude' afin de rédiger la CE pour cette étude."
                :closable="false"
                center
                effect="dark"
                show-icon
                style="margin-top: 10px;"
              />
            </el-row>
          </el-card>
        </template>
      </el-step>
      <!-- RDM (2) -->
      <el-step title="RM">
        <template #description>
          <el-card>
            <div>
              Les <b>R</b>apports de <b>M</b>ission sont envoyés aux réalisateurs. Ils détaillent les phases à accomplir et le nombre de JEH qui les concerne.
            </div>
            <el-table
              class="grid"
              :data="etude.missions"
            >
              <el-table-column
                label="Réalisateur"
              >
                <template #default="{row}">
                  <el-link
                    type="primary"
                    :style="'margin-left: 6px'"
                    @click="pushToConsultant(row)"
                  >
                    {{ getConsultantName(row) }}
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column
                prop="missionBegin"
                label="Date de début"
              />
              <el-table-column
                prop="missionEnd"
                label="Date de fin"
              />
              <el-table-column
                label="Nombre de phases"
              >
                <template #default="{row}">
                  <span>{{ row.phasesMission.length }}</span>
                </template>
              </el-table-column>
              <el-table-column
                prop="JEHNumber"
                label="Nombre de JEH"
              />
              <el-table-column
                label="Montant brut"
              >
                <template #default="{row}">
                  <span>{{ row.JEHNumber * row.JEH_price }}€</span>
                </template>
              </el-table-column>
              <el-table-column label="Opérations">
                <template #default="{row}">
                  <el-button
                    type="text"
                    icon="Download"
                    plain
                    :loading="loading"
                    @click="downloadRDM(row.id)"
                  >
                    Générer
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-row class="stCardRw">
              <el-button
                v-show="btn_rdm_levelup"
                :loading="loading"
                type="success"
                icon="Check"
                @click="levelupTo(3)"
              >
                Les RDM ont été signés
              </el-button>
              <el-button
                v-show="btn_rdm_help"
                type="warning"
              >
                Il faut au moins un RDM pour continuer !
              </el-button>
            </el-row>
          </el-card>
        </template>
      </el-step>
      <!-- FA (3) -->
      <el-step title="FA">
        <template #description>
          <el-card>
            <div>
              La <b>F</b>acture d'<b>A</b>compte doit être payée par le client.
              <p>
                <el-icon><Flag /></el-icon>
                <u>C'est à la trésorerie de générer et valider le paiement.</u>
              </p>
            </div>
            <el-row class="stCardRw">
              <el-alert
                v-show="btn_fa_alert"
                title="Valider la FA"
                type="warning"
                description="La trésorerie s'occupe de la facture."
                :closable="false"
                center
                effect="dark"
                show-icon
              />
            </el-row>
            <el-row class="stCardRw">
              <el-popconfirm
                title="Confirmez-vous vouloir vous passer de FA pour cette étude ?"
                confirm-button-type="danger"
                confirm-button-text="OUI"
                cancel-button-type="success"
                cancel-button-text="NON"
                @onConfirm="levelupTo(4)"
              >
              <template #reference>
                <el-button
                  v-show="btn_fa_alert"
                  type="danger"
                  icon="Check"
                >
                  Pas de FA pour cette étude
                </el-button>
              </template>
              </el-popconfirm>
            </el-row>
          </el-card>
        </template>
      </el-step>
      <!-- PVRI (4) -->
      <el-step title="PVRI">
        <template #description>
          <el-card>
            <div>
              Le <b>P</b>rocès <b>V</b>erbal de <b>R</b>ecette <b>I</b>ntermédiaire doit être édité puis signé par le client.
            </div>
            <PVRTable
              v-model="pvris"
              :loading="loading"
              @download="downloadPVR"
              @delete="deletePVR"
            />
            <el-row class="stCardRw">
              <el-button
                v-show="btn_pvri_levelup"
                type="success"
                icon="Check"
                @click="levelupTo(5)"
              >
                Le PVRI a été signé
              </el-button>
              <router-link :to="`/etudes/${$route.params.id}/pvr/ajouter`">
                <el-button
                  v-show="btn_pvri_help"
                  type="warning"
                  icon="Plus"
                >
                  Il faut un PVRI : en créer un.
                </el-button>
              </router-link>
            </el-row>
            <el-row class="stCardRw">
              <el-popconfirm
                title="Confirmez-vous vouloir vous passer de PVRI pour cette étude ?"
                confirm-button-type="danger"
                confirm-button-text="OUI"
                cancel-button-type="success"
                cancel-button-text="NON"
                @onConfirm="levelupTo(5)"
              >
              <template #reference>
                <el-button
                  v-show="btn_pvri_bypass && !btn_pvri_levelup"
                  type="danger"
                  icon="Check"
                >
                  Pas de PVRI pour cette étude
                </el-button>
              </template>
              </el-popconfirm>
            </el-row>
          </el-card>
        </template>
      </el-step>
      <!-- FI (5) -->
      <el-step title="FI">
        <template #description>
          <el-card>
            <div>
              La <b>F</b>acture <b>I</b>ntermédiaire doit être payée par le client.
              <p>
                <el-icon><Flag /></el-icon>
                <u>C'est à la trésorerie de générer et valider le paiement.</u>
              </p>
            </div>
            <el-row class="stCardRw">
              <el-alert
                v-show="btn_fi_alert"
                title="Valider la FI"
                type="warning"
                description="La trésorerie s'occupe de la facture."
                :closable="false"
                center
                effect="dark"
                show-icon
                style="margin-top: 10px;"
              />
            </el-row>
            <el-row class="stCardRw">
              <el-popconfirm
                title="Confirmez-vous vouloir vous passer de FI pour cette étude ?"
                confirm-button-type="danger"
                confirm-button-text="OUI"
                cancel-button-type="success"
                cancel-button-text="NON"
                @onConfirm="levelupTo(6)"
              >
              <template #reference>
                <el-button
                  v-show="btn_fi_alert"
                  type="danger"
                  icon="CircleCheck"
                >
                  Pas de FI pour cette étude
                </el-button>
              </template>
              </el-popconfirm>
            </el-row>
          </el-card>
        </template>
      </el-step>
      <!-- PVRF (6) -->
      <el-step title="PVRF">
        <template #description>
          <el-card>
            <div>
              Le <b>P</b>rocès <b>V</b>erbal de <b>R</b>ecette <b>F</b>inal doit être édité puis signé par le client.
            </div>
            <PVRTable
              v-model="pvrfs"
              :loading="loading"
              @download="downloadPVR"
              @delete="deletePVR"
            />
            <el-row class="stCardRw">
              <el-button
                v-show="btn_pvrf_levelup"
                type="success"
                icon="Check"
                @click="levelupTo(7)"
              >
                Le PVRF a été signé
              </el-button>
              <router-link :to="`/etudes/${$route.params.id}/pvr/ajouter`">
                <el-button
                  v-show="btn_pvrf_help"
                  type="warning"
                >
                  Il faut au moins un PVRF pour continuer !
                </el-button>
              </router-link>
            </el-row>
          </el-card>
        </template>
      </el-step>
      <!-- FS (7) -->
      <el-step title="FS">
        <template #description>
          <el-card>
            <div>
              La <b>F</b>acture de <b>S</b>olde doit être payée par le client.
              <p>
                <el-icon><Flag /></el-icon>
                <u>C'est à la trésorerie de générer et valider le paiement.</u>
              </p>
            </div>
            <el-row class="stCardRw">
              <el-alert
                v-show="btn_fs_alert"
                title="Valider la FS"
                type="warning"
                description="La trésorerie s'occupe de la facture."
                :closable="false"
                center
                effect="dark"
                show-icon
                style="margin-top: 10px;"
              />
            </el-row>
          </el-card>
        </template>
      </el-step>
      <!-- REX (8) -->
      <el-step title="Retour d'expérience">
        <template #description>
          <el-card>
            <div>
              Le travail de chaque réalisateur doit être commenté de manière interne.
            </div>
            <el-row class="stCardRw">
              <el-table
                class="grid"
                :data="reas"
              >
                <el-table-column label="Consultant">
                  <template #default="{row}">
                    <el-link
                      type="primary"
                      :style="'margin-left: 6px'"
                      @click="$router.push(`/realisateurs/${row.id}/voir`)"
                    >
                      {{ row.firstname + " " + row.lastname }}
                    </el-link>
                  </template>
                </el-table-column>
                <el-table-column label="Commentaire">
                  <template #default="{row}">
                    <el-row v-show="getComment(row.comments).date">
                      <el-rate
                        :value="getComment(row.comments).rating"
                        :max="10"
                        :disabled="true"
                        :allow-half="true"
                        :low-threshold="3.33"
                        :high-threshold="6.66"
                        :colors="['#ff1111', '#ffa200', '#62da05']"
                      />
                    </el-row>
                    <el-row v-show="getComment(row.comments).date">
                      {{ getComment(row.comments).content }}
                    </el-row>
                    <el-row v-show="!getComment(row.comments).date">
                      <el-row>
                        <router-link :to="`/etudes/${$route.params.id}/commentaires/${row.id}/ajouter`">
                          <el-button
                            type="success"
                            icon="Edit"
                            :disabled="!btn_peda_rediger"
                          >
                            Rédiger le commentaire
                          </el-button>
                        </router-link>
                        <span
                          v-show="!btn_peda_rediger"
                          style="margin-left: 12px"
                        >
                          <i>Disponible lorsque l'étude sera suffisamment avancée.</i>
                        </span>
                      </el-row>
                    </el-row>
                  </template>
                </el-table-column>
              </el-table>
            </el-row>
            <el-row
              v-show="(! etude.qualiValidatePeda) && etude.state >= 8"
              class="stCardRw"
              style="color: red; font-size: 120%"
            >
              <b>ATTENTION : </b>Les commentaires des réalisateurs ne sont pas finalisés.
            </el-row>
            <el-row class="stCardRw">
              <el-button
                v-show="btn_peda_levelup"
                :loading="loading"
                type="success"
                icon="Check"
                @click="levelupTo(9)"
              >
                Les commentaires ont été complétés
              </el-button>
              <el-button
                v-show="btn_peda_help"
                type="warning"
              >
                Il faut commenter tous les réalisateurs pour continuer
              </el-button>
            </el-row>
          </el-card>
        </template>
      </el-step>
      <!-- BV (9) -->
      <el-step title="BV">
        <template #description>
          <el-card>
            <div>
              Le <b>B</b>ulletin de <b>V</b>ersement doit être validé par le client et le pôle tréso.
              <p>
                <el-icon><Flag color="red"/></el-icon>
                <u>C'est à la trésorerie de générer et valider le BV.</u>
              </p>
            </div>
            <el-row class="stCardRw">
              <el-alert
                v-show="btn_bv_alert"
                title="Valider la FS"
                type="warning"
                description="La trésorerie s'occupe de la facture."
                :closable="false"
                center
                effect="dark"
                show-icon
                style="margin-top: 10px;"
              />
            </el-row>
          </el-card>
        </template>
      </el-step>
      <!-- FIN (10) -->
      <el-step
        title="Fin"
      >
        <template #description>
          <el-card style="font-size: 120%;">
            <el-row v-show="is_over">
              <el-icon><Check /></el-icon>
              Cette étude est <b><u>TERMINÉE</u></b>. Bravo à tous ! :D
            </el-row>
            <el-row v-show="!is_over">
              <el-icon><Close /></el-icon>
              Cette étude n'est pas encore terminée. Bon courage ! :)
            </el-row>
          </el-card>
        </template>
      </el-step>
      <!-- GUARANTEE (11) -->
      <el-step
        title="Garantie"
      >
        <template #description>
          <el-card style="font-size: 120%;">
            <template v-if="guaranteeEnd!=null">
              <el-row v-show="!is_guarantee_over">
                <el-icon><Close /></el-icon>
                Cette étude est sous garantie jusqu'au {{ guaranteeEnd.getDay()+"/"+(guaranteeEnd.getMonth()+1)+"/"+guaranteeEnd.getFullYear() }}.
              </el-row>
              <el-row v-show="is_guarantee_over">
                <el-icon><Check /></el-icon>
                Cette étude n'est plus sous garantie.
              </el-row>
            </template>
            <template v-else>
              <el-row>
                <el-icon><Close /></el-icon>
                Importez le PVRF pour démarrer la période de garantie.
              </el-row>
            </template>
          </el-card>
        </template>
      </el-step>
      <!-- x -->
    </el-steps>
  </div>
</template>

<script>
const axios = require("axios")
import Publishing from "@/mixins/Publishing"
import PVRTable from "./graphics/PVRTable"
export default {
  name: "ManageStep",
  components: { PVRTable },
  mixins: [Publishing],
  props: {
    etude: { type: Object, required: true }
  },
  data () {
    return {
      loading: false,
      btn_ce_generate: false,
      comments: []
    }
  },
  beforeCreate () {
    if(this.etude.state == undefined)
      this.etude.state = 0
  },
  computed: {
    // == DATA ==
    pvris () {
      return this.etude.pvr == undefined ? [] : this.etude.pvr.filter(pvr => pvr.documentType === "I")
    },
    pvrfs () {
      return this.etude.pvr == undefined ? [] : this.etude.pvr.filter(pvr => pvr.documentType === "F")
    },
    reas () {
      return this.etude.missions == undefined ? [] : this.etude.missions.map(m => m.consultant)
    },
    guaranteeEnd () {
      if(this.pvrfs[0] == undefined){
        return null
      }
      return new Date(new Date(this.pvrfs[0].signingDate).valueOf() + 1000*60*60*24*this.pvrfs[0].guaranteeDuration)
    },
    // == Documents ==
    // Devis
    btn_devis_generate () { 
      if (this.etude.docEtude){
        return this.etude.phases != []      
      }
      return false 
    },
    btn_devis_levelup () { return this.etude.state == 0 && this.btn_devis_generate },
    btn_devis_help () { return this.etude.state == 0 && ! this.btn_devis_levelup },
    // CE
    btn_ce_levelup () { return this.etude.state == 1 && this.btn_ce_generate },
    btn_ce_help () { return this.etude.state == 1 && ! this.btn_ce_levelup },
    // RDM
    btn_rdm_generate () { return true },
    btn_rdm_levelup () { return this.etude.state == 2 && this.etude.missions.length > 0 },
    btn_rdm_help () { return this.etude.state == 2 && ! this.btn_rdm_levelup },
    // FA
    btn_fa_alert () { return this.etude.state == 3 },
    // PVRI
    btn_pvri_generate () { return this.pvris.length > 0 },
    btn_pvri_levelup () { return this.etude.state == 4 && this.btn_pvri_generate },
    btn_pvri_help () { return this.etude.state == 4 && ! this.btn_pvri_levelup },
    btn_pvri_bypass () { return this.etude.state == 4 },
    //FI
    btn_fi_alert () { return this.etude.state == 5 },
    btn_fi_bypass () { return this.btn_fi_alert },
    // PVRF
    btn_pvrf_generate () { return this.pvrfs.length > 0 },
    btn_pvrf_levelup () { return this.etude.state == 6 && this.btn_pvrf_generate },
    btn_pvrf_help () { return this.etude.state == 6 && ! this.btn_pvrf_levelup },
    // FS
    btn_fs_alert () { return this.etude.state == 7 },
    // REX
    btn_peda_rediger () { return this.etude.state == 8 },
    btn_peda_levelup () { return this.etude.state == 8 && this.notAllCommented() },
    btn_peda_help () { return this.etude.state == 8 && ! this.btn_peda_levelup },
    // BV
    btn_bv_alert () { return this.etude.state == 9 },
    // Fin
    is_over () { return this.etude.state == 10 },
    is_guarantee_over () {
      if(this.guaranteeEnd == null){
        return false
      }
      return this.guaranteeEnd.valueOf() < Date.now()
    }
  },
  watch: {
    etude (nv) {
      if(nv.state == 10)
        this.etude.state = 11
    }
  },
  created () {
    axios.get(`/api/etudes/${this.$route.params.id}/ce/`, { withCredentials: true }).then((response) => {
      this.btn_ce_generate = response.data.description != ""
    }).catch(err => {
      this.$message({ message: "Une erreur est survenue lors de la récupération de la CE : " + err, type: "error" })
    })
    axios.get(
      "/api/realisateurs/cmts",
      {withCredentials: true}
    ).then((res) => {
      this.comments = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les commentaires : " + err, type: "error", offset: 40})
    })
  },
  methods: {
    levelupTo (new_state) {
      this.loading = true
      axios.put(
        `/api/etudes/${this.etude.id}/`,
        {
          ...this.etude,
          state: new_state,
          prospect: this.etude.prospect.id,
          qualityManager: this.etude.qualityManager.id,
          projectManager: this.etude.projectManager.id,
          clientContact: this.etude.clientContact.id,
          docEtude: this.etude.docEtude.id,
          linkedFiles: this.etude.linkedFiles.map(lf => lf.id)
        },
        { withCredentials: true }
      ).then(() => {
        this.$message({ message: "Étude mise à jour avec succès.", type: "success" })
        this.etude.state = new_state
      }).catch(err => {
        this.$message({ message: "Impossible de mettre à jour l'étude : " + err, type: "error" })
      }).finally(() => {
        this.loading = false
      })
    },

    getConsultantName (mission) {
      if(mission.consultant == undefined) {
        return "(vide)"
      } else {
        return mission.consultant.firstname + " " + mission.consultant.lastname
      }
    },
    pushToConsultant (mission) {
      if(mission.consultant != undefined) {
        this.$router.push(`/realisateurs/${mission.consultant.id}/voir`)
      }
    },
    getComment (rea_comments) {
      for(const rea_comm of rea_comments) {
        const corresponding = this.comments.find(c => c.id === rea_comm && c.associatedEtude == this.$route.params.id)
        if(corresponding != undefined) {
          return corresponding
        }
      }
      return {rating:-1, content:""}
    },
    notAllCommented () {
      if(this.etude.missions == undefined) {
        return false
      } else {
        for(const rea of this.reas) {
          if(this.getComment(rea.comments).rating == -1)
            return false
        }
        return true
      }
    },
    getEnding () {
      return this.is_over ? "success" : "primary"
    },
  }
}
</script>

<style scoped>
  .stCardRw {
    margin-top: 10px;
  }
</style>
