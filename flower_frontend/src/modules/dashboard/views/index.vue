<template>
  <BaseComponent
    title="Dashboard"
    :breadcrumb="[]"
  >
    <el-col :span="8">
      <DashGraphic
        fill-percentage="53"
        aside-size="70%"
        description="Objectif CA 2021"
      />
      <DashGraphic
        type="circle"
        aside-size="70%"
        fill-percentage="24"
        description="Participation aux questionnaires qualité"
      />
    </el-col>
    <el-col
      :span="12"
      :offset="4"
    >
      <el-row
        justify="center"
      >
        <h1>
          Bienvenue sur Flower
        </h1>
      </el-row>
      <el-row>
        <div width="80%">
          <img src="@/assets/flower.svg">
        </div>
      </el-row>
    </el-col>
  </BaseComponent>
</template>

<script>
import DashGraphic from "../components/DashGraphic"

export default {
  name: "Authentication",
  components: {DashGraphic}
}
</script>

<style>
  h1 {
    display: block;
    margin-left: auto;
    margin-right: auto;
    font-weight: bold;
  }
  img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    max-width: 50%;
    height: auto;
  }
</style>
