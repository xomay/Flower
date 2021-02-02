<template>
  <MemberPicker
    v-model="ret"
    :item-list="itemList"
    :placeholder="placeholder"
    :force-value="begin"
    :style="{width:'100%'}"
    @input="inputed"
  />
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"

export default {
  name: "MemberGElem",
  components: {MemberPicker},
  props: {
    outValue: { type: [String, Number, Object], required: true },
    index: { type: Number, required: true },
    itemList: { type: Array, required: true },
    placeholder: { type: String, required: true }
  },
  data () {
    return {
      ret: "",
      begin: ""
    }
  },
  watch: {
    itemList () {
      const found = this.itemList.find((item) => item.id === this.outValue)
      if(found == undefined) {
        this.begin = ""
      } else {
        if(found.value == undefined) {
          this.begin = found
        } else {
          this.begin = found.value
        }
      }
    }
  },
  methods: {
    inputed (value) {
      this.$emit(
        "inputOver",
        this.index,
        value
      )
    }
  }
}
</script>
