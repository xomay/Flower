<template>
  <el-autocomplete
    v-model="autocompleteValue"
    class="inline-input"
    :fetch-suggestions="queryValue"
    :placeholder="placeholder"
    @select="handleSelectvalue"
  />
</template>

<script>
export default {
  name: "MemberPicker",
  props: {
    value: { type: [String, Number], required: true },
    itemList: { type: Array, required: true },
    placeholder: { type: String, required: true }
  },
  data () {
    return {
      autocompleteValue: ""
    }
  },
  watch: {
    itemList () {
      const found = this.itemList.find((item) => item.id === this.value)
      this.autocompleteValue = found ? found.value : ""
    }
  },
  methods: {
    queryValue (queryString, cb) {
      const results = queryString ? this.itemList.filter((item) => item.value.toLowerCase().includes(queryString.toLowerCase())) : this.itemList
      cb(results)
      this.$emit(
        "checkEvent",
        this.autocompleteValue
      )
    },
    handleSelectvalue (value) {
      this.autocompleteValue = value.value
      this.$emit(
        "input",
        value.id
      )
    }
  }
}
</script>

<style>

</style>
