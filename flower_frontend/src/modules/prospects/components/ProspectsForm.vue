<template>
  <el-form
    ref="prosFormRef"
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
        label="Chargé dev'co"
        prop="charge"
        label-width="200px"
      >
        <MemberPicker
          v-model="value.charge"
          :item-list="members"
          placeholder="Chargé dev'co"
        />
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
    <el-col :span="10">
      <el-form-item
        label="Code postal"
        prop="postcode"
        label-width="200px"
      >
        <el-input v-model="value.postcode" />
      </el-form-item>
    </el-col>
    <el-col
      :span="12"
      :offset="2"
    >
      <el-form-item
        label="Ville"
        prop="town"
        label-width="200px"
      >
        <el-input v-model="value.town" />
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <ContactsGroup
        :value="value.contactWay"
        @add-field="contactsAddField"
        @delete-field="contactsRemoveField"
      />
    </el-col>
    <el-col :span="24">
      <el-form-item>
        <el-button
          :loading="loading"
          type="success"
          @click="validateForm"
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
import MemberPicker from "../../membres/components/MemberPicker.vue"
import ContactsGroup from "./ContactsGroup.vue"

export default {
  name: "ProspectsForm",
  components: {ContactsGroup, MemberPicker},
  props: {
    value: { type: Object, required: true },
    members: { type: Array, required: true },
    loading: Boolean,
    deletable: Boolean
  },
  data () {
    return {
      breadcrumb: [],
      firstWatch: true,
      formRules: {
        name: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        charge: [
          {required: true, message: "Obligatoire", trigger: "change"}
        ],
        address: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        postcode: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        town: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ]
      }
    }
  },
  methods: {
    validateForm () {
      this.$refs.prosFormRef.validate((r) => {
        if(r) {
          this.saveProspect()
        } else {
          this.$message({ message: "Certains champs ne sont pas valides !", type:"error", offset: 40 })
        }
      })
    },
    saveProspect () {
      this.value.contactWay = this.value.contactWay.filter(str => /\S/.test(str))
      this.$emit("save")
    },
    contactsAddField () {
      this.value.contactWay.push("")
    },
    contactsRemoveField (index) {
      this.value.contactWay.splice(
        index,
        1
      )
    }
  }
}
</script>
