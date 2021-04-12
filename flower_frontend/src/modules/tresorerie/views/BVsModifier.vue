<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
  >
    <el-form
      ref="formBV"
      :model="bv"
      label-position="left"
      :rules="rules"
    >
      <el-row v-show="rdm.length == -1">
        <el-alert
          type="error"
          title="Erreur : vous n'êtes pas censé être ici"
          :closable="false"
          center
          show-icon
        >
          En effet, tous les RDM de cette étude ont un BV.
        </el-alert>
      </el-row>
      <el-row v-show="bv.rdm_id != -1">
        <table class="tg">
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              Réalisateur
            </td>
            <td style="width:200px">
              {{ rdm.rea }}
            </td>
          </tr>
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              Référence interne
            </td>
            <td>
              {{ bv.reference }}
            </td>
          </tr>
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              Rémunération brute
            </td>
            <td>
              {{ Number(rdm.remunerationRaw).toFixed(2) }} €
            </td>
          </tr>
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              Nombre de JEH
            </td>
            <td>
              {{ rdm.JEHNumber }}
            </td>
          </tr>
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              Base URSAFF
            </td>
            <td>
              {{ Number(ursaff.baseValue).toFixed(2) }} €
            </td>
          </tr>
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              Assiette des cotisations
            </td>
            <td>
              {{ Number(rdm.assietteCotisation).toFixed(2) }} €
            </td>
          </tr>
        </table>
      </el-row>
      <el-row v-show="bv.rdm_id != -1">
        <el-col :span="7">
          <el-form-item
            label="Mode de paiement :"
            prop="versement_mode"
          >
            <el-select v-model="bv.versement_mode">
              <el-option value="Virement">
                Virement
              </el-option>
              <el-option value="Chèque">
                Chèque
              </el-option>
              <el-option value="Espèces">
                Espèces
              </el-option>
              <el-option value="Autre">
                Autre
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="7">
          <el-form-item
            label="Date du paiement :"
            prop="date"
          >
            <el-date-picker
              v-model="bv.date"
              format="dd/MM/yyyy"
              value-format="yyyy-MM-dd"
              type="date"
            />
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item
            label="Référence de paiement :"
            prop="reference_nationale"
          >
            <el-input
              v-model="bv.reference_nationale"
              placeholder="Référence de versement"
              style="width: 60%"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row v-show="bv.rdm_id != -1">
        <table class="tg">
          <thead>
            <tr>
              <th class="tg-e5lu">
                COTISATIONS ET CONTRIBUTIONS SOCIALES
              </th>
              <th
                class="tg-e5lu"
                style="width: 150px"
              >
                BASE
              </th>
              <th class="tg-e5lu">
                TAUX - Junior
              </th>
              <th class="tg-e5lu">
                MONTANT - Junior
              </th>
              <th class="tg-e5lu">
                TAUX - étudiant
              </th>
              <th class="tg-e5lu">
                MONTANT - étudiant
              </th>
            </tr>
          </thead>
          <tbody>
            <BVCotisationLine
              title="SANTE - Sécurité sociale - Maladie Maternité Invalidité Décès"
              :cotisation="bv.coti_sante"
            />
            <BVCotisationLine
              title="ACCIDENTS DU TRAVAIL-MALADIES PROFESSIONNELLES"
              :cotisation="bv.coti_accidents"
            />
            <BVCotisationLine
              title="RETRAITE - Sécurité sociale plafonnée TA"
              :cotisation="bv.coti_retraite_1"
            />
            <BVCotisationLine
              title="RETRAITE - Sécurité sociale déplafonnée"
              :cotisation="bv.coti_retraite_2"
            />
            <BVCotisationLine
              title="FAMILLE"
              :cotisation="bv.coti_famille"
            />
            <BVCotisationLine
              title="ASSURANCE CHÔMAGE"
              :cotisation="bv.coti_chomage"
            />
            <BVCotisationLine
              title="AUTRES CONTRIBUTIONS DUES PAR LA JUNIOR"
              :cotisation="bv.coti_autres"
            />
            <BVCotisationLine
              title="CSG déductible de l'impôt sur le revenu"
              :cotisation="bv.coti_csg"
            />
            <BVCotisationLine
              title="CSG/CRDS non déductibles de l'impôt sur le revenu"
              :cotisation="bv.coti_csgcrds"
            />
            <BVCotisationLine
              title="EXONERATIONS DE COTISATION JUNIOR"
              :cotisation="bv.coti_exonerations"
            />
          </tbody>
        </table>
      </el-row>
      <el-row v-show="bv.rdm_id != -1">
        <table class="tg">
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              TOTAL DES COTISATIONS DUES (indexées sur l'assiette de cotisation)
            </td>
            <td style="width: 90px">
              {{ sum_taux_junior_assiette.toFixed(2) }} %
            </td>
            <td style="width: 90px">
              {{ sum_montants_junior_assiette.toFixed(2) }} €
            </td>
            <td style="width: 90px">
              {{ sum_taux_realisateur_assiette.toFixed(2) }} %
            </td>
            <td style="width: 90px">
              {{ sum_montants_realisateur_assiette.toFixed(2) }} €
            </td>
          </tr>
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              TOTAL DES COTISATIONS DUES (indexées sur la rémunération brute)
            </td>
            <td>
              {{ Number(sum_taux_junior_brut).toFixed(2) }} %
            </td>
            <td>
              {{ Number(sum_montants_junior_brut).toFixed(2) }} €
            </td>
            <td>
              {{ sum_taux_realisateur_brut > 0 ? Number(sum_taux_realisateur_brut).toFixed(2) + "%" : "-" }}
            </td>
            <td>
              {{ sum_montants_realisateur_brut > 0 ? Number(sum_montants_realisateur_brut).toFixed(2) + "€" : "-" }}
            </td>
          </tr>
        </table>
      </el-row>
      <el-row v-show="bv.rdm_id != -1">
        <table class="tg">
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              Total des cotisations JUNIOR
            </td>
            <td style="width:120px">
              {{ Number(sum_montants_junior).toFixed(2) }} €
            </td>
          </tr>
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              Total des cotisations RÉALISATEUR
            </td>
            <td style="width:120px">
              {{ Number(sum_montants_realisateur).toFixed(2) }} €
            </td>
          </tr>
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              Total des cotisations TOTALES
            </td>
            <td style="width:120px">
              {{ (Number(sum_montants_realisateur)+Number(sum_montants_junior)).toFixed(2) }} €
            </td>
          </tr>
        </table>
      </el-row>
      <el-row v-show="bv.rdm_id != -1">
        <table class="tg">
          <tr class="tg-0lax">
            <td class="tg-y6fn">
              Montant NET payé à l'étudiant
            </td>
            <td style="width:120px">
              {{ (Number(rdm.remunerationRaw) - Number(sum_montants_junior)).toFixed(2) }} €
            </td>
          </tr>
        </table>
      </el-row>
      <el-row v-show="bv.rdm_id != -1">
        <el-button
          type="success"
          :loading="loading"
          style="margin: 12px auto;"
          @click="validateForm()"
        >
          Enregistrer
        </el-button>
      </el-row>
    </el-form>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import BVCotisationLine from "../components/BVCotisationLine"
import Utils from "@/mixins/Utils"
export default {
  name: "BVsCreeer",
  components: {BVCotisationLine},
  mixins: [Utils],
  data () {
    return {
      loading: true,
      title: "Éditer un BV : <loading>",
      rdm: {rea:""},
      ursaff: {},
      bv: {
        rea: "",
        rdm_id: -1,
        reference: "",
        reference_nationale: "",
        date: "",
        versement_mode: "Virement",
        coti_sante: {montant_base: 0, taux_junior: 0, taux_realisateur: 0},
        coti_accidents: {montant_base: 0, taux_junior: 0, taux_realisateur: 0},
        coti_retraite_1: {montant_base: 0, taux_junior: 0, taux_realisateur: 0},
        coti_retraite_2: {montant_base: 0, taux_junior: 0, taux_realisateur: 0},
        coti_famille: {montant_base: 0, taux_junior: 0, taux_realisateur: 0},
        coti_chomage: {montant_base: 0, taux_junior: 0, taux_realisateur: 0},
        coti_autres: {montant_base: 0, taux_junior: 0, taux_realisateur: 0},
        coti_csg:{montant_base: 0, taux_junior: 0, taux_realisateur: 0},
        coti_csgcrds: {montant_base: 0, taux_junior: 0, taux_realisateur: 0},
        coti_exonerations: {montant_base: 0, taux_junior: 0, taux_realisateur: 0}
      },
      breadcrumb: [
        {
          name: "Études (trésorerie)",
          link: "/tresorerie/etudes/"
        },
        {
          name: "<loading>",
          link: `/tresorerie/etudes/${this.$route.params.id}/`
        },
        {
          name: "Éditer le BV <loadding>",
          link: `/tresorerie/etudes/${this.$route.params.id}/bvs/modifier/${this.$route.params.bv_id}/`
        }
      ],
      rules: {
        reference_nationale: [
          { required: true, message: "Obligatoire", trigger: "change" }
        ],
        date: [
          { required: true, message: "Obligatoire", trigger: "change" }
        ]
      }
    }
  },
  computed: {
    // Sommes des taux
    sum_taux_junior_assiette () {
      return ((Number(this.bv.coti_sante.taux_junior) + Number(this.bv.coti_accidents.taux_junior) + Number(this.bv.coti_retraite_1.taux_junior)
        + Number(this.bv.coti_retraite_2.taux_junior) + Number(this.bv.coti_famille.taux_junior) + Number(this.bv.coti_autres.taux_junior)
        + Number(this.bv.coti_csg.taux_junior) + Number(this.bv.coti_csgcrds.taux_junior) + Number(this.bv.coti_exonerations.taux_junior)) * 100)
    },
    sum_taux_realisateur_assiette () {
      return ((Number(this.bv.coti_sante.taux_realisateur) + Number(this.bv.coti_accidents.taux_realisateur) + Number(this.bv.coti_retraite_1.taux_realisateur)
        + Number(this.bv.coti_retraite_2.taux_realisateur) + Number(this.bv.coti_famille.taux_realisateur) + Number(this.bv.coti_autres.taux_realisateur)
        + Number(this.bv.coti_csg.taux_realisateur) + Number(this.bv.coti_csgcrds.taux_realisateur) + Number(this.bv.coti_exonerations.taux_realisateur)) * 100)
    },
    sum_taux_junior_brut () {
      return ((Number(this.bv.coti_chomage.taux_junior)) * 100).toFixed(2)
    },
    sum_taux_realisateur_brut () {
      return ((Number(this.bv.coti_chomage.taux_realisateur)) * 100).toFixed(2)
    },
    // Somme des montants
    sum_montants_junior_assiette () {
      return (this.sum_taux_junior_assiette / 100 * Number(this.bv.coti_sante.montant_base))
    },
    sum_montants_realisateur_assiette () {
      return (this.sum_taux_realisateur_assiette / 100 * Number(this.bv.coti_sante.montant_base))
    },
    sum_montants_junior_brut () {
      return (this.sum_taux_junior_brut / 100 * Number(this.bv.coti_chomage.montant_base))
    },
    sum_montants_realisateur_brut () {
      return (this.sum_taux_realisateur_brut / 100 * Number(this.bv.coti_chomage.montant_base))
    },
    // Sommes des montants totaux
    sum_montants_junior () {
      return Number(this.sum_montants_junior_assiette) + Number(this.sum_montants_junior_brut)
    },
    sum_montants_realisateur () {
      return Number(this.sum_montants_realisateur_assiette) + Number(this.sum_montants_realisateur_brut)
    },
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      { widthCredentials: true }
    ).then((res) => {
      this.rdm = res.data.missions.find(m => m.bv_id == this.$route.params.bv_id)
      this.rdm.rea = `${this.rdm.consultant.firstname} ${this.rdm.consultant.lastname}`
      const bv_id = this.rdm.bv_id
      this.breadcrumb[1].name = res.data.name
      axios.get(
        `/api/bv/${bv_id}/`,
        { widthCredentials: true }
      ).then((res_bv) => {
        this.bv = this.transformsAllCotis(res_bv.data)
        this.title = "Éditer le BV : " + this.bv.reference
        this.breadcrumb[2].name = "Éditer le BV : " + this.bv.reference
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer le BV associé à la mission : " + err, type: "error"})
      }).finally(() => this.loading = false)
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les études : " + err, type: "error"})
      this.loading = false
    })
    axios.get(
      "/api/administration/base-ursaff/last/",
      { widthCredentials: true }
    ).then((res) => {
      this.ursaff = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la dernière base Ursaff : " + err, type: "error"})
    }).finally(() => this.loading = false)
  },
  methods: {
    validateForm () {
      this.$refs.formBV.validate((result) => {
        if(result) {
          this.saveBV()
        } else {
          this.$message({message: "Le formulaire n'est pas complet. Avez-vous pensé à la référence nationale ?", type:"error"})
        }
      })
    },
    transformsAllCotis (bv_data) {
      return {
        ...bv_data,
        coti_sante: this.stringToFloat(bv_data.coti_sante),
        coti_accidents: this.stringToFloat(bv_data.coti_accidents),
        coti_retraite_1: this.stringToFloat(bv_data.coti_retraite_1),
        coti_retraite_2: this.stringToFloat(bv_data.coti_retraite_2),
        coti_famille: this.stringToFloat(bv_data.coti_famille),
        coti_chomage: this.stringToFloat(bv_data.coti_chomage),
        coti_autres: this.stringToFloat(bv_data.coti_autres),
        coti_csg: this.stringToFloat(bv_data.coti_csg),
        coti_csgcrds: this.stringToFloat(bv_data.coti_csgcrds),
        coti_exonerations: this.stringToFloat(bv_data.coti_exonerations)
      }
    },
    stringToFloat (cotisation) {
      return {
        id : cotisation.id,
        montant_base: Number(cotisation.montant_base),
        taux_junior: Number(cotisation.taux_junior),
        taux_realisateur: Number(cotisation.taux_realisateur)
      }
    },
    saveBV () {
      this.loading = true
      axios.put(
        `/api/bv/${this.$route.params.bv_id}/`,
        { ...this.bv, rdm_id: this.bv.rdm.id },
        {widthCredentials: true}
      ).then(() => {
        this.$message({message: "BV enregistré avec succès !", type:"success"})
        this.$router.push(`/tresorerie/etudes/${this.$route.params.id}/`)
      }).catch((err) => {
        this.$message({message: "Erreur lors de l'enregistrement du BV : " + err, type:"error"})
        this.loading = false
      })
    }
  }
}
</script>

