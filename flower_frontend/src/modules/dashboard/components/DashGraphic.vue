<template>
  <el-container>
    <el-aside
      :width="asideSize"
    >
      {{ description }}
    </el-aside>
    <el-container>
      <el-main>
        <el-progress
          :type="type"
          :color="customColors"
          :percentage="fillPercentage"
        />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: "DashGraphic",
  props: {
    // Pourcentage de remplissement
    fillPercentage: { type: Number, required: true },
    //
    // Texte à gauche du graphique.
    description: { type: String, required: true },
    //
    // Type du graphique. Valeurs : [line, circle, dashboard]
    type: {type: String, default: "dashboard" },
    //
    // Taille du ASIDE. format css
    asideSize: { type: String, default: "25%" },
    //
    // Tableau d'association pourcentage/couleur
    customColors: {
      type: Array,
      default: function () { // On est obligé de passé par une function pour les defaults de type Array...
        return [
          {color: "#fc0303", percentage: 20},
          {color: "#fc3b00", percentage: 40},
          {color: "#fc7e00", percentage: 50},
          {color: "#e3bd00", percentage: 60},
          {color: "#046eba", percentage: 80},
          {color: "#05b04f", percentage: 90},
          {color: "#22ff00", percentage: 100}
        ]
      }
    }
  }
}
</script>

<style>
  .el-aside {
    background-color: #f3f5f7;
    color: rgb(0, 0, 0);
    text-align: center;
    line-height: 1000%; /* ça parait difficile à croire, mais c'est le seul moyen pour que ça soit au milieu verticalement... */
  }
  .el-main {
    color: #333;
    line-height: 100%;
  }
</style>
