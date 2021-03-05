<template>
  <el-row>
    <el-col :span="24">
      <LoginComponent class="mx-auto my-20" />
    </el-col>
  </el-row>
</template>

<script>
import LoginComponent from "../components/AuthenticationComponent"

export default {
  name: "Authentication",
  components: {LoginComponent}
}
</script>
