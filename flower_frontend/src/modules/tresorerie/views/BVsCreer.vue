<template>
  <BaseComponent
    title="Créer un BV"
    :breadcrumb="breadcrumb"
  >
    <el-form
      :v-model="bv"
      label-position="left"
    >
      <el-row>
        <el-col :span="12">
          <el-form-item
            label="Étude :"
          >
            <MemberPicker
              v-model="etude_id"
              :item-list="etudes"
              :loading="loading"
              placeholder="Étude"
              @input="updatedEtude()"
              @clear="bv.rdm = {}; etude_id = 0"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item
            prop="rdm"
            label="Mission :"
          >
            <MemberPicker
              v-model="bv.rdm"
              :item-list="rdms"
              :loading="loading"
              :disabled="etude_id == 0"
              placeholder="Mission"
              @input="updatedRDM()"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        Réalisateur : {{ bv.rea }}
      </el-row>
    </el-form>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import MemberPicker from "@/modules/membres/components/MemberPicker"

export default {
  name: "BVsCreeer",
  components: {MemberPicker},
  data () {
    return {
      loading: true,
      etude_id: 0,
      etudes: [],
      rdms: [],
      bv: {
        rea: "",
        rdm: -1,
        reference: "",
        reference_nationale: "",
        date: "",
        versement_mode: "",
        coti_sante: {},
        coti_accidents: {},
        coti_retraite_1: {},
        coti_retraite_2: {},
        coti_famille: {},
        coti_chomage: {},
        coti_autres: {},
        coti_csg: {},
        coti_csgcrds: {},
        coti_exonerations: {}
      },
      breadcrumb: [
        {
          name: "Liste des BV",
          link: "TODO"
        },
        {
          name: "Créer une NF",
          link: "/tresorerie/bv/creer/"
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/etudes/",
      { widthCredentials: true }
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.etudes = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les études : " + err, type: "error"})
    }).finally(() => this.loading = false)
  },
  methods: {
    updatedEtude () {
      this.loading = true
      axios.get(
        `/api/etudes/${this.etude_id}/missions/`,
        { widthCredentials: true }
      ).then((res) => {
        res.data.forEach((elt) => elt.rea = `${elt.consultant.firstname} ${elt.consultant.lastname}`)
        res.data.forEach((elt) => elt.value = `RDM pour ${elt.rea}`)
        this.rdms = res.data
        console.log(this.rdms)
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer les études : " + err, type: "error"})
      }).finally(() => this.loading = false)
    },
    updatedRDM () {
      const rdm = this.rdms.find(rdm => rdm.id === this.bv.rdm)
      console.log("new rdm : " + rdm.value)
      this.bv.rea = rdm.rea
    }
  }
}
</script>
