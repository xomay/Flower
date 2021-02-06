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
        placeholder="Suiveur de projet"
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
        placeholder="Suiveur qualité"
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
import MemberPicker from "@/modules/membres/components/MemberPicker"

export default {
  name: "ProjectForm",
  components: {MemberPicker},
  props: {
    value: { type: Object, required: true },
    loading: { type: Boolean, required: true },
    members: { type: Array, required: true },
    prospects: { type: Array, required: true }
  },
  data () {
    return {
      formRules: {
        prospect: [
          {required: true,message: "Obligatoire", trigger: "change"}
        ],
        name: [
          {required: true,message: "Obligatoire", trigger: "blur"}
        ],
        description: [
          {required: true,message: "Obligatoire", trigger: "blur"}
        ],
        mandat: [
          {required: true,message: "Obligatoire", trigger: "blur"}
        ],
        number: [
          {required: true,message: "Obligatoire", trigger: "blur"}
        ],
        confidential: [
          {required: true,message: "Obligatoire", trigger: "blur"}
        ],
        projectManager: [
          {required: true,message: "Obligatoire", trigger: "blur"}
        ],
        qualityManager: [
          {required: true,message: "Obligatoire", trigger: "blur"}
        ]
      }
    }
  }
}
</script>
