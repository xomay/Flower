<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
  >
    <el-row v-show="rdms.length == 0">
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
      :rdms="rdms"
      :ursaff="ursaff"
      :loading="loading"
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
      title: "Créer un BV : <loading>",
      rdms: [],
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
          name: "Créer un BV",
          link: `/tresorerie/etudes/${this.$route.params.id}/bvs/ajouter`
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
      this.rdms = res.data.missions.filter(m => res.data.bvData[m.id] === -1)
      this.rdms.forEach((elt) => elt.rea = `${elt.consultant.firstname} ${elt.consultant.lastname}`)
      this.rdms.forEach((elt) => elt.value = `RDM pour ${elt.rea}`)
      this.title = "Créer un BV : " + res.data.name
      this.breadcrumb[1].name = res.data.name
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les études : " + err, type: "error"})
    }).finally(() => this.loading = false)
    axios.get(
      "/api/administration/base-ursaff/last/",
      { widthCredentials: true }
    ).then((res) => {
      this.ursaff = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la dernière base Ursaff : " + err, type: "error"})
    }).finally(() => this.loading = false)
    axios.get(
      "/api/bv/",
      { widthCredentials: true }
    ).then((res) => {
      const future = res.data.length + 1
      if(future < 10)
        this.bv.reference = "BV_00"+future
      else if(future < 100)
        this.bv.reference = "BV_0"+future
      else
        this.bv.reference = "BV_"+future
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les anciens BV : " + err, type: "error"})
    }).finally(() => this.loading = false)
  },
  created () {
    this.bv.date = this.generateDateToday() // c.f. Utils
  },
  methods: {
    saveBV () {
      this.loading = true
      axios.post(
        "/api/bv/",
        this.bv,
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
