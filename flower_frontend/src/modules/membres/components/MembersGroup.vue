<template>
  <div>
    <el-row
      v-for="(member, index) in modelValue"
      :key="index"
      :span="12"
      :style="{margin:'10px 10px 10px 10px'}"
    >
      <el-col
        :span="2"
      >
        <el-button
          v-if="index == modelValue.length - 1"
          type="primary"
          size="small"
          icon="Plus"
          @click="addLocalGroup()"
        />
        <el-button
          v-else
          type="info"
          size="small"
          icon="Minus"
          @click="removeLocalGroup(index)"
        />
      </el-col>
      <el-col
        :span="12"
        :offset="2"
      >
        <el-form-item
          label=""
          label-width="0%"
        >
          <MemberGElem
            :out-value="modelValue[index]"
            :item-list="itemList"
            :placeholder="label(index)"
            :index="index"
            :style="{width:'100%'}"
            @inputOver="inputed"
          />
        </el-form-item>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import MemberGElem from "@/modules/membres/components/MemberGElem"

export default {
  name: "MembersGroup",
  components: {MemberGElem},
  props: {
    modelValue: {type: undefined, required: true},
    itemList: { type: Array, required: true },
  },
  emits: [
    "add-participant",
    "delete-participant"
  ],
  data () {
    return {
      textes: {},
      newIndex: -2
    }
  },
  watch: {
    itemList () {
      const found = this.itemList.find((item) => item.id === this.modelValue)
      this.autocompleteValue = found ? found.value : ""
    }
  },
  methods: {
    label (i) {
      return "Participant " + (i+1)
    },
    labelRef (i) {
      return "p" + i
    },
    addLocalGroup () {
      this.$emit("add-participant")
    },
    removeLocalGroup (index) {
      this.$emit("delete-participant", index)
    },
    inputed (groupIndex, listID) {
      var itemName = undefined
      console.log("inputed", groupIndex, listID, this.itemList)
      console.log("ID : ", listID)
      for (var i = 0; i < this.itemList.length; i++) {
        if(this.itemList[i].id == listID) {
          itemName = this.itemList[i].value
          break
        }
      }
      if(itemName == undefined) {
        this.$message("erreur")
        return
      }
      this.modelValue[groupIndex] = listID
      this.textes[groupIndex] = itemName
      console.log("inputed", this.modelValue, this.textes)
    },
  }
}
</script>
