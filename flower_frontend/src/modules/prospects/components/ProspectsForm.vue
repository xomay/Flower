<template>
  <el-form
    ref="prosFormRef"
    :model="value"
    :rules="formRules"
    label-position="left"
  >
    <el-col :span="24">
      <el-form-item
        label="Nom de l'entreprise"
        prop="name"
        label-width="200px"
      >
        <el-input
          v-model="value.name"
          placeholder="entreprise"
        />
      </el-form-item>
    </el-col>
    <el-col :span="10">
      <el-form-item
        label="Type d'entreprise"
        prop="type"
        label-width="200px"
      >
        <el-input
          v-model="value.type"
          placeholder="Type"
        />
      </el-form-item>
    </el-col>
    <el-col
      :span="12"
      :offset="2"
    >
      <el-form-item
        label="Domaine de l'entreprise"
        prop="domain"
        label-width="200px"
      >
        <el-input
          v-model="value.domain"
          placeholder="Domaine"
        />
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
        <el-input
          v-model="value.address"
          placeholder="Numéro et nom de rue"
        />
      </el-form-item>
    </el-col>
    <el-col :span="10">
      <el-form-item
        label="Code postal"
        prop="postcode"
        label-width="200px"
      >
        <el-input
          v-model="value.postcode"
          placeholder="Code postal de l'entreprise"
        />
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
        <el-input
          v-model="value.town"
          placeholder="Ville de l'entreprise"
        />
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <el-form-item
        label="Addresse de facturation"
        prop="address_tresorerie"
        label-width="200px"
      >
        <el-input
          v-model="value.address_tresorerie"
          type="textarea"
          :rows="2"
          resize="none"
          placeholder="Identique à l'addresse ci-dessus."
        />
      </el-form-item>
    </el-col>
    <el-col :span="24">
      <span>
        Moyens de contact :
      </span>
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
