<template>
  <el-autocomplete
    v-model="autocompleteValue"
    class="inline-input"
    :fetch-suggestions="queryValue"
    :placeholder="placeholder"
    clearable
    @select="handleSelectvalue"
    @clear="$emit('clear')"
  />
</template>

<script>
export default {
  name: "MemberPicker",
  props: {
    value: { type: undefined, required: true },
    itemList: { type: Array, required: true },
    placeholder: { type: String, required: true },
    forceValue: { type: String, default () { return null } }
  },
  data () {
    return {
      autocompleteValue: "",
      forcedSync: null
    }
  },
  watch: {
    itemList () {
      const found = this.itemList.find((item) => item.id === this.value)
      this.autocompleteValue = found ? found.value : ""
      if(this.forcedSync !== null) {
        this.autocompleteValue = this.forcedSync
      }
    },
    forceValue (v) {
      this.forcedSync = v
      this.autocompleteValue = this.forcedSync
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
    },
    // Used by reference to manually clear the content.
    clear () {
      this.autocompleteValue = ""
    }
  }
}
</script>
