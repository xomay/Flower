<template>
  <el-row>
    <el-col :span="24">
      <PasswordResetComponent class="mx-auto my-20" />
    </el-col>
  </el-row>
</template>

<script>
import PasswordResetComponent from "../components/PasswordResetComponent"

export default {
  name: "PasswordReset",
  components: {PasswordResetComponent}
}
</script>

<style>

</style>
