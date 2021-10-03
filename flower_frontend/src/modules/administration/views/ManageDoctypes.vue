<template>
  <BaseComponent
    title="Gérer les doctypes"
    :breadcrumb="breadcrumb"
  >
    <el-upload
      class="upload-demo"
      action="/api/doctypes/"
      :http-request="requestPostFile"
      drag
      :show-file-list="false"
    >
      <i :class="loading ? 'el-icon-loading' : 'el-icon-upload'" />
      <div class="el-upload__text">
        Déposez ou <em>cliquez ici</em> pour uploader le doctype.
      </div>
    </el-upload>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
export default {
  name: "ManageDoctypes",
  data () {
    return {
      loading : false,
      breadcrumb: [
        {
          name: "Gestion des doctypes",
          link: "/administration/doctypes"
        }
      ],
    }
  },
  methods: {
    requestPostFile (request) {
      this.loading = true
      let formData = new FormData()
      formData.append("file", request.file)
      axios.post(
        "api/doctypes/",
        formData,
        {
          withCredentials: true,
          headers: {
            "Content-Type": "multipart/form-data", // pour le navigateur
            "enctype": "multipart/form-data" // pour Django
          }
        }
      ).then((res) => {
        console.log("OK !")
        console.log(res)
      }).catch((err) => {
        this.$message({message: "Échec de l'upload du doctype : " + err, type: "error"})
        this.loading = false
      })
    }
  }
}
</script>

