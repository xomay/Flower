<template>
    <el-tooltip
    effect="dark"
    placement="top"
    style="white-space: pre-line; display: flex; align-items: center;"
    >
        <template #content>
            <div style="display: flex; align-items: center; flex-direction: column;">
                <span v-for="(line, index) in description" :key="index">{{ line }}<br /></span>
            </div>
        </template>
        <el-icon><InfoFilled /></el-icon>
    </el-tooltip>
</template>

<script>
export default {
  name: 'InfoTip',
  props: {
    description: {type: Array, default: () => []},
  },
};
</script>