<template>
  <div>
    <el-divider />
    <el-row justify="center">
      <h1 style="text-align: center;">
        Bienvenue
        <font
          color="blue"
        >
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
        Version actuelle : <u>mathysdev</u>
      </i>
    </el-row>
    <el-divider />
    <GraphicsBlock
      v-if="isCA()"
      :data="getData()"
    />
  </div>
</template>

<script>
import GraphicsBlock from "../components/GraphicsBlock"
import { Permissions } from "@/mixins/Permissions"

export default {
  name: "Authentication",
  components: {GraphicsBlock},
  mixins: [Permissions],
  methods: {
    getUsername () {
      return this.$store.currentUser.username
    },
    getData () {
      return [
        {name: "Objectif CA 2025", fill: 0},
        {name: "Participation aux questionnaires qualité", fill: 60}
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
    display:block;
    text-align: right;
    margin: 0 10px 0 auto;
    font-size: 1em;
  }
</style>
