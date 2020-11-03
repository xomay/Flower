<template>
  <el-form
    :model="value"
    :rules="formRules"
    label-position="left"
  >
    <el-col :span="24">
      <el-form-item
        label="Nom du prospect"
        prop="name"
        label-width="200px"
      >
        <el-input v-model="value.name" />
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <el-form-item
        label="Adresse"
        prop="address"
        label-width="200px"
      >
        <el-input v-model="value.address" />
      </el-form-item>
    </el-col>
    <el-col :span="12">
      <el-form-item
        label="Code postal"
        prop="postcode"
        label-width="200px"
      >
        <el-input v-model="value.postcode" />
      </el-form-item>
    </el-col>
    <el-col :span="12">
      <el-form-item
        label="Ville"
        prop="town"
        label-width="200px"
      >
        <el-input v-model="value.town" />
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <el-form-item>
        <el-button
          :loading="loading"
          type="success"
          @click="saveProspect"
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
  name: "ProspectsForm",
  props: {
    value: { type: Object, required: true },
    loading: Boolean,
    deletable: Boolean
  },
  data () {
    return {
      formRules: {
        name: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        address: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        postcode: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ],
        town: [
          {required: true,
            message: "Obligatoire",
            trigger: "blur"}
        ]
      }
    }
  },
  watch: {

    /*
     * Value: {
     *   handler () {
     *     console.log('value changed !')
     *   },
     *   deep: true
     * }
     */
  },
  methods: {
    saveProspect () {
      this.$emit("save")
    }
  }
}
</script>

<style>

</style>
