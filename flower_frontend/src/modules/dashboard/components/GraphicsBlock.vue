<template>
  <div>
    <el-col
      v-for="(item, index) in data"
      :key="index"
      :style="getWidth()"
    >
      <DashGraphic
        :fill-percentage="item.fill"
        aside-size="70%"
        :description="item.name"
      />
    </el-col>
  </div>
</template>

<script>
import DashGraphic from "./DashGraphic"

export default {
  name: "GraphicsBlock",
  components: {DashGraphic},
  props: {
    data: { type: Array, required: true }, // format { name="oui", fill="" }
  },
  methods: {
    getWidth () {
      return "width: " +(100.0 / this.data.length)+"%;"
    }
  }
}
</script>
