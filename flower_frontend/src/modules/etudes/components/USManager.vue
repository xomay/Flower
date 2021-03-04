<template>
  <div>
    <el-row
      v-for="(us, index) in uss"
      :key="index"
    >
      <el-col :span="4">
        {{ us.name }}
      </el-col>
      <el-col
        :span="20"
        style="margin-top: -10px"
      >
        <SliderUSState
          :us="us"
          :tooltip="index === uss.length - 1"
          :loading="loading"
          :rea-vue="reaVue"
          style="colored"
          @change="usChanged"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import SliderUSState from "./graphics/SliderUSState"
export default {
  name: "USManager",
  components: { SliderUSState },
  props: {
    uss: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    reaVue: { type: Boolean, default: false }
  },
  methods: {
    usChanged (us, newState) {
      this.$emit("us-change", us, newState)
    }
  }
}
</script>

<style scoped>
  .colored .el-slider__bar {
    background-color: red;
  }
</style>