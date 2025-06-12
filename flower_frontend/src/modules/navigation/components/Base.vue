<template>
  <div class="p-4">
    <el-breadcrumb
      class="float-right"
      separator-class="arrowRight"
    >
      <el-breadcrumb-item
        v-for="(item, index) in breadcrumb"
        :key="index"
        :to="{ path: item.link }"
      >
        {{ item.name }}
      </el-breadcrumb-item>
    </el-breadcrumb>
    <el-divider content-position="left">
      <span class="text-lg mr-2">{{ title }}</span>
      <slot name="action" />
    </el-divider>
    <slot />
  </div>
</template>

<script>
export default {
  name: "Base",
  props: {
    title: { type: String, required: true },
    breadcrumb: { type: Array, required: true }
  }
}
</script>

<style scoped>
.w-98 {
  width: 98%;
}
</style>
