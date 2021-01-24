<template>
  <div>
    <el-col
      v-for="item in data"
      :key="item"
      :style="getWidth()"
    >
      <DashGraphic
        :fill-percentage="item.fill"
        aside-size="70%"
        :description="item.name"
      />
    </el-col>
    <!--<el-col class="grParts">
      <DashGraphic
        aside-size="70%"
        :fill-percentage="percentageQuali"
        description="Participation aux questionnaires qualité"
      />
    </el-col>-->
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
