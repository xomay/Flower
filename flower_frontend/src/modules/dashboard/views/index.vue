<template>
  <div>
    <el-divider />
    <el-row
      justify="center"
    >
      <h1 style="margin: auto auto auto 35%;">
        Bienvenue
        <font color="blue">
          {{ getUsername() }}
        </font>
      </h1>
    </el-row>
    <el-divider />
    <el-row>
      <div width="80%">
        <img src="@/assets/flower.jpg">
      </div>
    </el-row>
    <el-divider />
    <el-row>
      <i class="versionText">
        Version actuelle : <u>alpha-32</u>
      </i>
    </el-row>
    <el-divider />
    <GraphicsBlock
      :data="getData()"
    />
  </div>
</template>

<script>
import GraphicsBlock from "../components/GraphicsBlock"

export default {
  name: "Authentication",
  components: {GraphicsBlock},
  methods: {
    getUsername () {
      return this.$store.currentUser.username
    },
    getData () {
      return [
        {name: "Objectif CA 2021", fill: 77},
        {name: "Participation aux questionnaires qualité", fill: 23}
      ]
    }
  }
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
  .versionText {
    margin: 0 auto 0 90em;
    font-size: 1em;
  }
</style>
