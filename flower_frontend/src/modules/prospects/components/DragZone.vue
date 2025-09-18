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
    <el-progress 
      :percentage="animatedPercentage"
      style="margin: 0 0 10px 5px;"
      />
    <div
      v-for="item in content"
      :key="item.id"
      class="drag-el"
      :draggable="true"
      @dragstart="startDrag($event, item)"
    >
    <el-popover
       content="Prospect à relancer"
       placement="top"
       :auto-close="1500"
       :disabled="!shouldShowAlert(item.prospect.nextDate)"
     >
      <template #reference>
      <el-card :style="(item.list === 'AR' || item.list === 'PC') && item.prospect.nextDate && shouldShowAlert(item.prospect.nextDate) ? 'border: 1px solid #f56c6c;' : ''">
        <el-row style="align-items: center;">
          <router-link :to="'/prospects/' + item.id + '/voir'">
            <el-link
            type="primary"
            style="margin: 0 20px 5px 0; font-size: 1em;"
            >
              {{ item.prospect.name }}
            </el-link>
          </router-link>
        </el-row>
        <el-col>
          <el-row>
            <el-text
            size="default"
            tag="b"
            >
              {{ item.prospect.type }}
            </el-text>
          </el-row>
          <el-row style="margin: 5px 0;">
            <el-tag effect="light" type="success" v-if="item.prospect.domain">
              <b>{{ item.prospect.domain }}</b>
            </el-tag>
          </el-row>
          <el-row style="margin: 10px 0;">
            <router-link :to="'/prospects/' + item.id + '/voir'">
              <el-button
              size="default"
              :type="item.prospect.charge ? '' : 'warning'"
              plain
              icon="Avatar">
              Chargé : {{ item.prospect.charge ? findMembre(item.prospect.charge) : "Aucun" }}
            </el-button>
          </router-link>
          </el-row>
          <el-button
          icon="Calendar"
          v-if="item.list !== 'NC'"
          @click="changeDate(item.id)"
          >
            Dernier contact : {{ item.prospect.nextDate ? niceDate(item.prospect.nextDate) : "non défini." }}
          </el-button>
        </el-col>
      </el-card>
      </template>
      </el-popover>
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
    contactsList: { type: Array, required: true },
    content: { type: Array, required: true },
    prospectsLength: { type: Number, required: false, default: 0 },
  },
  emits: ["dropped", "changedate"],
  data() {
    return {
      animatedPercentage: 0
    }
  },
  computed: {
    progressPercentage() {
      if (this.prospectsLength === 0) return 0
      return Math.round((this.content.length / this.prospectsLength) * 100)
    }
  },
  watch: {
    progressPercentage(newVal) {
      this.animateProgress(newVal)
    }
  },
  methods: {
    shouldShowAlert(nextDate) {
      if (!nextDate) return false
      const prospectDate = new Date(nextDate)
      const today = new Date()
      const diffInTime = today.getTime() - prospectDate.getTime()
      const diffInDays = Math.ceil(diffInTime / (1000 * 3600 * 24))
      return diffInDays >= 14
    },
    async animateProgress(targetPercentage) {
      const step = targetPercentage > this.animatedPercentage ? 1 : -1
      while (this.animatedPercentage !== targetPercentage) {
        this.animatedPercentage += step
        await new Promise(resolve => setTimeout(resolve, 20))
      }
    },
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
    changeDate (itemID, nextDate) {
      this.$emit(
        "changedate",
        itemID,
        this.listId,
        false
      )
    },
    findMembre (membreID) {
      const membre = this.membresList.find(m => m.id === membreID)
      if(membre == undefined) {
        return "Aucun"
      } else {
        return membre.firstname + " " + membre.lastname
      }
    },
    updateWin (item) {
      const newAdv = (item.prospect.advancement === "WIN") ? "LO" : "WIN"
      item.prospect.advancement = newAdv
      this.$emit(
        "dropped",
        item.id,
        newAdv,
        true
      )
    },
    getContact (contactID) {
      const ctt = this.contactsList.find(c => c.id === contactID)
      return ctt == undefined ? "" : ctt.contactWay
    },
    niceDate (dateString) {
      if(dateString == undefined || dateString == null) {
        return "non défini."
      } else {
        const tokens = dateString.split("-")
        return tokens[2] + "/" + tokens[1] + "/" + tokens[0]
      }
    }
  }
}
</script>

<style>
  .titleStyle {
    text-align: left;
    padding-left: 10px;
    font-size: 1.1em;
    font-weight: bold;
    margin-bottom: 5px;
  }

  .drop-zone {
    margin-bottom: 10px;
    padding: 5px;
    float: left;
    width: 18vw;
    min-width: 300px;
    min-height: 60vh;
  }

  .drag-el {
    margin-bottom: 5px;
    cursor: pointer;
  }

  /* Clear floats after the columns */
  .rowStyle:after {
    content: "";
    display: table;
    clear: both;
  }
</style>