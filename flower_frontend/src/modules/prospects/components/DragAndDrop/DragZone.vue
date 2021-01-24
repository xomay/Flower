<template>
  <div
    class="drop-zone"
    @drop="onDrop($event)"
    @dragover.prevent
    @dragenter.prevent
  >
    <h1
      class="titleStyle"
    >
      {{ title }}
    </h1>
    <div
      v-for="item in content"
      :key="item.title"
      class="drag-el"
      draggable
      @dragstart="startDrag($event, item)"
    >
      <el-card>
        {{ item.title }}
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: "DragZone",
  props: {
    listId: { type: Number, required: true },
    title: { type: String, required: true },
    content: { type: Array, required: true }
  },
  methods: {
    startDrag (evt, item) {
      evt.dataTransfer.dropEffect = "move"
      evt.dataTransfer.effectAllowed = "move"
      evt.dataTransfer.setData("itemID", item.id)
    },
    onDrop (evt) {
      const itemID = evt.dataTransfer.getData("itemID")
      this.$emit(
        "dropped",
        itemID,
        this.listId
      )
    }
  }
}
</script>

<style>
  .titleStyle {
    text-align: center;
    font-size: 1.1em;
    margin: 1vh auto 3vh auto;
    font-weight: bold;
    background: #20507812;
  }

  .drop-zone {
    background-color: #eee;
    margin-bottom: 10px;
    margin-right: 0.5%;
    padding: 10px;
    float: left;
    width: 32%;
    border: solid black;
  }

  .drag-el {
    background-color: #fff;
    margin-bottom: 10px;
    padding: 5px;
  }

  /* Clear floats after the columns */
  .rowStyle:after {
    content: "";
    display: table;
    clear: both;
  }
</style>