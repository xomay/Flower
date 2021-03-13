<template>
  <el-select
    v-model="value"
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
  </el-select>
</template>

<script>
export default {
  name: "ItemPicker",
  props: {
    value: { type: Number, required: true },
    itemList: { type: Array, required: true },
    placeholder: { type: String, required: true },
    loading: { type: Boolean, default: false },
    //remote: { type: Boolean, default: false },
    //calculateRemote: { type: String, required: true },
  },
  methods: {
    updateChange (newValue) {
      this.$emit("input", newValue)
    }
  }
}
</script>