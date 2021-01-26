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
        <el-row>
          <el-col :span="11">
            <u>Prospect :</u>
            <router-link :to="'/prospects/' + item.id + '/voir'">
              <el-button
                type="text"
                size="medium"
              >
                {{ item.prospect.name }}
              </el-button>
            </router-link>
          </el-col>
          <el-col
            v-if="item.list === 'RDV' || item.list === 'DS'"
            :span="13"
          >
            <el-switch
              v-model="item.devisOn"
              active-color="#137566"
              inactive-color="#494949"
              active-text="Devis"
              inactive-text="RdV"
              @change="updateDevisRdv(item)"
            />
          </el-col>
        </el-row>
        <p><u>Addresse :</u> {{ item.prospect.address }}, {{ item.prospect.town }} ({{ item.prospect.postcode }})</p>
        <p v-if="item.list === 'NC'">
          <u>Dev'co :</u>
          <span v-if="item.prospect.charge == null"><i>  aucun</i></span>
          <span v-else> {{ findMembre(item.prospect.charge) }}</span>
        </p>
        <p v-if="item.list === 'AR'">
          <u>Dernier contact :</u> {{ item.prospect.nextDate }}
        </p>
        <p v-if="item.list === 'RDV'">
          <u>Date du rendez-vous :</u> {{ item.prospect.nextDate }}
        </p>
        <p v-if="item.list === 'DS'">
          <u>Deadline du devis :</u> {{ item.prospect.nextDate }}
        </p>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: "DragZone",
  props: {
    listId: { type: String, required: true },
    title: { type: String, required: true },
    membresList: { type: Array, required: true },
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
        this.listId,
        false
      )
    },
    findMembre (membreID) {
      const membre = this.membresList.find(m => m.id === membreID)
      return membre.firstname + " " + membre.lastname
    },
    updateDevisRdv (item) {
      const newAdv = (item.prospect.advancement === "DS") ? "RDV" : "DS"
      item.prospect.advancement = newAdv
      this.$emit(
        "dropped",
        item.id,
        newAdv,
        true
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