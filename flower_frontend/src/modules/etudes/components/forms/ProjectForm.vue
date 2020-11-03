<template>
  <el-form
    :model="value"
    :rules="formRules"
    label-position="left"
  >
    <el-form-item
      label="Prospect"
      prop="prospect"
      label-width="140px"
    >
      <MemberPicker
        v-model="value.prospect"
        :item-list="prospects"
        placeholder="Entrez le nom du prospect"
      />
    </el-form-item>
    <el-form-item
      label="Nom de l'étude"
      prop="name"
      label-width="140px"
    >
      <el-input v-model="value.name" />
    </el-form-item>
    <el-form-item
      label="Présentation de l'étude"
      prop="description"
      label-width="140px"
    >
      <el-input
        v-model="value.description"
        type="textarea"
      />
    </el-form-item>
    <el-form-item
      label="Mandat"
      prop="mandat"
      label-width="140px"
    >
      <el-input v-model="value.mandat" />
    </el-form-item>
    <el-form-item
      label="Numéro de l'étude"
      prop="number"
      label-width="140px"
    >
      <el-input v-model="value.number" />
    </el-form-item>
    <el-form-item
      label="Confidentialité"
      prop="confidential"
      label-width="140px"
    >
      <el-checkbox v-model="value.confidential" />
    </el-form-item>
    <el-form-item
      label="Suiveur de projet"
      prop="projectManager"
      label-width="140px"
    >
      <MemberPicker
        v-model="value.projectManager"
        :item-list="members"
      />
    </el-form-item>
    <el-form-item
      label="Suiveur qualité"
      prop="qualityManager"
      label-width="140px"
    >
      <MemberPicker
        v-model="value.qualityManager"
        :item-list="members"
      />
    </el-form-item>
    <el-form-item>
      <el-button
        :loading="loading"
        icon="el-icon-plus"
        type="success"
        @click="$emit('save')"
      >
        Enregistrer l'étude
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
const axios = require("axios")
import MemberPicker from "@/modules/membres/components/MemberPicker"

export default {
  name: "ProjectForm",
  components: {MemberPicker},
  props: {
    value: { type: Object, required: true },
    loading: { type: Boolean, required: true }
  },
  data () {
    return {
      formRules: {
        prospect: [
          {required: true,
            message: "Obligatoire",
            trigger: "change"}
        ],
        name: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        description: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        mandat: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        number: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        confidential: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        projectManager: [
          {required: true,
            message: "Obligatoire",
            trigger: "change"}
        ],
        qualityManager: [
          {required: true,
            message: "Obligatoire",
            trigger: "change"}
        ]
      },
      prospects: [],
      members: []
    }
  },
  watch: {
    value () {
      this.value.prospect = this.value.prospect ? this.value.prospect.id : null
      this.value.projectManager = this.value.projectManager ? this.value.projectManager.id : null
      this.value.qualityManager = this.value.qualityManager ? this.value.qualityManager.id : null
    }
  },
  created () {
    axios.get(
      `${this.$server_url}/prospects`,
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.prospects = res.data
    }).
      catch((err) => {
        console.log(err)
        this.$message({message: "Impossible de récupérer la liste des prospects",
          type: "error",
          offset: 40})
      })
    axios.get(
      `${this.$server_url}/membres`,
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = `${elt.firstname} ${elt.lastname}`)
      this.members = res.data
    }).
      catch((err) => {
        console.log(err)
        this.$message({message: "Impossible de récupérer la liste des Membres",
          type: "error",
          offset: 40})
      })
  }
}
</script>

<style>

</style>
