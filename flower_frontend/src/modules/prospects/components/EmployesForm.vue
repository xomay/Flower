<template>
  <el-form
    :model="value"
    :rules="formRules"
    label-position="left"
  >
    <el-col :span="24">
      <el-form-item
        label="Genre"
        prop="gender"
        label-width="120px"
      >
        <el-select v-model="value.gender">
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
        <el-input v-model="value.firstname" />
      </el-form-item>
    </el-col>
    <el-col :span="12">
      <el-form-item
        label="Nom"
        prop="lastname"
        label-width="120px"
      >
        <el-input v-model="value.lastname" />
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <el-form-item
        label="Email"
        prop="email"
        label-width="120px"
      >
        <el-input v-model="value.email" />
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <el-form-item
        label="Mobile"
        prop="mobile"
        label-width="120px"
      >
        <el-input v-model="value.mobile" />
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <el-form-item
        label="Poste"
        prop="position"
        label-width="120px"
      >
        <el-input v-model="value.position" />
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <el-form-item>
        <el-button
          :loading="loading"
          type="success"
          @click="$emit('save')"
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
  </el-form>
</template>

<script>
export default {
  name: "EmployesForm",
  props: {
    value: { type: Object, required: true },
    loading: Boolean,
    deletable: Boolean
  },
  data () {
    return {
      breadcrumb: [],
      formRules: {
        gender: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        firstname: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        lastname: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        email: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        position: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ]
      }
    }
  }
}
</script>

<style>

</style>
