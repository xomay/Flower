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
    value: { type: Number, required: true },
    itemList: { type: Array, required: true },
    placeholder: { type: String, required: true },
    loading: { type: Boolean, default: false }
  },
  data () {
    return {
      originalValue: this.value
    }
  },
  methods: {
    updateChange (newValue) {
      this.$emit("input", newValue)
    }
  }
}
</script>