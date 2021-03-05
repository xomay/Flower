<template>
  <el-row>
    <el-col :span="24">
      <NewPasswordComponent class="mx-auto my-20" />
    </el-col>
  </el-row>
</template>

<script>
import NewPasswordComponent from "../components/NewPasswordComponent"

export default {
  name: "NewPassword",
  components: {NewPasswordComponent}
}
</script>
