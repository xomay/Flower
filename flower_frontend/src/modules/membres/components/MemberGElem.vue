<template>
  <MemberPicker
    v-model="ret"
    :item-list="itemList"
    :placeholder="placeholder"
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
      ret: ""
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
