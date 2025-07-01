<template>
  <el-popover
    placement="top-start"
    width="50"
    trigger="hover"
  >
    <div class="popCenter">
      <b>{{ currentValue }} / 10</b>
    </div>
    <template #reference>
    <el-rate
      :value="currentValue"
      :max="10"
      :disabled="!editable"
      :allow-half="true"
      :low-threshold="3.33"
      :high-threshold="6.66"
      :colors="['#ff1111', '#ffa200', '#62da05']"
      text-color="#ffffff"
      @change="edited"
    />
    </template>
  </el-popover>
</template>

<script>
export default {
  name:"StarRate",
  props: {
    modelValue: { type: undefined, required: true },
    editable: { type: Boolean, default: false }
  },
  emits: ["change"],
  data () {
    return {
      currentValue: 0
    }
  },
  watch: {
    modelValue (nv) {
      this.currentValue = nv
    }
  },
  methods: {
    edited (newValue) {
      this.$emit("change", newValue)
    }
  }
}
</script>

<style>
  .el-popover .popCenter {
    text-align: center !important;
  }
</style>