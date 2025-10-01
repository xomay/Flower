<template>
  <div>
    <el-form
      ref="refNfForm"
      :model="nf"
      label-position="left"
      :rules="rules"
      style="margin-top: 20px; height: 250px;"
    >
      <el-col :span="24">
        <el-form-item
          label="Demandeur"
          prop="demandeur"
        >
          <MemberPicker
            v-model="nf.demandeur"
            :item-list="membres"
            placeholder="Demandeur"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Date"
          prop="date"
        >
          <el-date-picker
            v-model="nf.date"
            format="DD-MM-YYYY"
            value-format="YYYY-MM-DD"
            type="date"
            @change="applyDateToMandat"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Mandat"
          prop="mandat"
        >
          <el-input-number
            v-model="nf.mandat"
            :min="2020"
            :max="2100"
            controls-position="right"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Objet"
          prop="objet"
        >
          <el-input
            v-model="nf.objet"
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4}"
            placeholder="Entrez l'objet de la NF"
          />
        </el-form-item>
      </el-col>
    </el-form>
    <NFsDetailForm
      ref="detailFormComponent"
      v-model="nf.details"
      :loading="loading"
      @add-bloc="addBloc"
      @delete-bloc="deleteBloc"
    />
    <el-row>
      <el-button
        type="success"
        style="margin-right: 80px; margin-left: 40px;"
        :loading="loading"
        @click="validateForm"
      >
        Sauvegarder
      </el-button>
      <el-popconfirm
        v-if="deletable"
        title="Supprimer définitivement cette NF ?"
        confirm-button-type="danger"
        confirm-button-text="Oui"
        cancel-button-type="success"
        cancel-button-text="Non"
        @confirm="deleteNF()"
      >
      <template #reference>
        <el-button
          :loading="loading"
          type="danger"
          icon="Cross"
        >
          Supprimer la NF
        </el-button>
      </template>
      </el-popconfirm>
    </el-row>
  </div>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"
import NFsDetailForm from "./NFsDetailForm"
export default {
  name: "NFsForm",
  components: { MemberPicker, NFsDetailForm },
  props: {
    nf: { type: Object, required: true },
    membres: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    deletable: { type: Boolean, default: false },
    defaultTva: { type: Number, default () { return 0.2 } }
  },
  data () {
    return {
      rules: {
        demandeur: [
          { required: true, message: "Obligatoire", trigger: "change" }
        ],
        date: [
          { required: true, message: "Obligatoire", trigger: "change" }
        ],
        mandat: [
          { required: true, message: "Obligatoire", trigger: "change" }
        ],
        objet: [
          { required: true, message: "Obligatoire", trigger: "change" }
        ]
      }
    }
  },
  methods: {
    validateForm () {
      if(this.$refs.detailFormComponent.$refs.nfsdetailform == undefined || this.$refs.detailFormComponent.$refs.nfsdetailform.length == 0) {
        this.$message({message: "Il faut au moins une dépense dans la NF.", type: "error"})
        return 0
      }
      var result = true
      this.$refs.detailFormComponent.$refs.nfsdetailform.forEach(f => f.validate((r) => result = r ? result : false))
      this.$refs.refNfForm.validate((r) => result = r ? result : false)
      if(result) {
        this.$emit("save")
      } else {
        this.$message({message: "Le formulaire n'est pas valide.", type: "error"})
      }
    },
    deleteNF () {
      this.$emit("delete")
    },
    applyDateToMandat () {
      if(this.nf.date != undefined && this.nf.date != "") {
        this.nf.mandat = this.nf.date.split("-", 3)[0]
      }
    },
    // DETAILS
    addBloc () {
      const newBloc = {
        description: "",
        detailType: "N",
        prixHT: 0,
        tva: this.defaultTva,
        nbKilometres: 0,
        prixCentimesKilometres: 0,
        index: this.nf.details.length + 1,
        ndf: this.$route.params.id
      }
      this.nf.details.push(newBloc)
    },
    deleteBloc (blocIndex) {
      this.nf.details.splice(
        blocIndex,
        1
      )
    },
  }
}
</script>
