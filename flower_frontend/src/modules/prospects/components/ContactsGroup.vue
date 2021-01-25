<template>
  <div>
    <el-row
      v-for="(contact, index) in value"
      :key="index"
      :span="12"
      :style="{margin:'10px 10px 10px 10px'}"
    >
      <el-col
        :span="1"
      >
        <el-button
          v-if="index == value.length - 1"
          type="primary"
          size="mini"
          icon="el-icon-plus"
          @click="addLocalField()"
        />
        <el-button
          v-else
          type="info"
          size="mini"
          icon="el-icon-minus"
          @click="removeLocalField(index)"
        />
      </el-col>
      <el-col
        :span="10"
        :offset="1"
      >
        <el-form-item
          label=""
          label-width="0%"
        >
          <el-input
            v-model="value[index]"
            :placeholder="label(index)"
            :style="{width:'100%'}"
          />
        </el-form-item>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "ContactsGroup",
  props: {
    value: {type: Array, required: true}
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
      return "Moyen de contact " + (i+1)
    },
    addLocalField () {
      this.$emit("add-field")
    },
    removeLocalField (index) {
      this.$emit("delete-field", index)
    }
  }
}
</script>
