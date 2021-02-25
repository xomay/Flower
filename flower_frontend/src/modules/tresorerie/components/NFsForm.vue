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
            format="dd/MM/yyyy"
            value-format="yyyy-MM-dd"
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
      @add-bloc="addBloc"
      @delete-bloc="deleteBloc"
    />
    <el-row>
      <el-button
        type="success"
        style="margin-right: 80px; margin-left: 40px;"
        @click="validateForm"
      >
        Sauvegarder
      </el-button>
      <el-popconfirm
        title="Supprimer définitivement cette NF ?"
        confirm-button-type="danger"
        confirm-button-text="Oui"
        cancel-button-type="success"
        cancel-button-text="Non"
        @onConfirm="deleteNF()"
      >
        <el-button
          slot="reference"
          type="danger"
          icon="el-icon-cross"
        >
          Supprimer la NF
        </el-button>
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
    membres: { type: Array, required: true }
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
      this.$router.push("/tresorerie/nfs/voir")
    },
    applyDateToMandat () {
      if(this.nf.date != undefined && this.nf.date != "") {
        this.nf.mandat = this.nf.date.split("-", 3)[0]
      }
    },
    // DETAILS
    addBloc () {
      const newBloc = {
        objet: "",
        detailType: "N",
        prixHT: 0,
        tva: 0,
        nbKilometres: 0,
        prixCentimesKilometres: 0,
        index: this.nf.details.length + 1
      }
      this.nf.details.push(newBloc)
    },
    deleteBloc ({blocIndex}) {
      this.nf.details.splice(
        blocIndex,
        1
      )
    },
  }
}
</script>
