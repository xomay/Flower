<template>
  <el-select
    v-model="originalValue"
    filterable
    clearable
    :placeholder="placeholder"
    :loading="loading"
    @change="updateChange"
  >
    <el-option
      v-for="item in itemList"
      :key="item.id"
      :label="item.value"
      :value="item.id"
    />
    <el-option
      :value="0"
      label="Non défini"
    />
  </el-select>
</template>

<script>
export default {
  name: "ItemPicker",
  props: {
    modelValue: { type: Number, required: true },
    itemList: { type: Array, required: true },
    placeholder: { type: String, required: true },
    loading: { type: Boolean, default: false }
  },
  emits: ["input"],
  data () {
    return {
      originalValue: this.modelValue
    }
  },
  watch: {
    modelValue () {
      this.originalValue = this.modelValue
    },
    itemList () {
      this.originalValue = this.modelValue
    }
  },
  methods: {
    updateChange (newValue) {
      this.$emit("input", newValue)
    }
  }
}
</script>