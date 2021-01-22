<template>
  <div>
    <el-row
      v-for="(member, index) in value"
      :key="index"
      :span="12"
      :style="{margin:'10px 10px 10px 10px'}"
    >
      <el-col
        :span="2"
      >
        <el-button
          v-if="index == value.length - 1"
          type="primary"
          size="mini"
          icon="el-icon-plus"
          @click="addLocalGroup()"
        />
        <el-button
          v-else
          type="info"
          size="mini"
          icon="el-icon-minus"
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
            :out-value="value[index]"
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
    value: {type: Array, required: true},
    itemList: { type: Array, required: true },
  },
  data () {
    return {
      textes: {},
      newIndex: -2
    }
  },
  watch: {
    itemList () {
      const found = this.itemList.find((item) => item.id === this.value)
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
      // TODO invalidate field car membre non trouvé.
      this.value[groupIndex] = listID
      this.textes[groupIndex] = itemName
    },
  }
}
</script>