<style> /* Pas scoped, afin que ça prenne effet dans les BVCotisationLine */
  .tg {
    border-collapse: collapse;
    border-spacing: 0;
    margin: 12px auto;
  }
  .tg td {
    border-color:black;
    border-style: solid;
    border-width: 1px;
    font-family: Arial, sans-serif;
    font-size: 14px;
    overflow: hidden;
    padding: 10px 5px;
    word-break: normal;
  }
  .tg th {
    border-color: black;
    border-style: solid;
    border-width: 1px;
    font-family: Arial, sans-serif;
    font-size: 14px;
    font-weight: normal;
    overflow: hidden;
    padding: 10px 5px;
    word-break: normal;
  }
  .tg .tg-baqh {
    text-align: center;
    vertical-align: top;
    text-align: center;
  }
  .tg .tg-e5lu {
    background-color: #000000;
    color: #ffffff;
    text-align: center;
    text-align: center;
    vertical-align: top
  }
  .tg .tg-c3ow {
    border-color: inherit;
    text-align: center;
    vertical-align: top;
    border-color: black;
    border-style: solid;
  }
  .tg .tg-4f0n {
    background-color: #000000;
    border-color: inherit;
    color: #ffffff;
    text-align: center;
    vertical-align: top
  }
  .tg .tg-llyw{
    background-color: #c0c0c0;
    border-color: inherit;
    text-align: left;
    vertical-align: top;
    text-align: center;
  }
  .tg .tg-lqy6 {
    text-align: right;
    vertical-align: top;
    text-align: center;
  }
  .tg .tg-0pky {
    border-color: inherit;
    text-align: left;
    vertical-align: top;
    text-align: center;
  }
  .tg .tg-0lax {
    text-align: left;
    vertical-align: top;
    text-align: center;
  }
  .tg .tg-y6fn {
    background-color: #c0c0c0;
    font-weight: bold;
    text-align: left;
    vertical-align: top;
    text-align: center;
  }
</style>
