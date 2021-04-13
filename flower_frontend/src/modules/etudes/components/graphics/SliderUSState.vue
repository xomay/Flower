<template>
  <el-slider
    v-model="value"
    :max="5"
    :disabled="loading"
    :format-tooltip="formatTooltipSlider"
    :marks="tooltip ? marks : {}"
    show-stops
    @change="sliderChanged"
  />
</template>

<script>
export default {
  name: "SliderUSState",
  props: {
    us: { type: Object, required: true },
    tooltip: { type: Boolean, required: true },
    loading: { type: Boolean, required: true },
    reaVue: { type: Boolean, default: false }
  },
  data () {
    return {
      value: 0,
      oldValue: 0,
      marks: {
        0: "En cours de définition",
        1: "À faire",
        2: "En cours de réalisation",
        3: "Terminé",
        4: "À modifier",
        5: "Validé"
      }
    }
  },
  created () {
    this.value = this.getSliderValue(this.us.state)
    this.oldValue = this.value
  },
  methods: {
    getSliderValue (state) {
      switch(state) {
      case "DEFIN": return 0
      case "TODO": return 1
      case "DOING": return 2
      case "DONE": return 3
      case "REDO": return 4
      case "OVER": return 5
      }
      return -1
    },
    valueToState (value) {
      switch(value) {
      case 0: return "DEFIN"
      case 1: return "TODO"
      case 2: return "DOING"
      case 3: return "DONE"
      case 4: return "REDO"
      case 5: return "OVER"
      }
    },
    formatTooltipSlider (state) {
      return this.marks[state]
    },
    sliderChanged (newState) {
      var allowed = true
      if(this.reaVue) {
        // Cas où c'est un réa qui bouge le slider. Il n'a pas le droit de faire certaines actions.
        if(this.oldValue == 0 || this.oldValue == 5) {
          // Pas le droit de changé si 'OVER' ou 'DEFIN'
          this.$message({ message: "En tant que réalisateur, vous n'avez pas le droit de modifier cet US si il est à cette étape", type: "error"})
          allowed = false
        } else if(newState == 0 || newState > 4) {
          // Pas le droit de METTRE en "DEFIN" ou en "OVER".
          this.$message({ message: "Seul un chargé de projet peut mettre un US à un état 'Terminé' ou 'à définir", type: "error"})
          allowed = false
        }
      }
      if(allowed) {
        this.$emit("change", this.us, this.valueToState(newState))
        this.oldValue = newState
      } else {
        this.value = this.oldValue
      }
    }
  }
}
</script>