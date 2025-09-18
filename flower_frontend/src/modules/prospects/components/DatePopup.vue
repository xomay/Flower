<template>
  <el-dialog
    :title="popupTitle"
    :model-value="visibility"
    @update:model-value="$emit('update:visibility', $event)"
    @opened="opened()"
  >
    <el-form
      ref="formPopup"
      :model="dateModel"
      label-position="left"
      size="small"
    >
      <el-form-item
        :label="dateName"
        prop="date"
        label-width="120px"
        :rules="[
          { required: true, message: 'Il faut préciser la date !' , trigger: 'blur' },
          { required: true, pattern: /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/, message: 'Entrez un format valide.', trigger: 'blur'}
        ]"
      >
        <el-date-picker
          v-model="dateModel.date"
          format="DD-MM-YYYY"
          value-format="YYYY-MM-DD"
          type="date"
          :placeholder="dateName"
          :first-day-of-week="1"
        />
      </el-form-item>
    </el-form>
    <template #footer>
    <span
      class="dialog-footer"
    >
      <el-button
        @click="cancel()"
      >
        Annuler
      </el-button>
      <el-button
        type="primary"
        @click="confirm()"
      >
        Confirmer
      </el-button>
    </span>
    </template>
  </el-dialog>
</template>

<script>
export default {
  name: "DatePopup",
  props: {
    // Titre affiché en gaut à gauche
    popupTitle: { type: String, required: true },
    // Nom du label à gauche du field
    dateName: { type: String, required: true },
    // Déclencheur du <el-dialog>
    visibility: { type: Boolean, required: true },
    // valeur par défaut du field
    placeholder: { type: String, default: function () { return this.getToday() } }
  },
  emits: ["finish", "update:visibility"],
  data () {
    return {
      dateModel: {
        date: ""
      }
    }
  },
  methods: {
    cancel () {
      this.$emit(
        "finish",
        false,
        ""
      )
    },
    confirm () {
      this.$refs.formPopup.validate(success => {
        if(success) {
          this.$emit(
            "finish",
            true,
            this.dateModel.date
          )
        }
      })
    },
    getToday () {
      const today = new Date()
      var dd = String(today.getDate())
      dd = dd.padStart(2, "0")
      var mm = String(today.getMonth() + 1).padStart(2, "0")
      var yyyy = today.getFullYear()
      return yyyy + "-" + mm + "-" + dd
    },
    opened () {
      this.dateModel.date = this.placeholder
    }
  }
}
</script>