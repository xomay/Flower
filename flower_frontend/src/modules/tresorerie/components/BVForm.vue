<template>
  <el-form
    ref="formBV"
    :model="bv"
    label-position="left"
    :rules="rules"
  >
    <el-row
      v-if="!editMode"
      v-show="rdms.length > 0"
    >
      <el-form-item
        prop="rdm"
        label="Mission :"
      >
        <MemberPicker
          v-model="bv.rdm_id"
          :item-list="rdms"
          :loading="loading"
          placeholder="Mission"
          style="width: 100%;"
          @input="updatedRDM()"
          @clear="bv.rdm = -1"
        />
      </el-form-item>
    </el-row>
    <el-row v-show="bv.rdm_id != -1">
      <table class="tg">
        <tr class="tg-0lax">
          <td class="tg-y6fn">
            Réalisateur
          </td>
          <td style="width:200px">
            {{ bv.rea }}
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
    <el-collapse
      v-model="activeCollapses"
      class="mt-2"
    >
      <el-collapse-item name="0">
        <template slot="title">
          <span class="mr-2 text-lg">Données additionelles</span>
        </template>
        <el-alert
          v-if="!editMode"
          type="warning"
          :closable="false"
          show-icon
          title="Pour laisser par défault, laisser vide."
        />
        <p>Sur le BV, il y a une ligne nommée "dont évolution de la rémunération liée à la suppression des cotisations chômage et maladie".</p>
        <p>Le calcul est le suivant : <i>(A% - B%)*assiette_de_cotisation + (C% + D%)*rémunération_brute</i>.</p>
        <el-col :span="12">
          <el-form-item
            label="Taux SCCM 1 (A%)"
            prop="taux_sccm_1"
          >
            <el-input-number
              v-model="bv.taux_sccm_1"
              :precision="4"
              :step="0.0001"
              :min="0"
              :max="1"
              controls-position="left"
            />
          </el-form-item>
          <el-form-item
            label="Taux SCCM 2 (B%)"
            prop="taux_sccm_2"
          >
            <el-input-number
              v-model="bv.taux_sccm_2"
              :precision="4"
              :step="0.0001"
              :min="0"
              :max="1"
              controls-position="left"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item
            label="Taux SCCM 3 (C%)"
            prop="taux_sccm_3"
          >
            <el-input-number
              v-model="bv.taux_sccm_3"
              :precision="4"
              :step="0.0001"
              :min="0"
              :max="1"
              controls-position="left"
            />
          </el-form-item>
          <el-form-item
            label="Taux SCCM 4 (D%)"
            prop="taux_sccm_4"
          >
            <el-input-number
              v-model="bv.taux_sccm_4"
              :precision="4"
              :step="0.0001"
              :min="0"
              :max="1"
              controls-position="left"
            />
          </el-form-item>
        </el-col>
        <p>
          ({{ (Number(bv.taux_sccm_1) * 100).toFixed(2) }}% - {{ (Number(bv.taux_sccm_2) * 100).toFixed(2) }}%) *
          {{ assiette_cotisation.toFixed(2) }}€
          + ({{ (Number(bv.taux_sccm_3) * 100).toFixed(2) }}% + {{ (Number(bv.taux_sccm_4) * 100).toFixed(2) }}%) *
          {{ montant_brut.toFixed(2) }}€ =
          <b>{{ (((Number(bv.taux_sccm_1) - Number(bv.taux_sccm_2))*assiette_cotisation) + ((Number(bv.taux_sccm_3) - Number(bv.taux_sccm_4))*montant_brut)).toFixed(2) }} €</b>
        </p>
        <p>Note : information non utilisée dans <u>aucun</u> calcul, car je ne sais pas à quel niveau cela intervient.</p>
        <el-form-item
          label="Allègement de cotisation Junior (€) :"
        >
          <el-input-number
            v-model="bv.allegement_de_cotisations_junior"
            :precision="2"
            :step="1"
            :min="0"
            controls-position="left"
          />
        </el-form-item>
      </el-collapse-item>
    </el-collapse>
    <el-row v-show="bv.rdm_id != -1">
      <el-button
        type="success"
        :loading="loading"
        style="margin: 40px 44%; width: 220px;"
        @click="validateForm()"
      >
        Enregistrer
      </el-button>
    </el-row>
  </el-form>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"
