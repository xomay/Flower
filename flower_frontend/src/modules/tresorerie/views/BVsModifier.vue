<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
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
    <BVForm
      :bv="bv"
      :rdms="[]"
      :input-rdm="rdm"
      :ursaff="ursaff"
      :loading="loading"
      :edit-mode="true"
      @save="saveBV()"
    />
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import BVForm from "../components/BVForm"
import Utils from "@/mixins/Utils"
export default {
  name: "BVsCreeer",
  components: {BVForm},
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
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      { widthCredentials: true }
    ).then((res) => {
      this.rdm = res.data.missions.find(m => m.bv_id == this.$route.params.bv_id)
      const bv_id = this.rdm.bv_id
      this.breadcrumb[1].name = res.data.name
      axios.get(
        `/api/bv/${bv_id}/`,
        { widthCredentials: true }
      ).then((res_bv) => {
        this.bv = this.transformsAllCotis(res_bv.data)
        this.bv.rea = `${this.rdm.consultant.firstname} ${this.rdm.consultant.lastname}`
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
