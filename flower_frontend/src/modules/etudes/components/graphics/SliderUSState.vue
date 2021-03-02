<template>
  <el-slider
    v-model="value"
    :max="5"
    :disabled="disabled || loading"
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
    disabled : { type: Boolean, default () { return false } },
    tooltip: { type: Boolean, required: true },
    loading: { type: Boolean, required: true }
  },
  data () {
    return {
      value: 0,
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
      this.$emit("change", this.us, this.valueToState(newState))
    }
  }
}
</script>