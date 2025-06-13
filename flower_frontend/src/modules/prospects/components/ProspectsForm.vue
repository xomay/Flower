<template>
  <el-form
    ref="prosFormRef"
    :model="modelValue"
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
          v-model="modelValue.name"
          placeholder="Entreprise"
        />
      </el-form-item>
    </el-col>
    <el-row>

      <el-col :span="10">
        <el-form-item
        label="Type d'entreprise"
        prop="type"
        label-width="200px"
        >
        <el-select
          v-model="modelValue.type"
          placeholder="Type"
        >
          <el-option label="Entreprise Privée" value="Entreprise Privée" />
          <el-option label="Administration Publique" value="Administration Publique" />
        </el-select>
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
        v-model="modelValue.domain"
        placeholder="Domaine"
        />
      </el-form-item>
      </el-col>
    </el-row>
    <el-col :span="24">
      <el-form-item
        label="Chargé dev'co"
        prop="charge"
        label-width="200px"
      >
        <MemberPicker
          v-model="modelValue.charge"
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
          v-model="modelValue.address"
          placeholder="Numéro et nom de rue"
        />
      </el-form-item>
    </el-col>
    <el-row>
    <el-col :span="10">
      <el-form-item
        label="Code postal"
        prop="postcode"
        label-width="200px"
      >
        <el-input
          v-model="modelValue.postcode"
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
          v-model="modelValue.town"
          placeholder="Ville de l'entreprise"
        />
      </el-form-item>
    </el-col>
    </el-row>
    <el-col :span="24">
      <el-form-item
        label="Addresse de facturation"
        prop="address_tresorerie"
        label-width="200px"
      >
        <el-input
          v-model="modelValue.address_tresorerie"
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
        :value="modelValue.contactWay"
        @add-field="contactsAddField"
        @delete-field="contactsRemoveField"
      />
    </el-col>
    <BaseComponent
      title="Employés"
      :breadcrumb="[]"
    >
      <template v-slot:action>
          <el-button
            type="text"
            icon="Plus"
            @click="addEmploye"
          >
            Ajouter
          </el-button>
      </template>
      <el-table
        class="grid"
        :data="employes"
        :stripe="true"
      >
        <el-table-column
          label="Nom"
          prop="lastname"
        >
          <template #default="{row}">
            <el-input
              v-model="row.lastname"
              :disabled="disabled"
              placeholder="Nom de l'employé"
            />
          </template>
        </el-table-column>
        <el-table-column
          label="Prénom"
          prop="firstname"
        >
          <template #default="{row}">
            <el-input
              v-model="row.firstname"
              :disabled="disabled"
              placeholder="Prénom de l'employé"
            />
          </template>
        </el-table-column>
        <el-table-column
          label="Genre"
          prop="genre"
        >
          <template #default="{row}">
            <el-select v-model="row.gender" placeholder="Entrez le genre">
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
          </template>
        </el-table-column>
        <el-table-column
          label="Poste"
          prop="position"
        >
          <template #default="{row}">
            <el-input
              v-model="row.position"
              :disabled="disabled"
              placeholder="Poste de l'employé"
            />
          </template>
        </el-table-column>
        <el-table-column
          label="Email"
          prop="email"
        >
          <template #default="{row}">
            <el-input
              v-model="row.email"
              :disabled="disabled"
              placeholder="Email de l'employé"
            />
          </template>
        </el-table-column>
        <el-table-column
          label="Mobile"
          prop="mobile"
        >
          <template #default="{row}">
            <el-input
              v-model="row.mobile"
              :disabled="disabled"
              placeholder="Téléphone de l'employé"
            />
          </template>
        </el-table-column>
        <el-table-column
          label="Alumni"
          prop="alumni"
          width="100"
          align="center"
        >
          <template #default="{row}">
            <el-checkbox
              v-model="row.alumni"
              :disabled="disabled"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="100"
          label="Supprimer"
        >
          <template #default="{row}">
            <el-button
              type="text"
              icon="Delete"
              @click="deleteEmploye(row)"
            />
          </template>
        </el-table-column>
      </el-table>
    </BaseComponent>
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
    modelValue: { type: Object, required: true },
    members: { type: Array, required: true },
    employes: { type: Array, required: true },
    loading: Boolean,
    deletable: Boolean
  },
  emits: ["save", "delete"],
  data () {
    return {
      breadcrumb: [],
      firstWatch: true,
      formRules: {
        name: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
        type: [
          {required: true, message: "Obligatoire", trigger: "blur"}
        ],
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
      this.modelValue.contactWay = this.modelValue.contactWay.filter(str => /\S/.test(str))
      this.$emit("save", this.employes)
    },
    contactsAddField () {
      this.modelValue.contactWay.push("")
    },
    contactsRemoveField (index) {
      this.modelValue.contactWay.splice(
        index,
        1
      )
    },
    addEmploye () {
      this.employes.push({
        id: this.employes.length + 1,
        genre: null,
        firstname: "",
        lastname: "",
        position: "",
        email: "",
        mobile: "",
        alumni: false,
      })
    },
    deleteEmploye (row) {
      const index = this.employes.indexOf(row)
      if (index > -1) {
        this.employes.splice(index, 1)
      }
    }
  }
}
</script>
