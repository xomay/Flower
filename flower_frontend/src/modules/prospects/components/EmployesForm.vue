<template>
  <el-form
    ref="employeFormRef"
    :model="modelValue"
    :rules="formRules"
    label-position="left"
  >
  <el-row :gutter="5">
    <el-col :span="24">
      <el-form-item
        label="Genre"
        prop="gender"
        label-width="120px"
      >
        <el-select v-model="modelValue.gender" placeholder="Entrez le genre">
          <el-option value="M.">
            M.
          </el-option>
          <el-option value="Mme.">
            Mme.
          </el-option>
          <el-option value="">
            Non renseigné
          </el-option>
        </el-select>
      </el-form-item>
    </el-col>
    <el-col :span="12">
      <el-form-item
        label="Prénom"
        prop="firstname"
        label-width="120px"
      >
        <el-input v-model="modelValue.firstname" placeholder="Prénom"/>
      </el-form-item>
    </el-col>
    <el-col :span="12">
      <el-form-item
        label="Nom"
        prop="lastname"
        label-width="120px"
      >
        <el-input v-model="modelValue.lastname" placeholder="Nom"/>
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <el-form-item
        label="Email"
        prop="email"
        label-width="120px"
      >
        <el-input v-model="modelValue.email" placeholder="Mail"/>
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <el-form-item
        label="Mobile"
        prop="mobile"
        label-width="120px"
      >
        <el-input v-model="modelValue.mobile" placeholder="Téléphone"/>
      </el-form-item>
    </el-col>
    <el-col :span="11">
      <el-form-item
        label="Poste"
        prop="position"
        label-width="120px"
      >
        <el-input v-model="modelValue.position" placeholder="Poste"/>
      </el-form-item>
    </el-col>
    <el-col :span="11">
    </el-col>
    <el-col :span="11">
      <el-form-item
        label="Alumni"
        prop="alumni"
        label-width="120px"
      >
        <el-checkbox v-model="modelValue.alumni" />
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <el-form-item>
        <el-button
          :loading="loading"
          type="success"
          @click="callValidateAll"
        >
          Enregistrer
        </el-button>
      </el-form-item>
      <el-form-item v-if="deletable">
        <el-button
          type="danger"
          @click="$emit('delete')"
        >
          Supprimer
        </el-button>
      </el-form-item>
    </el-col>
    </el-row>
  </el-form>
</template>

<script>
export default {
  name: "EmployesForm",
  props: {
    modelValue: { type: Object, required: true },
    loading: Boolean,
    deletable: Boolean
  },
  emits: ["save", "delete"],
  data () {
    return {
      breadcrumb: [],
      formRules: {
        gender: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        position: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        firstname: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"},
          { min: 1, max: 60, message: "Nombre de caractères invalide", trigger: "blur" }
        ],
        lastname: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"},
          { min: 1, max: 60, message: "Nombre de caractères invalide", trigger: "blur" }
        ],
        email: [
          {
            required: true,
            pattern: /^[\w\\.=-]+@[\w\\.-]+\.[\w]{2,3}$/,
            message: "Cette valeur doit être un email valide.",
            trigger: "blur"
          }
        ],
      }
    }
  },
  methods: {
    callValidateAll () {
      this.$refs.employeFormRef.validate((rslt) => {
        if(rslt == true) {
          this.$emit("save")
        } else {
          this.$message({message: "Certains champs ne sont pas valides.",
            type: "error",
            offset: 40})
        }
      })
    }
  },
}
</script>

<style>

</style>