import BVCotisationLine from "../components/BVCotisationLine"

export default {
  name: "BVForm",
  components: {MemberPicker, BVCotisationLine},
  props: {
    bv: { type: Object, required: true },
    ursaff: { type: Object, required: true },
    rdms: { type: Array, required: true },
    inputRdm: { type: Object, default () { return {} } },
    loading: { type: Boolean, required: true },
    editMode: { type: Boolean, default: false }
  },
  data () {
    return {
      rdm: {},
      activeCollapses: [],
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
    // Montants divers
    montant_brut () {
      return (this.rdm.JEHNumber * this.rdm.JEHPrice) * (1 - this.rdm.percentageJunior)
    },
    assiette_cotisation () {
      return 4 * this.rdm.JEHNumber * Number(this.ursaff.smic_horaire)
    },
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
  watch: {
    inputRdm (nv) { // sert à gérer l'input rdm. comme on modifie localement des trucs on peut pas directement le faire sur l'instance qui possède ce component.
      this.rdm = nv
    }
  },
  methods: {
    validateForm () {
      this.$refs.formBV.validate((result) => {
        if(result) {
          this.$emit("save")
        } else {
          this.$message({message: "Le formulaire n'est pas complet. Avez-vous pensé à la référence nationale ?", type:"error"})
        }
      })
    },
    updatedRDM () { // On a cliqué sur un nouveau RDM dans l'étude. Utilisé uniquement dans le mode NON édition.
      const rdm = this.rdms.find(rdm => rdm.id === this.bv.rdm_id)
      this.rdm = rdm
      // On affiche le nom du réalisateur.
      this.bv.rea = rdm.rea
      // On calcule toutes les cotisations. C'est pas très fun mais je sais pas trop comment faire autrement quoi
      this.bv.coti_sante = {
        montant_base: rdm.assietteCotisation,
        taux_junior: this.ursaff.taux_junior_sante,
        taux_realisateur: this.ursaff.taux_realisateur_sante
      }
      this.bv.coti_accidents = {
        montant_base: rdm.assietteCotisation,
        taux_junior: this.ursaff.taux_junior_accidents,
        taux_realisateur: this.ursaff.taux_realisateur_accidents
      }
      this.bv.coti_retraite_1 = {
        montant_base: rdm.assietteCotisation,
        taux_junior: this.ursaff.taux_junior_retraite_1,
        taux_realisateur: this.ursaff.taux_realisateur_retraite_1
      }
      this.bv.coti_retraite_2 = {
        montant_base: rdm.assietteCotisation,
        taux_junior: this.ursaff.taux_junior_retraite_2,
        taux_realisateur: this.ursaff.taux_realisateur_retraite_2
      }
      this.bv.coti_famille = {
        montant_base: rdm.assietteCotisation,
        taux_junior: this.ursaff.taux_junior_famille,
        taux_realisateur: this.ursaff.taux_realisateur_famille
      }
      this.bv.coti_chomage = {
        montant_base: rdm.remunerationRaw,
        taux_junior: this.ursaff.taux_junior_chomage,
        taux_realisateur: this.ursaff.taux_realisateur_chomage
      }
      this.bv.coti_autres = {
        montant_base: rdm.assietteCotisation,
        taux_junior: this.ursaff.taux_junior_autres,
        taux_realisateur: this.ursaff.taux_realisateur_autres
      }
      this.bv.coti_csg = {
        montant_base: rdm.assietteCotisation,
        taux_junior: this.ursaff.taux_junior_csg,
        taux_realisateur: this.ursaff.taux_realisateur_csg
      }
      this.bv.coti_csgcrds = {
        montant_base: rdm.assietteCotisation,
        taux_junior: this.ursaff.taux_junior_csgcrds,
        taux_realisateur: this.ursaff.taux_realisateur_csgcrds
      }
      this.bv.coti_exonerations = {
        montant_base: rdm.assietteCotisation,
        taux_junior: this.ursaff.taux_junior_exonerations,
        taux_realisateur: this.ursaff.taux_realisateur_exonerations
      }
    },
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
