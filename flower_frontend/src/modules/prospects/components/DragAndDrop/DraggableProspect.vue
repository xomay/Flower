<template>
  <el-card
    :id="createID()"
    class="w-64"
    shadow="hover"
    :draggable="true"
    :ondragstart="drag(event)"
  >
    <span>Prospect : {{ prospect.name }}</span><br>
    <span>Adresse : {{ prospect.address }}</span><br>
    <span>Code postal : {{ prospect.postcode }}</span><br>
    <span>Ville : {{ prospect.town }}</span><br>
  </el-card>
</template>

<script>
export default {
  name: "DraggableProspect",
  props: {
    prospect: {type: Object, required: true}
  },
  methods: {
    createID () {
      return "pr_" + prospect.id
    },
    drag (ev) {
      ev.dataTransfer.setData("text", ev.target.id)
    }
  }
}
</script>